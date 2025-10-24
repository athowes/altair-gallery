"""
Plot module registry for the Altair Gallery.

This module provides a central registry for all plot modules.
Each plot module should define:
- METADATA: dict with keys: id, title, tags, estimated_render_time
- create_chart(plot_id, **kwargs): function that returns an alt.Chart object
"""

import importlib
import os
from pathlib import Path


def discover_plots():
    """
    Discover all plot modules in the plots directory.
    
    Returns:
        dict: Mapping of plot_id to plot module
    """
    plots_dir = Path(__file__).parent
    plot_modules = {}
    
    for file in plots_dir.glob("*.py"):
        if file.name.startswith("_"):
            continue
            
        module_name = file.stem
        try:
            module = importlib.import_module(f"plots.{module_name}")
            
            # Validate the module has required attributes
            if hasattr(module, 'METADATA') and hasattr(module, 'create_chart'):
                metadata = module.METADATA
                plot_id = metadata.get('id')
                
                if plot_id:
                    plot_modules[plot_id] = module
        except Exception as e:
            print(f"Warning: Failed to load plot module {module_name}: {e}")
    
    return plot_modules


def get_plot_metadata(plot_id):
    """
    Get metadata for a specific plot.
    
    Args:
        plot_id: The ID of the plot
        
    Returns:
        dict: Plot metadata or None if not found
    """
    plots = discover_plots()
    if plot_id in plots:
        return plots[plot_id].METADATA
    return None


def create_plot(plot_id, seed, **kwargs):
    """
    Create a chart using the specified plot module.
    
    Args:
        plot_id: The ID of the plot module to use
        seed: Seed value for reproducible random data
        **kwargs: Additional arguments to pass to the plot's create_chart function
        
    Returns:
        alt.Chart: The generated chart or None if plot_id not found
    """
    plots = discover_plots()
    if plot_id in plots:
        return plots[plot_id].create_chart(seed=seed, **kwargs)
    return None


def list_available_plots():
    """
    List all available plot modules with their metadata.
    
    Returns:
        list: List of metadata dicts for all available plots
    """
    plots = discover_plots()
    return [module.METADATA for module in plots.values()]
