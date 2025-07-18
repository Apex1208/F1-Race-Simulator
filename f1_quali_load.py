import requests
import pandas as pd
import os

# Load your race data
race_df = pd.read_csv('data/f1_race_results_2000_2024.csv')

def fetch_qualifying_results(start_year=2000, end_year=2024):
    quali_data = []

    for year in range(start_year, end_year + 1):
        print(f"Fetching qualifying for {year}...")
        for round_num in range(1, 25):  # F1 maxes out around 23 races a season
            url = f"http://ergast.com/api/f1/{year}/{round_num}/qualifying.json?limit=100"
            res = requests.get(url)
            if res.status_code != 200:
                continue

            data = res.json()
            races = data['MRData']['RaceTable']['Races']
            if not races:
                continue

            race = races[0]
            if 'QualifyingResults' not in race:
                continue

            for result in race['QualifyingResults']:
                driver = result['Driver']
                driver_name = f"{driver['givenName']} {driver['familyName']}"
                q1 = result.get('Q1', None)
                q2 = result.get('Q2', None)
                q3 = result.get('Q3', None)

                quali_data.append([
                    year, int(race['round']), driver_name, q1, q2, q3
                ])

    quali_df = pd.DataFrame(quali_data, columns=[
        'Year', 'Round', 'Driver', 'Q1', 'Q2', 'Q3'
    ])
    return quali_df

# Fetch qualifying data
quali_df = fetch_qualifying_results()

# Merge with your existing race data
merged_df = pd.merge(
    race_df,
    quali_df,
    on=['Year', 'Round', 'Driver'],
    how='left'
)

# Save merged file
save_path = 'data/f1_race_with_quali.csv'
merged_df.to_csv(save_path, index=False)
print(f"\n✅ Final dataset with qualifying times saved to {save_path}")
