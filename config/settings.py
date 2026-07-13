import os

DEFAULT_THRESHOLDS = {
    "PSP_OFF_MIN_MAGNITUDE": 0.85,
    "PSP_ON_MAX_MAGNITUDE": 1.20,
}

PIPELINE_SPECIFIC_THRESHOLDS = {
    "MAIN_LINE_A": {
        "PSP_OFF_MIN_MAGNITUDE": 0.85,
        "PSP_ON_MAX_MAGNITUDE": 1.15,
    }
}

FORECAST_SETTINGS = {
    "DEFAULT_HORIZONS_YEARS": [1.0, 2.0, 5.0],
}

def get_thresholds(pipeline_name: str) -> dict:
    return PIPELINE_SPECIFIC_THRESHOLDS.get(pipeline_name, DEFAULT_THRESHOLDS)
