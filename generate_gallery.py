"""
Generate a performance-testing Altair gallery website.
Creates 10 HTML pages with 50 interactive plots each.
"""

import os
import json
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
    
    # Create interactive scatter plot
    chart = alt.Chart(data).mark_circle(size=60).encode(
        x=alt.X('x:Q', scale=alt.Scale(domain=[-4, 4])),
        y=alt.Y('y:Q', scale=alt.Scale(domain=[-4, 4])),
        color=alt.Color('category:N', legend=alt.Legend(title='Category')),
        tooltip=['x:Q', 'y:Q', 'category:N']
    ).properties(
        width=300,
        height=300,
        title=f'Plot {plot_id}'
    ).interactive()
    
    return chart


def generate_page_html(page_num, num_plots=50):
    """
    Generate HTML content for a single page with multiple plots.
    
    Args:
        page_num: Page number (1-indexed)
        num_plots: Number of plots per page
        
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
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            margin: -20px -20px 20px -20px;
        }}
        .header h1 {{
            margin: 0;
        }}
        .nav {{
            margin: 10px 0;
        }}
        .nav a {{
            color: #3498db;
            text-decoration: none;
            margin-right: 15px;
            padding: 5px 10px;
            background-color: white;
            border-radius: 3px;
        }}
        .nav a:hover {{
            background-color: #e8e8e8;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .plot-container {{
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Altair Gallery - Page {page_num}</h1>
        <div class="nav">
            <a href="index.html">Home</a>
            {''.join([f'<a href="page{i}.html">Page {i}</a>' for i in range(1, 11)])}
        </div>
    </div>
    
    <div class="gallery">
"""
    
    # Add plot containers
    for chart_info in chart_specs:
        html_template += f'        <div class="plot-container" id="{chart_info["id"]}"></div>\n'
    
    html_template += """    </div>
    
    <div class="footer">
        <p>Performance testing gallery with Altair plots</p>
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


def generate_index_html():
    """
    Generate the index/home page with navigation.
    
    Returns:
        HTML string
    """
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Altair Gallery - Home</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background-color: white;
            padding: 50px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 800px;
            text-align: center;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .description {
            color: #666;
            margin-bottom: 40px;
            line-height: 1.6;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }
        .stat-box {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .page-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
            margin-top: 30px;
        }
        .page-link {
            display: block;
            padding: 20px;
            background-color: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }
        .page-link:hover {
            background-color: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #999;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Altair Gallery</h1>
        <div class="description">
            <p>A performance testing gallery showcasing interactive Altair plots.</p>
            <p>Each page contains 50 randomly generated scatter plots with interactive features including zoom, pan, and tooltips.</p>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">10</div>
                <div class="stat-label">Pages</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">50</div>
                <div class="stat-label">Plots per Page</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">500</div>
                <div class="stat-label">Total Plots</div>
            </div>
        </div>
        
        <h2>Select a Page</h2>
        <div class="page-grid">
"""
    
    # Add links to all pages
    for i in range(1, 11):
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


def main():
    """
    Main function to generate all HTML pages.
    """
    # Create output directory if it doesn't exist
    output_dir = 'docs'
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating Altair Gallery website...")
    print(f"Output directory: {output_dir}")
    
    # Generate index page
    print("\nGenerating index page...")
    index_html = generate_index_html()
    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write(index_html)
    print("✓ index.html created")
    
    # Generate individual pages
    for page_num in range(1, 11):
        print(f"\nGenerating page {page_num}...")
        page_html = generate_page_html(page_num, num_plots=50)
        filename = os.path.join(output_dir, f'page{page_num}.html')
        with open(filename, 'w') as f:
            f.write(page_html)
        print(f"✓ page{page_num}.html created with 50 plots")
    
    print("\n" + "="*50)
    print("Gallery generation complete!")
    print(f"Total pages created: 11 (1 index + 10 gallery pages)")
    print(f"Total plots created: 500")
    print(f"Files are in the '{output_dir}/' directory")
    print("="*50)


if __name__ == "__main__":
    main()
