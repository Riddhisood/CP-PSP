import os
from datetime import date
from data.loader import load_data_from_file
from prediction.trend import calculate_chainage_trend
from prediction.forecaster import generate_standard_forecasts
from maintenance.scheduler import generate_priority_list
from reporting.exporter import export_priority_list_to_csv
from visualization.chart_builder import build_chainage_chart

def run_predictive_maintenance_pipeline(input_file_path: str, output_report_path: str, generate_charts: bool = False):
    print("🚀 Starting CP/PSP Predictive Maintenance Pipeline...")
    
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Input file not found at: {input_file_path}")
        
    all_readings = load_data_from_file(input_file_path)
    print(f"📥 Loaded and validated {len(all_readings)} total historical reading entries.")
    
    chainage_groups = {}
    for r in all_readings:
        key = (r.pipeline_name, r.chainage)
        chainage_groups.setdefault(key, []).append(r)
        
    latest_readings_with_trends = []
    
    os.makedirs("output/charts", exist_ok=True)
    
    for key, readings_list in chainage_groups.items():
        pipeline_name, chainage = key
        
        sorted_readings = sorted(readings_list, key=lambda r: r.reading_date)
        latest_reading = sorted_readings[-1]
        
        trend = calculate_chainage_trend(sorted_readings)
        
        latest_readings_with_trends.append((latest_reading, trend))
        
        if generate_charts and trend.psp_off_slope_per_day is not None:
            horizons = [1.0, 2.0, 3.0]
            forecasts = generate_standard_forecasts(latest_reading, trend, horizons)
            
            sanitized_pipeline = pipeline_name.replace("/", "_").replace("\\", "_")
            chart_filename = f"output/charts/{sanitized_pipeline}_km_{str(chainage).replace('.', '_')}.png"
            build_chainage_chart(sorted_readings, trend, forecasts, output_path=chart_filename)
            
    priority_list = generate_priority_list(latest_readings_with_trends)
    
    export_priority_list_to_csv(priority_list, output_report_path)
    print("🎉 Pipeline run execution completed successfully.")

if __name__ == "__main__":
    DATA_PATH = "CP_PSP_DATA.xlsx"
    REPORT_PATH = "output/maintenance_priorities.csv"
    
    if not os.path.exists(DATA_PATH):
        print(f"💡 Info: To run a live operational test, place a data file named '{DATA_PATH}' in this root directory.")
    else:
        run_predictive_maintenance_pipeline(DATA_PATH, REPORT_PATH, generate_charts=True)