pip install -r requirements.txt
python manage.py collectstatic
python -m pip install --upgrade pip
echo "Starting FastAPI server on port 7000..."
python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 7000
