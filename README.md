# Altair Gallery

A performance-testing website featuring 500 interactive Altair plots across 10 pages. Built to test the performance and load times of a large Altair visualization gallery deployed via GitHub Pages.

## Features

- 🎨 **10 Pages**: Each containing 50 interactive plots
- 📊 **500 Total Plots**: Randomly generated scatter plots with interactive features
- 🚀 **Performance Optimized**: Uses Vega-Lite JSON specs for efficient rendering
- 🔍 **Interactive**: Zoom, pan, and tooltips on all visualizations
- 🌐 **GitHub Pages**: Automatically deployed via GitHub Actions

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
pip install -r requirements.txt
```

### Generate the Gallery

```bash
python generate_gallery.py
```

This will create all HTML files in the `docs/` directory.

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
├── requirements.txt      # Python dependencies
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

1. Installs Python dependencies
2. Runs `generate_gallery.py` to create HTML files
3. Deploys the `docs/` directory to GitHub Pages

## Testing

To test the gallery:

1. Generate the files: `python generate_gallery.py`
2. Verify all 11 HTML files are created in `docs/`
3. Open `docs/index.html` in a browser
4. Navigate through pages and test interactivity (zoom, pan, tooltips)

## License

This project is for performance testing purposes.
