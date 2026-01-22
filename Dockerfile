FROM python:3.12-slim

WORKDIR /app

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

ENV DJANGO_SETTINGS_MODULE=sinistro_dash.settings

EXPOSE 8000
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "sinistro_dash.wsgi:application", "--bind", "0.0.0.0:8000"]
