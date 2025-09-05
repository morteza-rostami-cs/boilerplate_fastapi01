# base image
FROM python:3.11-slim as base

# env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# working dir
WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  curl \
  && rm -rf /var/lib/apt/lists/*

# copy only requirements first for caching
COPY requirements.txt /app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# then copy application code
COPY . /app/

# expose docker port
EXPOSE 8000

# start the app with Unicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--proxy-headers"]
