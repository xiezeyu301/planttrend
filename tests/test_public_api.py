from pathlib import Path
import sys
import unittest

import matplotlib
import pandas as pd


matplotlib.use('Agg')

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from planttrend import PlantTrend, describe_plot_config, get_available_styles, get_default_label_map, plot_columns, plot_correlation_heatmap, plot_distribution


class PublicApiTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame(
            {
                '时间': ['2024-01-01 00:00', '2024-01-01 01:00', '2024-01-01 02:00'],
                'FT301101H.AI1.PV': [10.0, 12.5, 11.2],
                'FT301103H.AI1.PV': [8.0, 8.5, 9.1],
                'LT301101H.AI1.PV': [30.0, 32.0, 31.5],
            }
        )

    def test_available_styles_contains_default(self):
        self.assertIn('default', get_available_styles())

    def test_default_label_map_is_empty(self):
        self.assertEqual(get_default_label_map(), {})

    def test_describe_plot_config_text_contains_expected_sections(self):
        description = describe_plot_config('columns')

        self.assertIn('plot_columns config reference', description)
        self.assertIn('Config keys', description)
        self.assertIn('Subplot config keys', description)
        self.assertIn('Axis dict keys', description)
        self.assertIn('subplots', description)
        self.assertIn('show_vline_values', description)

    def test_describe_plot_config_dict_contains_expected_keys(self):
        description = describe_plot_config('distribution', format='dict')

        self.assertEqual(description['function'], 'plot_distribution')
        self.assertTrue(any(item['name'] == 'bins' for item in description['config']))

    def test_plot_columns_returns_figure_and_axes(self):
        fig, axes = plot_columns(
            self.frame,
            columns=[
                ['FT301101H.AI1.PV'],
                [['LT301101H.AI1.PV'], ['FT301103H.AI1.PV']],
            ],
            x='时间',
            figsize=(12, 4),
            config={
                'style': 'clean',
                'show': False,
                'vlines': [{'x': '2024-01-01 01:00'}],
                'subplots': [
                    {},
                    {
                        'title': '液位与流量',
                        'axes': [
                            {'ylim': [29.0, 33.0]},
                            {'ylim': [7.5, 9.5], 'hlines': [8.8]},
                        ],
                    },
                ],
            },
        )

        self.assertIsNotNone(fig)
        self.assertEqual(len(axes), 2)
        fig.clf()

    def test_plot_columns_rejects_dict_items_in_columns(self):
        with self.assertRaises(ValueError):
            plot_columns(
                self.frame,
                columns=[
                    ['FT301101H.AI1.PV'],
                    {'columns': [['LT301101H.AI1.PV']]},
                ],
                config={'show': False},
            )

    def test_planttrend_class_supports_default_config(self):
        plotter = PlantTrend(config={'style': 'clean', 'show': False, 'map_dict': {'FT301101H.AI1.PV': '流量观测值'}})

        fig, axes = plotter.plot_columns(
            self.frame,
            columns=[
                ['FT301101H.AI1.PV'],
                [['LT301101H.AI1.PV'], ['FT301103H.AI1.PV']],
            ],
            x='时间',
            figsize=(12, 4),
            config={
                'subplots': [
                    {},
                    {
                        'title': '液位与流量',
                        'axes': [
                            {'ylim': [29.0, 33.0]},
                            {'ylim': [7.5, 9.5]},
                        ],
                    },
                ],
            },
        )

        self.assertEqual(len(axes), 2)
        self.assertEqual(plotter.get_config()['style'], 'clean')
        self.assertEqual(plotter.get_config()['map_dict']['FT301101H.AI1.PV'], '流量观测值')
        fig.clf()

    def test_map_dict_alias_updates_distribution_legend(self):
        plotter = PlantTrend(
            config={
                'show': False,
                'map_dict': {'FT301101H.AI1.PV': '流量观测值'},
                'legend_use_label_map': True,
            }
        )

        fig, ax = plotter.plot_distribution(
            self.frame,
            columns=['FT301101H.AI1.PV'],
            config={},
        )

        legend = ax.get_legend()
        labels = [text.get_text() for text in legend.get_texts()] if legend is not None else []
        self.assertIn('流量观测值', labels)
        fig.clf()

    def test_plot_distribution_returns_figure_and_axis(self):
        fig, ax = plot_distribution(
            self.frame,
            columns=['FT301101H.AI1.PV', 'FT301103H.AI1.PV'],
            figsize=(10, 4),
            config={
                'style': 'clean',
                'show': False,
                'bins': 10,
            },
        )

        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        fig.clf()

    def test_plot_correlation_heatmap_returns_figure_and_axis(self):
        fig, ax = plot_correlation_heatmap(
            self.frame,
            figsize=(8, 6),
            config={
                'show': False,
                'annot': True,
            },
        )

        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        fig.clf()


if __name__ == '__main__':
    unittest.main()