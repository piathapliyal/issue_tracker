
# Issue Tracker

A simple **Issue Tracking System** built with **Flask (Python)** for the backend and **Angular** for the frontend.  
Supports **viewing, searching, filtering, sorting, pagination, creating, and updating issues**.  

---

## Features
- List issues in a table (id, title, status, priority, assignee, updatedAt)  
- Search by title  
- Filter by status, priority, assignee  
- Sorting (asc/desc)  
- Pagination with page & pageSize  
- Create and update issues  
- Issue Detail page with full JSON view  

---

## Tech Stack
- **Backend:** Python, Flask, Flask-CORS  
- **Frontend:** Angular, TypeScript, Bootstrap  
- **Other:** REST APIs, Git/GitHub  

---

## ▶️ Getting Started

### Backend

cd backend
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
python app.py



Runs on: http://127.0.0.1:5000



Frontend
cd frontend
npm install
ng serve --open

Runs on: http://localhost:4200
