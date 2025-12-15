# Medical Equipment Maintenance Predictor

AI-powered predictive maintenance system for medical equipment.

## Project Structure

```
├── data/               # Dataset files
├── models/             # Trained ML models
├── notebooks/          # Jupyter notebooks
├── src/               # Python source files
│   ├── prediction.py
│   ├── spare_parts.py
│   ├── cost_analysis.py
│   ├── maintenance_scheduling.py
│   ├── data_preprocessing.py
│   └── weibull_analysis.py
├── ui/                # Streamlit UI
│   ├── app_main.py
│   └── pages/
├── outputs/           # Generated reports
└── requirements.txt   # Dependencies

```

## Features

- 🔮 **Failure Prediction**: ML-based equipment failure prediction
- 📅 **Maintenance Scheduling**: Optimized maintenance planning
- 🔧 **Spare Parts Optimization**: Intelligent inventory management
- 💰 **Cost-Benefit Analysis**: ROI and savings analysis
- 📊 **Weibull Analysis**: Reliability modeling

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run Streamlit UI
```bash
streamlit run ui/app_main.py
```

### Run Individual Modules
```bash
# Prediction
python src/prediction.py

# Spare Parts
python src/spare_parts.py

# Cost Analysis
python src/cost_analysis.py
```

## Technologies

- Python 3.11+
- Scikit-learn: Machine Learning
- Pandas: Data Processing
- Matplotlib: Visualization
- SciPy: Weibull Analysis
- Streamlit: Web UI

## License

MIT License
