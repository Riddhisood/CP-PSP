import pandas as pd

REQUIRED_COLUMNS = ["ID", "stName", "CHAINAGE", "PSP_ON", "PSP_OFF", "READING_DATE"]

def validate_and_clean_schema(df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.copy()
    
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df_cleaned.columns]
    if missing_cols:
        raise ValueError(f"Input data is missing mandatory columns: {missing_cols}")
        
    df_cleaned["READING_DATE"] = pd.to_datetime(df_cleaned["READING_DATE"]).dt.date
    
    df_cleaned["CHAINAGE"] = pd.to_numeric(df_cleaned["CHAINAGE"], errors="coerce")
    df_cleaned["PSP_ON"] = pd.to_numeric(df_cleaned["PSP_ON"], errors="coerce")
    df_cleaned["PSP_OFF"] = pd.to_numeric(df_cleaned["PSP_OFF"], errors="coerce")
    
    critical_nulls = df_cleaned[
        df_cleaned["CHAINAGE"].isna() | 
        df_cleaned["PSP_OFF"].isna() | 
        df_cleaned["READING_DATE"].isna()
    ]
    if not critical_nulls.empty:
        print(f"⚠️ Warning: Dropping {len(critical_nulls)} rows due to null values in critical fields (CHAINAGE, PSP_OFF, or READING_DATE).")
        df_cleaned = df_cleaned.dropna(subset=["CHAINAGE", "PSP_OFF", "READING_DATE"])
        
    df_cleaned = df_cleaned.sort_values(by=["stName", "CHAINAGE", "READING_DATE"]).reset_index(drop=True)
    
    return df_cleaned
