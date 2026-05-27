from typing import Dict, Mapping

import pandas as pd


DEFAULT_LABEL_MAP = {}


def load_label_map(csv_path: str, key_col: str = '位号', value_col: str = '注释', encoding: str = 'utf-8') -> Dict[str, str]:
    """Load a label map from a CSV file."""
    comment_df = pd.read_csv(csv_path, encoding=encoding)
    return dict(
        zip(
            comment_df[key_col].astype(str).str.strip(),
            comment_df[value_col].astype(str).str.strip(),
        )
    )


def get_default_label_map() -> Dict[str, str]:
    """Return a copy of the built-in label map."""
    return dict(DEFAULT_LABEL_MAP)


def merge_label_maps(*maps: Mapping[str, str]) -> Dict[str, str]:
    """Merge multiple label maps from left to right."""
    merged: Dict[str, str] = {}
    for mapping in maps:
        if mapping:
            merged.update(mapping)
    return merged
