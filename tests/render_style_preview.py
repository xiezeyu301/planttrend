from pathlib import Path
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.use('Agg')

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from planttrend._shared import _get_color_pool
from planttrend.styles import CHINESE_FONT_CANDIDATES, apply_plot_style, get_available_styles


OUTPUT_PATH = ROOT / 'docs' / 'style-preview.png'


def _build_demo_series():
    x = np.arange(0, 24)
    load = 65 + 12 * np.sin(x / 3.4) + 4 * np.cos(x / 1.8)
    flow = 48 + 7 * np.cos(x / 4.2 + 0.5)
    target = np.full_like(x, 58, dtype=float)
    return x, load, flow, target


def render_style_preview(output_path=OUTPUT_PATH):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    style_names = get_available_styles()
    columns = 2
    rows = int(np.ceil(len(style_names) / columns))
    preview = plt.figure(figsize=(16, 4.6 * rows), facecolor='#F3F4F6')
    preview.suptitle('planttrend style preview', fontsize=18, fontweight='bold', y=0.995)

    x, load, flow, target = _build_demo_series()

    for index, style_name in enumerate(style_names, start=1):
        apply_plot_style(style=style_name, chinese=True)
        ax = preview.add_subplot(rows, columns, index)
        colors = _get_color_pool(style_name)

        ax.plot(x, load, color=colors[0], linewidth=2.8, marker='o', markersize=3.8, label='reactor temp')
        ax.plot(x, flow, color=colors[1], linewidth=2.4, linestyle='--', marker='s', markersize=3.2, label='cooling flow')
        ax.plot(x, target, color=colors[2], linewidth=1.8, linestyle=':', label='target')
        ax.axhspan(54, 60, color=colors[2], alpha=0.08)
        ax.axvline(16, color=colors[3], linestyle='-.', linewidth=1.4, alpha=0.9)
        ax.annotate(
            'batch switch',
            xy=(16, load[16]),
            xytext=(12, load[16] + 8),
            fontsize=8,
            arrowprops={'arrowstyle': '->', 'lw': 1.0, 'color': colors[3]},
        )

        ax.set_title(style_name, pad=12, fontsize=13, fontweight='bold')
        ax.set_xlabel('hour')
        ax.set_ylabel('value')
        ax.set_xlim(0, 23)
        ax.set_xticks([0, 4, 8, 12, 16, 20, 23])
        ax.legend(loc='upper left', fontsize=8)

    preview.subplots_adjust(left=0.055, right=0.985, top=0.95, bottom=0.06, hspace=0.32, wspace=0.16)
    preview.savefig(output_path, dpi=180, bbox_inches='tight')
    plt.close(preview)
    plt.rcdefaults()
    plt.rcParams['font.sans-serif'] = CHINESE_FONT_CANDIDATES
    plt.rcParams['axes.unicode_minus'] = False
    return output_path


if __name__ == '__main__':
    generated = render_style_preview()
    print(f'Generated preview: {generated}')