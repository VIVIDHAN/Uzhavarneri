"""Unit tests for UzhavarNeri agronomic tools."""

import pytest
from uzhavarneri.tools import (
    get_block_weather,
    get_crop_guidelines,
    check_mandi_prices,
    validate_agrochemical_safety
)


def test_get_block_weather_thanjavur():
    res = get_block_weather("thanjavur", "orathanadu")
    assert "rainfall_next_24h_mm" in res
    assert "risk_level" in res
    assert isinstance(res["rainfall_next_24h_mm"], (int, float))


def test_get_crop_guidelines_samba():
    # 45 DAS should fall in Active Tillering & Panicle Initiation
    res = get_crop_guidelines("samba_paddy", 45)
    assert res["crop"] == "Samba Paddy (Rice)"
    assert "Tillering" in res["current_stage"]
    assert "Urea" in res["fertilizer_window"]


def test_check_mandi_prices():
    res = check_mandi_prices("paddy_common", "thanjavur")
    assert res["market_district"] == "Thanjavur"
    assert res["modal_price_rs_per_quintal"] >= 2000


def test_validate_agrochemical_safety_prohibits_heavy_rain():
    # 25mm rain should block chemical spray
    res = validate_agrochemical_safety("Urea", rainfall_forecast_mm=25.0)
    assert res["status"] == "BLOCKED"
    assert "POSTPONE" in res["verdict"]


def test_validate_agrochemical_safety_blocks_banned_pesticide():
    # Monocrotophos is strictly banned
    res = validate_agrochemical_safety("Monocrotophos 36% SL", rainfall_forecast_mm=0.0)
    assert res["status"] == "BLOCKED"
    assert "BANNED" in res["verdict"]


def test_validate_agrochemical_safety_permits_safe_conditions():
    # Clear weather and legal spray
    res = validate_agrochemical_safety("Neem Oil 1500ppm", rainfall_forecast_mm=2.0, wind_speed_kmh=8.0)
    assert res["status"] == "APPROVED"
