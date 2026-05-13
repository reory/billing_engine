# aggregates the data for the invoice generation

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import UsageEvent, AggregatedUsage

class AggregatorService:
    """Aggregates raw usage events into daily usage totals."""

    @staticmethod
    def run_daily_aggregation(db: Session):

        # Define the aggregation window (24 hrs)
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=1)

        # Fetch raw usage events for the period
        events = (
            db.query(UsageEvent)
            .filter(UsageEvent.timestamp >= period_start)
            .filter(UsageEvent.timestamp <= period_end)
            .all()
        )

        # Group by (customer_id, metric)
        grouped = {}
        for event in events:
            key = (event.customer_id, event.metric)
            grouped.setdefault(key, 0.0)
            grouped[key] += event.units

        # Write aggregated rows
        for (customer_id, metric), total_units in grouped.items():
            agg = AggregatedUsage(
                customer_id=customer_id,
                metric=metric,
                total_units=total_units,
                period_start=period_start,
                period_end=period_end,
            )
            db.add(agg)

        db.commit()

        return {
            "status": "ok",
            "aggregated_records": len(grouped),
            "period_start": period_start,
            "period_end": period_end,
        }

    @staticmethod
    def run_aggregation(db: Session):
        """Public wrapper for daily aggregation."""
        return AggregatorService.run_daily_aggregation(db)
