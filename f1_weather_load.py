import pandas as pd
import requests
import time

API_KEY = "AUJZVMPUFFX6E3ZQYSHAZFZXE"

# Load your main dataset
df = pd.read_csv("data/f1_race_with_quali.csv")

# Predefined coordinates for known circuits (expand this as needed)
circuit_coords = {
    "Albert Park Grand Prix Circuit": (-37.8497, 144.968),
    "Autodromo Enzo e Dino Ferrari": (44.3439, 11.7167),
    "Autodromo Internazionale del Mugello": (43.9994, 11.3717),
    "Autodromo Nazionale di Monza": (45.6156, 9.2811),
    "Autódromo Hermanos Rodríguez": (19.4042, -99.0907),
    "Autódromo Internacional do Algarve": (37.2283, -8.6267),
    "Autódromo José Carlos Pace": (-23.7036, -46.6997),
    "Bahrain International Circuit": (26.0325, 50.5106),
    "Baku City Circuit": (40.3725, 49.8533),
    "Buddh International Circuit": (28.3518, 77.5341),
    "Circuit Gilles Villeneuve": (45.5, -73.5228),
    "Circuit Park Zandvoort": (52.3889, 4.5400),
    "Circuit Paul Ricard": (43.2506, 5.7917),
    "Circuit de Barcelona-Catalunya": (41.5706, 2.2611),
    "Circuit de Monaco": (43.7347, 7.4206),
    "Circuit de Nevers Magny-Cours": (46.8642, 3.1633),
    "Circuit de Spa-Francorchamps": (50.4372, 5.9714),
    "Circuit of the Americas": (30.1328, -97.6411),
    "Fuji Speedway": (35.3717, 138.9275),  # Added based on actual location
    "Hockenheimring": (49.3278, 8.5658),
    "Hungaroring": (47.5789, 19.2486),
    "Indianapolis Motor Speedway": (39.795, -86.2347),
    "Istanbul Park": (40.9517, 29.405),
    "Jeddah Corniche Circuit": (21.6319, 39.1044),
    "Korean International Circuit": (34.7333, 126.4175),
    "Las Vegas Strip Street Circuit": (36.1147, -115.1728),  # Estimated from Strip location
    "Losail International Circuit": (25.49, 51.4533),
    "Marina Bay Street Circuit": (1.2914, 103.8644),
    "Miami International Autodrome": (25.9581, -80.2389),
    "Nürburgring": (50.3356, 6.9475),
    "Red Bull Ring": (47.2197, 14.7647),
    "Sepang International Circuit": (2.7608, 101.7382),
    "Shanghai International Circuit": (31.3389, 121.2197),
    "Silverstone Circuit": (52.0786, -1.0169),
    "Sochi Autodrom": (43.4057, 39.9578),
    "Suzuka Circuit": (34.8431, 136.5419),
    "Valencia Street Circuit": (39.4589, -0.3319),
    "Yas Marina Circuit": (24.4672, 54.6031),

    # Add more as needed
}

# Step 1: Get unique (Date, Circuit) combinations
unique_races = df[['Date', 'Circuit']].drop_duplicates()

# Step 2: Fetch weather for each unique race
weather_data = []

for _, row in unique_races.iterrows():
    date = row['Date']
    circuit = row['Circuit']
    coords = circuit_coords.get(circuit)

    if not coords:
        print(f"Skipping unknown circuit: {circuit}")
        continue

    lat, lon = coords
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/{date}?unitGroup=metric&key={API_KEY}&include=days"

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather = response.json()['days'][0]

        weather_data.append({
            'Date': date,
            'Circuit': circuit,
            'Weather': weather.get('conditions', 'Unknown'),
            'Temp': weather.get('temp', None),
            'Precip': weather.get('precip', 0.0)
        })

        print(f"✅ Weather fetched for {circuit} on {date}")
    except Exception as e:
        print(f"❌ Failed for {circuit} on {date}: {e}")

    time.sleep(1.2)  # Respect API rate limits

# Step 3: Merge weather back into full dataframe
weather_df = pd.DataFrame(weather_data)
merged_df = df.merge(weather_df, on=['Date', 'Circuit'], how='left')

# Step 4: Save final dataset
merged_df.to_csv("data/f1_race_with_quali_weather.csv", index=False)
print("✅ All done! Weather data merged and saved.")
