import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class add_new_holding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str, instrument_id: str, 
               quantity: float, cost_basis: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return '1'
            return str(max(int(k) for k in table.keys()) + 1)
        
        portfolios = data.get("portfolios", {})
        instruments = data.get("instruments", {})
        holdings = data.get("portfolio_holdings", {})
        
        # Validate portfolio exists
        if str(portfolio_id) not in portfolios:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        holding_id = generate_id(holdings)
        timestamp = "2025-08-07T00:00:00Z"
        
        new_holding = {
            "holding_id": holding_id,
            "portfolio_id": portfolio_id,
            "instrument_id": instrument_id,
            "quantity": round(float(quantity), 4),
            "cost_basis": round(float(cost_basis), 4),
            "created_at": timestamp
        }
        
        holdings[str(holding_id)] = new_holding
        return json.dumps(new_holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_holding",
                "description": "Add a new holding to a portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"},
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "quantity": {"type": "number", "description": "Quantity of the holding"},
                        "cost_basis": {"type": "number", "description": "Cost basis of the holding"}
                    },
                    "required": ["portfolio_id", "instrument_id", "quantity", "cost_basis"]
                }
            }
        }
