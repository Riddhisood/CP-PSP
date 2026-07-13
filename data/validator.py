import pandas as pd

REQUIRED_COLUMNS = ["ID", "stName", "PSP_ON", "PSP_OFF", "READING_DATE"]

def validate_and_clean_schema(df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.copy()
    
    df_cleaned.columns = df_cleaned.columns.str.strip()
    
    if df_cleaned.columns.duplicated().any():
        df_cleaned = df_cleaned.loc[:, ~df_cleaned.columns.duplicated()].copy()
        
    if "READING_" in df_cleaned.columns:
        df_cleaned = df_cleaned.rename(columns={"READING_": "READING_DATE"})
    else:
        date_candidates = [col for col in df_cleaned.columns if "READING" in col.upper() and "CHAINAGE" not in col.upper()]
        if date_candidates:
            df_cleaned = df_cleaned.rename(columns={date_candidates[0]: "READING_DATE"})
        else:
            raise ValueError("Input data is missing a date column (could not find 'READING_').")

    chainage_candidates = [col for col in df_cleaned.columns if col.upper() == "CHAINAGE"]
    if not chainage_candidates:
        chainage_candidates = [col for col in df_cleaned.columns if "CHAINAGE" in col.upper() and col != "READING_DATE"]
        
    if chainage_candidates:
        df_cleaned = df_cleaned.rename(columns={chainage_candidates[0]: "READING_CHAINAGE"})
    else:
        raise ValueError("Input data is missing a chainage location column (could not find any column containing 'CHAINAGE').")

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df_cleaned.columns]
    if missing_cols:
        raise ValueError(f"Input data is missing mandatory columns or has name mismatches: {missing_cols}")
        
    df_cleaned["READING_DATE"] = pd.to_datetime(df_cleaned["READING_DATE"], errors="coerce").dt.date
    
    df_cleaned["READING_CHAINAGE"] = pd.to_numeric(df_cleaned["READING_CHAINAGE"], errors="coerce")
    df_cleaned["PSP_ON"] = pd.to_numeric(df_cleaned["PSP_ON"], errors="coerce")
    df_cleaned["PSP_OFF"] = pd.to_numeric(df_cleaned["PSP_OFF"], errors="coerce")
    
    critical_nulls = df_cleaned[
        df_cleaned["READING_CHAINAGE"].isna() | 
        df_cleaned["PSP_OFF"].isna() | 
        df_cleaned["READING_DATE"].isna()
    ]
    if not critical_nulls.empty:
        print(f"⚠️ Warning: Dropping {len(critical_nulls)} rows due to null values or invalid formats in critical fields.")
        df_cleaned = df_cleaned.dropna(subset=["READING_CHAINAGE", "PSP_OFF", "READING_DATE"])
        
    df_cleaned = df_cleaned.sort_values(by=["stName", "READING_CHAINAGE", "READING_DATE"]).reset_index(drop=True)
    
    return df_cleaned