import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv("data/f1_final_dataset_with_driverform_top3.csv")

# Helper to convert qualifying times to seconds
def convert_quali_time(time_str):
    if pd.isna(time_str) or time_str == '99:99.99':
        return None
    parts = time_str.split(':')
    return float(parts[0]) * 60 + float(parts[1]) if len(parts) == 2 else float(time_str)

# Add target variable
df['Winner'] = (df['Position'] == 1).astype(int)

# Encode categorical features
weather_encoder = LabelEncoder()
df['Weather_Encoded'] = weather_encoder.fit_transform(df['Weather'])

circuit_encoder = LabelEncoder()
df['Circuit_Encoded'] = circuit_encoder.fit_transform(df['Circuit'])

# Features and target
features = [
    'Grid', 'BestQualiTime', 'ConstructorWinRate_AllTime',
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

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.2, random_state=42)

# --- XGBoost ---
xgb_model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42,
                         use_label_encoder=False, eval_metric='logloss')
xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)

print("\n===== XGBoost Performance =====")
print(classification_report(y_test, y_pred_xgb))

cm_xgb = confusion_matrix(y_test, y_pred_xgb)
plt.figure(figsize=(5, 4))
sns.heatmap(cm_xgb, annot=True, fmt='d', cmap='Blues')
plt.title('XGBoost Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# --- CatBoost ---
cat_model = CatBoostClassifier(iterations=100, learning_rate=0.1, depth=6, verbose=0, random_seed=42)
cat_model.fit(X_train, y_train)
y_pred_cat = cat_model.predict(X_test)

print("\n===== CatBoost Performance =====")
print(classification_report(y_test, y_pred_cat))

cm_cat = confusion_matrix(y_test, y_pred_cat)
plt.figure(figsize=(5, 4))
sns.heatmap(cm_cat, annot=True, fmt='d', cmap='Greens')
plt.title('CatBoost Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()
