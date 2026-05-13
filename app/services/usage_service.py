# Business logic layer (keeps routers thin).

from sqlalchemy.orm import Session
from app.models import UsageEvent
from app.schemas import UsageEventCreate

class UsageService:
    @staticmethod
    def record_usage(db: Session, data: UsageEventCreate) -> UsageEvent:
        event = UsageEvent(
            customer_id=data.customer_id,
            metric=data.metric,
            units=data.units,
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
