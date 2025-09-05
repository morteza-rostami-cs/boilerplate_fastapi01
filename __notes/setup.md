<!--
# Install dependencies
pip install -r requirements.txt

# Start FastAPI
uvicorn app.main:app --reload

# swagger docs
http://127.0.0.1:8000/docs

# run celery/redis on windows
celery -A app.tasks.worker.celery_app worker --loglevel=info -P solo


# build docker
# Build image
docker build -t fastapi-bot-backend .

# Run container
docker run -d -p 8000:8000 --name fastapi-bot fastapi-bot-backend


#build and run container => docker-compose

# build images
docker-compose build

# start containers
docker-compose up

# detach terminal
docker-compose up -d

docker-compose down

# use different .env files for docker local and docker-compose on production

docker-compose --env-file .env.docker up

docker-compose --env-file .env up


# also you can use variable:
env_file:
  - ${ENV_FILE:-.env.docker}

# and set it when running compose
ENV_FILE=.env docker-compose up



 -->
