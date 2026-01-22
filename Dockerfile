FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# ⬇️ entra na pasta do Django
WORKDIR /app/sinistro_dash

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "sinistro_dash.wsgi:application", "--bind", "0.0.0.0:8080"]
