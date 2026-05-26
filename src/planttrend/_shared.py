import matplotlib.pyplot as plt


def _resolve_label(name, label_map=None):
    if label_map is None:
        return name
    return label_map.get(name, name)


def _flatten_columns(items):
    flattened = []
    for item in items:
        if isinstance(item, (list, tuple)):
            flattened.extend(_flatten_columns(item))
        else:
            flattened.append(item)
    return flattened


def _ensure_columns_exist(df, columns, x=None):
    required = set()
    for item in columns:
        if isinstance(item, (list, tuple)):
            required.update(_flatten_columns(item))
        else:
            required.add(item)

    if x is not None:
        required.add(x)

    missing = [column for column in required if column not in df.columns]
    if missing:
        raise KeyError(f'Missing columns: {missing}')


def _get_color_pool(style):
    if style == 'dark':
        return ['#60A5FA', '#FBBF24', '#34D399', '#F87171', '#A78BFA', '#22D3EE', '#F472B6', '#F59E0B']
    if style == 'industrial':
        return ['#8C5E34', '#2C6E6F', '#C46B48', '#6D597A', '#4C956C', '#BC4749', '#6C757D', '#355070']
    if style == 'clean':
        return ['#2563EB', '#DC2626', '#059669', '#D97706', '#7C3AED', '#0891B2', '#EA580C', '#4F46E5']
    if style == 'academic':
        return ['#1F3A5F', '#8A1538', '#1D6F5F', '#B36A00', '#5E548E', '#2A6F97', '#7F5539', '#3C6E71']
    if style == 'web':
        return ['#1570EF', '#F04438', '#12B76A', '#F79009', '#7A5AF8', '#06AED4', '#F63D68', '#6172F3']
    if style == 'elementplus':
        return ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399', '#36CFC9', '#9254DE', '#73D13D']
    if style == 'dashboard':
        return ['#175CD3', '#DC6803', '#039855', '#D92D20', '#7A5AF8', '#0BA5EC', '#DD2590', '#667085']
    return list(plt.cm.tab20.colors)
