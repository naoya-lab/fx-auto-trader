import unittest

from fx_auto_trader.backtest import Bar, run_sma_backtest, summarize


class BacktestTests(unittest.TestCase):
    def test_backtest_returns_trades_and_summary(self):
        closes = [10, 10, 10, 9, 8, 7, 8, 9, 10, 11, 10, 9]
        bars = [Bar(str(i), p, p + 0.1, p - 0.1, p) for i, p in enumerate(closes)]
        trades = run_sma_backtest(bars, fast_period=2, slow_period=3, pip_size=1, spread_pips=0, slippage_pips=0)
        self.assertTrue(trades)
        self.assertEqual(summarize(trades)["trade_count"], len(trades))

    def test_rejects_invalid_periods(self):
        bars = [Bar(str(i), 10, 11, 9, 10) for i in range(8)]
        with self.assertRaises(ValueError):
            run_sma_backtest(bars, fast_period=3, slow_period=3)


if __name__ == "__main__":
    unittest.main()
