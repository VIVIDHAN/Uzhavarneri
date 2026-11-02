"""UzhavarNeri Agent: Autonomous agricultural advisor with Strands Agents SDK."""

from __future__ import annotations

import time
from typing import Any, Dict, List
from strands import Agent

from .config import get_agent_model, get_llm_provider
from .guardrails import AgrochemicalSafetyGuard
from .tools import TOOLS

SYSTEM_PROMPT = """You are UzhavarNeri (உழவர்நெறி), an expert, climate-resilient agricultural advisor dedicated to smallholder farmers in Tamil Nadu.
You understand English, Tamil (தமிழ்), and Tanglish.

Your primary duty is to protect farmers from weather disasters, fertilizer loss, and crop failure during the Northeast Monsoon (வடகிழக்கு பருவமழை).

Rules for your advice:
1. Always call `get_block_weather` when a farmer asks about rain, weather, spraying, or harvesting in a specific district or taluk.
2. Always call `get_crop_guidelines` to check the exact growth stage using the Days After Sowing (DAS) according to Tamil Nadu Agricultural University (TNAU) agronomic schedules.
3. If the farmer asks to apply Urea, DAP, or chemical sprays, ALWAYS call `validate_agrochemical_safety` with the forecast rainfall.
4. If rainfall > 15mm is forecast within 24 hours, FIRMLY advise POSTPONING fertilizer or chemical application, because rainfall washes chemicals away into irrigation canals, wasting thousands of rupees. Instruct them to dig or clear field drainage trenches instead.
5. If the farmer mentions a banned chemical (like Monocrotophos or Endosulfan), warn them that it is banned by the government and recommend safe bio-alternatives (e.g. Neem oil, Pseudomonas).
6. Always end your response with a short, friendly spoken Tamil summary section titled:
'🎙️ குரல் வழி செய்தி (Tamil Audio Summary):'
written in everyday spoken Tamil so a farmer listening on WhatsApp can easily understand today's action."""


class UzhavarNeriAgent:
    """Production agricultural agent with safety interventions and multi-turn state."""

    def __init__(self, model: Any = None):
        self.model = model or get_agent_model()
        self.guard = AgrochemicalSafetyGuard()
        self.agent = Agent(
            model=self.model,
            system_prompt=SYSTEM_PROMPT,
            tools=TOOLS,
            interventions=[self.guard],
            callback_handler=None,
        )
        self.provider = get_llm_provider()

    def chat(self, message: str) -> Dict[str, Any]:
        """Process farmer query and return response with guardrail interventions and latency."""
        t0 = time.perf_counter()
        before_guard_count = len(self.guard.log)

        # Run the Strands Agent
        result = self.agent(message)
        latency_ms = round((time.perf_counter() - t0) * 1000)

        new_interventions = self.guard.log[before_guard_count:]

        return {
            "reply": str(result).strip(),
            "interventions": new_interventions,
            "latency_ms": latency_ms,
            "provider": self.provider,
        }


if __name__ == "__main__":
    agent = UzhavarNeriAgent()
    query = "Samba paddy 45 days in Orathanadu, Thanjavur. Can I spray urea tomorrow?"
    print(f"Farmer: {query}\n")
    out = agent.chat(query)
    print("--- UzhavarNeri Advice ---")
    print(out["reply"])
    print(f"\n[Interventions: {len(out['interventions'])} | Latency: {out['latency_ms']} ms]")
