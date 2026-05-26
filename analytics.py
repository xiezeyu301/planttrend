import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ._shared import _ensure_columns_exist, _get_color_pool, _resolve_label
from .labels import get_default_label_map, merge_label_maps
from .styles import apply_plot_style


def plot_correlation_heatmap(
    df,
    columns=None,
    style='default',
    label_map=None,
    chinese=True,
    font_family=None,
    figsize=(10, 8),
    cmap='coolwarm',
    annot=True,
    show=True,
):
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
    ax.set_title('相关性热力图')

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
    df,
    columns,
    style='default',
    label_map=None,
    chinese=True,
    font_family=None,
    bins=30,
    figsize=(12, 4),
    alpha=0.55,
    legend_loc='auto',
    legend_outside=False,
    legend_use_label_map=False,
    show=True,
):
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

    ax.set_title('分布对比图')
    ax.set_xlabel('数值')
    ax.set_ylabel('频数')
    if legend_outside:
        ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1.0), borderaxespad=0.0)
        plt.tight_layout(rect=(0, 0, 0.82, 1))
    else:
        ax.legend(loc='best' if legend_loc == 'auto' else legend_loc)
        plt.tight_layout()
    if show:
        plt.show()
    return fig, ax