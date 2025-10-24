# Modularity Design

This document explains the modular plot system in the Altair Gallery.

## Overview

The codebase has been refactored to separate plot definitions into independent, reusable modules. Each visualization type is now self-contained, making it easy to:

- Add new plot types without modifying existing code
- Swap plot types for different states via configuration
- Reuse plot modules in other projects
- Test and maintain plots independently

## Architecture

### Directory Structure

```
plots/
├── __init__.py           # Plot registry and loader
├── README.md            # Module documentation
├── scatter_plot.py      # Scatter plot implementation
├── bar_chart.py         # Bar chart implementation
├── line_chart.py        # Line chart implementation
├── heatmap.py           # Heatmap implementation
└── [your_plot].py       # Add new plots here
```

### Plot Module Interface

Each plot module must implement:

```python
# Metadata dictionary
METADATA = {
    'id': 'unique_id',                # Used in layout_config.yaml
    'title': 'Human Readable Name',   # Display name
    'tags': ['tag1', 'tag2'],        # Searchable keywords
    'estimated_render_time': 0.15    # Seconds (approximate)
}

# Chart creation function
def create_chart(seed, **kwargs):
    """
    Generate the visualization.
    
    Args:
        seed: Random seed for reproducible data generation
        **kwargs: Additional customization parameters
        
    Returns:
        alt.Chart: Altair Chart object
    """
    np.random.seed(seed)
    # ... generate data and create chart
    return chart
```

### Plot Registry

The `plots/__init__.py` module provides automatic discovery:

```python
from plots import discover_plots, create_plot, list_available_plots

# Discover all plot modules
plots = discover_plots()
# {'scatter_plot': <module>, 'bar_chart': <module>, ...}

# Create a specific plot
chart = create_plot('scatter_plot', seed=42)

# List available plots with metadata
available = list_available_plots()
```

## Usage Examples

### Example 1: Generate a Single Plot

```python
from plots import create_plot

# Create a scatter plot
chart = create_plot('scatter_plot', seed=42, num_points=150)

# Save to file
chart.save('my_plot.html')
```

### Example 2: Use in Configuration

```yaml
# layout_config.yaml
defaults:
  chart_type: "scatter_plot"
  num_plots: 300

overrides:
  CA:
    chart_type: "bar_chart"    # Use bar charts for California
  FL:
    chart_type: "line_chart"   # Use line charts for Florida
```

### Example 3: Programmatic Generation

```python
from plots import list_available_plots, create_plot

# Get all available plot types
plots = list_available_plots()

# Generate one of each type
for plot_info in plots:
    chart = create_plot(plot_info['id'], seed=123)
    chart.save(f"{plot_info['id']}_example.html")
```

## Integration with Gallery Generator

The `generate_gallery.py` script uses the plot registry:

```python
from plots import create_plot

# Generate a chart based on configuration
chart = create_plot(chart_type, seed=seed)

# Convert to Vega-Lite spec for HTML embedding
spec = chart.to_dict()
```

## Benefits of Modular Design

### 1. **Isolation**
Each plot is completely independent. Changes to one plot don't affect others.

### 2. **Reusability**
Plot modules can be imported and used in any Python project:

```python
from altair_gallery.plots import create_plot
my_chart = create_plot('scatter_plot', seed=42)
```

### 3. **Extensibility**
Adding new plot types is trivial:

1. Create `plots/my_new_plot.py`
2. Define `METADATA` and `create_chart()`
3. Reference it in `layout_config.yaml`

### 4. **Testability**
Each module can be tested independently:

```python
def test_scatter_plot():
    chart = create_plot('scatter_plot', seed=42)
    assert chart is not None
    assert 'mark' in chart.to_dict()
```

### 5. **Discoverability**
The registry automatically finds new modules - no manual registration needed.

## Available Plot Types

### scatter_plot
Interactive scatter plot with categorical coloring and zoom/pan capabilities.

**Tags**: scatter, interactive, points, categories  
**Parameters**: `num_points` (default: 100)

### bar_chart
Simple categorical bar chart with tooltips.

**Tags**: bar, categorical, comparison  
**Parameters**: `num_categories` (default: 5)

### line_chart
Time series line chart showing trends over time.

**Tags**: line, time-series, trend, temporal  
**Parameters**: `num_points` (default: 50)

### heatmap
Grid-based heatmap for visualizing matrix data.

**Tags**: heatmap, matrix, correlation, intensity  
**Parameters**: `grid_size` (default: 10)

## Adding a New Plot Type

Follow these steps to add a new visualization:

### Step 1: Create Module File

Create `plots/my_plot.py`:

```python
"""
Brief description of your visualization.
"""

import altair as alt
import pandas as pd
import numpy as np

METADATA = {
    'id': 'my_plot',
    'title': 'My Custom Plot',
    'tags': ['custom', 'example'],
    'estimated_render_time': 0.10
}

def create_chart(seed, **kwargs):
    """Create the chart."""
    np.random.seed(seed)
    
    # Generate data
    data = pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100)
    })
    
    # Create chart
    chart = alt.Chart(data).mark_point().encode(
        x='x:Q',
        y='y:Q'
    ).properties(
        width=300,
        height=300,
        title=f'My Plot {seed}'
    )
    
    return chart
```

### Step 2: Test the Module

```python
from plots import create_plot

chart = create_plot('my_plot', seed=42)
assert chart is not None
chart.save('test_my_plot.html')
```

### Step 3: Use in Configuration

Update `layout_config.yaml`:

```yaml
overrides:
  WA:
    chart_type: "my_plot"
```

### Step 4: Generate Gallery

```bash
python generate_gallery.py
```

That's it! Your new plot type is now integrated.

## Best Practices

1. **Use Reproducible Random Data**: Always respect the `seed` parameter
2. **Follow Size Standards**: Use 300x300 as base dimensions
3. **Maintain Theme Consistency**: Use neutral colors (#6c757d family)
4. **Add Interactivity**: Include tooltips where appropriate
5. **Document Parameters**: Clearly describe all `**kwargs`
6. **Keep It Simple**: One visualization concept per module
7. **Test Independently**: Ensure module works standalone

## Migration Notes

### Before (Monolithic)
```python
# generate_gallery.py
def create_random_scatter_plot(plot_id):
    # ... 40 lines of code
    return chart

def create_random_bar_chart(plot_id):
    # ... 35 lines of code
    return chart
```

### After (Modular)
```python
# plots/scatter_plot.py
METADATA = {...}
def create_chart(seed, **kwargs):
    # ... 40 lines of code
    return chart

# plots/bar_chart.py
METADATA = {...}
def create_chart(seed, **kwargs):
    # ... 35 lines of code
    return chart

# generate_gallery.py
from plots import create_plot
chart = create_plot(chart_type, seed=seed)
```

## Performance Considerations

- **Module Loading**: Plots are loaded once and cached by Python's import system
- **Data Generation**: Each chart generates its own data (no shared state)
- **Memory**: Charts are generated on-demand and converted to Vega-Lite JSON
- **Scalability**: Can easily handle 15,000+ charts (300 per state × 50 states)

## Future Enhancements

Potential improvements to the modular system:

1. **Plot Categories**: Group related plots (e.g., statistical, geospatial)
2. **Parameter Validation**: Use pydantic or dataclasses for type checking
3. **Plot Composition**: Allow combining multiple plots
4. **Theme System**: Configurable color schemes per plot
5. **Data Adapters**: Support external data sources
6. **Testing Framework**: Automated visual regression testing

## Questions?

See `plots/README.md` for module-specific documentation or `example_usage.py` for working code examples.
