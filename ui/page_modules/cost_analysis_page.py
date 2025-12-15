"""
Cost Analysis Page
"""

import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from src.spare_parts import calculate_spare_parts_need
from src.cost_analysis import calculate_maintenance_costs, generate_cost_report, plot_cost_comparison, plot_savings_pie


def show():
    st.title("💰 Cost-Benefit Analysis")
    
    output_file = os.path.join('outputs', 'model_output.csv')
    
    try:
        predictions = pd.read_csv(output_file)
        
        # Calculate spare parts
        spare_parts_df, spare_parts_summary = calculate_spare_parts_need(predictions)
        
        # Calculate costs
        analysis = calculate_maintenance_costs(predictions, spare_parts_summary)
        
        # Main metrics
        st.markdown("### 💵 Financial Overview:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Corrective Maintenance",
                f"${analysis['corrective_maintenance_cost']:,.0f}",
                delta="Higher Cost",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                "Preventive Maintenance",
                f"${analysis['preventive_maintenance_cost']:,.0f}",
                delta="Lower Cost",
                delta_color="normal"
            )
        
        with col3:
            st.metric(
                "Total Savings",
                f"${analysis['total_savings']:,.0f}",
                delta=f"{analysis['savings_percentage']:.1f}%",
                delta_color="normal"
            )
        
        st.markdown("---")
        
        # ROI and recommendation
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            ### 📊 Key Metrics:
            - **Equipment Analyzed:** {analysis['num_equipment']}
            - **Predicted Failures:** {analysis['predicted_failures']}
            - **ROI:** {analysis['roi']:.1f}%
            """)
        
        with col2:
            if analysis['savings_percentage'] > 20:
                st.success("""
                ### ✅ Recommendation:
                **Highly Recommended**  
                Implementing preventive maintenance can save significant costs!
                """)
            else:
                st.info("""
                ### ℹ️ Recommendation:
                Preventive maintenance shows positive ROI.
                """)
        
        st.markdown("---")
        
        # Charts
        st.markdown("### 📈 Cost Comparison Charts:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            chart_path = os.path.join('outputs', 'cost_comparison.png')
            fig1 = plot_cost_comparison(analysis, save_path=chart_path)
            st.pyplot(fig1)
        
        with col2:
            pie_path = os.path.join('outputs', 'savings_pie.png')
            fig2 = plot_savings_pie(analysis, save_path=pie_path)
            st.pyplot(fig2)
        
        # Full report
        st.markdown("---")
        st.markdown("### 📄 Detailed Report:")
        
        with st.expander("View Full Report"):
            report = generate_cost_report(analysis)
            st.text(report)
        
        # Save analysis
        analysis_file = os.path.join('outputs', 'cost_analysis_report.csv')
        analysis_df = pd.DataFrame([analysis])
        analysis_df.to_csv(analysis_file, index=False)
        
        st.success("✅ Cost analysis saved")
        
    except FileNotFoundError:
        st.warning("⚠️ No predictions available. Please run a prediction first.")
