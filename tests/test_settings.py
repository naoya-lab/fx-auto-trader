import unittest

from fx_auto_trader.settings import get_mode


class SettingsTests(unittest.TestCase):
    def test_defaults_to_backtest(self):
        self.assertEqual(get_mode({}), "backtest")

    def test_accepts_backtest_case_insensitively(self):
        self.assertEqual(get_mode({"FXBOT_MODE": " BACKTEST "}), "backtest")

    def test_rejects_demo_until_broker_setup_is_reviewed(self):
        with self.assertRaises(ValueError):
            get_mode({"FXBOT_MODE": "demo"})

    def test_rejects_live_mode(self):
        with self.assertRaises(ValueError):
            get_mode({"FXBOT_MODE": "live"})


if __name__ == "__main__":
    unittest.main()
