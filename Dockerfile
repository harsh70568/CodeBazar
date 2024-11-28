FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app
COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN mkdir -p /app/media /app/uploaded_images

# Expose ports for Django and FastAPI
EXPOSE 8000
EXPOSE 7000

# Default command to run Django and FastAPI
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000 & uvicorn backend.api.main:app --host 0.0.0.0 --port 7000"]