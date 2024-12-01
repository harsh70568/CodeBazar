pip install -r requirements.txt
python manage.py collectstatic --noinput
python -m pip install --upgrade pip
if [[ $CREATE_SUPERUSER ]];
then
    python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi

