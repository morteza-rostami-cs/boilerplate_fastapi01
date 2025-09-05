import time
from fastapi import APIRouter, BackgroundTasks
from celery.result import AsyncResult

# tasks
from app.tasks.jobs import long_task

router = APIRouter(prefix="/tasks", tags=["tasks"])

#******************* redis & celery job

@router.post("/celery-job")
async def run_celery_job(job_id: str):
  # schedule a task
  # long_task => is decorated (wrapped in an task object) so: obj.delay()
  # sends the task to the broker (Redis) asynchronously
  task: AsyncResult = long_task.delay(job_id) # .delay(*args, **kwargs)
  return {"msg": f"Celery job {job_id} scheduled", "task_id": task.id}

#******************* redis & celery job

def write_log(message: str):
  """simulate writing a log entry (blocking task)"""
  with open("task_logs.txt", "a") as file:
    file.write(f"{message}\n")

def long_running_job(job_id: str):
  """simulate a long job (blocking, but offloaded)"""
  time.sleep(5)
  with open("task_logs.txt", 'a') as file:
    file.write(f"Job {job_id} completed\n")

# register a log_message job
@router.post("/log")
async def log_message(message: str, background_tasks: BackgroundTasks):
  # register a background message
  # add_task => tasks positional args arguments => all passed into write_log in order
  # f"new log: {message}" =>goes to => (message)
  # name of arguments in write_log => can be use in add_task
  background_tasks.add_task(func=write_log, message=f"new log: {message}")
  return {"msg": "Log scheduled"}

# register a job with id
@router.post("/long-job")
async def run_job(job_id: str, background_tasks: BackgroundTasks):
  background_tasks.add_task(func=long_running_job, job_id=job_id)
  # let client know => job was scheduled
  return {"msg": f"Job {job_id} starts in background"}