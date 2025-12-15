"""
Cost-Benefit Analysis Module
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ثوابت التكلفة (يمكن تعديلها)
COST_PREVENTIVE_MAINTENANCE = 500      # تكلفة الصيانة الوقائية
COST_CORRECTIVE_MAINTENANCE = 2000     # تكلفة الصيانة بعد العطل
COST_DOWNTIME_PER_DAY = 1000          # تكلفة توقف الجهاز يومياً
COST_SPARE_PART = 300                  # تكلفة قطعة الغيار


def calculate_maintenance_costs(predictions_df, spare_parts_summary):
    """
    Calculate maintenance costs
    
    Parameters:
    -----------
    predictions_df : DataFrame
        Failure predictions
    spare_parts_summary : dict
        Spare parts requirements summary
        
    Returns:
    --------
    dict: Cost analysis
    """
    
    num_equipment = len(predictions_df)
    num_predicted_failures = len(predictions_df[predictions_df['predicted_failure_prob'] >= 0.5])
    
    # Scenario 1: Corrective Maintenance Only
    corrective_cost = (
        num_predicted_failures * COST_CORRECTIVE_MAINTENANCE +
        num_predicted_failures * (COST_DOWNTIME_PER_DAY * 3) +  # avg 3 days downtime
        num_predicted_failures * COST_SPARE_PART * 1.5  # higher emergency cost
    )
    
    # Scenario 2: Preventive Maintenance
    preventive_cost = (
        num_predicted_failures * COST_PREVENTIVE_MAINTENANCE +
        spare_parts_summary['total_parts_needed'] * COST_SPARE_PART +
        num_predicted_failures * (COST_DOWNTIME_PER_DAY * 0.5)  # less downtime
    )
    
    # Calculate savings
    savings = corrective_cost - preventive_cost
    savings_percentage = (savings / corrective_cost * 100) if corrective_cost > 0 else 0
    
    analysis = {
        'num_equipment': num_equipment,
        'predicted_failures': num_predicted_failures,
        'corrective_maintenance_cost': corrective_cost,
        'preventive_maintenance_cost': preventive_cost,
        'total_savings': savings,
        'savings_percentage': savings_percentage,
        'roi': (savings / preventive_cost * 100) if preventive_cost > 0 else 0
    }
    
    return analysis


def generate_cost_report(analysis):
    """
    Generate cost analysis report
    """
    report = f"""
╔══════════════════════════════════════════════════════╗
║        COST-BENEFIT ANALYSIS REPORT                  ║
╚══════════════════════════════════════════════════════╝

📊 Equipment Overview:
----------------------
Total Equipment: {analysis['num_equipment']}
Predicted Failures: {analysis['predicted_failures']}

💰 Cost Comparison:
-------------------
Corrective Maintenance (Reactive):
   • Total Cost: ${analysis['corrective_maintenance_cost']:,.2f}
   • Includes: Repairs + Downtime + Emergency Parts

Preventive Maintenance (Proactive):
   • Total Cost: ${analysis['preventive_maintenance_cost']:,.2f}
   • Includes: Scheduled Maintenance + Planned Parts

📈 Savings Analysis:
--------------------
Total Savings: ${analysis['total_savings']:,.2f}
Savings Percentage: {analysis['savings_percentage']:.1f}%
Return on Investment (ROI): {analysis['roi']:.1f}%

✅ Recommendation:
------------------
"""
    
    if analysis['savings_percentage'] > 20:
        report += "✓ Highly recommend implementing preventive maintenance\n"
        report += f"  You can save {analysis['savings_percentage']:.1f}% on maintenance costs!\n"
    elif analysis['savings_percentage'] > 0:
        report += "✓ Preventive maintenance shows positive ROI\n"
    else:
        report += "⚠ Consider optimizing maintenance strategy\n"
    
    return report


def plot_cost_comparison(analysis, save_path='cost_comparison.png'):
    """
    Plot cost comparison chart
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # الرسمة 1: مقارنة التكاليف
    categories = ['Corrective\nMaintenance', 'Preventive\nMaintenance']
    costs = [
        analysis['corrective_maintenance_cost'],
        analysis['preventive_maintenance_cost']
    ]
    colors = ['#ff6b6b', '#51cf66']
    
    bars = ax1.bar(categories, costs, color=colors, alpha=0.8, edgecolor='black')
    ax1.set_ylabel('Cost ($)', fontsize=12, fontweight='bold')
    ax1.set_title('Maintenance Cost Comparison', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # إضافة القيم على الأعمدة
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # الرسمة 2: Breakdown التكاليف
    preventive_breakdown = {
        'Scheduled\nMaintenance': analysis['predicted_failures'] * COST_PREVENTIVE_MAINTENANCE,
        'Spare Parts': analysis['predicted_failures'] * COST_SPARE_PART,
        'Minor\nDowntime': analysis['predicted_failures'] * COST_DOWNTIME_PER_DAY * 0.5
    }
    
    corrective_breakdown = {
        'Emergency\nRepairs': analysis['predicted_failures'] * COST_CORRECTIVE_MAINTENANCE,
        'Emergency\nParts': analysis['predicted_failures'] * COST_SPARE_PART * 1.5,
        'Major\nDowntime': analysis['predicted_failures'] * COST_DOWNTIME_PER_DAY * 3
    }
    
    x = np.arange(len(preventive_breakdown))
    width = 0.35
    
    ax2.bar(x - width/2, list(preventive_breakdown.values()), width, 
            label='Preventive', color='#51cf66', alpha=0.8, edgecolor='black')
    ax2.bar(x + width/2, list(corrective_breakdown.values()), width,
            label='Corrective', color='#ff6b6b', alpha=0.8, edgecolor='black')
    
    ax2.set_ylabel('Cost ($)', fontsize=12, fontweight='bold')
    ax2.set_title('Cost Breakdown Comparison', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(list(preventive_breakdown.keys()), fontsize=9)
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Chart saved to: {save_path}")
    
    return fig


def plot_savings_pie(analysis, save_path='savings_pie.png'):
    """
    Plot savings pie chart
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Ensure positive values
    preventive_cost = max(0, analysis['preventive_maintenance_cost'])
    total_savings = max(0, analysis['total_savings'])
    
    # Handle zero values
    if preventive_cost == 0 and total_savings == 0:
        sizes = [1, 0]
    else:
        sizes = [preventive_cost, total_savings]
    
    labels = ['Preventive Cost', 'Savings']
    colors = ['#ffd93d', '#51cf66']
    explode = (0, 0.1) if total_savings > 0 else (0, 0)
    
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=90,
           textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    ax.set_title(f'Total Savings: ${analysis["total_savings"]:,.0f}\n({analysis["savings_percentage"]:.1f}% Reduction)',
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Chart saved to: {save_path}")
    
    return fig


if __name__ == "__main__":
    print("💰 Cost-Benefit Analysis Module")
    print("=" * 50)
    
    try:
        # قراءة البيانات
        predictions = pd.read_csv('model_output.csv')
        
        # محاكاة spare parts summary
        spare_parts_summary = {
            'total_parts_needed': 1,
            'urgent_parts': 1,
            'medium_priority': 0,
            'low_priority': 0
        }
        
        # حساب التكاليف
        analysis = calculate_maintenance_costs(predictions, spare_parts_summary)
        
        # طباعة التقرير
        print(generate_cost_report(analysis))
        
        # رسم المقارنات
        plot_cost_comparison(analysis)
        plot_savings_pie(analysis)
        
        # حفظ التحليل
        analysis_df = pd.DataFrame([analysis])
        analysis_df.to_csv('cost_analysis_report.csv', index=False)
        print("\n✅ Analysis saved to: cost_analysis_report.csv")
        
    except FileNotFoundError:
        print("❌ Error: model_output.csv not found. Run model.py first!")
