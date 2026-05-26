import matplotlib.pyplot as plt
import pandas as pd

from ._shared import _resolve_label


def _create_subplots(count, figsize_width, figsize_height):
    fig, subplot_axes = plt.subplots(count, 1, figsize=(figsize_width, figsize_height * count))
    return fig, [subplot_axes] if count == 1 else subplot_axes


def _create_axes_for_subplot(base_ax, axis_count):
    axes_list = [base_ax]
    for index in range(1, axis_count):
        axis = base_ax.twinx()
        if index >= 2:
            axis.spines['right'].set_position(('outward', 60 * (index - 1)))
        axes_list.append(axis)
    return axes_list


def _plot_axis_columns(df, ax, cols_on_axis, x, color_pool, color_idx, label_map, legend_use_label_map):
    label = ' / '.join(_resolve_label(col, label_map) for col in cols_on_axis)
    axis_colors = []
    plotted_lines = []

    for col in cols_on_axis:
        color = color_pool[color_idx % len(color_pool)]
        color_idx += 1
        axis_colors.append(color)

        legend_label = _resolve_label(col, label_map) if legend_use_label_map else col

        df.plot(x=x, y=col, ax=ax, label=legend_label, color=color)
        plotted_lines.append(ax.lines[-1])

    main_color = axis_colors[0] if axis_colors else None
    ax.set_ylabel(label, color=main_color)
    ax.tick_params(axis='y', colors=main_color)
    return label, color_idx, plotted_lines


def _merge_legends(base_ax, axes_list, legend_loc, legend_outside):
    handles, labels = [], []

    for ax in axes_list:
        h, l = ax.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)

        legend = ax.get_legend()
        if legend is not None:
            legend.remove()

    if handles:
        if legend_outside:
            base_ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(1.01, 1.0), borderaxespad=0.0)
        elif legend_loc == 'auto':
            base_ax.legend(handles, labels)
        else:
            base_ax.legend(handles, labels, loc=legend_loc)


def _format_vline_value(value):
    numeric_value = pd.to_numeric(pd.Series([value]), errors='coerce').iloc[0]
    if pd.notna(numeric_value):
        return f'{float(numeric_value):.2f}'.rstrip('0').rstrip('.')
    return str(value)


def _annotate_vertical_line_values(axes_list, axis_specs, axis_data_lines, resolved_vertical_lines):
    if not resolved_vertical_lines:
        return

    for ax, cols_on_axis, data_lines in zip(axes_list, axis_specs, axis_data_lines):
        for line_spec in resolved_vertical_lines:
            row = line_spec['row']
            if row is None:
                continue

            for index, (column, line) in enumerate(zip(cols_on_axis, data_lines)):
                value = row.get(column)
                if pd.isna(value):
                    continue

                y_value = pd.to_numeric(pd.Series([value]), errors='coerce').iloc[0]
                if pd.isna(y_value):
                    continue

                line_color = line.get_color()
                annotation_color = line_spec['color'] if line_spec.get('_color_specified') else line_color
                ax.scatter([line_spec['resolved_x']], [y_value], color=line_color, s=18, zorder=5)
                ax.annotate(
                    _format_vline_value(y_value),
                    xy=(line_spec['resolved_x'], y_value),
                    xytext=(6, 8 + index * 12),
                    textcoords='offset points',
                    color=annotation_color,
                    fontsize=8,
                    bbox={
                        'boxstyle': 'round,pad=0.2',
                        'facecolor': '#FFFFFF',
                        'edgecolor': annotation_color,
                        'alpha': 0.75,
                    },
                )


def _add_vertical_lines(base_ax, resolved_vertical_lines):
    if not resolved_vertical_lines:
        return []

    for line_spec in resolved_vertical_lines:
        base_ax.axvline(
            x=line_spec['resolved_x'],
            color=line_spec['color'],
            linestyle=line_spec['linestyle'],
            linewidth=line_spec['linewidth'],
            alpha=line_spec['alpha'],
            label=line_spec['label'],
        )

    return resolved_vertical_lines


def _add_horizontal_lines(ax, resolved_horizontal_lines):
    if not resolved_horizontal_lines:
        return []

    for line_spec in resolved_horizontal_lines:
        line_kwargs = {
            'y': line_spec['y'],
            'linestyle': line_spec['linestyle'],
            'linewidth': line_spec['linewidth'],
            'alpha': line_spec['alpha'],
            'label': line_spec['label'],
        }
        if line_spec.get('_color_specified'):
            line_kwargs['color'] = line_spec['color']
        else:
            line_kwargs['color'] = ax._get_lines.get_next_color()
        ax.axhline(**line_kwargs)

    return resolved_horizontal_lines


def _add_vertical_spaces(base_ax, resolved_vertical_spaces):
    if not resolved_vertical_spaces:
        return []

    for space_spec in resolved_vertical_spaces:
        base_ax.axvspan(
            xmin=space_spec['resolved_x0'],
            xmax=space_spec['resolved_x1'],
            color=space_spec['color'],
            alpha=space_spec['alpha'],
            label=space_spec['label'],
        )

    return resolved_vertical_spaces


def _add_horizontal_spaces(ax, resolved_horizontal_spaces):
    if not resolved_horizontal_spaces:
        return []

    for space_spec in resolved_horizontal_spaces:
        ax.axhspan(
            ymin=space_spec['y0'],
            ymax=space_spec['y1'],
            color=space_spec['color'],
            alpha=space_spec['alpha'],
            label=space_spec['label'],
        )

    return resolved_horizontal_spaces


def _apply_x_limits(base_ax, resolved_x_limits):
    if not resolved_x_limits:
        return

    for limit_spec in resolved_x_limits:
        base_ax.set_xlim(limit_spec['resolved_x0'], limit_spec['resolved_x1'])


def _apply_y_limits(ax, resolved_y_limits):
    if not resolved_y_limits:
        return

    for limit_spec in resolved_y_limits:
        ax.set_ylim(limit_spec['y0'], limit_spec['y1'])