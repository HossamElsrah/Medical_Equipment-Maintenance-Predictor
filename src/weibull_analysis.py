"""
Weibull Reliability Analysis Module
"""

import pandas as pd
import numpy as np
from scipy.stats import weibull_min
import matplotlib.pyplot as plt
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fit_weibull_distribution(failure_data):
    """
    Fit Weibull distribution to failure data
    
    Parameters:
    -----------
    failure_data : array-like
        Time-to-failure data
        
    Returns:
    --------
    dict: Weibull parameters
    """
    shape, loc, scale = weibull_min.fit(failure_data, floc=0)
    
    # Calculate Mean Time To Failure (MTTF)
    mttf = scale * np.exp(np.log(np.e) / shape)
    
    return {
        'shape': shape,
        'scale': scale,
        'mttf': mttf
    }


def calculate_failure_probability(time, shape, scale):
    """
    Calculate failure probability at given time
    
    Parameters:
    -----------
    time : float
        Time point
    shape : float
        Weibull shape parameter
    scale : float
        Weibull scale parameter
        
    Returns:
    --------
    float: Failure probability
    """
    return weibull_min.cdf(time, shape, 0, scale)


def calculate_reliability(time, shape, scale):
    """
    Calculate reliability at given time
    
    Parameters:
    -----------
    time : float
        Time point
    shape : float
        Weibull shape parameter
    scale : float
        Weibull scale parameter
        
    Returns:
    --------
    float: Reliability (1 - failure probability)
    """
    return 1 - calculate_failure_probability(time, shape, scale)


def plot_weibull_analysis(failure_data, save_path=None):
    """
    Plot Weibull PDF and CDF
    
    Parameters:
    -----------
    failure_data : array-like
        Time-to-failure data
    save_path : str (optional)
        Path to save plot
        
    Returns:
    --------
    matplotlib figure
    """
    params = fit_weibull_distribution(failure_data)
    shape = params['shape']
    scale = params['scale']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    x = np.linspace(0, failure_data.max(), 300)
    
    # PDF
    pdf = weibull_min.pdf(x, shape, 0, scale)
    ax1.plot(x, pdf, 'b-', linewidth=2)
    ax1.set_xlabel('Time to Failure', fontweight='bold')
    ax1.set_ylabel('Probability Density', fontweight='bold')
    ax1.set_title('Weibull Probability Density Function', fontweight='bold')
    ax1.grid(alpha=0.3)
    
    # CDF
    cdf = weibull_min.cdf(x, shape, 0, scale)
    ax2.plot(x, cdf, 'r-', linewidth=2)
    ax2.set_xlabel('Time to Failure', fontweight='bold')
    ax2.set_ylabel('Cumulative Failure Probability', fontweight='bold')
    ax2.set_title('Weibull Cumulative Distribution Function', fontweight='bold')
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


if __name__ == "__main__":
    # Example: Generate sample failure data
    np.random.seed(42)
    sample_failures = weibull_min.rvs(2.5, 0, 150, size=100)
    
    params = fit_weibull_distribution(sample_failures)
    print("Weibull Parameters:")
    print(f"Shape (β): {params['shape']:.2f}")
    print(f"Scale (η): {params['scale']:.2f}")
    print(f"MTTF: {params['mttf']:.2f}")
    
    # Plot
    fig = plot_weibull_analysis(sample_failures)
    plt.show()
