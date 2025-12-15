"""
Medical Equipment Maintenance Predictor - Main UI
"""
import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.insert(0, os.path.join(project_root, 'ui'))

# Page configuration
st.set_page_config(
    page_title="Medical Equipment Maintenance Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("🏥 Medical Equipment")
st.sidebar.title("Maintenance Predictor")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation:",
    ["🏠 Home", "🔮 Predict Failure", "📅 Maintenance Schedule", "🔧 Spare Parts", "💰 Cost Analysis"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**About:**  
This system predicts medical equipment failures and optimizes maintenance scheduling.

**Features:**
- Failure Prediction
- Maintenance Scheduling
- Spare Parts Optimization
- Cost-Benefit Analysis
""")

# Main content
if menu == "🏠 Home":
    from page_modules import home  # type: ignore
    home.show()

elif menu == "🔮 Predict Failure":
    from page_modules import prediction_page  # type: ignore
    prediction_page.show()

elif menu == "📅 Maintenance Schedule":
    from page_modules import maintenance_page  # type: ignore
    maintenance_page.show()

elif menu == "🔧 Spare Parts":
    from page_modules import spare_parts_page  # type: ignore
    spare_parts_page.show()

elif menu == "💰 Cost Analysis":
    from page_modules import cost_analysis_page  # type: ignore
    cost_analysis_page.show()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Medical Equipment Maintenance Predictor**")
st.sidebar.markdown("*AI-Powered Predictive Maintenance System*")
