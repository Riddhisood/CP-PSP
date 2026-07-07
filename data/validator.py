import pandas as pd

REQUIRED_COLUMNS = ["ID", "stName", "READING_CHAINAGE", "PSP_ON", "PSP_OFF", "READING_DATE"]

def validate_and_clean_schema(df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.copy()
    
    if "READING_`_DATE" in df_cleaned.columns and "READING_DATE" not in df_cleaned.columns:
        df_cleaned = df_cleaned.rename(columns={"READING_`_DATE": "READING_DATE"})
    elif "READING_DATE" not in df_cleaned.columns:
        date_cols = [col for col in df_cleaned.columns if "READING" in col and "DATE" in col]
        if date_cols:
            df_cleaned = df_cleaned.rename(columns={date_cols[0]: "READING_DATE"})

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df_cleaned.columns]
    if missing_cols:
        raise ValueError(f"Input data is missing mandatory columns or has name mismatches: {missing_cols}")
        
    df_cleaned["READING_DATE"] = pd.to_datetime(df_cleaned["READING_DATE"]).dt.date
    
    df_cleaned["READING_CHAINAGE"] = pd.to_numeric(df_cleaned["READING_CHAINAGE"], errors="coerce")
    df_cleaned["PSP_ON"] = pd.to_numeric(df_cleaned["PSP_ON"], errors="coerce")
    df_cleaned["PSP_OFF"] = pd.to_numeric(df_cleaned["PSP_OFF"], errors="coerce")
    
    critical_nulls = df_cleaned[
        df_cleaned["READING_CHAINAGE"].isna() | 
        df_cleaned["PSP_OFF"].isna() | 
        df_cleaned["READING_DATE"].isna()
    ]
    if not critical_nulls.empty:
        print(f"⚠️ Warning: Dropping {len(critical_nulls)} rows due to null values in critical fields (READING_CHAINAGE, PSP_OFF, or READING_DATE).")
        df_cleaned = df_cleaned.dropna(subset=["READING_CHAINAGE", "PSP_OFF", "READING_DATE"])
        
    df_cleaned = df_cleaned.sort_values(by=["stName", "READING_CHAINAGE", "READING_DATE"]).reset_index(drop=True)
    
    return df_cleaned
