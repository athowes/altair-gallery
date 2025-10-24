"""
Bar chart visualization module.

Creates a simple bar chart with random categorical data.
Displays values with tooltips for interaction.
"""

import altair as alt
import pandas as pd
import numpy as np


METADATA = {
    'id': 'bar_chart',
    'title': 'Categorical Bar Chart',
    'tags': ['bar', 'categorical', 'comparison'],
    'estimated_render_time': 0.12  # seconds
}


def create_chart(seed, num_categories=5, **kwargs):
    """
    Create a bar chart with random categorical data.
    
    Args:
        seed: Random seed for reproducibility
        num_categories: Number of categories to display (default: 5)
        **kwargs: Additional customization options
        
    Returns:
        alt.Chart: An Altair bar chart
    """
    # Set seed for reproducibility
    np.random.seed(seed)
    
    # Generate random data
    categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E'][:num_categories]
    data = pd.DataFrame({
        'category': categories,
        'value': np.random.randint(10, 100, len(categories))
    })
    
    # Create bar chart with neutral theme
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('category:N', title='Category'),
        y=alt.Y('value:Q', title='Value'),
        color=alt.Color('category:N', 
                       scale=alt.Scale(range=['#6c757d', '#868e96', '#adb5bd', '#ced4da', '#dee2e6']),
                       legend=None),
        tooltip=['category:N', 'value:Q']
    ).properties(
        width=300,
        height=300,
        title=f'Bar Chart {seed}'
    ).configure_axis(
        gridColor='#e9ecef',
        gridOpacity=0.5,
        gridWidth=0.5
    ).configure_view(
        strokeWidth=0
    )
    
    return chart
