import pandas as pd


DEFAULT_LABEL_MAP = {
    'LT301101H.AI1.PV': '冷冻锅H液位显示',
    'TE301101H.AI1.PV': '冷冻锅H温度显示',
    'KV_301101H_AI.AI1.PV': '循环水进冷冻锅H阀门反馈',
    'KV_301103H_AI.AI1.PV': '冷冻水进冷冻锅H阀门A反馈',
    'KV_301104H_AI.AI1.PV': '冷冻水进冷冻锅H阀门B反馈',
    'A301101H_II.AI1.PV': '结晶罐H搅拌电流显示',
    'TE301101.AI1.PV': '冷却水进冷冻锅总管温度',
    'TE301101_1.AI1.PV': '冷却水出冷冻锅总管温度',
    'KIC_301101H.PID1.SV': '8#冷冻锅冷却水流量设定值',
    'FT301101H.AI1.PV': '8#冷冻锅冷却水流量观测值',
    'KIC_301103H.PID1.SV': '8#冷冻锅冷冻水流量1设定值',
    'FT301103H.AI1.PV': '8#冷冻锅冷冻水流量1',
    'KIC_301104H.PID1.SV': '8#冷冻锅冷冻水流量2设定值',
    'FT301104H.AI1.PV': '8#冷冻锅冷冻水流量2',
}


def load_label_map(csv_path, key_col='位号', value_col='注释', encoding='utf-8'):
    comment_df = pd.read_csv(csv_path, encoding=encoding)
    return dict(
        zip(
            comment_df[key_col].astype(str).str.strip(),
            comment_df[value_col].astype(str).str.strip(),
        )
    )


def get_default_label_map():
    return dict(DEFAULT_LABEL_MAP)


def merge_label_maps(*maps):
    merged = {}
    for mapping in maps:
        if mapping:
            merged.update(mapping)
    return merged
