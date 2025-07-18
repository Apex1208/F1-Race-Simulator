import requests
import pandas as pd
import os

def fetch_all_race_results(start_year=2000, end_year=2024, save_path='data/f1_race_results_2000_2024.csv'):
    race_data = []

    for year in range(start_year, end_year + 1):
        print(f"Fetching results for {year}...")
        offset = 0
        limit = 100

        while True:
            url = f"http://ergast.com/api/f1/{year}/results.json?limit={limit}&offset={offset}"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"⚠️ Failed to fetch data for {year}, offset {offset}")
                break

            data = response.json()
            races = data['MRData']['RaceTable']['Races']
            if not races:
                break

            for race in races:
                race_name = race['raceName']
                circuit = race['Circuit']['circuitName']
                date = race['date']
                round_num = int(race['round'])

                for result in race['Results']:
                    driver = result['Driver']
                    constructor = result['Constructor']

                    driver_name = f"{driver['givenName']} {driver['familyName']}"
                    constructor_name = constructor['name']
                    grid = int(result['grid'])
                    position = int(result['position'])
                    status = result['status']

                    race_data.append([
                        year, round_num, race_name, circuit, date,
                        driver_name, constructor_name, grid, position, status
                    ])
            offset += limit

    # Convert to DataFrame
    df = pd.DataFrame(race_data, columns=[
        'Year', 'Round', 'Race', 'Circuit', 'Date',
        'Driver', 'Constructor', 'Grid', 'Position', 'Status'
    ])

    # Save to CSV
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)

    print(f"\n✅ Saved {len(df)} race results to {save_path}")
    return df

# Run it!
df_race = fetch_all_race_results()

# Show summary
print(df_race.head())
print(df_race.info())
print(f"\nUnique drivers: {df_race['Driver'].nunique()}")
print(f"Unique constructors: {df_race['Constructor'].nunique()}")
