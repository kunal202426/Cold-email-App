from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from database import get_db
from models import Lead
from services import quota_service, email_service

router = APIRouter(prefix="/api", tags=["quota"])


@router.get("/quota/today")
def get_quota(db: Session = Depends(get_db)):
    return quota_service.get_today_stats(db)


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total    = db.query(func.count(Lead.id)).scalar()
    sent     = db.query(func.count(Lead.id)).filter(Lead.status == "sent").scalar()
    queued   = db.query(func.count(Lead.id)).filter(Lead.status == "queued").scalar()
    failed   = db.query(func.count(Lead.id)).filter(Lead.status == "failed").scalar()
    replied  = db.query(func.count(Lead.id)).filter(Lead.status == "replied").scalar()
    pending  = db.query(func.count(Lead.id)).filter(Lead.status == "pending").scalar()
    quota    = quota_service.get_today_stats(db)
    return {
        "total": total,
        "sent": sent,
        "queued": queued,
        "failed": failed,
        "replied": replied,
        "pending": pending,
        "quota": quota,
    }


@router.post("/queue/process")
def process_queue(db: Session = Depends(get_db)):
    """Send queued emails within today's remaining quota."""
    can_send, remaining = quota_service.can_send_today(db)
    if not can_send:
        raise HTTPException(status_code=429, detail="Daily quota exhausted")

    queued_leads = (
        db.query(Lead)
        .filter(Lead.status == "queued")
        .order_by(Lead.queued_at.asc())
        .limit(remaining)
        .all()
    )

    results = {"processed": 0, "sent": 0, "failed": 0, "details": []}

    for lead in queued_leads:
        can_send, _ = quota_service.can_send_today(db)
        if not can_send:
            break
        results["processed"] += 1
        try:
            email_service.send_cold_email(lead.hr_email, lead.email_subject, lead.email_body)
            lead.status = "sent"
            lead.sent_at = datetime.utcnow()
            db.commit()
            quota_service.increment_quota(db)
            results["sent"] += 1
            results["details"].append({"id": lead.id, "email": lead.hr_email, "result": "sent"})
        except Exception as e:
            lead.status = "failed"
            lead.error_log = str(e)
            lead.retry_count = (lead.retry_count or 0) + 1
            db.commit()
            results["failed"] += 1
            results["details"].append({"id": lead.id, "email": lead.hr_email, "result": "failed", "error": str(e)})

    return results
