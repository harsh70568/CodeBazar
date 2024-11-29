pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
python -m uvicorn backend.api.main:app --reload 7000