"""
Maintenance Scheduling Module
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def create_maintenance_schedule(predictions_df, days_ahead=30):
    """
    Create optimized maintenance schedule
    
    Parameters:
    -----------
    predictions_df : DataFrame
        Predictions with failure probabilities
    days_ahead : int
        Number of days to schedule ahead
        
    Returns:
    --------
    DataFrame: Maintenance schedule
    """
    schedule = predictions_df.copy()
    
    # Assign priority based on failure probability
    schedule['priority'] = schedule['predicted_failure_prob'].apply(
        lambda x: 'High' if x >= 0.7 else ('Medium' if x >= 0.5 else 'Low')
    )
    
    # Assign urgency score
    schedule['urgency_score'] = (
        schedule['predicted_failure_prob'] * 0.7 + 
        (1 - schedule['days_to_failure'] / schedule['days_to_failure'].max()) * 0.3
    )
    
    # Sort by urgency
    schedule = schedule.sort_values('urgency_score', ascending=False)
    
    return schedule


def assign_maintenance_dates(schedule_df, start_date=None, max_daily_capacity=3):
    """
    Assign specific maintenance dates based on capacity
    
    Parameters:
    -----------
    schedule_df : DataFrame
        Schedule with priorities
    start_date : datetime (optional)
        Start date for scheduling
    max_daily_capacity : int
        Maximum maintenance jobs per day
        
    Returns:
    --------
    DataFrame: Schedule with assigned dates
    """
    if start_date is None:
        start_date = datetime.today()
    
    schedule = schedule_df.copy()
    assigned_dates = []
    current_date = start_date
    daily_count = 0
    
    for idx, row in schedule.iterrows():
        # High priority: schedule immediately
        if row['priority'] == 'High':
            assigned_dates.append(current_date)
            daily_count += 1
        # Medium priority: schedule within a week
        elif row['priority'] == 'Medium':
            assigned_dates.append(current_date + timedelta(days=3))
        # Low priority: schedule based on suggested date
        else:
            suggested = row.get('suggested_maintenance_date', current_date + timedelta(days=14))
            if isinstance(suggested, str):
                suggested = pd.to_datetime(suggested).date()
            assigned_dates.append(suggested)
        
        # Check daily capacity
        if daily_count >= max_daily_capacity:
            current_date += timedelta(days=1)
            daily_count = 0
    
    schedule['scheduled_maintenance_date'] = assigned_dates
    
    return schedule


def generate_maintenance_summary(schedule_df):
    """
    Generate maintenance schedule summary
    
    Parameters:
    -----------
    schedule_df : DataFrame
        Complete maintenance schedule
        
    Returns:
    --------
    dict: Summary statistics
    """
    summary = {
        'total_equipment': len(schedule_df),
        'high_priority': len(schedule_df[schedule_df['priority'] == 'High']),
        'medium_priority': len(schedule_df[schedule_df['priority'] == 'Medium']),
        'low_priority': len(schedule_df[schedule_df['priority'] == 'Low']),
        'avg_failure_prob': schedule_df['predicted_failure_prob'].mean(),
        'next_7_days': len(schedule_df[
            pd.to_datetime(schedule_df['scheduled_maintenance_date']) <= 
            datetime.today() + timedelta(days=7)
        ]) if 'scheduled_maintenance_date' in schedule_df.columns else 0
    }
    
    return summary


if __name__ == "__main__":
    # Example usage
    sample_predictions = pd.DataFrame([
        {'equipment_id': 'EQ-01', 'predicted_failure_prob': 0.85, 'days_to_failure': 10},
        {'equipment_id': 'EQ-02', 'predicted_failure_prob': 0.45, 'days_to_failure': 25},
        {'equipment_id': 'EQ-03', 'predicted_failure_prob': 0.20, 'days_to_failure': 50},
    ])
    
    schedule = create_maintenance_schedule(sample_predictions)
    schedule = assign_maintenance_dates(schedule)
    
    print("Maintenance Schedule:")
    print(schedule[['equipment_id', 'priority', 'scheduled_maintenance_date']])
    
    summary = generate_maintenance_summary(schedule)
    print(f"\nSummary: {summary}")
