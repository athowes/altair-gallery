# Altair Gallery

A performance-testing website featuring interactive Altair plots. Built to test the performance and load times of a large Altair visualization gallery deployed via GitHub Pages.

## Features

- 🎨 **Customizable Pages**: Configure the number of pages (default: 10)
- 📊 **Customizable Plots**: Set plots per page (default: 50, total: 500)
- 🚀 **Performance Optimized**: Uses Vega-Lite JSON specs for efficient rendering
- 🔍 **Interactive**: Zoom, pan, and tooltips on all visualizations
- 🌐 **GitHub Pages**: Automatically deployed via GitHub Actions
- ⚙️ **Flexible Configuration**: Command-line parameters for easy customization

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

This will create all HTML files in the `docs/` directory with the default settings (10 pages, 50 plots per page).

#### Customization Options

You can customize the number of pages and plots per page using command-line arguments:

```bash
# Generate 5 pages with 25 plots each
uv run python generate_gallery.py --num-pages 5 --plots-per-page 25

# Generate 3 pages with 10 plots each
uv run python generate_gallery.py --num-pages 3 --plots-per-page 10

# View available options
uv run python generate_gallery.py --help
```

Parameters:
- `--num-pages`: Number of gallery pages to generate (default: 10)
- `--plots-per-page`: Number of plots per page (default: 50)

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
├── pyproject.toml        # Project configuration and dependencies
├── uv.lock              # Lock file for reproducible installs
├── docs/                 # Generated HTML files (served by GitHub Pages)
│   ├── index.html       # Landing page with navigation
│   ├── page1.html       # Page 1 with 50 plots
│   ├── page2.html       # Page 2 with 50 plots
│   └── ...              # Pages 3-10
└── .github/
    └── workflows/
        └── deploy.yml   # GitHub Actions workflow for deployment
```

## How It Works

1. **Random Data Generation**: Each plot generates 100 random points with 4 categories
2. **Altair Visualization**: Creates interactive scatter plots using Altair
3. **Vega-Lite Specs**: Plots are embedded as JSON specifications for efficiency
4. **Client-Side Rendering**: Vega-Embed renders plots in the browser
5. **GitHub Pages**: Automatically deployed on push to main branch

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
2. Verify all 11 HTML files are created in `docs/`
3. Open `docs/index.html` in a browser
4. Navigate through pages and test interactivity (zoom, pan, tooltips)

## License

This project is for performance testing purposes.
