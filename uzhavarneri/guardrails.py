"""Deterministic safety guardrails for UzhavarNeri using Strands InterventionHandler."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Set
from strands.interventions import Confirm, Deny, Guide, InterventionHandler, Proceed

BANNED_CHEMICALS = {"monocrotophos", "endosulfan", "methyl parathion", "paraquat", "carbofuran"}


class AgrochemicalSafetyGuard(InterventionHandler):
    """Intercepts and validates agricultural chemical and harvest recommendations before execution."""

    name = "agrochemical-safety-guard"

    def __init__(self):
        super().__init__()
        self.log: List[Dict[str, Any]] = []
        self._guided_signatures: Set[str] = set()

    def before_invocation(self, event, **kwargs):
        # Reset guided set on new farmer invocation
        self._guided_signatures.clear()
        return Proceed()

    def before_tool_call(self, event, **kwargs):
        tool_name = event.tool_use.get("name", "")
        args = event.tool_use.get("input", {}) or {}
        sig = f"{tool_name}:{json.dumps(args, sort_keys=True)}"

        # 1. Convergence guard: If the agent was already guided about this exact call, Deny to avoid infinite loops
        if sig in self._guided_signatures:
            rec = {
                "tool": tool_name,
                "args": args,
                "verdict": "DENY",
                "reason": "Retried an unsafe agrochemical action unchanged."
            }
            self.log.append(rec)
            return Deny(reason="This chemical action violates monsoon safety rules. Explain why to the farmer and recommend drainage instead.")

        # 2. Inspect chemical validation tool inputs
        if tool_name == "validate_agrochemical_safety":
            chem = str(args.get("chemical_name", "")).lower().strip()
            rain = float(args.get("rainfall_forecast_mm", 0.0))

            # Banned pesticide check
            for banned in BANNED_CHEMICALS:
                if banned in chem:
                    self._guided_signatures.add(sig)
                    rec = {
                        "tool": tool_name,
                        "chemical": chem,
                        "verdict": "DENY",
                        "reason": f"Prohibited pesticide detected: {chem}"
                    }
                    self.log.append(rec)
                    return Deny(reason=f"Pesticide '{chem}' is strictly banned in Tamil Nadu under CIBRC regulations. Warn the farmer and recommend organic/safe alternatives.")

            # Extreme rainfall check (> 20mm)
            if rain >= 20.0 and any(keyword in chem for keyword in ["urea", "spray", "potash", "dap", "pesticide"]):
                self._guided_signatures.add(sig)
                rec = {
                    "tool": tool_name,
                    "chemical": chem,
                    "rain_mm": rain,
                    "verdict": "GUIDE",
                    "reason": f"Heavy rain ({rain}mm) forecast. Chemical broadcast prohibited."
                }
                self.log.append(rec)
                return Guide(feedback=f"Heavy rain of {rain}mm is forecast within 24 hours. Instruct the farmer to postpone applying {chem} until weather clears and open field drains instead.")

        rec = {
            "tool": tool_name,
            "args": args,
            "verdict": "PROCEED",
            "reason": "Safe operational parameters."
        }
        self.log.append(rec)
        return Proceed()
