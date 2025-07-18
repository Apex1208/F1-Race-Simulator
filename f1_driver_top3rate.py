import pandas as pd

# Load dataset
df = pd.read_csv("data/f1_final_dataset_with_bestquali.csv")

# Sort the data properly
df = df.sort_values(by=["Driver", "Year", "Round"]).reset_index(drop=True)

# Define the recent window size
RECENT_WINDOW = 5

# Compute top-3 finish rate for each driver
def add_recent_top3_rate(df, window=RECENT_WINDOW):
    rates = []
    for driver, group in df.groupby("Driver"):
        group = group.sort_values(by=["Year", "Round"])
        past_results = []
        for _, row in group.iterrows():
            if len(past_results) < window:
                rates.append(0.0)
            else:
                top3_rate = sum(past_results[-window:]) / window
                rates.append(top3_rate)
            past_results.append(1 if row["Position"] <= 3 else 0)
    return rates

# Apply and add to DataFrame
df["DriverRecentTop3Rate"] = add_recent_top3_rate(df)

# Save updated dataset
df.to_csv("data/f1_final_dataset_with_driverform_top3.csv", index=False)
print("✅ DriverRecentTop3Rate feature added and saved as 'f1_final_dataset_with_driverform_top3.csv'")
