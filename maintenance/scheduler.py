from datetime import date, timedelta
from typing import List, Optional
from core.models import Reading, TrendMetrics, MaintenanceEstimate
from config.settings import get_thresholds

def estimate_time_to_maintenance(
    latest_reading: Reading, 
    trend: TrendMetrics, 
    priority_index: int = 9999
) -> MaintenanceEstimate:
    
    thresholds = get_thresholds(latest_reading.pipeline_name)
    min_off_threshold = thresholds["PSP_OFF_MIN_MAGNITUDE"]
    
    if latest_reading.psp_off < min_off_threshold:
        return MaintenanceEstimate(
            pipeline_name=latest_reading.pipeline_name,
            chainage=latest_reading.chainage,
            current_status="ALREADY DUE",
            time_remaining_months=0.0,
            estimated_crossing_date=latest_reading.reading_date,
            priority_rank=priority_index
        )
        
    slope = trend.psp_off_slope_per_day
    
    if slope is None or slope >= 0:
        return MaintenanceEstimate(
            pipeline_name=latest_reading.pipeline_name,
            chainage=latest_reading.chainage,
            current_status="STABLE",
            time_remaining_months=None,
            estimated_crossing_date=None,
            priority_rank=priority_index
        )
        
    delta_v = min_off_threshold - latest_reading.psp_off
    days_remaining = delta_v / slope
    
    months_remaining = days_remaining / 30.4375
    crossing_date = latest_reading.reading_date + timedelta(days=int(days_remaining))
    
    return MaintenanceEstimate(
        pipeline_name=latest_reading.pipeline_name,
        chainage=latest_reading.chainage,
        current_status="DEGRADING",
        time_remaining_months=round(months_remaining, 1),
        estimated_crossing_date=crossing_date,
        priority_rank=priority_index
    )

def generate_priority_list(
    latest_readings_with_trends: List[tuple[Reading, TrendMetrics]]
) -> List[MaintenanceEstimate]:
    
    estimates = []
    for reading, trend in latest_readings_with_trends:
        est = estimate_time_to_maintenance(reading, trend)
        estimates.append(est)
        
    def sort_key(e: MaintenanceEstimate):
        if e.current_status == "ALREADY DUE":
            return (0, 0.0)
        if e.current_status == "DEGRADING" and e.time_remaining_months is not None:
            return (1, e.time_remaining_months)
        return (2, float("inf"))
        
    estimates.sort(key=sort_key)
    
    for rank, est in enumerate(estimates, start=1):
        est.priority_rank = rank
        
    return estimates
