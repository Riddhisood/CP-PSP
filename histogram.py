import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Replace this with your actual array of computed daily slopes from prediction/trend.py
# simulating a standard degradation distribution across the 152 pipeline locations
np.random.seed(42)
sample_slopes = np.random.normal(loc=-0.0005, scale=0.0008, size=152)

# Set up the plotting environment
plt.figure(figsize=(10, 5.5), dpi=300)
sns.set_theme(style="whitegrid")

# Create the histogram plot
ax = sns.histplot(
    sample_slopes, 
    bins=25, 
    kde=True, 
    color="#4A7BB0", 
    edgecolor="white", 
    linewidth=1
)

# Customize axis boundaries and labels using standard text configurations
plt.title("Distribution of Daily Potential Drift Rates (OLS Slopes)", fontsize=14, pad=15, weight="bold")
plt.xlabel("Daily Degradation Slope (V/day)", fontsize=11, labelpad=10)
plt.ylabel("Count of Pipeline Locations", fontsize=11, labelpad=10)

# Add a critical alert reference threshold line at slope = 0
plt.axvline(x=0, color="#D9534F", linestyle="--", linewidth=1.5, label="Stability Threshold (m = 0)")
plt.legend(loc="upper right", frameon=True)

# Clean up layout adjustments and export
plt.tight_layout()
plt.savefig("output/charts/overall_slope_distribution.png", dpi=300)
plt.close()