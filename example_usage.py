"""
Example demonstrating the modular plot system.

This script shows how easy it is to use the plot modules independently.
"""

from plots import discover_plots, create_plot, list_available_plots

# List all available plot types
print("=" * 60)
print("Available Plot Modules")
print("=" * 60)

plots_info = list_available_plots()
for info in sorted(plots_info, key=lambda x: x['id']):
    print(f"\n{info['title']}")
    print(f"  ID: {info['id']}")
    print(f"  Tags: {', '.join(info['tags'])}")
    print(f"  Estimated render time: {info['estimated_render_time']}s")

# Example: Create a specific chart
print("\n" + "=" * 60)
print("Creating Charts")
print("=" * 60)

# Create a scatter plot
scatter = create_plot('scatter_plot', seed=42)
print(f"\n✓ Created scatter plot")
print(f"  Chart type: {scatter.to_dict()['mark']['type']}")

# Create a bar chart
bar = create_plot('bar_chart', seed=123)
print(f"\n✓ Created bar chart")
print(f"  Chart type: {bar.to_dict()['mark']}")

# Create a line chart
line = create_plot('line_chart', seed=456)
print(f"\n✓ Created line chart")
print(f"  Chart type: {line.to_dict()['mark']['type']}")

# Create a heatmap
heatmap = create_plot('heatmap', seed=789)
print(f"\n✓ Created heatmap")
print(f"  Chart type: {heatmap.to_dict()['mark']['type']}")

print("\n" + "=" * 60)
print("Each plot is a standalone alt.Chart object that can be:")
print("  - Saved to HTML: chart.save('output.html')")
print("  - Converted to JSON: chart.to_json()")
print("  - Displayed in Jupyter: chart")
print("  - Further customized: chart.properties(width=500)")
print("=" * 60)
