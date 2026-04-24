# 🚀 Autonomous Cold Email Outreach Pipeline

An end-to-end, full-stack AI platform built to automate highly-personalized, intelligent cold email outreach. This system aggregates HR leads, ensures zero duplicate outreach, leverages Google Gemini AI to generate context-aware, hyper-personalized emails based on specific engineering projects, and automatically dispatches them via SMTP while strictly obeying custom rate limits.

![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)

## ✨ Core Features

*   **Intelligent Generative AI Engine**: Utlizes Gemini 2.5 Flash-Lite under the hood with a highly constrained, battle-tested structural prompt. The AI evaluates the target company's current engineering landscape and dynamically aligns it with actual portfolio project data. 
*   **Zero-Hallucination Guarantee**: The system operates on a hard-coded mapping of physical projects. It actively strips out corporate fluff and strictly obeys strict 80-120 word limits for high-impact hook-bridge-proof-ask flows.
*   **Duplicate Detection Pipeline**: Real-time cross-referencing on the frontend prevents targeting the same HR/Company combination twice. 
*   **Automated Dispatch & Queue Management**: Enforces a strict 90 email/day SMTP quota to prevent domain blacklisting. Any leads added past the daily quota are automatically sent to a pending queue for processing the next day.
*   **Modern Glassmorphic Dashboard**: A fully responsive React + Vite GUI featuring real-time telemetry, lead lifecycle tracking, edit/preview modals, and daily quota progress bars.

## 🏗 System Architecture

The application is entirely self-hosted to ensure zero paid-service dependencies. 

- **Frontend**: Built with React & Vite using Tailwind CSS for a dark-mode, glass-styled aesthetic. Syncs state automatically using `@tanstack/react-query`.
- **Backend**: Async Python architecture handled natively by FastAPI.
- **Database**: Local SQLite managed by SQLAlchemy ORM. Keeps a persistent track of daily operational quotas and lifecycle states (`PENDING`, `DRAFTED`, `SENT`, `FAILED`).
- **AI Infrastructure**: `google-generativeai` utilizing the generative Free Tier limit (15 RPM / 1M RPD).
- **Mailing**: Core `smtplib` interface targeting Google's external Application Passwords.

---

## 💻 Local Developer Setup

### Prerequisites
- Node.js (v18+)
- Python (v3.11+)
- A Google API Key for Gemini.
- A Gmail Application Password (standard passwords are blocked by SMTP).

### 1. Clone the Repository
```bash
git clone https://github.com/kunal202426/Cold-email-App.git
cd Cold-email-App
```

### 2. Backend Configuration
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```
Create a `.env` file in the `backend/` directory with your secure credentials:
```env
GEMINI_API_KEY=your_gemini_key_here
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_digit_app_password
DATABASE_URL=sqlite:///./cold_email.db
```

### 3. Frontend Configuration
```bash
cd ../frontend
npm install
```

### 4. Boot Up the Platform
We've included a unified runner script. Simply double-click `start.bat` from the root directory to simultaneously launch the FastAPI Server natively on Port 8000 and the Vite hot-reloading server on Port 5173. 

Access the dashboard at `http://localhost:5173`.
