from sqlalchemy.orm import Session
from models import Lead


def check_duplicate(email: str, db: Session) -> dict:
    existing = db.query(Lead).filter(Lead.hr_email == email).first()
    if existing:
        return {
            "is_duplicate": True,
            "lead_id": existing.id,
            "status": existing.status,
            "sent_at": str(existing.sent_at) if existing.sent_at else None,
            "created_at": str(existing.created_at),
            "message": f"Already {existing.status} on {existing.sent_at or existing.created_at}"
        }
    return {"is_duplicate": False}


def get_all_leads(db: Session, status: str = None, company: str = None) -> list:
    q = db.query(Lead)
    if status:
        q = q.filter(Lead.status == status)
    if company:
        q = q.filter(Lead.company.ilike(f"%{company}%"))
    return q.order_by(Lead.created_at.desc()).all()


def get_lead_by_id(lead_id: int, db: Session):
    return db.query(Lead).filter(Lead.id == lead_id).first()


def delete_lead(lead_id: int, db: Session) -> bool:
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return False
    db.delete(lead)
    db.commit()
    return True


def update_lead_status(lead_id: int, new_status: str, db: Session):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return None
    lead.status = new_status
    db.commit()
    db.refresh(lead)
    return lead
