from .worker import celery_app
import time

# define a background task via => decorator
# self => task's instance
@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def long_task(self, job_id: str):
  """ just a celery job, fakes a task """
  try:
    # simulate a long running job
    time.sleep(10)

    result = f"Celery Job {job_id} completed"

    # write something to a file
    with open("task_logs.txt", 'a') as file:
      file.write(result + '\n')

    # this return value stores in redis => under each task_id
    return result
  except Exception as e:
    raise self.retry(exc=e)