from typing import Any, Mapping, Sequence, Tuple, TypedDict, Union, Literal


StyleName = Literal[
    'default',
    'clean',
    'industrial',
    'dark',
    'academic',
    'web',
    'elementplus',
    'dashboard',
]

LabelMap = Mapping[str, str]
FigureSizeTuple = Tuple[float, float]


class FigureSizeDict(TypedDict):
    width: float
    height: float


FigureSize = Union[FigureSizeTuple, FigureSizeDict]


class LegendConfig(TypedDict, total=False):
    loc: str
    outside: bool
    use_label_map: bool


class AxisConfig(TypedDict, total=False):
    column: Union[str, Sequence[str]]
    columns: Union[str, Sequence[str]]
    hlines: Any
    horizontal_lines: Any
    hspaces: Any
    horizontal_spaces: Any
    ylim: Any


class SubplotConfig(TypedDict, total=False):
    title: str
    subplot_title: str
    legend_loc: str
    legend_outside: bool
    vlines: Any
    vertical_lines: Any
    vspaces: Any
    vertical_spaces: Any
    hlines: Any
    horizontal_lines: Any
    hspaces: Any
    horizontal_spaces: Any
    xlim: Any
    ylim: Any
    show_vline_values: bool
    axes: Sequence[AxisConfig]


class ColumnPlotConfig(TypedDict, total=False):
    style: StyleName
    map_dict: LabelMap
    label_map: LabelMap
    chinese: bool
    font_family: str
    figsize: FigureSize
    legend: LegendConfig
    legend_loc: str
    legend_outside: bool
    legend_use_label_map: bool
    vlines: Any
    vertical_lines: Any
    vspaces: Any
    vertical_spaces: Any
    hlines: Any
    horizontal_lines: Any
    hspaces: Any
    horizontal_spaces: Any
    xlim: Any
    ylim: Any
    display_range: Any
    figure_title: str
    subplots: Sequence[SubplotConfig]
    show_vline_values: bool
    show: bool


class DistributionPlotConfig(TypedDict, total=False):
    style: StyleName
    map_dict: LabelMap
    label_map: LabelMap
    chinese: bool
    font_family: str
    figsize: FigureSize
    legend: LegendConfig
    legend_loc: str
    legend_outside: bool
    legend_use_label_map: bool
    bins: int
    alpha: float
    title: str
    xlabel: str
    ylabel: str
    show: bool


class CorrelationHeatmapConfig(TypedDict, total=False):
    style: StyleName
    map_dict: LabelMap
    label_map: LabelMap
    chinese: bool
    font_family: str
    figsize: FigureSize
    cmap: str
    annot: bool
    title: str
    show: bool


ColumnSubplot = Union[Sequence[str], Sequence[Sequence[str]]]
ColumnPlotLayout = Sequence[ColumnSubplot]