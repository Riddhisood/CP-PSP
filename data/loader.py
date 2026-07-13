import pandas as pd
from typing import List
from core.models import Reading
from data.validator import validate_and_clean_schema

def _get_val(row, col_name, var_type=float):
    if col_name in row and pd.notna(row[col_name]):
        try:
            return var_type(row[col_name])
        except (ValueError, TypeError):
            return None
    return None

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
            psp_on=_get_val(row, "PSP_ON"),
            psp_off=float(row["PSP_OFF"]),
            reading_date=row["READING_DATE"],
            
            id_src=_get_val(row, "ID_SRC", str),
            tlpid=_get_val(row, "TLPID", str),
            csp_on=_get_val(row, "CSP_ON"),
            csp_off=_get_val(row, "CSP_OFF"),
            ac_psp=_get_val(row, "AC_PSP"),
            id_segment=_get_val(row, "idSegment", str),
            st_name_sh=_get_val(row, "stNameSh", str),
            nm_start_met=_get_val(row, "nmStartMe"),
            nm_end_met=_get_val(row, "nmEndMet"),
            nm_diam_inch=_get_val(row, "nmDiamIn"),
            st_material=_get_val(row, "stMaterial", str),
            st_product=_get_val(row, "stProduct", str),
            nm_wt_inch=_get_val(row, "nmWTInch"),
            depth_of_cover=_get_val(row, "depth_of_c"),
            coating_type=_get_val(row, "coating_ty", str),
            coating_joi=_get_val(row, "coating_joi", str),
            year_of_co=_get_val(row, "year_of_co", int),
            soil_res_1=_get_val(row, "soil_res_1"),
            soil_res_2=_get_val(row, "soil_res_2"),
            soil_res_3=_get_val(row, "soil_res_3"),
            quarter=_get_val(row, "quarter", str),
            distance_u=_get_val(row, "distance_u"),
            distance_d=_get_val(row, "distance_d"),
            chainage_u=_get_val(row, "chainage_u"),
            chainage_d=_get_val(row, "chainage_d"),
            current_up=_get_val(row, "current_up"),
            current_do=_get_val(row, "current_dc"),
            total_curre=_get_val(row, "total_curre"),
            anode_hor_1=_get_val(row, "anode_hor"),
            anode_hor_2=_get_val(row, "anode_hor.1"),
            anode_res_1=_get_val(row, "anode_res"),
            anode_res_2=_get_val(row, "anode_res.1"),
            anode_bec_1=_get_val(row, "anode_bec"),
            anode_bec_2=_get_val(row, "anode_bec.1"),
            total_res=_get_val(row, "total_res"),
            quarter_nu=_get_val(row, "quarter_nu", int),
            total_current_field=_get_val(row, "Total_Current")
        )
        readings.append(reading)
        
    return readings