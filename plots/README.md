# Plot Modules

This directory contains modular, self-contained plot definitions for the Altair Gallery.

## Overview

Each plot module is a standalone Python file that defines:
- **Metadata**: Information about the plot (ID, title, tags, estimated render time)
- **Chart creation function**: A function that generates and returns an Altair chart

## Structure of a Plot Module

Every plot module must follow this structure:

```python
"""
Brief description of the visualization.
"""

import altair as alt
import pandas as pd
import numpy as np


METADATA = {
    'id': 'unique_plot_id',           # Unique identifier (used in config files)
    'title': 'Human-Readable Title',  # Display name
    'tags': ['tag1', 'tag2'],         # Searchable tags
    'estimated_render_time': 0.15     # Approximate render time in seconds
}


def create_chart(seed, **kwargs):
    """
    Create the visualization.
    
    Args:
        seed: Random seed for reproducibility
        **kwargs: Additional customization options
        
    Returns:
        alt.Chart: An Altair chart object
    """
    # Set random seed
    np.random.seed(seed)
    
    # Generate data
    data = pd.DataFrame({
        # Your data here
    })
    
    # Create and return chart
    chart = alt.Chart(data).mark_point().encode(
        # Your encodings here
    ).properties(
        width=300,
        height=300
    )
    
    return chart
```

## Available Plot Modules

### scatter_plot.py
- **ID**: `scatter_plot`
- **Type**: Interactive scatter plot
- **Tags**: scatter, interactive, points, categories
- **Description**: Displays random points in 2D space with category colors

### bar_chart.py
- **ID**: `bar_chart`
- **Type**: Categorical bar chart
- **Tags**: bar, categorical, comparison
- **Description**: Shows values across categories with tooltips

### line_chart.py
- **ID**: `line_chart`
- **Type**: Time series line chart
- **Tags**: line, time-series, trend, temporal
- **Description**: Displays trends over time with point markers

### heatmap.py
- **ID**: `heatmap`
- **Type**: Correlation heatmap
- **Tags**: heatmap, matrix, correlation, intensity
- **Description**: Shows intensity values in a grid layout

## Adding a New Plot Module

1. **Create a new Python file** in this directory (e.g., `my_plot.py`)

2. **Define METADATA** with a unique ID:
   ```python
   METADATA = {
       'id': 'my_plot',
       'title': 'My Custom Plot',
       'tags': ['custom', 'example'],
       'estimated_render_time': 0.10
   }
   ```

3. **Implement create_chart()** function:
   ```python
   def create_chart(seed, **kwargs):
       np.random.seed(seed)
       # Generate your data
       # Create your chart
       return chart
   ```

4. **Use in configuration**: Reference the plot by its ID in `layout_config.yaml`:
   ```yaml
   overrides:
     WA:
       chart_type: "my_plot"
   ```

## Usage in Code

The plot registry automatically discovers all modules in this directory:

```python
from plots import discover_plots, create_plot, list_available_plots

# List all available plots
plots = list_available_plots()

# Create a specific plot
chart = create_plot('scatter_plot', seed=42)

# The chart is a standard Altair Chart object
spec = chart.to_dict()
```

## Best Practices

- **Keep it simple**: Each module should do one thing well
- **Use reproducible data**: Always respect the `seed` parameter
- **Follow the theme**: Use neutral colors matching the gallery style
- **Standard size**: Use 300x300 as the base chart size
- **Include tooltips**: Make charts interactive where appropriate
- **Document parameters**: Clearly document any **kwargs accepted
- **Test independently**: Each module should work standalone

## Testing

Test your plot module works correctly:

```python
from plots import create_plot

# Create a chart
chart = create_plot('your_plot_id', seed=42)

# Verify it returns an Altair chart
assert chart is not None
assert hasattr(chart, 'to_dict')

# Check the spec is valid
spec = chart.to_dict()
print(spec)
```
