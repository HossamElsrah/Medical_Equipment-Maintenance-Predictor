"""
Spare Parts Optimization Module
"""

import pandas as pd
import numpy as np


def calculate_spare_parts_need(predictions_df, threshold=0.7):
    """
    Calculate spare parts requirements based on failure predictions
    
    Parameters:
    -----------
    predictions_df : DataFrame
        Contains: equipment_id, predicted_failure_prob, days_to_failure
    threshold : float
        Failure probability threshold (default: 0.7 = 70%)
    
    Returns:
    --------
    DataFrame: Spare parts requirements table
    """
    
    spare_parts_data = []
    
    for _, row in predictions_df.iterrows():
        equipment_id = row['equipment_id']
        failure_prob = row['predicted_failure_prob']
        days_to_failure = row['days_to_failure']
        
        # Determine spare parts need
        if failure_prob >= threshold:
            need_spare = "Yes - Urgent"
            priority = "High"
            quantity = 1
        elif failure_prob >= 0.5:
            need_spare = "Yes - Monitor"
            priority = "Medium"
            quantity = 1
        else:
            need_spare = "No"
            priority = "Low"
            quantity = 0
            
        spare_parts_data.append({
            'equipment_id': equipment_id,
            'failure_probability': failure_prob,
            'days_to_failure': days_to_failure,
            'spare_parts_needed': need_spare,
            'priority': priority,
            'quantity_required': quantity
        })
    
    spare_parts_df = pd.DataFrame(spare_parts_data)
    
    # Calculate totals
    total_parts_needed = spare_parts_df['quantity_required'].sum()
    urgent_parts = len(spare_parts_df[spare_parts_df['priority'] == 'High'])
    
    summary = {
        'total_parts_needed': int(total_parts_needed),
        'urgent_parts': urgent_parts,
        'medium_priority': len(spare_parts_df[spare_parts_df['priority'] == 'Medium']),
        'low_priority': len(spare_parts_df[spare_parts_df['priority'] == 'Low'])
    }
    
    return spare_parts_df, summary


def generate_spare_parts_report(spare_parts_df, summary):
    """
    Generate text report for spare parts
    """
    report = f"""
╔══════════════════════════════════════════════════════╗
║      SPARE PARTS OPTIMIZATION REPORT                 ║
╚══════════════════════════════════════════════════════╝

📊 Summary:
-----------
Total Spare Parts Needed: {summary['total_parts_needed']}
   • High Priority (Urgent): {summary['urgent_parts']}
   • Medium Priority: {summary['medium_priority']}
   • Low Priority: {summary['low_priority']}

📦 Recommendations:
-------------------
"""
    
    if summary['urgent_parts'] > 0:
        report += f"⚠️  Order {summary['urgent_parts']} parts IMMEDIATELY\n"
    if summary['medium_priority'] > 0:
        report += f"⚡ Prepare {summary['medium_priority']} parts within next week\n"
    
    report += f"\n💰 Estimated Cost Savings:\n"
    report += f"   By ordering in advance, you can save 20-30% on emergency costs\n"
    
    return report


if __name__ == "__main__":
    print("Spare Parts Optimization Module")
    print("=" * 50)
    
    try:
        predictions = pd.read_csv('outputs/model_output.csv')
        spare_parts_df, summary = calculate_spare_parts_need(predictions)
        
        print("\nSpare Parts Requirements:")
        print(spare_parts_df.to_string(index=False))
        
        print(generate_spare_parts_report(spare_parts_df, summary))
        
        spare_parts_df.to_csv('outputs/spare_parts_report.csv', index=False)
        print("\nReport saved")
        
    except FileNotFoundError:
        print("Error: model_output.csv not found")
