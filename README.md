# SmartFitAI Gym — React + Django REST + GenAI

A portfolio starter gym app with a responsive React dashboard, workout library, membership plans, and an AI fitness coach.

## Requirements
Python 3.10+, Node.js 18+, and MySQL Server 8+. OpenAI API key is optional. This version uses MySQL and includes an initial gymapi migration.

## 1. Create the MySQL database
Run in MySQL Workbench:
```sql
CREATE DATABASE fitgenai_gym CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 2. Backend (Windows PowerShell)
```powershell
cd backend
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and set DB_USER / DB_PASSWORD for your MySQL server
python manage.py showmigrations gymapi
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```
API runs at http://127.0.0.1:8000/api/

## 3. Optional OpenAI GenAI
Put your key in `backend/.env`:
`OPENAI_API_KEY=your_key_here`
`OPENAI_MODEL=gpt-4o-mini`
Restart Django. Without a key, the AI coach uses a local fallback plan.

## 4. Frontend (new terminal)
```powershell
cd frontend
npm install
npm run dev
```
Open the Vite URL, usually http://localhost:5173.

## API endpoints
- GET `/api/health/`
- GET `/api/workouts/`
- GET `/api/plans/`
- POST `/api/ai/coach/` with `{ "goal":"Build strength", "level":"beginner", "days_per_week":3, "equipment":"Full gym" }`

The `gymapi/0001_initial.py` migration creates `gymapi_workout` and `gymapi_membershipplan` tables. Sample membership prices are illustrative; no payments or real membership signup are implemented. AI fitness guidance is general information, not medical advice.
