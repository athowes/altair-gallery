"""
Line chart visualization module.

Creates a time-series line chart with random trend data.
Useful for showing temporal patterns and trends.
"""

import altair as alt
import pandas as pd
import numpy as np


METADATA = {
    'id': 'line_chart',
    'title': 'Time Series Line Chart',
    'tags': ['line', 'time-series', 'trend', 'temporal'],
    'estimated_render_time': 0.13  # seconds
}


def create_chart(seed, num_points=50, **kwargs):
    """
    Create a line chart with time series data.
    
    Args:
        seed: Random seed for reproducibility
        num_points: Number of data points to generate (default: 50)
        **kwargs: Additional customization options
        
    Returns:
        alt.Chart: An Altair line chart
    """
    # Set seed for reproducibility
    np.random.seed(seed)
    
    # Generate time series data with trend
    time_points = pd.date_range('2024-01-01', periods=num_points, freq='D')
    trend = np.linspace(0, 10, num_points)
    noise = np.random.randn(num_points) * 2
    values = trend + noise
    
    data = pd.DataFrame({
        'date': time_points,
        'value': values
    })
    
    # Create line chart with neutral theme
    chart = alt.Chart(data).mark_line(
        point=True,
        strokeWidth=2
    ).encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('value:Q', title='Value'),
        tooltip=['date:T', 'value:Q']
    ).properties(
        width=300,
        height=300,
        title=f'Line Chart {seed}'
    ).configure_axis(
        gridColor='#e9ecef',
        gridOpacity=0.5,
        gridWidth=0.5
    ).configure_view(
        strokeWidth=0
    ).configure_line(
        color='#6c757d'
    ).configure_point(
        color='#6c757d',
        size=50
    )
    
    return chart
