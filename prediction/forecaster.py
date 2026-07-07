from datetime import date, timedelta
from typing import List, Optional
from core.models import Reading, TrendMetrics, ForecastPoint

def forecast_to_date(latest_reading: Reading, trend: TrendMetrics, target_date: date) -> ForecastPoint:
    if trend.psp_off_slope_per_day is None or latest_reading.psp_off is None:
        return ForecastPoint(
            target_date=target_date,
            predicted_psp_on=None,
            predicted_psp_off=None
        )
        
    days_delta = (target_date - latest_reading.reading_date).days
    
    predicted_off = latest_reading.psp_off + (trend.psp_off_slope_per_day * days_delta)
    predicted_off = max(0.0, predicted_off)
    
    predicted_on = None
    if latest_reading.psp_on is not None and trend.psp_on_slope_per_day is not None:
        predicted_on = latest_reading.psp_on + (trend.psp_on_slope_per_day * days_delta)
        predicted_on = max(0.0, predicted_on)
        
    return ForecastPoint(
        target_date=target_date,
        predicted_psp_on=predicted_on,
        predicted_psp_off=predicted_off
    )

def generate_standard_forecasts(latest_reading: Reading, trend: TrendMetrics, horizons_years: List[float]) -> List[ForecastPoint]:
    forecasts = []
    for years in horizons_years:
        days_to_add = int(years * 365.25)
        target_date = latest_reading.reading_date + timedelta(days=days_to_add)
        forecast_pt = forecast_to_date(latest_reading, trend, target_date)
        forecasts.append(forecast_pt)
    return forecasts
