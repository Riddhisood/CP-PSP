import matplotlib.pyplot as plt
from datetime import date
from typing import List, Optional
from core.models import Reading, TrendMetrics, ForecastPoint
from config.settings import get_thresholds

def build_chainage_chart(
    historical_readings: List[Reading],
    trend: TrendMetrics,
    forecast_points: List[ForecastPoint],
    output_path: Optional[str] = None
) -> None:
    if not historical_readings:
        return

    sorted_history = sorted(historical_readings, key=lambda r: r.reading_date)
    pipeline_name = sorted_history[0].pipeline_name
    chainage = sorted_history[0].chainage

    thresholds = get_thresholds(pipeline_name)
    min_off = thresholds["PSP_OFF_MIN_MAGNITUDE"]
    max_on = thresholds["PSP_ON_MAX_MAGNITUDE"]

    plt.figure(figsize=(10, 6))

    hist_dates = [r.reading_date for r in sorted_history]
    hist_off = [r.psp_off for r in sorted_history]
    plt.scatter(hist_dates, hist_off, color="blue", label="Actual PSP OFF", zorder=5)

    hist_on_readings = [r for r in sorted_history if r.psp_on is not None]
    if hist_on_readings:
        hist_on_dates = [r.reading_date for r in hist_on_readings]
        hist_on = [r.psp_on for r in hist_on_readings]
        plt.scatter(hist_on_dates, hist_on, color="darkorange", label="Actual PSP ON", zorder=5)

    if trend.psp_off_slope_per_day is not None and forecast_points:
        sorted_forecasts = sorted(forecast_points, key=lambda f: f.target_date)
        
        line_dates = [sorted_history[-1].reading_date] + [f.target_date for f in sorted_forecasts]
        
        off_line_vals = [sorted_history[-1].psp_off] + [f.predicted_psp_off for f in sorted_forecasts]
        plt.plot(line_dates, off_line_vals, color="blue", linestyle="--", label="Forecast PSP OFF")

        if sorted_history[-1].psp_on is not None and trend.psp_on_slope_per_day is not None:
            on_line_vals = [sorted_history[-1].psp_on] + [f.predicted_psp_on for f in sorted_forecasts]
            plt.plot(line_dates, on_line_vals, color="darkorange", linestyle="--", label="Forecast PSP ON")

    all_dates = hist_dates + [f.target_date for f in forecast_points]
    min_date, max_date = min(all_dates), max(all_dates)

    plt.hlines(min_off, min_date, max_date, colors="red", linestyles=":", label=f"Min OFF Threshold ({min_off}V)")
    plt.hlines(max_on, min_date, max_date, colors="darkred", linestyles="-.", label=f"Max ON Caution ({max_on}V)")

    plt.title(f"CP Protection Profile & Trend Forecasting\nPipeline: {pipeline_name} | Chainage: {chainage} km (Confidence: {trend.status})")
    plt.xlabel("Survey Date")
    plt.ylabel("Potential Magnitude (-V)")
    plt.legend(loc="upper left")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150)
        plt.close()
    else:
        plt.show()
        