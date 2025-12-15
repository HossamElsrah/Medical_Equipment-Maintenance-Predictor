"""
Prediction Page
"""

import streamlit as st
import pandas as pd
import joblib
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from src.prediction import predict_equipment_failure


@st.cache_resource
def load_models():
    try:
        model_path = os.path.join('models', 'machine_failure_model.pkl')
        scaler_path = os.path.join('models', 'scaler.pkl')
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    except:
        return None, None


def show():
    st.title("🔮 Equipment Failure Prediction")
    
    model, scaler = load_models()
    
    if model is None or scaler is None:
        st.error("❌ Model not loaded. Please check model files.")
        return
    
    st.markdown("### Enter Equipment Data:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        equipment_id = st.text_input("Equipment ID", value="EQ-01")
        air_temp = st.number_input("Air Temperature (K)", min_value=250.0, max_value=350.0, value=300.0, step=0.1)
        process_temp = st.number_input("Process Temperature (K)", min_value=250.0, max_value=350.0, value=310.0, step=0.1)
        rotational_speed = st.number_input("Rotational Speed (rpm)", min_value=500, max_value=3000, value=1500, step=10)
    
    with col2:
        torque = st.number_input("Torque (Nm)", min_value=0.0, max_value=100.0, value=40.0, step=0.1)
        tool_wear = st.number_input("Tool Wear (min)", min_value=0, max_value=250, value=180, step=1)
        equipment_type = st.selectbox("Equipment Type", ["Low (L)", "Medium (M)", "High (H)"])
        
        type_l = 1 if equipment_type == "Low (L)" else 0
        type_m = 1 if equipment_type == "Medium (M)" else 0
    
    st.markdown("---")
    
    if st.button("🔮 Predict", type="primary"):
        equipment_data = {
            'equipment_id': equipment_id,
            'Air temperature [K]': air_temp,
            'Process temperature [K]': process_temp,
            'Rotational speed [rpm]': rotational_speed,
            'Torque [Nm]': torque,
            'Tool wear [min]': tool_wear,
            'Type_L': type_l,
            'Type_M': type_m
        }
        
        result = predict_equipment_failure(equipment_data)
        
        # Save result
        result_df = pd.DataFrame([result])
        output_file = os.path.join('outputs', 'model_output.csv')
        os.makedirs('outputs', exist_ok=True)
        result_df.to_csv(output_file, index=False)
        
        # Display results
        st.markdown("### 📊 Prediction Results:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Equipment ID", result['equipment_id'])
        
        with col2:
            prob = result['predicted_failure_prob']
            st.metric("Failure Probability", f"{prob:.1%}", 
                     delta="High Risk" if prob >= 0.7 else "Low Risk",
                     delta_color="inverse" if prob >= 0.7 else "normal")
        
        with col3:
            st.metric("Days to Failure", f"{result['days_to_failure']} days")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **Status:** {result['status']}  
            **Last Maintenance:** {result['last_maintenance']}  
            **Suggested Next Maintenance:** {result['suggested_maintenance_date']}
            """)
        
        with col2:
            if prob >= 0.7:
                st.error("""
                ⚠️ **HIGH RISK - Immediate Action Required**
                - Schedule maintenance ASAP
                - Prepare spare parts
                - Monitor closely
                """)
            elif prob >= 0.5:
                st.warning("""
                ⚡ **MEDIUM RISK - Monitor Closely**
                - Schedule maintenance within 1 week
                - Check spare parts availability
                """)
            else:
                st.success("""
                ✅ **LOW RISK - Routine Maintenance**
                - Continue normal operations
                - Schedule routine check
                """)
