from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

from database import get_db
from models import Lead
from services import leads_service, quota_service, gemini_service, email_service

router = APIRouter(prefix="/api/leads", tags=["leads"])


class LeadCreate(BaseModel):
    hr_name: str
    hr_email: str
    hr_position: Optional[str] = None
    company: str
    company_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    notes: Optional[str] = None


class StatusUpdate(BaseModel):
    status: str


def lead_to_dict(lead: Lead) -> dict:
    return {
        "id": lead.id,
        "hr_name": lead.hr_name,
        "hr_email": lead.hr_email,
        "hr_position": lead.hr_position,
        "company": lead.company,
        "company_url": lead.company_url,
        "linkedin_url": lead.linkedin_url,
        "notes": lead.notes,
        "status": lead.status,
        "email_subject": lead.email_subject,
        "email_body": lead.email_body,
        "sent_at": str(lead.sent_at) if lead.sent_at else None,
        "queued_at": str(lead.queued_at) if lead.queued_at else None,
        "created_at": str(lead.created_at) if lead.created_at else None,
        "retry_count": lead.retry_count,
        "error_log": lead.error_log,
    }


@router.get("/check")
def check_duplicate(email: str = Query(...), db: Session = Depends(get_db)):
    return leads_service.check_duplicate(email, db)


@router.post("", status_code=201)
def add_lead(data: LeadCreate, db: Session = Depends(get_db)):
    # Level 1: duplicate check
    dup = leads_service.check_duplicate(data.hr_email, db)
    if dup["is_duplicate"]:
        raise HTTPException(status_code=409, detail=dup["message"])

    # Generate email via Gemini
    try:
        email_content = gemini_service.generate_email(data.dict())
    except Exception as e:
        # Save as failed lead so we still have the record
        new_lead = Lead(
            **data.dict(),
            status="failed",
            error_log=str(e),
        )
        db.add(new_lead)
        db.commit()
        db.refresh(new_lead)
        raise HTTPException(status_code=502, detail=f"AI generation failed: {str(e)}")

    # Quota check
    can_send, remaining = quota_service.can_send_today(db)

    new_lead = Lead(
        **data.dict(),
        email_subject=email_content["subject"],
        email_body=email_content["body"],
    )

    if can_send:
        try:
            email_service.send_cold_email(data.hr_email, email_content["subject"], email_content["body"])
            new_lead.status = "sent"
            new_lead.sent_at = datetime.utcnow()
            db.add(new_lead)
            db.commit()
            db.refresh(new_lead)
            quota_service.increment_quota(db)
        except Exception as e:
            new_lead.status = "failed"
            new_lead.error_log = str(e)
            db.add(new_lead)
            db.commit()
            db.refresh(new_lead)
            raise HTTPException(status_code=502, detail=f"Email send failed: {str(e)}")
    else:
        new_lead.status = "queued"
        new_lead.queued_at = datetime.utcnow()
        db.add(new_lead)
        db.commit()
        db.refresh(new_lead)

    return lead_to_dict(new_lead)


@router.get("")
def list_leads(
    status: Optional[str] = None,
    company: Optional[str] = None,
    db: Session = Depends(get_db)
):
    leads = leads_service.get_all_leads(db, status=status, company=company)
    return [lead_to_dict(l) for l in leads]


@router.get("/{lead_id}")
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = leads_service.get_lead_by_id(lead_id, db)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead_to_dict(lead)


@router.patch("/{lead_id}/status")
def update_status(lead_id: int, body: StatusUpdate, db: Session = Depends(get_db)):
    valid = {"pending", "queued", "sent", "failed", "replied"}
    if body.status not in valid:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid}")
    lead = leads_service.update_lead_status(lead_id, body.status, db)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead_to_dict(lead)


@router.delete("/{lead_id}", status_code=204)
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    deleted = leads_service.delete_lead(lead_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Lead not found")
