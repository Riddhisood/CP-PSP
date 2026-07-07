import pandas as pd
from typing import List
from core.models import Reading
from data.validator import validate_and_clean_schema

def load_data_from_file(file_path: str) -> List[Reading]:
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
        
    df_normalized = validate_and_clean_schema(df)
    
    readings = []
    for _, row in df_normalized.iterrows():
        reading = Reading(
            reading_id=str(row["ID"]),
            pipeline_name=str(row["stName"]),
            chainage=float(row["READING_CHAINAGE"]),
            psp_on=float(row["PSP_ON"]) if pd.notna(row["PSP_ON"]) else None,
            psp_off=float(row["PSP_OFF"]),
            reading_date=row["READING_DATE"],
            depth_of_cover=float(row["depth_of_cover"]) if "depth_of_cover" in row and pd.notna(row["depth_of_cover"]) else None,
            coating_type=str(row["coating_type"]) if "coating_type" in row and pd.notna(row["coating_type"]) else None,
            year_of_coating=int(row["year_of_coating"]) if "year_of_coating" in row and pd.notna(row["year_of_coating"]) else None
        )
        readings.append(reading)
        
    return readings