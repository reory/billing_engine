# Pricing rules + rating engine.

from typing import Dict, List, Tuple

# Simple pricing config: price per unit by metric
PRICING_RULES: Dict[str, float] = {
    "api_calls": 0.01,   # per api call £0.01
    "storage_gb": 0.40,  # per GB £0.40
    "workflows":0.05     # per workflow run £0.05
}

class PricingEngine:
    def __init__(self, rules: Dict[str, float] | None = None) -> None:
        self.rules = rules or PRICING_RULES

    def price_metric(self, metric: str, units: float) -> float:
        """Return the cost for a single metric based on the units."""

        price_per_unit = self.rules.get(metric, 0.0)
        return round(units * price_per_unit, 2)

    def calculate_invoice_amount(
        self,
        customer_id: str,
        usage: List[Tuple[str, float]],
    ) -> float:
        """
        usage: list of (metric, total_units) for the billing period.
        Example: [("api_calls", 12500), ("storage_gb", 12.5)]
        """
        total = 0.0
        for metric, units in usage:
            total += self.price_metric(metric, units)
        return round(total, 2)
