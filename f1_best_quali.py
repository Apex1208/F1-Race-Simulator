import pandas as pd
import numpy as np

# Load your dataset
df = pd.read_csv("data/f1_final_dataset_with_winrates.csv")

# Helper function to convert time string like "1:23.456" to seconds
def time_to_seconds(time_str):
    if pd.isna(time_str):
        return np.nan
    try:
        minutes, seconds = time_str.split(":")
        return float(minutes) * 60 + float(seconds)
    except:
        return np.nan

# Convert Q1, Q2, Q3 to seconds
df["Q1_secs"] = df["Q1"].apply(time_to_seconds)
df["Q2_secs"] = df["Q2"].apply(time_to_seconds)
df["Q3_secs"] = df["Q3"].apply(time_to_seconds)

# Compute best qualifying time from the three (ignore NaNs)
df["BestQualiTime"] = df[["Q1_secs", "Q2_secs", "Q3_secs"]].min(axis=1)

# Save updated dataset
df.to_csv("data/f1_final_dataset_with_bestquali.csv", index=False)

print("✅ BestQualiTime column created and dataset saved as f1_final_dataset_with_bestquali.csv")
