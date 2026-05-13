# Pydantic request/response models.

from pydantic import BaseModel

class UsageEventCreate(BaseModel):
    customer_id: str
    metric: str
    units: float
