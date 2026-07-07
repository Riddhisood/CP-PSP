import csv
from typing import List
from core.models import MaintenanceEstimate

def export_priority_list_to_csv(estimates: List[MaintenanceEstimate], output_path: str) -> None:
    headers = [
        "Priority Rank",
        "Pipeline Name",
        "Chainage (km)",
        "Current Status",
        "Time Remaining (Months)",
        "Estimated Crossing Date"
    ]
    
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for est in estimates:
            writer.writerow([
                est.priority_rank,
                est.pipeline_name,
                est.chainage,
                est.current_status,
                est.time_remaining_months if est.time_remaining_months is not None else "N/A",
                est.estimated_crossing_date if est.estimated_crossing_date is not None else "N/A"
            ])
            
    print(f"📊 Priority report successfully generated and saved to: {output_path}")
    