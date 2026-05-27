from .analytics import plot_correlation_heatmap, plot_distribution
from .client import PlantTrend
from .columns import plot_columns
from .config_info import describe_plot_config
from .labels import get_default_label_map, load_label_map, merge_label_maps
from .styles import apply_plot_style, get_available_styles

__version__ = '0.1.0'

__all__ = [
    'apply_plot_style',
    'PlantTrend',
    'describe_plot_config',
    'get_default_label_map',
    'get_available_styles',
    'load_label_map',
    'merge_label_maps',
    'plot_columns',
    'plot_correlation_heatmap',
    'plot_distribution',
]
