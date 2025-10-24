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
from plots import create_plot


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

LAZY_LOADER_JS = """(function(global) {
    function load(config) {
        if (!config || !Array.isArray(config.specs)) {
            console.warn('AltairLazyLoader: missing chart specifications.');
            return;
        }
        if (typeof global.vegaEmbed !== 'function') {
            console.error('AltairLazyLoader: vegaEmbed is not available on the page.');
            return;
        }

        const embedOptions = config.embedOptions || {};
        const maxConcurrent = typeof config.maxConcurrent === 'number' && config.maxConcurrent > 0 ? config.maxConcurrent : 6;
        const rootMargin = typeof config.rootMargin === 'string' ? config.rootMargin : '200px 0px';

        const renderQueue = [];
        let activeRenders = 0;
        let drainScheduled = false;

        const specsById = new Map(config.specs.map(function(info) {
            return [info.id, info];
        }));

        function scheduleDrain() {
            if (drainScheduled) {
                return;
            }
            drainScheduled = true;
            const runner = function() {
                drainScheduled = false;
                drainQueue();
            };
            if ('requestIdleCallback' in global) {
                global.requestIdleCallback(runner, { timeout: 200 });
            } else {
                global.setTimeout(runner, 0);
            }
        }

        function drainQueue() {
            while (activeRenders < maxConcurrent && renderQueue.length > 0) {
                const chartInfo = renderQueue.shift();
                activeRenders += 1;

                global.vegaEmbed('#' + chartInfo.id, chartInfo.spec, embedOptions)
                    .catch(function(error) {
                        console.error('AltairLazyLoader: failed to render chart ' + chartInfo.id, error);
                        const el = global.document.getElementById(chartInfo.id);
                        if (el) {
                            el.innerHTML = '<pre style="color:#c92a2a;font-family:monospace;">Failed to render chart</pre>';
                        }
                    })
                    .finally(function() {
                        activeRenders -= 1;
                        scheduleDrain();
                    });
            }
        }

        function queueRender(chartInfo) {
            renderQueue.push(chartInfo);
            scheduleDrain();
        }

        if ('IntersectionObserver' in global) {
            const observer = new global.IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        observer.unobserve(entry.target);
                        if (!entry.target.dataset.rendered) {
                            entry.target.dataset.rendered = 'true';
                            const info = specsById.get(entry.target.id);
                            if (info) {
                                queueRender(info);
                            }
                        }
                    }
                });
            }, { rootMargin: rootMargin });

            config.specs.forEach(function(info) {
                const el = global.document.getElementById(info.id);
                if (el) {
                    observer.observe(el);
                }
            });
        } else {
            config.specs.forEach(function(info) {
                queueRender(info);
            });
        }
    }

    global.AltairLazyLoader = {
        load: load
    };
}(window));
"""


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


# Plot creation functions are now in the plots/ module
# See plots/scatter_plot.py and plots/bar_chart.py


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
    
    # Generate plots using modular plot system
    for i in range(num_plots):
        seed = hash(state + str(i)) % 10000  # State-specific seed for reproducibility
        
        # Use the appropriate plot module based on chart_type
        chart = create_plot(chart_type, seed=seed)
        
        if chart is None:
            # Fallback to scatter_plot if chart_type is not found
            chart = create_plot('scatter_plot', seed=seed)
        
        # Get the Vega-Lite specification as a dictionary
        spec = chart.to_dict()
        chart_specs.append({
            'id': f'vis-{seed}',
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
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }}
        .nav a {{
            color: #6c757d;
            text-decoration: none;
            padding: 8px 16px;
            font-size: 0.9375rem;
            font-weight: 500;
            transition: color 0.2s;
        }}
        .nav a:hover {{
            color: #212529;
        }}
        .nav select {{
            padding: 8px 12px;
            font-size: 0.9375rem;
            font-family: inherit;
            color: #495057;
            background-color: #ffffff;
            border: 2px solid #dee2e6;
            border-radius: 4px;
            cursor: pointer;
            transition: border-color 0.2s;
        }}
        .nav select:hover {{
            border-color: #adb5bd;
        }}
        .nav select:focus {{
            outline: none;
            border-color: #6c757d;
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
                <select onchange="if(this.value) window.location.href=this.value;">
                    <option value="">Go to state...</option>
"""
    
    # Add dropdown options for all states
    for nav_state in all_states:
        nav_state_name = STATE_NAMES[nav_state]
        selected = ' selected' if nav_state == state else ''
        html_template += f'                    <option value="{nav_state}.html"{selected}>{nav_state_name}</option>\n'
    
    html_template += """                </select>
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
    </script>
    <script src="assets/lazy-loader.js"></script>
    <script type="text/javascript">
        const loaderConfig = {
            specs: chartSpecs,
            embedOptions: {
                actions: {
                    export: true,
                    source: false,
                    compiled: false,
                    editor: false
                }
            },
            maxConcurrent: 6,
            rootMargin: '200px 0px'
        };
        
        if (window.AltairLazyLoader && typeof window.AltairLazyLoader.load === 'function') {
            window.AltairLazyLoader.load(loaderConfig);
        } else {
            console.error('AltairLazyLoader is not available.');
        }
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
        .state-selector {{
            max-width: 400px;
            margin: 30px auto;
            text-align: center;
        }}
        .state-selector select {{
            width: 100%;
            padding: 12px 16px;
            font-size: 1rem;
            font-family: inherit;
            color: #495057;
            background-color: #ffffff;
            border: 2px solid #dee2e6;
            border-radius: 4px;
            cursor: pointer;
            transition: border-color 0.2s;
        }}
        .state-selector select:hover {{
            border-color: #adb5bd;
        }}
        .state-selector select:focus {{
            outline: none;
            border-color: #6c757d;
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
            <p>Different states showcase various visualization types including scatter plots, bar charts, line charts, and heatmaps.</p>
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
        <div class="state-selector">
            <select id="stateSelect" onchange="if(this.value) window.location.href=this.value;">
                <option value="">Choose a state...</option>
"""
    
    # Add dropdown options for all states
    for state in all_states:
        state_name = STATE_NAMES[state]
        html += f'                <option value="{state}.html">{state_name}</option>\n'
    
    html += """            </select>
        </div>
        
        <div class="footer">
            <p>Built with Altair and Vega-Lite</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def write_lazy_loader_script(output_dir):
    """Write the shared lazy loading script into the docs/assets directory."""
    assets_dir = os.path.join(output_dir, 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    script_path = os.path.join(assets_dir, 'lazy-loader.js')
    with open(script_path, 'w') as f:
        f.write(LAZY_LOADER_JS)
    return script_path


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
    script_path = write_lazy_loader_script(output_dir)
    
    print("Generating Altair Gallery website...")
    print(f"Output directory: {output_dir}")
    print(f"Configuration: {config_file}")
    print(f"States: {len(US_STATES)}")
    print(f"Plots per state: {layout_config['defaults']['num_plots']}")
    print(f"Shared assets: {os.path.relpath(script_path, output_dir)}")
    
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
