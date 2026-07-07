from core.models import Reading, EvaluationResult
from config.settings import get_thresholds

def classify_reading(reading: Reading) -> EvaluationResult:
    thresholds = get_thresholds(reading.pipeline_name)
    
    psp_off_min = thresholds["PSP_OFF_MIN_MAGNITUDE"]
    psp_on_max = thresholds["PSP_ON_MAX_MAGNITUDE"]
    
    is_under = reading.psp_off < psp_off_min
    
    is_over = False
    if reading.psp_on is not None:
        is_over = reading.psp_on > psp_on_max
        
    if is_under:
        status_label = "UNDER-PROTECTED"
    elif is_over:
        status_label = "OVERPROTECTION CAUTION"
    else:
        status_label = "HEALTHY"
        
    return EvaluationResult(
        reading=reading,
        is_under_protected=is_under,
        is_over_protected=is_over,
        status_label=status_label
    )

def classify_batch(readings: list[Reading]) -> list[EvaluationResult]:
    return [classify_reading(r) for r in readings]
