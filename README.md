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
  chart_type: "scatter_plot"  # or "bar_chart"
  num_plots: 300

overrides:
  CA:
    chart_type: "bar_chart"  # Override for specific states
```

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
├── docs/                 # Generated site (index + 50 state pages)
│   ├── assets/
│   │   └── lazy-loader.js # Shared lazy loading script
│   ├── index.html
│   └── *.html            # One page per state
└── .github/workflows/    # GitHub Actions deployment
```

## How It Works

1. `layout_config.yaml` defines default chart settings plus state-specific overrides.
2. `generate_gallery.py` builds reproducible random datasets and serializes each Altair chart to Vega-Lite JSON.
3. The generator writes static HTML for every state and the home page, alongside `docs/assets/lazy-loader.js`.
4. In the browser, `lazy-loader.js` watches each plot container with `IntersectionObserver`, queueing renders through Vega-Embed with a capped level of concurrency to keep the UI responsive.
5. GitHub Pages serves the generated files directly—no runtime backend required.

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
