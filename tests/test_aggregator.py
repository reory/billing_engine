from app.services.usage_service import UsageService
from app.services.aggregator_service import AggregatorService
from app.schemas import UsageEventCreate
from app.models import AggregatedUsage


def test_aggregation_sums_usage(db):
    """
    Ensure the aggregator correctly groups and sums raw usage events.
    """

    # Insert raw usage
    UsageService.record_usage(db, UsageEventCreate(
        customer_id="cust_123",
        metric="api_calls",
        units=50
    ))
    UsageService.record_usage(db, UsageEventCreate(
        customer_id="cust_123",
        metric="api_calls",
        units=25
    ))

    result = AggregatorService.run_daily_aggregation(db)

    assert result["aggregated_records"] == 1

    agg = db.query(AggregatedUsage).first()
    assert agg.total_units == 75
    assert agg.customer_id == "cust_123"
    assert agg.metric == "api_calls"
    assert agg.period_start is not None
    assert agg.period_end is not None
