import matplotlib.pyplot as plt


CHINESE_FONT_CANDIDATES = [
    'Microsoft YaHei',
    'SimHei',
    'Noto Sans CJK SC',
    'WenQuanYi Micro Hei',
    'DejaVu Sans',
]


STYLE_PRESETS = {
    'default': {
        'axes.facecolor': '#FFFFFF',
        'figure.facecolor': '#FFFFFF',
        'axes.grid': True,
        'grid.color': '#D9E2EC',
        'grid.linestyle': '--',
        'grid.alpha': 0.7,
        'axes.edgecolor': '#BCCCDC',
        'axes.labelcolor': '#243B53',
        'axes.titlecolor': '#102A43',
        'xtick.color': '#334E68',
        'ytick.color': '#334E68',
        'lines.linewidth': 1.8,
    },
    'clean': {
        'axes.facecolor': '#F8FAFC',
        'figure.facecolor': '#F8FAFC',
        'axes.grid': True,
        'grid.color': '#CBD5E1',
        'grid.linestyle': '-',
        'grid.alpha': 0.45,
        'axes.edgecolor': '#CBD5E1',
        'axes.labelcolor': '#1E293B',
        'axes.titlecolor': '#0F172A',
        'xtick.color': '#334155',
        'ytick.color': '#334155',
        'lines.linewidth': 2.0,
    },
    'industrial': {
        'axes.facecolor': '#F4F1EA',
        'figure.facecolor': '#F7F3EB',
        'axes.grid': True,
        'grid.color': '#C7BBAA',
        'grid.linestyle': ':',
        'grid.alpha': 0.6,
        'axes.edgecolor': '#A38F75',
        'axes.labelcolor': '#4A4032',
        'axes.titlecolor': '#2F2920',
        'xtick.color': '#5F5547',
        'ytick.color': '#5F5547',
        'lines.linewidth': 2.0,
    },
    'dark': {
        'axes.facecolor': '#111827',
        'figure.facecolor': '#030712',
        'axes.grid': True,
        'grid.color': '#374151',
        'grid.linestyle': '--',
        'grid.alpha': 0.5,
        'axes.edgecolor': '#4B5563',
        'axes.labelcolor': '#E5E7EB',
        'axes.titlecolor': '#F9FAFB',
        'xtick.color': '#D1D5DB',
        'ytick.color': '#D1D5DB',
        'text.color': '#F9FAFB',
        'lines.linewidth': 1.8,
    },
    'academic': {
        'axes.facecolor': '#FFFFFF',
        'figure.facecolor': '#FFFFFF',
        'axes.grid': True,
        'grid.color': '#D1D5DB',
        'grid.linestyle': ':',
        'grid.alpha': 0.55,
        'axes.edgecolor': '#6B7280',
        'axes.labelcolor': '#111827',
        'axes.titlecolor': '#111827',
        'xtick.color': '#374151',
        'ytick.color': '#374151',
        'axes.linewidth': 1.0,
        'lines.linewidth': 1.6,
        'legend.frameon': False,
        'figure.dpi': 120,
        'savefig.dpi': 300,
    },
    'web': {
        'axes.facecolor': '#FFFFFF',
        'figure.facecolor': '#F5F7FA',
        'axes.grid': True,
        'grid.color': '#E5E7EB',
        'grid.linestyle': '-',
        'grid.alpha': 0.75,
        'axes.edgecolor': '#D0D5DD',
        'axes.labelcolor': '#344054',
        'axes.titlecolor': '#101828',
        'xtick.color': '#475467',
        'ytick.color': '#475467',
        'axes.linewidth': 1.0,
        'lines.linewidth': 2.2,
        'patch.edgecolor': '#FFFFFF',
        'legend.frameon': True,
        'legend.facecolor': '#FFFFFF',
        'legend.edgecolor': '#EAECF0',
    },
    'elementplus': {
        'axes.facecolor': '#FFFFFF',
        'figure.facecolor': '#F5F7FA',
        'axes.grid': True,
        'grid.color': '#E4E7ED',
        'grid.linestyle': '--',
        'grid.alpha': 0.7,
        'axes.edgecolor': '#DCDFE6',
        'axes.labelcolor': '#303133',
        'axes.titlecolor': '#303133',
        'xtick.color': '#606266',
        'ytick.color': '#606266',
        'axes.linewidth': 1.0,
        'lines.linewidth': 2.0,
        'legend.frameon': True,
        'legend.facecolor': '#FFFFFF',
        'legend.edgecolor': '#DCDFE6',
    },
    'dashboard': {
        'axes.facecolor': '#FCFCFD',
        'figure.facecolor': '#F2F4F7',
        'axes.grid': True,
        'grid.color': '#D0D5DD',
        'grid.linestyle': '-',
        'grid.alpha': 0.55,
        'axes.edgecolor': '#D0D5DD',
        'axes.labelcolor': '#1D2939',
        'axes.titlecolor': '#101828',
        'xtick.color': '#475467',
        'ytick.color': '#475467',
        'axes.linewidth': 1.1,
        'lines.linewidth': 2.4,
        'legend.frameon': True,
        'legend.facecolor': '#FFFFFF',
        'legend.edgecolor': '#D0D5DD',
    },
}


def get_available_styles():
    return tuple(STYLE_PRESETS.keys())


def apply_plot_style(style='default', chinese=True, font_family=None):
    if style not in STYLE_PRESETS:
        available = ', '.join(get_available_styles())
        raise ValueError(f'Unknown style: {style}. Available styles: {available}')

    plt.style.use('default')
    plt.rcParams.update(STYLE_PRESETS[style])

    if chinese:
        plt.rcParams['font.sans-serif'] = [font_family] if font_family else CHINESE_FONT_CANDIDATES
        plt.rcParams['axes.unicode_minus'] = False

    return style
