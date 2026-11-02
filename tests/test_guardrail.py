"""Unit tests for AgrochemicalSafetyGuard intervention handler."""

from types import SimpleNamespace
from strands.interventions import Deny, Guide, Proceed
from uzhavarneri.guardrails import AgrochemicalSafetyGuard


def test_guardrail_allows_normal_weather_tool():
    guard = AgrochemicalSafetyGuard()
    event = SimpleNamespace(
        tool_use={"name": "get_block_weather", "input": {"district": "Thanjavur"}}
    )
    result = guard.before_tool_call(event)
    assert isinstance(result, Proceed)


def test_guardrail_guides_on_rain_fertilizer():
    guard = AgrochemicalSafetyGuard()
    event = SimpleNamespace(
        tool_use={
            "name": "validate_agrochemical_safety",
            "input": {"chemical_name": "Urea", "rainfall_forecast_mm": 35.0}
        }
    )
    first_attempt = guard.before_tool_call(event)
    assert isinstance(first_attempt, Guide)
    assert "postpone" in first_attempt.feedback.lower()

    # Convergence test: identical second attempt must be Denied
    second_attempt = guard.before_tool_call(event)
    assert isinstance(second_attempt, Deny)


def test_guardrail_denies_banned_pesticide():
    guard = AgrochemicalSafetyGuard()
    event = SimpleNamespace(
        tool_use={
            "name": "validate_agrochemical_safety",
            "input": {"chemical_name": "Endosulfan 35 EC", "rainfall_forecast_mm": 0.0}
        }
    )
    result = guard.before_tool_call(event)
    assert isinstance(result, Deny)
    assert "banned" in result.reason.lower()
