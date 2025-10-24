"""
Heatmap visualization module.

Creates a rectangular heatmap showing correlations or intensity values.
Useful for displaying matrix-like data with color encoding.
"""

import altair as alt
import pandas as pd
import numpy as np


METADATA = {
    'id': 'heatmap',
    'title': 'Correlation Heatmap',
    'tags': ['heatmap', 'matrix', 'correlation', 'intensity'],
    'estimated_render_time': 0.18  # seconds
}


def create_chart(seed, grid_size=10, **kwargs):
    """
    Create a heatmap with random intensity values.
    
    Args:
        seed: Random seed for reproducibility
        grid_size: Size of the grid (grid_size x grid_size cells, default: 10)
        **kwargs: Additional customization options
        
    Returns:
        alt.Chart: An Altair heatmap
    """
    # Set seed for reproducibility
    np.random.seed(seed)
    
    # Generate grid data
    data_list = []
    for i in range(grid_size):
        for j in range(grid_size):
            data_list.append({
                'x': i,
                'y': j,
                'value': np.random.rand()
            })
    
    data = pd.DataFrame(data_list)
    
    # Create heatmap with neutral theme
    chart = alt.Chart(data).mark_rect().encode(
        x=alt.X('x:O', title='X Axis'),
        y=alt.Y('y:O', title='Y Axis'),
        color=alt.Color('value:Q', 
                       scale=alt.Scale(scheme='greys'),
                       legend=alt.Legend(title='Intensity')),
        tooltip=['x:O', 'y:O', 'value:Q']
    ).properties(
        width=300,
        height=300,
        title=f'Heatmap {seed}'
    ).configure_view(
        strokeWidth=0
    )
    
    return chart
