import tempfile
import unittest
from pathlib import Path

from fx_auto_trader.backtest import Bar, load_csv, run_sma_backtest, summarize


class BacktestTests(unittest.TestCase):
    def test_rejects_nonfinite_csv_prices_in_each_column(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'prices.csv'
            for column in range(4):
                for value in ('nan', 'inf', '-inf'):
                    with self.subTest(column=column, value=value):
                        prices = ['100'] * 4
                        prices[column] = value
                        path.write_text('timestamp,open,high,low,close\n' +
                                        ''.join(f'day-{i},{",".join(prices)}\n' for i in range(3)))
                        with self.assertRaises(ValueError):
                            load_csv(path)

    def test_rejects_nonfinite_costs(self):
        bars = [Bar(str(i), 100, 100, 100, 100) for i in range(8)]
        for parameter in ('pip_size', 'spread_pips', 'slippage_pips', 'units'):
            for value in (float('nan'), float('inf'), -float('inf')):
                with self.subTest(parameter=parameter, value=value):
                    with self.assertRaises(ValueError):
                        run_sma_backtest(bars, **{parameter: value})

    def test_fills_after_signal_and_deducts_round_trip_costs(self):
        closes = [3, 2, 1, 4, 5, 1, 1]
        bars = [Bar(str(i), close, close, close, close) for i, close in enumerate(closes)]
        trades = run_sma_backtest(bars, fast_period=1, slow_period=2,
                                  pip_size=1, spread_pips=1, slippage_pips=.5, units=10)
        self.assertEqual(len(trades), 1)
        self.assertEqual((trades[0].entry_time, trades[0].exit_time), ('4', '6'))
        self.assertEqual(trades[0].net_pips, -6)
        self.assertEqual(summarize(trades)['net_yen'], -60)
