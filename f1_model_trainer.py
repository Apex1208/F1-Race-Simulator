import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv("data/f1_final_dataset_with_driverform_top3.csv")

# Data preprocessing
def convert_quali_time(time_str):
    """Convert qualification time to seconds"""
    if pd.isna(time_str) or time_str == '99:99.99':
        return None
    parts = time_str.split(':')
    if len(parts) == 2:
        return float(parts[0]) * 60 + float(parts[1])
    return float(time_str)

# Create target variable
df['Winner'] = (df['Position'] == 1).astype(int)

# Encode categorical features
weather_encoder = LabelEncoder()
df['Weather_Encoded'] = weather_encoder.fit_transform(df['Weather'])

circuit_encoder = LabelEncoder()
df['Circuit_Encoded'] = circuit_encoder.fit_transform(df['Circuit'])

# Define features and target
features = [
    'Grid', 'BestQualiTime', 'ConstructorWinRate_AllTime', 'DriverRecentTop3Rate',
    'ConstructorWinRate_Recent', 'Weather_Encoded', 'Circuit_Encoded'
]
X = df[features]
y = df['Winner']

# Balance the dataset
winners = df[df['Winner'] == 1]
non_winners = df[df['Winner'] == 0].sample(n=len(winners)*5, random_state=42)
balanced_df = pd.concat([winners, non_winners])

X_balanced = balanced_df[features]
y_balanced = balanced_df['Winner']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model with multiple metrics
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]  # Probabilities for positive class (Winner)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_proba)

print("\n Model Evaluation Metrics:")
print("-----------------------------")
print(f"Accuracy      : {accuracy:.2f}")
print(f"Precision     : {precision:.2f}")
print(f"Recall        : {recall:.2f}")
print(f"F1 Score      : {f1:.2f}")
print(f"ROC AUC Score : {roc_auc:.2f}")

print("\n Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Non-Winner", "Winner"]))

# Confusion Matrix Visualization
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Non-Winner", "Winner"], yticklabels=["Non-Winner", "Winner"])
plt.title("Random Forest Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# Feature Importance

def plot_feature_importance(model, features):
    importances = model.feature_importances_
    indices = importances.argsort()[::-1]
    plt.figure(figsize=(10, 6))
    plt.title("Feature Importance")
    plt.bar(range(len(features)), importances[indices], align="center")
    plt.xticks(range(len(features)), [features[i] for i in indices], rotation=45)
    plt.xlabel("Feature")
    plt.ylabel("Importance Score")
    plt.tight_layout()
    plt.show()
    print("\nFeature Importance Scores:")
    for i in indices:
        print(f"{features[i]:<30}: {importances[i]:.4f}")

plot_feature_importance(model, features)

def get_user_input():
    print("\nF1 Race Winner Predictor ")
    print("----------------------------")

    circuits = sorted(circuit_encoder.classes_)
    print("\nAvailable Circuits:")
    for i, circuit in enumerate(circuits, 1):
        print(f"{i}. {circuit}")

    while True:
        try:
            circuit_num = int(input("\nSelect circuit number: "))
            if 1 <= circuit_num <= len(circuits):
                circuit = circuits[circuit_num - 1]
                break
            print(f"Please enter a number between 1 and {len(circuits)}")
        except ValueError:
            print("Please enter a valid number")

    weather_options = sorted(weather_encoder.classes_)
    print("\nAvailable Weather Conditions:")
    for i, weather in enumerate(weather_options, 1):
        print(f"{i}. {weather}")

    while True:
        try:
            weather_num = int(input("\nSelect weather condition number: "))
            if 1 <= weather_num <= len(weather_options):
                weather = weather_options[weather_num - 1]
                break
            print(f"Please enter a number between 1 and {len(weather_options)}")
        except ValueError:
            print("Please enter a valid number")

    print("\nAvailable Drivers (Current and Reserve):")
    current_drivers = [
        "Max Verstappen", "Sergio Perez", "Lewis Hamilton", "George Russell",
        "Charles Leclerc", "Carlos Sainz", "Lando Norris", "Oscar Piastri",
        "Fernando Alonso", "Lance Stroll", "Pierre Gasly", "Esteban Ocon",
        "Alex Albon", "Logan Sargeant", "Kevin Magnussen", "Nico Hulkenberg",
        "Valtteri Bottas", "Zhou Guanyu", "Yuki Tsunoda", "Daniel Ricciardo",
        "Mick Schumacher", "Felipe Drugovich", "Theo Pourchaire", "Liam Lawson",
        "Jack Doohan", "Patricio O'Ward", "Robert Shwartzman", "Stoffel Vandoorne"
    ]

    for i, driver in enumerate(current_drivers, 1):
        print(f"{i}. {driver}")

    drivers = []
    print("\nEnter driver information (at least 2 drivers):")
    while True:
        try:
            driver_num = int(input("\nSelect driver number (or 0 to finish): "))
            if driver_num == 0:
                if len(drivers) >= 2:
                    break
                print("You need at least 2 drivers to predict")
                continue
            if 1 <= driver_num <= len(current_drivers):
                driver_name = current_drivers[driver_num - 1]

                grid = int(input(f"Starting grid position for {driver_name} (1-20): "))
                if grid < 1 or grid > 20:
                    print("Grid position must be between 1 and 20")
                    continue

                quali_time = input(f"Recent qualification time for {driver_name} (MM:SS.sss format): ")
                try:
                    best_quali = convert_quali_time(quali_time)
                    if best_quali is None:
                        print("Invalid qualification time format")
                        continue
                except:
                    print("Invalid time format. Please use MM:SS.sss")
                    continue

                driver_data = df[df['Driver'] == driver_name]
                if not driver_data.empty:
                    recent_race = driver_data.sort_values(by='Year', ascending=False).iloc[0]
                    constructor = recent_race['Constructor']
                    top3_rate = recent_race['DriverRecentTop3Rate']
                    all_time_win = recent_race['ConstructorWinRate_AllTime']
                    recent_win = recent_race['ConstructorWinRate_Recent']
                else:
                    constructor = "Unknown"
                    top3_rate = 0.2
                    all_time_win = 50.0
                    recent_win = 45.0
                    print(f"⚠️ Using default values for {driver_name}")

                drivers.append({
                    'Driver': driver_name,
                    'Grid': grid,
                    'BestQualiTime': best_quali,
                    'DriverRecentTop3Rate': top3_rate,
                    'ConstructorWinRate_AllTime': all_time_win,
                    'ConstructorWinRate_Recent': recent_win
                })
                print(f"Added {driver_name} ({constructor}) with recent Top3 rate: {top3_rate:.2f}")
            else:
                print(f"Please enter a number between 1 and {len(current_drivers)} or 0 to finish")
        except ValueError:
            print("Please enter a valid number")

    return circuit, weather, drivers

def predict_winner_probabilities(circuit, weather, driver_data):
    try:
        weather_encoded = weather_encoder.transform([weather])[0]
        circuit_encoded = circuit_encoder.transform([circuit])[0]
    except ValueError as e:
        print(f"Error: {e}")
        return []

    X_new = []
    for driver in driver_data:
        X_new.append([
            driver['Grid'],
            driver['BestQualiTime'],
            driver['ConstructorWinRate_AllTime'],
            driver['DriverRecentTop3Rate'],
            driver['ConstructorWinRate_Recent'],
            weather_encoded,
            circuit_encoded
        ])

    probas = model.predict_proba(X_new)
    results = [(driver['Driver'], proba[1]) for driver, proba in zip(driver_data, probas)]

    return sorted(results, key=lambda x: x[1], reverse=True)

def main():
    circuit, weather, drivers = get_user_input()
    predictions = predict_winner_probabilities(circuit, weather, drivers)

    print("\n🏆 Race Winner Predictions:")
    print("--------------------------")
    print(f"Circuit: {circuit}")
    print(f"Weather: {weather}\n")

    print("Driver\t\tWin Probability")
    print("--------------------------------")
    for driver, prob in predictions:
        print(f"{driver:20} {prob:.1%}")

if __name__ == "__main__":
    main()
