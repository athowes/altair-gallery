# Altair Gallery

A performance-testing website featuring interactive Altair plots organized by US state, deployed via GitHub Pages.

## Features

- 🗺️ **State-Based Gallery**: 50 US states, each with 300 interactive plots (15,000 total)
- 🚀 **Performance Optimized**: Static Vega-Lite specs, CDN-hosted Vega libraries, and lazy rendering via `lazy-loader.js`
- ⚙️ **Flexible Configuration**: YAML-based defaults and per-state overrides for chart type and plot count
- 🌐 **Auto-Deployed**: GitHub Actions deployment to GitHub Pages

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (fast Python package manager)

### Installation

Install uv if you haven't already:

```bash
# On macOS and Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip:
pip install uv
```

Install dependencies:

```bash
uv sync
```

### Generate the Gallery

```bash
# Generate with default configuration
uv run python generate_gallery.py

# Use custom configuration file
uv run python generate_gallery.py --config my_config.yaml
```

This command writes the HTML pages into `docs/` and emits a shared lazy-loading helper at `docs/assets/lazy-loader.js`.

Configure via `layout_config.yaml` to set default chart types, plot counts, and state-specific overrides:

```yaml
defaults:
  chart_type: "scatter_plot"  # Default chart type (any plot module ID)
  num_plots: 300

overrides:
  CA:
    chart_type: "bar_chart"    # Use bar charts for California
  FL:
    chart_type: "line_chart"   # Use line charts for Florida
  IL:
    chart_type: "heatmap"      # Use heatmaps for Illinois
```

Available chart types: `scatter_plot`, `bar_chart`, `line_chart`, `heatmap` (see `plots/` directory for all modules)

### Local Preview

```bash
# Using Python HTTP server
python3 -m http.server 8000 --directory docs
# Visit http://localhost:8000

# Or open directly (macOS)
open docs/index.html
```

## Project Structure

```
.
├── generate_gallery.py   # Main script
├── layout_config.yaml    # Configuration file
├── pyproject.toml        # Dependencies
├── plots/                # Modular plot definitions
│   ├── __init__.py       # Plot registry and loader
│   ├── README.md         # Plot module documentation
│   ├── scatter_plot.py   # Scatter plot module
│   ├── bar_chart.py      # Bar chart module
│   ├── line_chart.py     # Line chart module
│   ├── heatmap.py        # Heatmap module
│   └── ...               # Additional plot modules
├── docs/                 # Generated site (index + 50 state pages)
│   ├── assets/
│   │   └── lazy-loader.js # Shared lazy loading script
│   ├── index.html
│   └── *.html            # One page per state
└── .github/workflows/    # GitHub Actions deployment
```

## How It Works

1. **Modular Plots**: Each visualization type is defined in its own module in the `plots/` directory. Each module exports metadata and a `create_chart()` function.
2. **Configuration**: `layout_config.yaml` defines default chart settings plus state-specific overrides, referencing plot modules by ID.
3. **Generation**: `generate_gallery.py` discovers available plot modules, builds reproducible random datasets, and serializes each Altair chart to Vega-Lite JSON.
4. **Static Output**: The generator writes static HTML for every state and the home page, alongside `docs/assets/lazy-loader.js`.
5. **Lazy Loading**: In the browser, `lazy-loader.js` watches each plot container with `IntersectionObserver`, queueing renders through Vega-Embed with a capped level of concurrency to keep the UI responsive.
6. **Deployment**: GitHub Pages serves the generated files directly—no runtime backend required.

## Modular Architecture

Each visualization is now a self-contained Python module in the `plots/` directory. This makes the codebase:
- **Isolated**: Each plot is independent and reusable
- **Extensible**: Add new plot types without touching existing code
- **Testable**: Test each visualization independently
- **Discoverable**: Automatic plot registry via module discovery

See **[MODULARITY.md](MODULARITY.md)** for detailed architecture documentation.

## Adding New Plot Types

To add a new visualization type:

1. Create a new module in `plots/` (see `plots/README.md` for details)
2. Define `METADATA` with a unique ID and `create_chart()` function
3. Reference the new plot type in `layout_config.yaml`
4. Run `generate_gallery.py` to rebuild the site

Example:
```python
# plots/my_custom_plot.py
METADATA = {
    'id': 'my_custom_plot',
    'title': 'My Custom Visualization',
    'tags': ['custom'],
    'estimated_render_time': 0.10
}

def create_chart(seed, **kwargs):
    # Your implementation
    return chart
```

Try it yourself: `python example_usage.py`

## Deployment

Automatically deploys to GitHub Pages via GitHub Actions on push to main:
1. Installs dependencies with `uv sync`
2. Generates HTML files with `generate_gallery.py`
3. Deploys `docs/` directory

## Testing

```bash
uv run python generate_gallery.py
# Verify docs/assets/lazy-loader.js exists
# Verify 51 HTML files in docs/ (index + 50 states)
# Open docs/index.html and test interactivity
```

## License

This project is for performance testing purposes.
