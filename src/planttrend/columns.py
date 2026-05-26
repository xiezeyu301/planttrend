import matplotlib.pyplot as plt

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
from .labels import get_default_label_map, merge_label_maps
from .styles import apply_plot_style


def plot_columns(
    df,
    columns,
    x='时间',
    figsize_width=20,
    figsize_height=3,
    style='default',
    label_map=None,
    chinese=True,
    font_family=None,
    legend_loc='auto',
    legend_outside=False,
    legend_use_label_map=False,
    vlines=None,
    vertical_lines=None,
    vspaces=None,
    vertical_spaces=None,
    hlines=None,
    horizontal_lines=None,
    hspaces=None,
    horizontal_spaces=None,
    xlim=None,
    ylim=None,
    subplot_options=None,
    display_range=None,
    figure_title=None,
    show_vline_values=True,
    show=True,
):
    apply_plot_style(style=style, chinese=chinese, font_family=font_family)
    df = _select_display_range(df, display_range)
    label_map = merge_label_maps(get_default_label_map(), label_map)
    _ensure_columns_exist(df, columns, x=x)
    vertical_lines = _merge_vertical_lines(vlines=vlines, vertical_lines=vertical_lines)
    vertical_spaces = _merge_vertical_spaces(vspaces=vspaces, vertical_spaces=vertical_spaces)
    horizontal_lines = _merge_horizontal_lines(hlines=hlines, horizontal_lines=horizontal_lines)
    horizontal_spaces = _merge_horizontal_spaces(hspaces=hspaces, horizontal_spaces=horizontal_spaces)
    x_limits = _normalize_x_limits(xlim)
    y_limits = _normalize_y_limits(ylim)
    resolved_vertical_lines = _resolve_vertical_line_specs(df, x, vertical_lines)
    resolved_vertical_spaces = _resolve_x_range_specs(df, x, vertical_spaces)
    resolved_x_limits = _resolve_x_range_specs(df, x, x_limits)
    subplot_options = _normalize_subplot_options(subplot_options, len(columns))

    fig, subplot_axes = _create_subplots(len(columns), figsize_width, figsize_height)
    color_pool = _get_color_pool(style)

    for subplot_index, (base_ax, subplot_spec) in enumerate(zip(subplot_axes, columns)):
        subplot_option = subplot_options[subplot_index]
        axis_specs = _normalize_subplot_spec(subplot_spec)
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
