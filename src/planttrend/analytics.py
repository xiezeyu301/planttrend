from typing import Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ._shared import _ensure_columns_exist, _get_color_pool, _resolve_label
from ._types import CorrelationHeatmapConfig, DistributionPlotConfig, FigureSize
from .labels import get_default_label_map, merge_label_maps
from .styles import apply_plot_style


def _normalize_analytics_config(config):
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

    if 'columns' in normalized:
        raise ValueError("Use the function parameter for 'columns' instead of config.")

    return normalized


def _resolve_figsize(figsize, config, default):
    if figsize is not None and any(key in config for key in ('figsize', 'figsize_width', 'figsize_height')):
        raise ValueError('figsize cannot be provided both as a parameter and in config.')

    if figsize is None:
        figsize = config.get('figsize')
        if figsize is None:
            return config.get('figsize_width', default[0]), config.get('figsize_height', default[1])

    if isinstance(figsize, dict):
        if 'width' not in figsize or 'height' not in figsize:
            raise ValueError("figsize dict must include 'width' and 'height'.")
        return figsize['width'], figsize['height']

    if isinstance(figsize, (list, tuple)) and len(figsize) == 2:
        return figsize[0], figsize[1]

    raise ValueError('figsize must be a 2-item tuple/list, a dict with width/height, or None.')


def plot_correlation_heatmap(
    df: pd.DataFrame,
    columns: Optional[Sequence[str]] = None,
    figsize: Optional[FigureSize] = None,
    config: Optional[CorrelationHeatmapConfig] = None,
) -> Tuple[Figure, Axes]:
    """Plot a numeric-column correlation heatmap.

    Use ``config`` for visual options such as ``style``, ``cmap``, ``annot`` and
    ``title``. Call ``describe_plot_config('correlation_heatmap')`` for the full
    supported config reference.
    """
    config = _normalize_analytics_config(config)
    figsize = _resolve_figsize(figsize, config, default=(10, 8))
    style = config.get('style', 'default')
    label_map = config.get('label_map')
    chinese = config.get('chinese', True)
    font_family = config.get('font_family')
    cmap = config.get('cmap', 'coolwarm')
    annot = config.get('annot', True)
    show = config.get('show', True)
    title = config.get('title', '相关性热力图')

    apply_plot_style(style=style, chinese=chinese, font_family=font_family)
    label_map = merge_label_maps(get_default_label_map(), label_map)

    target_df = df.select_dtypes(include=[np.number]) if columns is None else df[columns]
    corr = target_df.corr().to_numpy()
    display_columns = [_resolve_label(col, label_map) for col in target_df.columns]

    fig, ax = plt.subplots(figsize=figsize)
    image = ax.imshow(corr, cmap=cmap, vmin=-1, vmax=1, aspect='auto')
    ax.set_xticks(np.arange(len(display_columns)))
    ax.set_yticks(np.arange(len(display_columns)))
    ax.set_xticklabels(display_columns, rotation=45, ha='right')
    ax.set_yticklabels(display_columns)
    ax.set_title(title)

    if annot:
        for row_index in range(corr.shape[0]):
            for col_index in range(corr.shape[1]):
                value = corr[row_index, col_index]
                text_color = '#111827' if abs(value) < 0.55 else '#F9FAFB'
                ax.text(col_index, row_index, f'{value:.2f}', ha='center', va='center', color=text_color, fontsize=9)

    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    if show:
        plt.show()
    return fig, ax


def plot_distribution(
    df: pd.DataFrame,
    columns: Sequence[str],
    figsize: Optional[FigureSize] = None,
    config: Optional[DistributionPlotConfig] = None,
) -> Tuple[Figure, Axes]:
    """Plot overlaid histograms for one or more numeric columns.

    Use ``config`` for histogram, legend and style options such as ``bins``,
    ``alpha``, ``legend_loc`` and ``style``. Call
    ``describe_plot_config('distribution')`` for the full config reference.
    """
    config = _normalize_analytics_config(config)
    figsize = _resolve_figsize(figsize, config, default=(12, 4))
    style = config.get('style', 'default')
    label_map = config.get('label_map')
    chinese = config.get('chinese', True)
    font_family = config.get('font_family')
    bins = config.get('bins', 30)
    alpha = config.get('alpha', 0.55)
    legend_loc = config.get('legend_loc', 'auto')
    legend_outside = config.get('legend_outside', False)
    legend_use_label_map = config.get('legend_use_label_map', False)
    show = config.get('show', True)
    title = config.get('title', '分布对比图')
    xlabel = config.get('xlabel', '数值')
    ylabel = config.get('ylabel', '频数')

    apply_plot_style(style=style, chinese=chinese, font_family=font_family)
    label_map = merge_label_maps(get_default_label_map(), label_map)

    if isinstance(columns, str):
        columns = [columns]

    _ensure_columns_exist(df, columns)
    fig, ax = plt.subplots(figsize=figsize)
    color_pool = _get_color_pool(style)

    for index, column in enumerate(columns):
        series = pd.to_numeric(df[column], errors='coerce').dropna()
        if series.empty:
            continue

        legend_label = _resolve_label(column, label_map) if legend_use_label_map else column

        ax.hist(
            series.to_numpy(),
            bins=bins,
            alpha=alpha,
            color=color_pool[index % len(color_pool)],
            label=legend_label,
            density=False,
        )

        mean_value = float(np.mean(series.to_numpy()))
        ax.axvline(mean_value, color=color_pool[index % len(color_pool)], linestyle='--', linewidth=1.5)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend_outside:
        ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1.0), borderaxespad=0.0)
        plt.tight_layout(rect=(0, 0, 0.82, 1))
    else:
        ax.legend(loc='best' if legend_loc == 'auto' else legend_loc)
        plt.tight_layout()
    if show:
        plt.show()
    return fig, ax
