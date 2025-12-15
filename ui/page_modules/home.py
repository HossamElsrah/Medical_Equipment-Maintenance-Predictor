"""
Home Page
"""

import streamlit as st
import pandas as pd
import os

def show():
    st.title("🏥 Medical Equipment Maintenance Predictor")
    st.markdown("### AI-Powered Predictive Maintenance System")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔮 Prediction
        - Machine Learning Models
        - Weibull Analysis
        - Failure Probability
        """)
    
    with col2:
        st.markdown("""
        ### 📅 Scheduling
        - Optimized Planning
        - Priority-Based
        - Resource Management
        """)
    
    with col3:
        st.markdown("""
        ### 💰 Cost Savings
        - ROI Analysis
        - Spare Parts Optimization
        - Reduced Downtime
        """)
    
    st.markdown("---")
    
    st.success("✅ System Status: Online")
    
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    
    output_file = os.path.join('outputs', 'model_output.csv')
    
    try:
        predictions = pd.read_csv(output_file)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Equipment", len(predictions))
        
        with col2:
            high_risk = len(predictions[predictions['predicted_failure_prob'] >= 0.7])
            st.metric("High Risk", high_risk, delta=None, delta_color="inverse")
        
        with col3:
            avg_prob = predictions['predicted_failure_prob'].mean()
            st.metric("Avg Failure Prob", f"{avg_prob:.1%}")
        
        with col4:
            avg_days = predictions['days_to_failure'].mean()
            st.metric("Avg Days to Failure", f"{int(avg_days)} days")
    
    except FileNotFoundError:
        st.info("👉 Run a prediction first to see statistics")
