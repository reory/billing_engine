# SQLAlchemy models: UsageEvent, AggregatedUsage, Invoice.

# app/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class UsageEvent(Base):
    __tablename__ = "usage_events"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    metric = Column(String, index=True)
    units = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class AggregatedUsage(Base):
    __tablename__ = "aggregated_usage"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    metric = Column(String, index=True)
    total_units = Column(Float)
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    amount = Column(Float)
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
