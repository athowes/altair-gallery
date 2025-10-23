"""
Generate a performance-testing Altair gallery website.
Creates configurable HTML pages with interactive plots (default: 50 pages with 300 plots each).
"""

import os
import json
import argparse
import yaml
import altair as alt
import pandas as pd
import numpy as np


# US States data
US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

STATE_NAMES = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}


def load_layout_config(config_path='layout_config.yaml'):
    """Load the YAML layout configuration."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def resolve_layout(manifest, state):
    """
    Resolve the final layout configuration for a given state.
    
    Args:
        manifest: Loaded YAML configuration
        state: Two-letter state code
        
    Returns:
        Resolved layout configuration dictionary
    """
    # Start with defaults
    config = {**manifest["defaults"]}
    
    # Apply overrides if they exist for this state
    if state in manifest.get("overrides", {}):
        override = manifest["overrides"][state]
        config.update(override)
    
    return config


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


def create_random_bar_chart(plot_id):
    """
    Create an Altair bar chart with random data.
    
    Args:
        plot_id: Unique identifier for the plot
        
    Returns:
        Altair Chart object
    """
    # Set seed for reproducibility based on plot_id
    np.random.seed(plot_id)
    
    # Generate random data
    categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
    data = pd.DataFrame({
        'category': categories,
        'value': np.random.randint(10, 100, len(categories))
    })
    
    # Create bar chart with neutral theme
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('category:N', title='Category'),
        y=alt.Y('value:Q', title='Value'),
        color=alt.Color('category:N', 
                       scale=alt.Scale(range=['#6c757d', '#868e96', '#adb5bd', '#ced4da', '#dee2e6']),
                       legend=None),
        tooltip=['category:N', 'value:Q']
    ).properties(
        width=300,
        height=300,
        title=f'Bar Chart {plot_id}'
    ).configure_axis(
        gridColor='#e9ecef',
        gridOpacity=0.5,
        gridWidth=0.5
    ).configure_view(
        strokeWidth=0
    )
    
    return chart


def generate_page_html(state, layout_config, all_states):
    """
    Generate HTML content for a single state page with multiple plots.
    
    Args:
        state: Two-letter state code
        layout_config: Resolved layout configuration for this state  
        all_states: List of all state codes for navigation
        
    Returns:
        HTML string
    """
    state_name = STATE_NAMES[state]
    chart_type = layout_config['chart_type']
    num_plots = layout_config['num_plots']
    
    # Create list to store chart specs
    chart_specs = []
    
    # Generate plots
    for i in range(num_plots):
        plot_id = hash(state + str(i)) % 10000  # State-specific plot IDs
        
        if chart_type == 'bar_chart':
            chart = create_random_bar_chart(plot_id)
        else:  # default to scatter_plot
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
    <title>{state_name} - Altair Gallery</title>
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
            <h1>{state_name} ({state}) - Chart Type: {chart_type.replace('_', ' ').title()}</h1>
            <div class="nav">
                <a href="index.html">Home</a>
"""
    
    # Add navigation to all states
    for nav_state in all_states:
        html_template += f'                <a href="{nav_state}.html">{nav_state}</a>\n'
    
    html_template += """
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


def generate_index_html(layout_config, all_states):
    """
    Generate the index/home page with navigation.
    
    Args:
        layout_config: Loaded YAML configuration
        all_states: List of all state codes
    
    Returns:
        HTML string
    """
    total_plots = len(all_states) * layout_config['defaults']['num_plots']
    plots_per_page = layout_config['defaults']['num_plots']
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
            <p>A performance testing gallery showcasing interactive Altair plots by US state.</p>
            <p>Each state contains {plots_per_page} randomly generated plots with interactive features including zoom, pan, and tooltips.</p>
            <p>States marked with ★ use bar charts instead of the default scatter plots.</p>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{len(all_states)}</div>
                <div class="stat-label">States</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{plots_per_page}</div>
                <div class="stat-label">Plots per State</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{total_plots}</div>
                <div class="stat-label">Total Plots</div>
            </div>
        </div>
        
        <h2>Select a State</h2>
        <div class="page-grid">
"""
    
    # Add links to all states
    states_with_overrides = set(layout_config.get('overrides', {}).keys())
    for state in all_states:
        state_name = STATE_NAMES[state]
        star = " ★" if state in states_with_overrides else ""
        html += f'            <a href="{state}.html" class="page-link">{state_name}{star}</a>\n'
    
    html += """        </div>
        
        <div class="footer">
            <p>Built with Altair and Vega-Lite</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def main(config_file='layout_config.yaml'):
    """
    Main function to generate all HTML pages using YAML configuration.
    
    Args:
        config_file: Path to YAML configuration file (default: 'layout_config.yaml')
    """
    # Load configuration
    layout_config = load_layout_config(config_file)
    
    # Create output directory if it doesn't exist
    output_dir = 'docs'
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating Altair Gallery website...")
    print(f"Output directory: {output_dir}")
    print(f"Configuration: {config_file}")
    print(f"States: {len(US_STATES)}")
    print(f"Plots per state: {layout_config['defaults']['num_plots']}")
    
    # Generate index page
    print("\nGenerating index page...")
    index_html = generate_index_html(layout_config, US_STATES)
    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write(index_html)
    print("✓ index.html created")
    
    # Generate individual state pages
    for state in US_STATES:
        print(f"\nGenerating {state} ({STATE_NAMES[state]})...")
        state_layout = resolve_layout(layout_config, state)
        page_html = generate_page_html(state, state_layout, US_STATES)
        filename = os.path.join(output_dir, f'{state}.html')
        with open(filename, 'w') as f:
            f.write(page_html)
        chart_type = state_layout['chart_type']
        num_plots = state_layout['num_plots']
        print(f"✓ {state}.html created with {num_plots} {chart_type} plots")
    
    total_plots = len(US_STATES) * layout_config['defaults']['num_plots']
    states_with_overrides = list(layout_config.get('overrides', {}).keys())
    print("\n" + "="*50)
    print("Gallery generation complete!")
    print(f"Total pages created: {len(US_STATES) + 1} (1 index + {len(US_STATES)} state pages)")
    print(f"Total plots created: {total_plots}")
    print(f"States with custom layouts: {', '.join(states_with_overrides) if states_with_overrides else 'None'}")
    print(f"Files are in the '{output_dir}/' directory")
    print("="*50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate a state-based Altair gallery website using YAML configuration.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--config',
        type=str,
        default='layout_config.yaml',
        help='Path to YAML configuration file'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not os.path.exists(args.config):
        parser.error(f"Configuration file '{args.config}' not found")
    
    main(args.config)
