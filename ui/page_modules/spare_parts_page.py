"""
Spare Parts Page
"""

import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from src.spare_parts import calculate_spare_parts_need, generate_spare_parts_report


def show():
    st.title("🔧 Spare Parts Optimization")
    
    output_file = os.path.join('outputs', 'model_output.csv')
    
    try:
        predictions = pd.read_csv(output_file)
        
        spare_parts_df, summary = calculate_spare_parts_need(predictions, threshold=0.7)
        
        st.markdown("### 📦 Spare Parts Requirements:")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Parts Needed", summary['total_parts_needed'])
        
        with col2:
            st.metric("High Priority", summary['urgent_parts'], delta="Urgent", delta_color="inverse")
        
        with col3:
            st.metric("Medium Priority", summary['medium_priority'])
        
        with col4:
            st.metric("Low Priority", summary['low_priority'])
        
        st.markdown("---")
        
        # Detailed table
        st.markdown("### 📋 Detailed Requirements:")
        st.dataframe(spare_parts_df, use_container_width=True)
        
        # Save report
        report_file = os.path.join('outputs', 'spare_parts_report.csv')
        spare_parts_df.to_csv(report_file, index=False)
        
        # Text report
        st.markdown("### 📄 Report:")
        report = generate_spare_parts_report(spare_parts_df, summary)
        st.text(report)
        
        st.success("✅ Spare parts report saved")
        
    except FileNotFoundError:
        st.warning("⚠️ No predictions available. Please run a prediction first.")
