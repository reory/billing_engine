# This file defines the function the worker will execute.

from app.database import SessionLocal
from app.services.aggregator_service import AggregatorService

def run_daily_aggregation_job():
    db = SessionLocal()

    try:
        service = AggregatorService()
        result = service.run_daily_aggregation(db)
        print("✅ Aggregation Complete:", result)
    finally:
        db.close()
