from typing import List, Dict, Tuple
from datetime import date
import numpy as np
from core.models import Reading, TrendMetrics

def _calculate_slope(dates: List[date], values: List[float]) -> float:
    reference_date = dates[0]
    days = np.array([(d - reference_date).days for d in dates], dtype=float)
    y = np.array(values, dtype=float)
    
    A = np.vstack([days, np.ones(len(days))]).T
    slope, _ = np.linalg.lstsq(A, y, rcond=None)[0]
    return float(slope)

def calculate_chainage_trend(readings: List[Reading]) -> TrendMetrics:
    sorted_readings = sorted(readings, key=lambda r: r.reading_date)
    count = len(sorted_readings)
    
    if count < 2:
        return TrendMetrics(
            psp_on_slope_per_day=None,
            psp_off_slope_per_day=None,
            confidence_score=0.0,
            data_points_used=count,
            status="INSUFFICIENT_HISTORY"
        )
        
    dates = [r.reading_date for r in sorted_readings]
    
    unique_dates = len(set(dates))
    if unique_dates < count:
        raise ValueError("Multiple readings detected on the exact same date for the same chainage location.")

    psp_off_vals = [r.psp_off for r in sorted_readings]
    psp_off_slope = _calculate_slope(dates, psp_off_vals)
    
    valid_on_readings = [r for r in sorted_readings if r.psp_on is not None]
    if len(valid_on_readings) >= 2:
        on_dates = [r.reading_date for r in valid_on_readings]
        on_vals = [r.psp_on for r in valid_on_readings]
        psp_on_slope = _calculate_slope(on_dates, on_vals)
    else:
        psp_on_slope = None
        
    confidence = 0.4 if count == 2 else 0.9
    status = "LOW_CONFIDENCE_TREND" if count == 2 else "STABLE_TREND"
    
    return TrendMetrics(
        psp_on_slope_per_day=psp_on_slope,
        psp_off_slope_per_day=psp_off_slope,
        confidence_score=confidence,
        data_points_used=count,
        status=status
    )

def calculate_all_trends(readings: List[Reading]) -> Dict[Tuple[str, float], TrendMetrics]:
    groups = {}
    for r in readings:
        key = (r.pipeline_name, r.chainage)
        groups.setdefault(key, []).append(r)
        
    return {key: calculate_chainage_trend(readings_list) for key, readings_list in groups.items()}
