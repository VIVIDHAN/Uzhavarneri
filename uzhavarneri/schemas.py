"""Pydantic schemas for typed, reliable agronomic outputs."""

from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class WeatherCondition(BaseModel):
    district: str
    taluk: str
    rainfall_next_24h_mm: float = Field(..., description="Forecast rainfall in millimeters over the next 24 hours")
    rainfall_next_72h_mm: float = Field(..., description="Forecast cumulative rainfall in millimeters over the next 72 hours")
    max_wind_speed_kmh: float = Field(..., description="Expected peak wind speed in km/h")
    risk_level: Literal["LOW", "MODERATE", "SEVERE_STORM", "CYCLONIC"]
    summary: str


class CropStageInfo(BaseModel):
    crop_name: str
    days_after_sowing: int
    stage_name: str
    critical_needs: str
    fertilizer_window: str
    monsoon_risk_action: str


class AgrochemicalVerdict(BaseModel):
    chemical_or_fertilizer: str
    status: Literal["APPROVED", "BLOCKED", "CAUTION"]
    reason: str
    drainage_recommendation: str


class AgronomicActionPlan(BaseModel):
    immediate_action_24h: str = Field(..., description="Concrete instruction for today (e.g. dig drainage, hold fertilizer)")
    forecast_outlook_72h: str = Field(..., description="Short summary of upcoming rain and soil condition")
    drainage_guidance: str = Field(..., description="Specific field trench or sluice advice")
    agrochemical_safety: AgrochemicalVerdict = Field(..., description="Safety evaluation for fertilizer/pesticides")
    mandi_advice: Optional[str] = Field(None, description="Harvest holding or regulated market selling advisory")
    tamil_voice_script: str = Field(..., description="Colloquial spoken Tamil summary designed for voice broadcast")
