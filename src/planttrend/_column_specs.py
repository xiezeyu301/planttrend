import numpy as np
import pandas as pd


def _normalize_subplot_spec(spec):
    if not isinstance(spec, (list, tuple)):
        return [[spec]]

    if len(spec) == 0:
        return [[]]

    if all(not isinstance(item, (list, tuple)) for item in spec):
        return [list(spec)]

    return [list(axis_spec) if isinstance(axis_spec, (list, tuple)) else [axis_spec] for axis_spec in spec]


def _normalize_vertical_lines(vertical_lines):
    if vertical_lines is None:
        return []

    if not isinstance(vertical_lines, (list, tuple)):
        vertical_lines = [vertical_lines]

    normalized = []
    for line in vertical_lines:
        if isinstance(line, dict):
            spec = dict(line)
        else:
            spec = {'x': line}

        spec['_color_specified'] = 'color' in spec

        if 'x' not in spec:
            raise ValueError('Each vertical line spec must include an x value.')

        spec.setdefault('color', '#6B7280')
        spec.setdefault('linestyle', '--')
        spec.setdefault('linewidth', 1.2)
        spec.setdefault('alpha', 0.9)
        spec.setdefault('label', '_nolegend_')

        if 'columns' in spec and 'column' not in spec:
            spec['column'] = spec.pop('columns')

        if 'column' in spec:
            if isinstance(spec['column'], str):
                spec['column'] = [spec['column']]
            else:
                spec['column'] = list(spec['column'])

        normalized.append(spec)

    return normalized


def _merge_vertical_lines(vlines=None, vertical_lines=None):
    merged = []

    for line_group in (vlines, vertical_lines):
        merged.extend(_normalize_vertical_lines(line_group))

    return merged


def _normalize_horizontal_lines(horizontal_lines):
    if horizontal_lines is None:
        return []

    if not isinstance(horizontal_lines, (list, tuple)):
        horizontal_lines = [horizontal_lines]

    normalized = []
    for line in horizontal_lines:
        if isinstance(line, dict):
            spec = dict(line)
        else:
            spec = {'y': line}

        spec['_color_specified'] = 'color' in spec

        if 'y' not in spec:
            raise ValueError('Each horizontal line spec must include a y value.')

        spec.setdefault('linestyle', '--')
        spec.setdefault('linewidth', 1.2)
        spec.setdefault('alpha', 0.9)
        spec.setdefault('label', '_nolegend_')

        if 'columns' in spec and 'column' not in spec:
            spec['column'] = spec.pop('columns')

        if 'column' in spec:
            if isinstance(spec['column'], str):
                spec['column'] = [spec['column']]
            else:
                spec['column'] = list(spec['column'])

        normalized.append(spec)

    return normalized


def _merge_horizontal_lines(hlines=None, horizontal_lines=None):
    merged = []

    for line_group in (hlines, horizontal_lines):
        merged.extend(_normalize_horizontal_lines(line_group))

    return merged


def _normalize_vertical_spaces(vertical_spaces):
    if vertical_spaces is None:
        return []

    if not isinstance(vertical_spaces, (list, tuple)):
        vertical_spaces = [vertical_spaces]

    normalized = []
    for space in vertical_spaces:
        if isinstance(space, dict):
            spec = dict(space)
        elif isinstance(space, (list, tuple)) and len(space) == 2:
            spec = {'x0': space[0], 'x1': space[1]}
        else:
            raise ValueError('Each vertical space spec must be a dict or a 2-item list/tuple.')

        if 'x' in spec and ('x0' not in spec or 'x1' not in spec):
            x_range = spec.pop('x')
            if not isinstance(x_range, (list, tuple)) or len(x_range) != 2:
                raise ValueError("Vertical space spec field 'x' must be a 2-item list/tuple.")
            spec.setdefault('x0', x_range[0])
            spec.setdefault('x1', x_range[1])

        if 'xmin' in spec and 'x0' not in spec:
            spec['x0'] = spec.pop('xmin')
        if 'xmax' in spec and 'x1' not in spec:
            spec['x1'] = spec.pop('xmax')

        if 'x0' not in spec or 'x1' not in spec:
            raise ValueError("Each vertical space spec must include x0/x1 values or an 'x' range.")

        spec.setdefault('color', '#9CA3AF')
        spec.setdefault('alpha', 0.5)
        spec.setdefault('label', '_nolegend_')

        if 'columns' in spec and 'column' not in spec:
            spec['column'] = spec.pop('columns')

        if 'column' in spec:
            if isinstance(spec['column'], str):
                spec['column'] = [spec['column']]
            else:
                spec['column'] = list(spec['column'])

        normalized.append(spec)

    return normalized


def _merge_vertical_spaces(vspaces=None, vertical_spaces=None):
    merged = []

    for space_group in (vspaces, vertical_spaces):
        merged.extend(_normalize_vertical_spaces(space_group))

    return merged


def _normalize_horizontal_spaces(horizontal_spaces):
    if horizontal_spaces is None:
        return []

    if not isinstance(horizontal_spaces, (list, tuple)):
        horizontal_spaces = [horizontal_spaces]

    normalized = []
    for space in horizontal_spaces:
        if isinstance(space, dict):
            spec = dict(space)
        elif isinstance(space, (list, tuple)) and len(space) == 2:
            spec = {'y0': space[0], 'y1': space[1]}
        else:
            raise ValueError('Each horizontal space spec must be a dict or a 2-item list/tuple.')

        if 'y' in spec and ('y0' not in spec or 'y1' not in spec):
            y_range = spec.pop('y')
            if not isinstance(y_range, (list, tuple)) or len(y_range) != 2:
                raise ValueError("Horizontal space spec field 'y' must be a 2-item list/tuple.")
            spec.setdefault('y0', y_range[0])
            spec.setdefault('y1', y_range[1])

        if 'ymin' in spec and 'y0' not in spec:
            spec['y0'] = spec.pop('ymin')
        if 'ymax' in spec and 'y1' not in spec:
            spec['y1'] = spec.pop('ymax')

        if 'y0' not in spec or 'y1' not in spec:
            raise ValueError("Each horizontal space spec must include y0/y1 values or a 'y' range.")

        spec.setdefault('color', '#9CA3AF')
        spec.setdefault('alpha', 0.5)
        spec.setdefault('label', '_nolegend_')

        if 'columns' in spec and 'column' not in spec:
            spec['column'] = spec.pop('columns')

        if 'column' in spec:
            if isinstance(spec['column'], str):
                spec['column'] = [spec['column']]
            else:
                spec['column'] = list(spec['column'])

        normalized.append(spec)

    return normalized


def _merge_horizontal_spaces(hspaces=None, horizontal_spaces=None):
    merged = []

    for space_group in (hspaces, horizontal_spaces):
        merged.extend(_normalize_horizontal_spaces(space_group))

    return merged


def _is_simple_range_pair(value):
    return (
        isinstance(value, (list, tuple))
        and len(value) == 2
        and all(not isinstance(item, (dict, list, tuple)) for item in value)
    )


def _normalize_x_limits(xlim):
    if xlim is None:
        return []

    if isinstance(xlim, dict) or _is_simple_range_pair(xlim):
        xlim = [xlim]

    normalized = []
    for limit in xlim:
        if isinstance(limit, dict):
            spec = dict(limit)
        elif _is_simple_range_pair(limit):
            spec = {'x': tuple(limit)}
        else:
            raise ValueError('Each xlim spec must be a dict or a 2-item list/tuple.')

        if 'xlim' in spec and 'x' not in spec:
            spec['x'] = spec.pop('xlim')

        if 'x' in spec and ('x0' not in spec or 'x1' not in spec):
            x_range = spec.pop('x')
            if not isinstance(x_range, (list, tuple)) or len(x_range) != 2:
                raise ValueError("xlim spec field 'x' must be a 2-item list/tuple.")
            spec.setdefault('x0', x_range[0])
            spec.setdefault('x1', x_range[1])

        if 'xmin' in spec and 'x0' not in spec:
            spec['x0'] = spec.pop('xmin')
        if 'xmax' in spec and 'x1' not in spec:
            spec['x1'] = spec.pop('xmax')

        if 'x0' not in spec or 'x1' not in spec:
            raise ValueError("Each xlim spec must include x0/x1 values or an 'x' range.")

        if 'columns' in spec and 'column' not in spec:
            spec['column'] = spec.pop('columns')

        if 'column' in spec:
            if isinstance(spec['column'], str):
                spec['column'] = [spec['column']]
            else:
                spec['column'] = list(spec['column'])

        normalized.append(spec)

    return normalized


def _normalize_y_limits(ylim):
    if ylim is None:
        return []

    if isinstance(ylim, dict) or _is_simple_range_pair(ylim):
        ylim = [ylim]

    normalized = []
    for limit in ylim:
        if isinstance(limit, dict):
            spec = dict(limit)
        elif _is_simple_range_pair(limit):
            spec = {'y': tuple(limit)}
        else:
            raise ValueError('Each ylim spec must be a dict or a 2-item list/tuple.')

        if 'ylim' in spec and 'y' not in spec:
            spec['y'] = spec.pop('ylim')

        if 'y' in spec and ('y0' not in spec or 'y1' not in spec):
            y_range = spec.pop('y')
            if not isinstance(y_range, (list, tuple)) or len(y_range) != 2:
                raise ValueError("ylim spec field 'y' must be a 2-item list/tuple.")
            spec.setdefault('y0', y_range[0])
            spec.setdefault('y1', y_range[1])

        if 'ymin' in spec and 'y0' not in spec:
            spec['y0'] = spec.pop('ymin')
        if 'ymax' in spec and 'y1' not in spec:
            spec['y1'] = spec.pop('ymax')

        if 'y0' not in spec or 'y1' not in spec:
            raise ValueError("Each ylim spec must include y0/y1 values or a 'y' range.")

        if 'columns' in spec and 'column' not in spec:
            spec['column'] = spec.pop('columns')

        if 'column' in spec:
            if isinstance(spec['column'], str):
                spec['column'] = [spec['column']]
            else:
                spec['column'] = list(spec['column'])

        normalized.append(spec)

    return normalized


def _normalize_option_columns(spec):
    normalized = dict(spec)

    if 'columns' in normalized and 'column' not in normalized:
        normalized['column'] = normalized.pop('columns')

    if 'column' in normalized:
        if isinstance(normalized['column'], str):
            normalized['column'] = [normalized['column']]
        else:
            normalized['column'] = list(normalized['column'])

    return normalized


def _normalize_subplot_options(subplot_options, expected_count):
    if subplot_options is None:
        return [{} for _ in range(expected_count)]

    if not isinstance(subplot_options, (list, tuple)):
        raise ValueError('subplot_options must be a list or tuple.')

    normalized = []
    for option in subplot_options:
        if option is None:
            normalized.append({})
        elif isinstance(option, dict):
            normalized.append(dict(option))
        else:
            raise ValueError('Each subplot option must be a dict or None.')

    if len(normalized) > expected_count:
        raise ValueError('subplot_options cannot be longer than columns.')

    normalized.extend({} for _ in range(expected_count - len(normalized)))
    return normalized


def _normalize_axis_options(axis_options):
    if axis_options is None:
        return []

    if not isinstance(axis_options, (list, tuple)):
        raise ValueError('subplot axis options must be a list or tuple.')

    normalized = []
    for option in axis_options:
        if option is None:
            normalized.append({})
        elif isinstance(option, dict):
            normalized.append(_normalize_option_columns(option))
        else:
            raise ValueError('Each axis option must be a dict or None.')

    return normalized


def _resolve_axis_option(axis_options, axis_index, cols_on_axis):
    if not axis_options:
        return {}

    resolved = {}
    target_columns = set(cols_on_axis)

    if axis_index < len(axis_options):
        positional_option = axis_options[axis_index]
        if positional_option and not positional_option.get('column'):
            resolved.update(positional_option)

    for option in axis_options:
        option_columns = option.get('column')
        if option_columns and target_columns & set(option_columns):
            resolved.update(option)

    return resolved


def _resolve_vertical_line_specs(df, x, vertical_lines):
    return [
        dict(line_spec, resolved_x=resolved_x, row=row)
        for line_spec in vertical_lines
        for resolved_x, row in [_resolve_vertical_line_target(df, x, line_spec['x'])]
    ]


def _resolve_x_range_specs(df, x, range_specs):
    return [
        dict(range_spec, resolved_x0=resolved_x0, resolved_x1=resolved_x1)
        for range_spec in range_specs
        for resolved_x0, _ in [_resolve_vertical_line_target(df, x, range_spec['x0'])]
        for resolved_x1, _ in [_resolve_vertical_line_target(df, x, range_spec['x1'])]
    ]


def _coerce_vertical_line_x(x_value, series):
    if not isinstance(series, pd.Series) or series.empty:
        return x_value

    if not pd.api.types.is_datetime64_any_dtype(series):
        return x_value

    timestamp = pd.Timestamp(x_value)
    series_tz = getattr(series.dt, 'tz', None)

    if series_tz is None:
        if timestamp.tzinfo is not None:
            return timestamp.tz_localize(None)
        return timestamp

    if timestamp.tzinfo is None:
        return timestamp.tz_localize(series_tz)
    return timestamp.tz_convert(series_tz)


def _get_row_from_integer_selector(df, selector):
    position = int(selector)
    if 0 <= position < len(df):
        return df.iloc[position]

    if selector in df.index:
        row = df.loc[selector]
        if isinstance(row, pd.DataFrame):
            return row.iloc[0]
        return row

    return None


def _get_position_from_row(df, row):
    if row is None:
        return None

    row_name = row.name
    if row_name in df.index:
        matches = np.flatnonzero(df.index.to_numpy() == row_name)
        if len(matches) > 0:
            return int(matches[0])

    return None


def _is_position_based_x(series):
    return not pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_datetime64_any_dtype(series)


def _resolve_vertical_line_target(df, x, x_value):
    x_series = df[x] if x in df.columns else None
    if not isinstance(x_series, pd.Series) or x_series.empty:
        return x_value, None

    position_based_x = _is_position_based_x(x_series)

    if isinstance(x_value, (int, np.integer)):
        should_use_row_selector = (
            pd.api.types.is_datetime64_any_dtype(x_series)
            or not pd.api.types.is_numeric_dtype(x_series)
        )
        if should_use_row_selector:
            row = _get_row_from_integer_selector(df, int(x_value))
            if row is not None:
                if position_based_x:
                    return int(x_value), row
                return _coerce_vertical_line_x(row[x], x_series), row

    resolved_x = _coerce_vertical_line_x(x_value, x_series)
    matched_rows = df.loc[x_series == resolved_x]
    if not matched_rows.empty:
        row = matched_rows.iloc[0]
        if position_based_x:
            row_position = _get_position_from_row(df, row)
            if row_position is not None:
                return row_position, row
        return resolved_x, row

    return resolved_x, None


def _select_display_range(df, display_range):
    if display_range is None:
        return df

    if isinstance(display_range, slice):
        return df.iloc[display_range]

    if not isinstance(display_range, (list, tuple)) or len(display_range) != 2:
        raise ValueError('display_range must be a slice or a 2-item list/tuple.')

    start, end = display_range

    if any(value is None for value in (start, end)):
        return df.loc[start:end]

    if isinstance(start, (int, np.integer)) and isinstance(end, (int, np.integer)):
        index_is_integer = pd.api.types.is_integer_dtype(df.index)
        if index_is_integer and start in df.index and end in df.index:
            return df.loc[start:end]
        return df.iloc[int(start):int(end)]

    return df.loc[start:end]


def _filter_line_specs_for_columns(line_specs, target_columns):
    if not line_specs:
        return []

    target_column_set = set(target_columns)
    filtered = []

    for line_spec in line_specs:
        if not line_spec.get('column'):
            filtered.append(line_spec)
            continue

        line_columns = set(line_spec.get('column', []))
        if target_column_set & line_columns:
            filtered.append(line_spec)

    return filtered