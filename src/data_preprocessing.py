"""
Data Preprocessing Module
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_data(file_path=None):
    """
    Load dataset
    
    Parameters:
    -----------
    file_path : str
        Path to CSV file
        
    Returns:
    --------
    DataFrame: Loaded data
    """
    if file_path is None:
        file_path = os.path.join(PROJECT_ROOT, 'data', 'ai4i2020.csv')
    
    df = pd.read_csv(file_path)
    return df


def prepare_features(df):
    """
    Prepare features for modeling
    
    Parameters:
    -----------
    df : DataFrame
        Raw dataframe
        
    Returns:
    --------
    X, y: Features and target
    """
    # Drop unnecessary columns
    df_model = df.drop(columns=['UDI', 'Product ID', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF'], errors='ignore')
    
    # One-hot encoding
    df_model = pd.get_dummies(df_model, columns=['Type'], drop_first=True)
    
    # Separate features and target
    X = df_model.drop('Machine failure', axis=1, errors='ignore')
    y = df_model['Machine failure'] if 'Machine failure' in df_model.columns else None
    
    return X, y


def scale_features(X_train, X_test=None):
    """
    Scale features using StandardScaler
    
    Parameters:
    -----------
    X_train : DataFrame
        Training features
    X_test : DataFrame (optional)
        Test features
        
    Returns:
    --------
    Scaled features and scaler object
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled, scaler
    
    return X_train_scaled, scaler


def get_equipment_features(equipment_type='M', air_temp=300, process_temp=310, 
                          rpm=1500, torque=40, tool_wear=180):
    """
    Generate equipment features dictionary
    
    Returns:
    --------
    dict: Equipment features
    """
    type_l = 1 if equipment_type == 'L' else 0
    type_m = 1 if equipment_type == 'M' else 0
    
    return {
        'Air temperature [K]': air_temp,
        'Process temperature [K]': process_temp,
        'Rotational speed [rpm]': rpm,
        'Torque [Nm]': torque,
        'Tool wear [min]': tool_wear,
        'Type_L': type_l,
        'Type_M': type_m
    }


if __name__ == "__main__":
    # Example usage
    df = load_data()
    print(f"Dataset shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    
    X, y = prepare_features(df)
    print(f"\nFeatures shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}")
