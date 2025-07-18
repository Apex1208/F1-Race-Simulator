# 🏁 F1 Race Predictor

A terminal-based machine learning application to predict the winner of a Formula 1 race based on driver statistics, constructor performance, grid position, qualifying time, circuit, and weather conditions.

---

## 🚀 Features

- Predicts win probabilities for all drivers in a given race
- Command-line interactive interface
- Inputs:
  - Circuit name
  - Weather condition
  - Driver details (name, constructor, grid position, best qualifying time)
- Outputs:
  - Sorted list of drivers with predicted win probabilities
- Uses a pre-trained Random Forest model on historical Formula 1 data

---

## 🗂️ Project Structure

F1-Race-Predictor/<br/>
├── f1_predictor.py # Main executable script<br/>
├── model/<br/>
│ └── rf_f1_model.pkl # Trained Random Forest model<br/>
├── data/<br/>
│ └── driver_info.csv # Static info for current drivers/constructors<br/>
├── utils/<br/>
│ ├── encoding.py # Functions to encode circuit and weather<br/>
│ └── feature_engineering.py # Functions to compute derived input features<br/>
├── README.md # Project documentation<br/>


---

## 🛠️ Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/Apex1208/F1-Race-Predictor.git
cd F1-Race-Predictor
```

2. **Install Required Libraries**

Make sure you have Python 3 installed. Then install the dependencies manually:

```bash
pip install pandas scikit-learn joblib numpy
```

---
## ▶️ How to Run the Predictor
Run the main script using:
```bash
python f1_predictor.py
```
You will be prompted to enter:
- Circuit name (e.g., Monaco, Silverstone, etc.)
- Weather condition (Dry, Wet, etc.)
- Driver details (name, constructor, grid position, best qualifying time)<br/>

After entering the data, the script will display win probabilities for each driver.

--- 

## 📈 Example Output

Enter Circuit: Monaco<br/>
Enter Weather: Dry<br/>

--- Enter driver details ---<br/>
Driver 1:<br/>
  Name: Charles Leclerc<br/>
  Constructor: Ferrari<br/>
  Grid Position: 1<br/>
  Best Qualifying Time: 1:10.231<br/>
...<br/>

Top Predictions:<br/>
1. Charles Leclerc (Ferrari) - 38.7%<br/>
2. Max Verstappen (Red Bull) - 32.1%<br/>
3. Lewis Hamilton (Mercedes) - 14.9%<br/>
...<br/>

---

## 📊 Model Info

- **Type:** Random Forest Classifier  
- **Trained on:** Historical F1 race data  
- **Features used:**
  - Grid Position  
  - Best Qualifying Time  
  - Constructor Win Rate (All Time & Recent)  
  - Driver Recent Top 3 Finish Rate  
  - Encoded Circuit and Weather  

---

## 🔮 Future Improvements

- Add support for full race finishing position prediction  
- Auto-load data from the official F1 API  
- Build a Streamlit or Flask web app version  
- Add visualization of predicted podiums  
