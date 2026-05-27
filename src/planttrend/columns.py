from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ._column_rendering import (
    _add_horizontal_lines,
    _add_horizontal_spaces,
    _add_vertical_lines,
    _add_vertical_spaces,
    _annotate_vertical_line_values,
    _apply_x_limits,
    _apply_y_limits,
    _create_axes_for_subplot,
    _create_subplots,
    _merge_legends,
    _plot_axis_columns,
)
from ._column_specs import (
    _filter_line_specs_for_columns,
    _merge_horizontal_lines,
    _merge_horizontal_spaces,
    _merge_vertical_lines,
    _merge_vertical_spaces,
    _normalize_axis_options,
    _normalize_subplot_options,
    _normalize_subplot_spec,
    _normalize_x_limits,
    _normalize_y_limits,
    _resolve_axis_option,
    _resolve_vertical_line_specs,
    _resolve_x_range_specs,
    _select_display_range,
)
from ._shared import _ensure_columns_exist, _flatten_columns, _get_color_pool
from ._types import ColumnPlotConfig, ColumnPlotLayout, FigureSize
from .labels import get_default_label_map, merge_label_maps
from .styles import apply_plot_style


def _normalize_plot_columns(columns):
    if not isinstance(columns, (list, tuple)):
        raise ValueError('columns must be a list or tuple of subplot column definitions.')

    normalized = list(columns)
    if any(isinstance(item, dict) for item in normalized):
        raise ValueError('columns must not include dict items; use config.subplots for subplot-specific options.')

    return normalized


def _normalize_plot_config(config):
    if config is None:
        return {}
    if not isinstance(config, dict):
        raise ValueError('config must be a dict or None.')

    normalized = dict(config)
    if 'map_dict' in normalized and 'label_map' not in normalized:
        normalized['label_map'] = normalized['map_dict']

    legend = normalized.pop('legend', None)
    if legend is not None:
        if not isinstance(legend, dict):
            raise ValueError('config.legend must be a dict.')
        if 'loc' in legend and 'legend_loc' not in normalized:
            normalized['legend_loc'] = legend['loc']
        if 'outside' in legend and 'legend_outside' not in normalized:
            normalized['legend_outside'] = legend['outside']
        if 'use_label_map' in legend and 'legend_use_label_map' not in normalized:
            normalized['legend_use_label_map'] = legend['use_label_map']

    if 'subplot_options' in normalized and 'subplots' not in normalized:
        normalized['subplots'] = normalized.pop('subplot_options')

    for reserved_key in ('x', 'columns'):
        if reserved_key in normalized:
            raise ValueError(f"Use the plot_columns parameter for '{reserved_key}' instead of config.")

    return normalized


def _resolve_figsize(figsize, config):
    if figsize is not None and any(key in config for key in ('figsize', 'figsize_width', 'figsize_height')):
        raise ValueError('figsize cannot be provided both as a parameter and in config.')

    if figsize is None:
        figsize = config.get('figsize')
        if figsize is None:
            return config.get('figsize_width', 20), config.get('figsize_height', 3)

    if isinstance(figsize, dict):
        if 'width' not in figsize or 'height' not in figsize:
            raise ValueError("figsize dict must include 'width' and 'height'.")
        return figsize['width'], figsize['height']

    if isinstance(figsize, (list, tuple)) and len(figsize) == 2:
        return figsize[0], figsize[1]

    raise ValueError('figsize must be a 2-item tuple/list, a dict with width/height, or None.')


def plot_columns(
    df: pd.DataFrame,
    columns: ColumnPlotLayout,
    x: str = '时间',
    figsize: Optional[FigureSize] = None,
    config: Optional[ColumnPlotConfig] = None,
) -> Tuple[Figure, List[Axes]]:
    """Plot trend subplots with optional multi-axis layout.

    ``columns`` defines the subplot layout and ``config`` carries global and
    subplot-local rendering options. Call ``describe_plot_config('columns')`` for
    the full supported config structure.
    """
    subplot_definitions = _normalize_plot_columns(columns)
    config = _normalize_plot_config(config)
    figsize_width, figsize_height = _resolve_figsize(figsize, config)

    style = config.get('style', 'default')
    label_map = config.get('label_map')
    chinese = config.get('chinese', True)
    font_family = config.get('font_family')
    legend_loc = config.get('legend_loc', 'auto')
    legend_outside = config.get('legend_outside', False)
    legend_use_label_map = config.get('legend_use_label_map', False)
    vlines = config.get('vlines')
    vertical_lines = config.get('vertical_lines')
    vspaces = config.get('vspaces')
    vertical_spaces = config.get('vertical_spaces')
    hlines = config.get('hlines')
    horizontal_lines = config.get('horizontal_lines')
    hspaces = config.get('hspaces')
    horizontal_spaces = config.get('horizontal_spaces')
    xlim = config.get('xlim')
    ylim = config.get('ylim')
    display_range = config.get('display_range')
    figure_title = config.get('figure_title')
    show_vline_values = config.get('show_vline_values', True)
    show = config.get('show', True)

    apply_plot_style(style=style, chinese=chinese, font_family=font_family)
    df = _select_display_range(df, display_range)
    label_map = merge_label_maps(get_default_label_map(), label_map)
    _ensure_columns_exist(df, subplot_definitions, x=x)
    vertical_lines = _merge_vertical_lines(vlines=vlines, vertical_lines=vertical_lines)
    vertical_spaces = _merge_vertical_spaces(vspaces=vspaces, vertical_spaces=vertical_spaces)
    horizontal_lines = _merge_horizontal_lines(hlines=hlines, horizontal_lines=horizontal_lines)
    horizontal_spaces = _merge_horizontal_spaces(hspaces=hspaces, horizontal_spaces=horizontal_spaces)
    x_limits = _normalize_x_limits(xlim)
    y_limits = _normalize_y_limits(ylim)
    resolved_vertical_lines = _resolve_vertical_line_specs(df, x, vertical_lines)
    resolved_vertical_spaces = _resolve_x_range_specs(df, x, vertical_spaces)
    resolved_x_limits = _resolve_x_range_specs(df, x, x_limits)
    subplot_options = _normalize_subplot_options(config.get('subplots'), len(subplot_definitions))

    fig, subplot_axes = _create_subplots(len(subplot_definitions), figsize_width, figsize_height)
    color_pool = _get_color_pool(style)

    for base_ax, subplot_definition, subplot_option in zip(subplot_axes, subplot_definitions, subplot_options):
        axis_specs = _normalize_subplot_spec(subplot_definition)
        subplot_columns = _flatten_columns(axis_specs)
        axes_list = _create_axes_for_subplot(base_ax, len(axis_specs))
        axis_data_lines = []
        title_parts = []
        color_idx = 0

        subplot_axis_options = _normalize_axis_options(subplot_option.get('axes'))
        subplot_vertical_lines = _resolve_vertical_line_specs(
            df,
            x,
            _merge_vertical_lines(
                vlines=subplot_option.get('vlines'),
                vertical_lines=subplot_option.get('vertical_lines'),
            ),
        )
        subplot_vertical_spaces = _resolve_x_range_specs(
            df,
            x,
            _merge_vertical_spaces(
                vspaces=subplot_option.get('vspaces'),
                vertical_spaces=subplot_option.get('vertical_spaces'),
            ),
        )
        subplot_x_limits = _resolve_x_range_specs(df, x, _normalize_x_limits(subplot_option.get('xlim')))
        subplot_horizontal_lines = _merge_horizontal_lines(
            hlines=subplot_option.get('hlines'),
            horizontal_lines=subplot_option.get('horizontal_lines'),
        )
        subplot_horizontal_spaces = _merge_horizontal_spaces(
            hspaces=subplot_option.get('hspaces'),
            horizontal_spaces=subplot_option.get('horizontal_spaces'),
        )
        subplot_y_limits = _normalize_y_limits(subplot_option.get('ylim'))

        for index, (ax, cols_on_axis) in enumerate(zip(axes_list, axis_specs)):
            label, color_idx, plotted_lines = _plot_axis_columns(
                df,
                ax,
                cols_on_axis,
                x,
                color_pool,
                color_idx,
                label_map,
                legend_use_label_map,
            )
            axis_data_lines.append(plotted_lines)
            title_parts.append(label)

            axis_option = _resolve_axis_option(subplot_axis_options, index, cols_on_axis)
            axis_horizontal_spaces = _filter_line_specs_for_columns(horizontal_spaces, cols_on_axis)
            axis_horizontal_spaces.extend(
                _filter_line_specs_for_columns(subplot_horizontal_spaces, cols_on_axis)
            )
            axis_horizontal_spaces.extend(
                _filter_line_specs_for_columns(
                    _merge_horizontal_spaces(
                        hspaces=axis_option.get('hspaces'),
                        horizontal_spaces=axis_option.get('horizontal_spaces'),
                    ),
                    cols_on_axis,
                )
            )
            _add_horizontal_spaces(ax, axis_horizontal_spaces)

            axis_horizontal_lines = _filter_line_specs_for_columns(horizontal_lines, cols_on_axis)
            axis_horizontal_lines.extend(
                _filter_line_specs_for_columns(subplot_horizontal_lines, cols_on_axis)
            )
            axis_horizontal_lines.extend(
                _filter_line_specs_for_columns(
                    _merge_horizontal_lines(
                        hlines=axis_option.get('hlines'),
                        horizontal_lines=axis_option.get('horizontal_lines'),
                    ),
                    cols_on_axis,
                )
            )
            _add_horizontal_lines(ax, axis_horizontal_lines)

            axis_y_limits = _filter_line_specs_for_columns(y_limits, cols_on_axis)
            axis_y_limits.extend(_filter_line_specs_for_columns(subplot_y_limits, cols_on_axis))
            axis_y_limits.extend(
                _filter_line_specs_for_columns(_normalize_y_limits(axis_option.get('ylim')), cols_on_axis)
            )
            _apply_y_limits(ax, axis_y_limits)

            if index > 0:
                ax.grid(False)

        combined_vertical_spaces = _filter_line_specs_for_columns(resolved_vertical_spaces, subplot_columns)
        combined_vertical_spaces.extend(
            _filter_line_specs_for_columns(subplot_vertical_spaces, subplot_columns)
        )
        _add_vertical_spaces(base_ax, combined_vertical_spaces)

        combined_x_limits = _filter_line_specs_for_columns(resolved_x_limits, subplot_columns)
        combined_x_limits.extend(_filter_line_specs_for_columns(subplot_x_limits, subplot_columns))
        _apply_x_limits(base_ax, combined_x_limits)

        combined_vertical_lines = _filter_line_specs_for_columns(resolved_vertical_lines, subplot_columns)
        combined_vertical_lines.extend(
            _filter_line_specs_for_columns(subplot_vertical_lines, subplot_columns)
        )
        subplot_show_vline_values = subplot_option.get('show_vline_values', show_vline_values)
        if subplot_show_vline_values:
            _annotate_vertical_line_values(axes_list, axis_specs, axis_data_lines, combined_vertical_lines)
        _add_vertical_lines(base_ax, combined_vertical_lines)
        base_ax.set_title(subplot_option.get('title') or subplot_option.get('subplot_title') or ' | '.join(title_parts))
        _merge_legends(
            base_ax,
            axes_list,
            legend_loc=subplot_option.get('legend_loc', legend_loc),
            legend_outside=subplot_option.get('legend_outside', legend_outside),
        )

    if figure_title:
        fig.suptitle(figure_title)

    if legend_outside and figure_title:
        plt.tight_layout(rect=(0, 0, 0.82, 0.96))
    elif legend_outside:
        plt.tight_layout(rect=(0, 0, 0.82, 1))
    elif figure_title:
        plt.tight_layout(rect=(0, 0, 1, 0.96))
    else:
        plt.tight_layout()

    if show:
        plt.show()
    return fig, subplot_axes
