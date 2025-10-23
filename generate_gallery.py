"""
Generate a performance-testing Altair gallery website.
Creates configurable HTML pages with interactive plots (default: 10 pages with 50 plots each).
"""

import os
import json
import argparse
import altair as alt
import pandas as pd
import numpy as np


def create_random_scatter_plot(plot_id, num_points=100):
    """
    Create an Altair scatter plot with random data.
    
    Args:
        plot_id: Unique identifier for the plot
        num_points: Number of random points to generate
        
    Returns:
        Altair Chart object
    """
    # Set seed for reproducibility based on plot_id
    np.random.seed(plot_id)
    
    # Generate random data
    data = pd.DataFrame({
        'x': np.random.randn(num_points),
        'y': np.random.randn(num_points),
        'category': np.random.choice(['A', 'B', 'C', 'D'], num_points)
    })
    
    # Create interactive scatter plot with neutral theme
    chart = alt.Chart(data).mark_circle(size=60).encode(
        x=alt.X('x:Q', scale=alt.Scale(domain=[-4, 4])),
        y=alt.Y('y:Q', scale=alt.Scale(domain=[-4, 4])),
        color=alt.Color('category:N', 
                       scale=alt.Scale(range=['#6c757d', '#868e96', '#adb5bd', '#ced4da']),
                       legend=alt.Legend(title='Category')),
        tooltip=['x:Q', 'y:Q', 'category:N']
    ).properties(
        width=300,
        height=300,
        title=f'Plot {plot_id}'
    ).configure_axis(
        gridColor='#e9ecef',
        gridOpacity=0.5,
        gridWidth=0.5
    ).configure_view(
        strokeWidth=0
    ).interactive()
    
    return chart


def generate_page_html(page_num, num_plots=50, num_pages=10):
    """
    Generate HTML content for a single page with multiple plots.
    
    Args:
        page_num: Page number (1-indexed)
        num_plots: Number of plots per page
        num_pages: Total number of pages for navigation
        
    Returns:
        HTML string
    """
    # Create list to store chart specs
    chart_specs = []
    
    # Generate plots
    for i in range(num_plots):
        plot_id = (page_num - 1) * num_plots + i + 1
        chart = create_random_scatter_plot(plot_id)
        # Get the Vega-Lite specification as a dictionary
        spec = chart.to_dict()
        chart_specs.append({
            'id': f'vis-{plot_id}',
            'spec': spec
        })
    
    # Create HTML template with embedded specs
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Altair Gallery - Page {page_num}</title>
    <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            color: #333333;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .header {{
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 30px;
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 2rem;
            font-weight: 600;
            color: #212529;
            margin: 0 0 20px 0;
            letter-spacing: -0.5px;
        }}
        .nav {{
            margin: 20px 0 0 0;
        }}
        .nav a {{
            color: #6c757d;
            text-decoration: none;
            margin-right: 20px;
            padding: 8px 16px;
            font-size: 0.9375rem;
            font-weight: 500;
            transition: color 0.2s;
        }}
        .nav a:hover {{
            color: #212529;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }}
        .plot-container {{
            background-color: #ffffff;
            padding: 20px;
            border: 1px solid #e9ecef;
        }}
        .footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #6c757d;
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Altair Gallery - Page {page_num}</h1>
            <div class="nav">
                <a href="index.html">Home</a>
                {''.join([f'<a href="page{i}.html">Page {i}</a>' for i in range(1, num_pages + 1)])}
            </div>
        </div>
        
        <div class="gallery">
"""
    
    # Add plot containers
    for chart_info in chart_specs:
        html_template += f'        <div class="plot-container" id="{chart_info["id"]}"></div>\n'
    
    html_template += """        </div>
        
        <div class="footer">
            <p>Performance testing gallery with Altair plots</p>
        </div>
    </div>
    
    <script type="text/javascript">
"""
    
    # Embed chart specifications
    html_template += f"        const chartSpecs = {json.dumps(chart_specs, indent=8)};\n"
    
    html_template += """        
        // Render all charts
        chartSpecs.forEach(function(chartInfo) {
            vegaEmbed('#' + chartInfo.id, chartInfo.spec, {
                actions: {
                    export: true,
                    source: false,
                    compiled: false,
                    editor: false
                }
            });
        });
    </script>
</body>
</html>
"""
    
    return html_template


def generate_index_html(num_pages=10, plots_per_page=50):
    """
    Generate the index/home page with navigation.
    
    Args:
        num_pages: Total number of gallery pages
        plots_per_page: Number of plots per page
    
    Returns:
        HTML string
    """
    total_plots = num_pages * plots_per_page
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Altair Gallery - Home</title>
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            color: #333333;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 20px;
        }}
        h1 {{
            font-size: 2.5rem;
            font-weight: 600;
            color: #212529;
            margin: 0 0 30px 0;
            text-align: center;
            letter-spacing: -0.5px;
        }}
        .description {{
            color: #6c757d;
            margin-bottom: 50px;
            text-align: center;
            font-size: 1.0625rem;
        }}
        .description p {{
            margin: 10px 0;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin-bottom: 60px;
            padding-bottom: 50px;
            border-bottom: 1px solid #e0e0e0;
        }}
        .stat-box {{
            text-align: center;
            padding: 30px 20px;
            border: 1px solid #e9ecef;
        }}
        .stat-number {{
            font-size: 2.5rem;
            font-weight: 600;
            color: #495057;
            line-height: 1;
        }}
        .stat-label {{
            color: #6c757d;
            margin-top: 10px;
            font-size: 0.9375rem;
            font-weight: 500;
        }}
        h2 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #212529;
            margin: 0 0 30px 0;
            text-align: center;
            letter-spacing: -0.25px;
        }}
        .page-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .page-link {{
            display: block;
            padding: 24px;
            background-color: #ffffff;
            color: #495057;
            text-decoration: none;
            border: 1px solid #dee2e6;
            text-align: center;
            font-weight: 500;
            font-size: 0.9375rem;
            transition: all 0.2s;
        }}
        .page-link:hover {{
            background-color: #f8f9fa;
            border-color: #adb5bd;
            color: #212529;
        }}
        .footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #6c757d;
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Altair Gallery</h1>
        <div class="description">
            <p>A performance testing gallery showcasing interactive Altair plots.</p>
            <p>Each page contains {plots_per_page} randomly generated scatter plots with interactive features including zoom, pan, and tooltips.</p>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{num_pages}</div>
                <div class="stat-label">Pages</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{plots_per_page}</div>
                <div class="stat-label">Plots per Page</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{total_plots}</div>
                <div class="stat-label">Total Plots</div>
            </div>
        </div>
        
        <h2>Select a Page</h2>
        <div class="page-grid">
"""
    
    # Add links to all pages
    for i in range(1, num_pages + 1):
        html += f'            <a href="page{i}.html" class="page-link">Page {i}</a>\n'
    
    html += """        </div>
        
        <div class="footer">
            <p>Built with Altair and Vega-Lite</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def main(num_pages=10, plots_per_page=50):
    """
    Main function to generate all HTML pages.
    
    Args:
        num_pages: Number of gallery pages to generate (default: 10)
        plots_per_page: Number of plots per page (default: 50)
    """
    # Create output directory if it doesn't exist
    output_dir = 'docs'
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating Altair Gallery website...")
    print(f"Output directory: {output_dir}")
    print(f"Pages: {num_pages}")
    print(f"Plots per page: {plots_per_page}")
    
    # Generate index page
    print("\nGenerating index page...")
    index_html = generate_index_html(num_pages, plots_per_page)
    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write(index_html)
    print("✓ index.html created")
    
    # Generate individual pages
    for page_num in range(1, num_pages + 1):
        print(f"\nGenerating page {page_num}...")
        page_html = generate_page_html(page_num, plots_per_page, num_pages)
        filename = os.path.join(output_dir, f'page{page_num}.html')
        with open(filename, 'w') as f:
            f.write(page_html)
        print(f"✓ page{page_num}.html created with {plots_per_page} plots")
    
    total_plots = num_pages * plots_per_page
    print("\n" + "="*50)
    print("Gallery generation complete!")
    print(f"Total pages created: {num_pages + 1} (1 index + {num_pages} gallery pages)")
    print(f"Total plots created: {total_plots}")
    print(f"Files are in the '{output_dir}/' directory")
    print("="*50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate a performance-testing Altair gallery website.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--num-pages',
        type=int,
        default=10,
        help='Number of gallery pages to generate'
    )
    parser.add_argument(
        '--plots-per-page',
        type=int,
        default=50,
        help='Number of plots per page'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.num_pages < 1:
        parser.error("--num-pages must be at least 1")
    if args.plots_per_page < 1:
        parser.error("--plots-per-page must be at least 1")
    
    main(args.num_pages, args.plots_per_page)
