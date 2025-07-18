import pandas as pd

# Load the complete dataset (you likely already have this loaded)
df = pd.read_csv("data/f1_race_with_quali_weather_filled.csv")

# Make sure the 'Winner' column exists
if 'Winner' not in df.columns:
    df['Winner'] = (df['Position'] == 1).astype(int)

# -- 1. All-Time Constructor Win Rate (2000–2024) --
alltime_stats = df.groupby('Constructor').agg(
    AllTimeWins=('Winner', 'sum'),
    AllTimeRaces=('Winner', 'count')
).reset_index()

alltime_stats['ConstructorWinRate_AllTime'] = alltime_stats['AllTimeWins'] / alltime_stats['AllTimeRaces']

# -- 2. Recent Constructor Win Rate (2020–2024) --
recent_df = df[df['Year'] >= 2020]

recent_stats = recent_df.groupby('Constructor').agg(
    RecentWins=('Winner', 'sum'),
    RecentRaces=('Winner', 'count')
).reset_index()

recent_stats['ConstructorWinRate_Recent'] = recent_stats['RecentWins'] / recent_stats['RecentRaces']

# -- 3. Merge both win rates back to the original DataFrame --
df = df.merge(alltime_stats[['Constructor', 'ConstructorWinRate_AllTime']], on='Constructor', how='left')
df = df.merge(recent_stats[['Constructor', 'ConstructorWinRate_Recent']], on='Constructor', how='left')

# Save updated version
df.to_csv("data/f1_final_dataset_with_winrates.csv", index=False)
print("✅ Win rate features added successfully.")

print(df[['Constructor', 'ConstructorWinRate_AllTime', 'ConstructorWinRate_Recent']].drop_duplicates().head())

print("All constructors present in final dataset:")
print(df['Constructor'].value_counts())

print("\nCheck McLaren rows specifically:")
print(df[df['Constructor'].str.lower().str.contains('mclaren')])


