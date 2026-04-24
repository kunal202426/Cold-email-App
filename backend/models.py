from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from database import Base


class Lead(Base):
    __tablename__ = "leads"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    hr_name       = Column(Text, nullable=False)
    hr_email      = Column(Text, nullable=False, unique=True)
    hr_position   = Column(Text)
    company       = Column(Text, nullable=False)
    company_url   = Column(Text)
    linkedin_url  = Column(Text)
    notes         = Column(Text)

    # email lifecycle
    status        = Column(Text, default="pending")
    email_subject = Column(Text)
    email_body    = Column(Text)
    sent_at       = Column(TIMESTAMP)
    queued_at     = Column(TIMESTAMP)
    created_at    = Column(TIMESTAMP, server_default=func.now())

    # rate limit tracking
    retry_count   = Column(Integer, default=0)
    error_log     = Column(Text)


class DailyQuota(Base):
    __tablename__ = "daily_quota"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    date        = Column(Text, unique=True)
    emails_sent = Column(Integer, default=0)
    quota_limit = Column(Integer, default=90)
