# Endpoints for recording + retrieving usage.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import UsageEventCreate
from app.services.usage_service import UsageService
from app import deps

router = APIRouter()

@router.post("/", summary="Record a usage event")
def record_usage(
    payload: UsageEventCreate,
    db: Session = Depends(deps.get_db),
):
    event = UsageService.record_usage(db, payload)
    return {
        "status": "ok",
        "event": event.id,
        "customer_id": event.customer_id,
        "metric": event.metric,
        "units": event.units,
        "timestamp": event.timestamp.isoformat() if event.timestamp else None
    }
