# Altair Gallery

A performance-testing website featuring interactive Altair plots organized by US state, deployed via GitHub Pages.

## Features

- 🗺️ **State-Based Gallery**: 50 US states, each with 300 interactive plots (15,000 total)
- 🚀 **Performance Optimized**: Vega-Lite JSON specs with client-side rendering
- ⚙️ **Flexible Configuration**: YAML-based configuration for chart types and plot counts
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

Configure via `layout_config.yaml` to set default chart types, plot counts, and state-specific overrides:

```yaml
defaults:
  chart_type: "scatter_plot"  # or "bar_chart"
  num_plots: 300

overrides:
  CA:
    chart_type: "bar_chart"  # Override for specific states
```

### Local Preview

```bash
# Using Python HTTP server
python -m http.server 8000 --directory docs
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
├── docs/                 # Generated HTML (51 files: index + 50 states)
└── .github/workflows/    # GitHub Actions deployment
```

## How It Works

The script generates one HTML page per US state (50 total) with 300 plots each. Each plot uses reproducible random data and is rendered client-side via Vega-Embed. Static HTML files with embedded Vega-Lite JSON specs ensure fast loading and efficient rendering.

## Deployment

Automatically deploys to GitHub Pages via GitHub Actions on push to main:
1. Installs dependencies with `uv sync`
2. Generates HTML files with `generate_gallery.py`
3. Deploys `docs/` directory

## Testing

```bash
uv run python generate_gallery.py
# Verify 51 HTML files in docs/ (index + 50 states)
# Open docs/index.html and test interactivity
```

## License

This project is for performance testing purposes.
