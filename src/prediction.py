"""
Equipment Failure Prediction Module
"""

import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load model and scaler
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'machine_failure_model.pkl')
SCALER_PATH = os.path.join(PROJECT_ROOT, 'models', 'scaler.pkl')

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


def predict_equipment_failure(equipment_data):
    """
    Predict failure probability for equipment
    
    Parameters:
    -----------
    equipment_data : dict
        Equipment features including:
        - equipment_id
        - Air temperature [K]
        - Process temperature [K]
        - Rotational speed [rpm]
        - Torque [Nm]
        - Tool wear [min]
        - Type_L, Type_M
        
    Returns:
    --------
    dict: Prediction results
    """
    input_df = pd.DataFrame([equipment_data])
    equipment_id = input_df['equipment_id'][0]
    input_features = input_df.drop(columns=['equipment_id'])
    
    # Scaling
    input_scaled = scaler.transform(input_features)
    
    # Prediction
    pred_class = model.predict(input_scaled)[0]
    pred_prob = model.predict_proba(input_scaled)[0][1]
    
    failure_label = 'Failure' if pred_class == 1 else 'No Failure'
    
    # Estimate remaining days
    MAX_TOOL_WEAR = 250
    remaining_days = max(0, int((MAX_TOOL_WEAR - equipment_data['Tool wear [min]']) * 0.5))
    suggested_maintenance_date = datetime.today() + timedelta(days=max(remaining_days - 7, 0))
    
    return {
        'equipment_id': equipment_id,
        'predicted_failure_prob': round(pred_prob, 3),
        'days_to_failure': remaining_days,
        'last_maintenance': datetime.today().date(),
        'suggested_maintenance_date': suggested_maintenance_date.date(),
        'status': failure_label
    }


def batch_predict(equipment_list):
    """
    Predict for multiple equipment
    
    Parameters:
    -----------
    equipment_list : list of dict
        List of equipment data
        
    Returns:
    --------
    DataFrame: Batch prediction results
    """
    results = []
    for equipment in equipment_list:
        result = predict_equipment_failure(equipment)
        results.append(result)
    
    return pd.DataFrame(results)


if __name__ == "__main__":
    # Example usage
    sample_data = {
        'equipment_id': 'EQ-01',
        'Air temperature [K]': 300,
        'Process temperature [K]': 310,
        'Rotational speed [rpm]': 1500,
        'Torque [Nm]': 40,
        'Tool wear [min]': 180,
        'Type_L': 0,
        'Type_M': 1
    }
    
    result = predict_equipment_failure(sample_data)
    print("Prediction Result:")
    print(result)
