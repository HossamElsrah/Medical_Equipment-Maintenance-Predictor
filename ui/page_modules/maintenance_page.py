"""
Maintenance Schedule Page
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from src.maintenance_scheduling import create_maintenance_schedule, assign_maintenance_dates


def show():
    st.title("📅 Maintenance Schedule")
    
    output_file = os.path.join('outputs', 'model_output.csv')
    
    try:
        predictions = pd.read_csv(output_file)
        
        st.markdown("### Current Equipment Status:")
        
        # Create schedule
        schedule = create_maintenance_schedule(predictions)
        schedule = assign_maintenance_dates(schedule)
        
        # Display table
        st.dataframe(
            schedule[['equipment_id', 'predicted_failure_prob', 'days_to_failure', 
                     'priority', 'scheduled_maintenance_date']],
            use_container_width=True
        )
        
        # Save schedule
        schedule_file = os.path.join('outputs', 'maintenance_schedule.csv')
        schedule.to_csv(schedule_file, index=False)
        
        st.success(f"✅ Maintenance schedule saved")
        
        # Priority distribution chart
        st.markdown("### 📊 Priority Distribution:")
        
        priority_counts = schedule['priority'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = {'High': '#ff6b6b', 'Medium': '#ffd93d', 'Low': '#51cf66'}
        priority_colors = [colors.get(p, '#999') for p in priority_counts.index]
        
        ax.bar(priority_counts.index, priority_counts.values, color=priority_colors, edgecolor='black')
        ax.set_xlabel('Priority Level', fontweight='bold')
        ax.set_ylabel('Number of Equipment', fontweight='bold')
        ax.set_title('Maintenance Priority Distribution', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig)
        
    except FileNotFoundError:
        st.warning("⚠️ No predictions available. Please run a prediction first.")
