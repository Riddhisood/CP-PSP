from dataclasses import dataclass
from datetime import date
from typing import Optional, List

@dataclass
class Reading:
    reading_id: str
    pipeline_name: str
    chainage: float
    psp_on: Optional[float]
    psp_off: float
    reading_date: date
    
    id_src: Optional[str] = None
    tlpid: Optional[str] = None
    csp_on: Optional[float] = None
    csp_off: Optional[float] = None
    ac_psp: Optional[float] = None
    id_segment: Optional[str] = None
    st_name_sh: Optional[str] = None
    nm_start_met: Optional[float] = None
    nm_end_met: Optional[float] = None
    nm_diam_inch: Optional[float] = None
    st_material: Optional[str] = None
    st_product: Optional[str] = None
    nm_wt_inch: Optional[float] = None
    depth_of_cover: Optional[float] = None
    coating_type: Optional[str] = None
    coating_joi: Optional[str] = None
    year_of_co: Optional[int] = None
    soil_res_1: Optional[float] = None
    soil_res_2: Optional[float] = None
    soil_res_3: Optional[float] = None
    quarter: Optional[str] = None
    distance_u: Optional[float] = None
    distance_d: Optional[float] = None
    chainage_u: Optional[float] = None
    chainage_d: Optional[float] = None
    current_up: Optional[float] = None
    current_do: Optional[float] = None
    total_curre: Optional[float] = None
    anode_hor_1: Optional[float] = None
    anode_hor_2: Optional[float] = None
    anode_res_1: Optional[float] = None
    anode_res_2: Optional[float] = None
    anode_bec_1: Optional[float] = None
    anode_bec_2: Optional[float] = None
    total_res: Optional[float] = None
    quarter_nu: Optional[int] = None
    total_current_field: Optional[float] = None

@dataclass
class EvaluationResult:
    reading: Reading
    is_under_protected: bool
    is_over_protected: bool
    status_label: str

@dataclass
class TrendMetrics:
    psp_on_slope_per_day: Optional[float]
    psp_off_slope_per_day: Optional[float]
    confidence_score: float
    data_points_used: int
    status: str

@dataclass
class ForecastPoint:
    target_date: date
    predicted_psp_on: Optional[float]
    predicted_psp_off: Optional[float]

@dataclass
class MaintenanceEstimate:
    pipeline_name: str
    chainage: float
    current_status: str
    time_remaining_months: Optional[float]
    estimated_crossing_date: Optional[date]
    priority_rank: int