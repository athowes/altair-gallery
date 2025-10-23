# Altair Gallery

A performance-testing website featuring interactive Altair plots organized by US state. Built to test the performance and load times of a large Altair visualization gallery deployed via GitHub Pages.

## Features

- 🗺️ **State-Based Gallery**: One page per US state (50 states total)
- 📊 **15,000 Interactive Plots**: 300 plots per state with zoom, pan, and tooltips
- 🚀 **Performance Optimized**: Uses Vega-Lite JSON specs for efficient rendering
- 🔍 **Interactive**: Zoom, pan, and tooltips on all visualizations
- 🌐 **GitHub Pages**: Automatically deployed via GitHub Actions
- ⚙️ **Flexible Configuration**: YAML-based configuration for customizing chart types and plot counts per state

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
uv run python generate_gallery.py
```

This will create all HTML files in the `docs/` directory using the default configuration from `layout_config.yaml` (50 state pages with 300 plots each).

#### Customization Options

You can customize the gallery by modifying `layout_config.yaml` or by specifying a different configuration file:

```bash
# Use default configuration
uv run python generate_gallery.py

# Use a custom configuration file
uv run python generate_gallery.py --config my_config.yaml

# View available options
uv run python generate_gallery.py --help
```

The YAML configuration file allows you to:
- Set default chart type (scatter_plot or bar_chart) for all states
- Set default number of plots per state
- Override chart types for specific states (e.g., CA, TX, NY use bar charts in the default config)

Example `layout_config.yaml`:
```yaml
defaults:
  chart_type: "scatter_plot"
  num_plots: 300

overrides:
  CA:
    chart_type: "bar_chart"
  TX:
    chart_type: "bar_chart"
```

### Local Preview

You can preview the gallery locally by opening the files in a web browser:

```bash
# Open index page in your default browser (macOS)
open docs/index.html

# Or use Python's built-in HTTP server
python -m http.server 8000 --directory docs
# Then visit http://localhost:8000
```

## Project Structure

```
.
├── generate_gallery.py   # Main script to generate the gallery
├── layout_config.yaml    # YAML configuration for chart types and plot counts
├── pyproject.toml        # Project configuration and dependencies
├── uv.lock              # Lock file for reproducible installs
├── docs/                 # Generated HTML files (served by GitHub Pages)
│   ├── index.html       # Landing page with navigation to all states
│   ├── AL.html          # Alabama page with 300 plots
│   ├── AK.html          # Alaska page with 300 plots
│   ├── CA.html          # California page with 300 bar charts
│   └── ...              # Pages for all 50 US states
└── .github/
    └── workflows/
        └── deploy.yml   # GitHub Actions workflow for deployment
```

## How It Works

1. **State-Based Organization**: Creates one page per US state (50 total)
2. **Random Data Generation**: Each plot generates random data with reproducible seeds based on state and plot ID
3. **Altair Visualization**: Creates interactive scatter plots or bar charts using Altair based on YAML configuration
4. **Vega-Lite Specs**: Plots are embedded as JSON specifications for efficiency
5. **Client-Side Rendering**: Vega-Embed renders plots in the browser
6. **GitHub Pages**: Automatically deployed on push to main branch

## Performance Considerations

The gallery is optimized for load time:

- Static HTML files with embedded JSON specs (no server-side rendering needed)
- Vega-Lite specifications are compact and efficient
- CSS Grid layout for responsive design
- CDN-hosted Vega libraries for fast loading
- Minimal JavaScript - only what's needed for rendering

## Deployment

The site automatically deploys to GitHub Pages via GitHub Actions when changes are pushed to the main branch. The workflow:

1. Installs uv and Python
2. Installs dependencies with `uv sync`
3. Runs `generate_gallery.py` to create HTML files
4. Deploys the `docs/` directory to GitHub Pages

## Testing

To test the gallery:

1. Generate the files: `uv run python generate_gallery.py`
2. Verify all 51 HTML files are created in `docs/` (1 index + 50 state pages)
3. Open `docs/index.html` in a browser
4. Navigate through state pages and test interactivity (zoom, pan, tooltips)
5. Verify that CA, TX, and NY show bar charts while other states show scatter plots (with default config)

## License

This project is for performance testing purposes.
