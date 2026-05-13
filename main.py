# Entry point. Creates FastAPI app, includes routers.

from fastapi import FastAPI
from app.routers import usage, invoice, aggregator
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Usage-Based Billing Engine")

app.include_router(usage.router, prefix="/usage", tags=["usage"])
app.include_router(invoice.router, prefix="/invoice", tags=["invoice"])
app.include_router(aggregator.router, prefix="/aggregate", tags=["aggregator"])

# Homepage for billing service (backend only)
@app.get("/")
def root():
    return {"status": "Billing engine running successfully"}
