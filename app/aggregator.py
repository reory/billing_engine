# Background worker that aggregates usage per billing period.

from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class AggregatedUsage(Base):
    __tablename__ = "aggregated_usage"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    metric = Column(String, index=True)
    total_units = Column(Float)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
