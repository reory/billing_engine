# This schedules the job to run every 24 hours.
# run command -  python scheduler.py

import redis
from rq_scheduler import Scheduler
from app.jobs.aggregate_job import run_daily_aggregation_job

redis_conn = redis.Redis()

scheduler = Scheduler(connection=redis_conn)

# Schedule job for every 24 hours
scheduler.schedule(
    scheduled_time=None, # Runs immediately the first time
    func=run_daily_aggregation_job,
    interval=60 * 60 * 24, # 24 hours
    repeat=None
)
