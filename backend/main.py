import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from database import engine, Base
from routers import leads, quota

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cold Email Outreach API",
    description="HR cold email outreach app with Gemini AI + Gmail SMTP",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leads.router)
app.include_router(quota.router)


@app.get("/health")
def health():
    return {"status": "ok", "message": "Cold Email API is running"}
