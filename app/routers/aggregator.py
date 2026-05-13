# Add an endpoint to trigger aggregation

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import deps
from app.services.aggregator_service import AggregatorService

router = APIRouter()
aggregator = AggregatorService()


@router.post("/run", summary="Run daily usage aggregation")
def run_aggregation(db: Session = Depends(deps.get_db)):
    return aggregator.run_daily_aggregation(db)
