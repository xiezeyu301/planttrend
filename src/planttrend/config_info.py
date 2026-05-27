from typing import Any, Dict, Union

PLOT_CONFIG_SPECS = {
    'columns': {
        'function': 'plot_columns',
        'summary': 'Multi-axis trend plotting with global config plus subplot-local overrides from config.subplots.',
        'parameters': [
            {'name': 'df', 'required': True, 'description': 'Source pandas DataFrame.'},
            {'name': 'columns', 'required': True, 'description': 'Subplot column definitions. Use nested lists only.'},
            {'name': 'x', 'required': False, 'default': '时间', 'description': 'X-axis column name.'},
            {'name': 'figsize', 'required': False, 'default': '(20, 3)', 'description': 'Figure size as (width, height_per_subplot).'},
            {'name': 'config', 'required': False, 'default': '{}', 'description': 'Global plotting config.'},
        ],
        'config': [
            {'name': 'style', 'default': 'default', 'description': 'Style preset name.'},
            {'name': 'map_dict', 'default': 'None', 'description': 'Column label mapping dictionary.'},
            {'name': 'label_map', 'default': 'None', 'description': 'Alias of map_dict.'},
            {'name': 'chinese', 'default': 'True', 'description': 'Enable Chinese font configuration.'},
            {'name': 'font_family', 'default': 'None', 'description': 'Override font family.'},
            {'name': 'figsize', 'default': 'None', 'description': 'Optional size in config when figsize parameter is omitted.'},
            {'name': 'legend', 'default': 'None', 'description': 'Legend dict with loc/outside/use_label_map.'},
            {'name': 'legend_loc', 'default': 'auto', 'description': 'Legend location.'},
            {'name': 'legend_outside', 'default': 'False', 'description': 'Place legend outside subplot.'},
            {'name': 'legend_use_label_map', 'default': 'False', 'description': 'Use mapped labels in legend.'},
            {'name': 'vlines', 'default': 'None', 'description': 'Vertical line specs.'},
            {'name': 'vertical_lines', 'default': 'None', 'description': 'Alias of vlines.'},
            {'name': 'vspaces', 'default': 'None', 'description': 'Vertical span specs.'},
            {'name': 'vertical_spaces', 'default': 'None', 'description': 'Alias of vspaces.'},
            {'name': 'hlines', 'default': 'None', 'description': 'Horizontal line specs.'},
            {'name': 'horizontal_lines', 'default': 'None', 'description': 'Alias of hlines.'},
            {'name': 'hspaces', 'default': 'None', 'description': 'Horizontal span specs.'},
            {'name': 'horizontal_spaces', 'default': 'None', 'description': 'Alias of hspaces.'},
            {'name': 'xlim', 'default': 'None', 'description': 'Global x-axis limits or ranges.'},
            {'name': 'ylim', 'default': 'None', 'description': 'Global y-axis limits or ranges.'},
            {'name': 'display_range', 'default': 'None', 'description': 'Slice or range applied before plotting.'},
            {'name': 'figure_title', 'default': 'None', 'description': 'Figure-level title.'},
            {'name': 'subplots', 'default': 'None', 'description': 'Per-subplot config list aligned with columns.'},
            {'name': 'show_vline_values', 'default': 'True', 'description': 'Annotate values on vertical lines.'},
            {'name': 'show', 'default': 'True', 'description': 'Call matplotlib show().' },
        ],
        'subplot': [
            {'name': 'title', 'description': 'Subplot title.'},
            {'name': 'subplot_title', 'description': 'Alias of title.'},
            {'name': 'legend_loc', 'description': 'Legend location override.'},
            {'name': 'legend_outside', 'description': 'Legend outside override.'},
            {'name': 'vlines', 'description': 'Subplot-specific vertical lines.'},
            {'name': 'vertical_lines', 'description': 'Alias of vlines.'},
            {'name': 'vspaces', 'description': 'Subplot-specific vertical spans.'},
            {'name': 'vertical_spaces', 'description': 'Alias of vspaces.'},
            {'name': 'hlines', 'description': 'Subplot-level horizontal lines.'},
            {'name': 'horizontal_lines', 'description': 'Alias of hlines.'},
            {'name': 'hspaces', 'description': 'Subplot-level horizontal spans.'},
            {'name': 'horizontal_spaces', 'description': 'Alias of hspaces.'},
            {'name': 'xlim', 'description': 'Subplot x-axis range.'},
            {'name': 'ylim', 'description': 'Subplot y-axis limits.'},
            {'name': 'show_vline_values', 'description': 'Override vertical line annotations.'},
            {'name': 'axes', 'description': 'Axis-level config list.'},
        ],
        'axis': [
            {'name': 'column', 'description': 'Axis column selector.'},
            {'name': 'columns', 'description': 'Alias of column.'},
            {'name': 'hlines', 'description': 'Axis-specific horizontal lines.'},
            {'name': 'horizontal_lines', 'description': 'Alias of hlines.'},
            {'name': 'hspaces', 'description': 'Axis-specific horizontal spans.'},
            {'name': 'horizontal_spaces', 'description': 'Alias of hspaces.'},
            {'name': 'ylim', 'description': 'Axis y-axis limits.'},
        ],
    },
    'distribution': {
        'function': 'plot_distribution',
        'summary': 'Distribution comparison with lightweight parameters plus config.',
        'parameters': [
            {'name': 'df', 'required': True, 'description': 'Source pandas DataFrame.'},
            {'name': 'columns', 'required': True, 'description': 'Target numeric columns.'},
            {'name': 'figsize', 'required': False, 'default': '(12, 4)', 'description': 'Figure size as (width, height).'},
            {'name': 'config', 'required': False, 'default': '{}', 'description': 'Distribution plotting config.'},
        ],
        'config': [
            {'name': 'style', 'default': 'default', 'description': 'Style preset name.'},
            {'name': 'map_dict', 'default': 'None', 'description': 'Column label mapping dictionary.'},
            {'name': 'label_map', 'default': 'None', 'description': 'Alias of map_dict.'},
            {'name': 'chinese', 'default': 'True', 'description': 'Enable Chinese font configuration.'},
            {'name': 'font_family', 'default': 'None', 'description': 'Override font family.'},
            {'name': 'figsize', 'default': 'None', 'description': 'Optional size in config when figsize parameter is omitted.'},
            {'name': 'legend', 'default': 'None', 'description': 'Legend dict with loc/outside/use_label_map.'},
            {'name': 'legend_loc', 'default': 'auto', 'description': 'Legend location.'},
            {'name': 'legend_outside', 'default': 'False', 'description': 'Place legend outside figure.'},
            {'name': 'legend_use_label_map', 'default': 'False', 'description': 'Use mapped labels in legend.'},
            {'name': 'bins', 'default': '30', 'description': 'Histogram bin count.'},
            {'name': 'alpha', 'default': '0.55', 'description': 'Histogram transparency.'},
            {'name': 'title', 'default': '分布对比图', 'description': 'Plot title.'},
            {'name': 'xlabel', 'default': '数值', 'description': 'X-axis title.'},
            {'name': 'ylabel', 'default': '频数', 'description': 'Y-axis title.'},
            {'name': 'show', 'default': 'True', 'description': 'Call matplotlib show().' },
        ],
    },
    'correlation_heatmap': {
        'function': 'plot_correlation_heatmap',
        'summary': 'Correlation heatmap with optional column selection.',
        'parameters': [
            {'name': 'df', 'required': True, 'description': 'Source pandas DataFrame.'},
            {'name': 'columns', 'required': False, 'default': 'None', 'description': 'Optional numeric columns to include.'},
            {'name': 'figsize', 'required': False, 'default': '(10, 8)', 'description': 'Figure size as (width, height).'},
            {'name': 'config', 'required': False, 'default': '{}', 'description': 'Heatmap plotting config.'},
        ],
        'config': [
            {'name': 'style', 'default': 'default', 'description': 'Style preset name.'},
            {'name': 'map_dict', 'default': 'None', 'description': 'Column label mapping dictionary.'},
            {'name': 'label_map', 'default': 'None', 'description': 'Alias of map_dict.'},
            {'name': 'chinese', 'default': 'True', 'description': 'Enable Chinese font configuration.'},
            {'name': 'font_family', 'default': 'None', 'description': 'Override font family.'},
            {'name': 'figsize', 'default': 'None', 'description': 'Optional size in config when figsize parameter is omitted.'},
            {'name': 'cmap', 'default': 'coolwarm', 'description': 'Matplotlib colormap.'},
            {'name': 'annot', 'default': 'True', 'description': 'Render correlation values inside cells.'},
            {'name': 'title', 'default': '相关性热力图', 'description': 'Plot title.'},
            {'name': 'show', 'default': 'True', 'description': 'Call matplotlib show().' },
        ],
    },
}


PLOT_CONFIG_ALIASES = {
    'plot_columns': 'columns',
    'columns': 'columns',
    'plot_distribution': 'distribution',
    'distribution': 'distribution',
    'plot_correlation_heatmap': 'correlation_heatmap',
    'correlation_heatmap': 'correlation_heatmap',
    'heatmap': 'correlation_heatmap',
}


def _normalize_plot_kind(plot_kind):
    if plot_kind not in PLOT_CONFIG_ALIASES:
        available = ', '.join(sorted(PLOT_CONFIG_SPECS))
        raise ValueError(f'Unknown plot kind: {plot_kind}. Available kinds: {available}')
    return PLOT_CONFIG_ALIASES[plot_kind]


def _format_entry(entry):
    parts = [entry['name']]
    if entry.get('required'):
        parts.append('required')
    if 'default' in entry:
        parts.append(f"default={entry['default']}")
    details = ', '.join(parts)
    return f"- {details}: {entry['description']}"


def _format_section(title, entries):
    lines = [title]
    lines.extend(_format_entry(entry) for entry in entries)
    return lines


def describe_plot_config(plot_kind: str = 'columns', format: str = 'text') -> Union[str, Dict[str, Any]]:
    """Describe the supported config keys for a public plotting API."""
    normalized_kind = _normalize_plot_kind(plot_kind)
    spec = PLOT_CONFIG_SPECS[normalized_kind]

    if format == 'dict':
        return spec
    if format != 'text':
        raise ValueError("format must be 'text' or 'dict'.")

    lines = [f"{spec['function']} config reference", spec['summary'], '']
    lines.extend(_format_section('Parameters', spec['parameters']))
    lines.append('')
    lines.extend(_format_section('Config keys', spec['config']))

    if 'subplot' in spec:
        lines.append('')
        lines.extend(_format_section('Subplot config keys', spec['subplot']))
    if 'axis' in spec:
        lines.append('')
        lines.extend(_format_section('Axis dict keys', spec['axis']))

    return '\n'.join(lines)