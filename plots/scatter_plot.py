"""
Scatter plot visualization module.

Creates an interactive scatter plot with random data points categorized into groups.
Features zoom, pan, and tooltip interactions.
"""

import altair as alt
import pandas as pd
import numpy as np


METADATA = {
    'id': 'scatter_plot',
    'title': 'Interactive Scatter Plot',
    'tags': ['scatter', 'interactive', 'points', 'categories'],
    'estimated_render_time': 0.15  # seconds
}


def create_chart(seed, num_points=100, **kwargs):
    """
    Create an interactive scatter plot with random data.
    
    Args:
        seed: Random seed for reproducibility
        num_points: Number of random points to generate (default: 100)
        **kwargs: Additional customization options
        
    Returns:
        alt.Chart: An interactive Altair scatter plot
    """
    # Set seed for reproducibility
    np.random.seed(seed)
    
    # Generate random data
    data = pd.DataFrame({
        'x': np.random.randn(num_points),
        'y': np.random.randn(num_points),
        'category': np.random.choice(['A', 'B', 'C', 'D'], num_points)
    })
    
    # Create interactive scatter plot with neutral theme
    chart = alt.Chart(data).mark_circle(size=60).encode(
        x=alt.X('x:Q', scale=alt.Scale(domain=[-4, 4])),
        y=alt.Y('y:Q', scale=alt.Scale(domain=[-4, 4])),
        color=alt.Color('category:N', 
                       scale=alt.Scale(range=['#6c757d', '#868e96', '#adb5bd', '#ced4da']),
                       legend=alt.Legend(title='Category')),
        tooltip=['x:Q', 'y:Q', 'category:N']
    ).properties(
        width=300,
        height=300,
        title=f'Plot {seed}'
    ).configure_axis(
        gridColor='#e9ecef',
        gridOpacity=0.5,
        gridWidth=0.5
    ).configure_view(
        strokeWidth=0
    ).interactive()
    
    return chart
