pip install -r requirements.txt
python manage.py collectstatic --noinput
python -m pip install --upgrade pip
echo "Starting Django server on port 8000..."
python manage.py runserver 0.0.0.0:8000 & 
echo "Starting FastAPI server on port 7000..."
python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 7000
