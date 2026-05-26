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

from planttrend import get_available_styles, plot_columns, plot_correlation_heatmap, plot_distribution


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

    def test_plot_columns_returns_figure_and_axes(self):
        fig, axes = plot_columns(
            self.frame,
            columns=[['FT301101H.AI1.PV'], ['LT301101H.AI1.PV', 'FT301103H.AI1.PV']],
            x='时间',
            show=False,
        )

        self.assertIsNotNone(fig)
        self.assertEqual(len(axes), 2)
        fig.clf()

    def test_plot_distribution_returns_figure_and_axis(self):
        fig, ax = plot_distribution(
            self.frame,
            columns=['FT301101H.AI1.PV', 'FT301103H.AI1.PV'],
            show=False,
        )

        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        fig.clf()

    def test_plot_correlation_heatmap_returns_figure_and_axis(self):
        fig, ax = plot_correlation_heatmap(self.frame, show=False)

        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        fig.clf()


if __name__ == '__main__':
    unittest.main()