# Expense Tracker (Django)

## Features
- Expense CRUD operations
- Category-wise expense summary
- Excel & PDF report generation
- SQLite database
- Amount in Indian Rupees (₹)
- Clean Bootstrap UI

## Tech Stack
- Django
- SQLite
- Django ORM
- Bootstrap
- Pandas, OpenPyXL, ReportLab

## Setup Instructions
pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

## API Endpoints
POST   /expenses

GET    /expenses

GET    /expenses/<id>

PUT    /expenses/<id>

DELETE /expenses/<id>

GET    /reports/category-summary

GET    /reports/excel
GET    /reports/pdf
