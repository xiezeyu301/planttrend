from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .analytics import plot_correlation_heatmap, plot_distribution
from .columns import plot_columns
from .config_info import describe_plot_config
from ._types import ColumnPlotConfig, ColumnPlotLayout, CorrelationHeatmapConfig, DistributionPlotConfig, FigureSize


ConfigDict = Dict[str, Any]


def _merge_configs(base_config: Optional[ConfigDict], override_config: Optional[ConfigDict]) -> ConfigDict:
    merged = dict(base_config or {})

    for key, value in (override_config or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_configs(merged[key], value)
        else:
            merged[key] = value

    return merged


class PlantTrend:
    """Stateful plotting client for reusing shared defaults across charts."""

    def __init__(self, config: Optional[ConfigDict] = None) -> None:
        """Create a plotter with an optional default config dictionary."""
        self._config = _merge_configs({}, config)

    def get_config(self) -> ConfigDict:
        """Return a copy of the current default config."""
        return _merge_configs({}, self._config)

    def update_config(self, config: Optional[ConfigDict] = None, **kwargs: Any) -> 'PlantTrend':
        """Merge config values into the current defaults and return ``self``."""
        incoming = _merge_configs(config, kwargs)
        self._config = _merge_configs(self._config, incoming)
        return self

    def reset_config(self) -> 'PlantTrend':
        """Clear all stored defaults and return ``self``."""
        self._config = {}
        return self

    def clone(self, config: Optional[ConfigDict] = None, **kwargs: Any) -> 'PlantTrend':
        """Create a new ``PlantTrend`` with the current defaults plus overrides."""
        incoming = _merge_configs(config, kwargs)
        return PlantTrend(config=_merge_configs(self._config, incoming))

    def describe_config(self, plot_kind: str = 'columns', format: str = 'text') -> Union[str, Dict[str, Any]]:
        """Return the supported config reference for a plot kind."""
        return describe_plot_config(plot_kind=plot_kind, format=format)

    def plot_columns(
        self,
        df: pd.DataFrame,
        columns: ColumnPlotLayout,
        x: str = '时间',
        figsize: Optional[FigureSize] = None,
        config: Optional[ColumnPlotConfig] = None,
    ) -> Tuple[Figure, List[Axes]]:
        """Plot trend columns using the stored defaults merged with call-local config."""
        merged_config = _merge_configs(self._config, config)
        return plot_columns(df, columns=columns, x=x, figsize=figsize, config=merged_config)

    def plot_distribution(
        self,
        df: pd.DataFrame,
        columns: Sequence[str],
        figsize: Optional[FigureSize] = None,
        config: Optional[DistributionPlotConfig] = None,
    ) -> Tuple[Figure, Axes]:
        """Plot distributions using the stored defaults merged with call-local config."""
        merged_config = _merge_configs(self._config, config)
        return plot_distribution(df, columns=columns, figsize=figsize, config=merged_config)

    def plot_correlation_heatmap(
        self,
        df: pd.DataFrame,
        columns: Optional[Sequence[str]] = None,
        figsize: Optional[FigureSize] = None,
        config: Optional[CorrelationHeatmapConfig] = None,
    ) -> Tuple[Figure, Axes]:
        """Plot a correlation heatmap using the stored defaults plus call-local config."""
        merged_config = _merge_configs(self._config, config)
        return plot_correlation_heatmap(df, columns=columns, figsize=figsize, config=merged_config)