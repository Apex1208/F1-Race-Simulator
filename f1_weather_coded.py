import pandas as pd
from sklearn.preprocessing import LabelEncoder

def predict_f1_winner(model, circuit, weather, drivers_info):
    # Weather encoding - reuse same encoding from training
    weather_encoder = LabelEncoder()
    weather_encoder.fit(["Dry", "Wet", "Intermediate"])  # or use actual unique weather conditions used in training
    
    if weather not in weather_encoder.classes_:
        print(f"Warning: Weather '{weather}' not seen during training. Defaulting to 'Dry'.")
        weather = "Dry"
    
    weather_encoded = weather_encoder.transform([weather])[0]
    
    # Prepare input data
    input_data = []
    driver_names = []

    for info in drivers_info:
        driver_names.append(info["Driver"])
        input_data.append({
            "Grid": info["Grid"],
            "BestQualiTime": info["BestQualiTime"],
            "ConstructorWinRate_AllTime": info["ConstructorWinRate_AllTime"],
            "ConstructorWinRate_Recent": info["ConstructorWinRate_Recent"],
            "Weather_Encoded": weather_encoded
        })

    df_input = pd.DataFrame(input_data)

    # Predict probabilities
    probs = model.predict_proba(df_input)[:, 1]  # Probability of being the winner

    # Return sorted predictions
    results = list(zip(driver_names, probs))
    results.sort(key=lambda x: x[1], reverse=True)

    return results
