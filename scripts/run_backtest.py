"""Run the starter SMA backtest against an OHLC CSV file."""
import argparse

from fx_auto_trader.backtest import load_csv, run_sma_backtest, summarize


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", help="CSV with timestamp,open,high,low,close columns")
    parser.add_argument("--fast", type=int, default=3, help="fast SMA period (default: 3)")
    parser.add_argument("--slow", type=int, default=5, help="slow SMA period (default: 5)")
    parser.add_argument("--spread", type=float, default=1.0, help="spread cost in pips (default: 1)")
    parser.add_argument("--slippage", type=float, default=0.2, help="slippage per side in pips (default: 0.2)")
    parser.add_argument("--units", type=int, default=10_000, help="trade size in currency units (default: 10000)")
    args = parser.parse_args()

    bars = load_csv(args.csv_file)
    trades = run_sma_backtest(
        bars,
        fast_period=args.fast,
        slow_period=args.slow,
        spread_pips=args.spread,
        slippage_pips=args.slippage,
        units=args.units,
    )
    print("Summary:", summarize(trades))
    print("Trades:")
    for trade in trades:
        print(
            f"{trade.entry_time} -> {trade.exit_time}: "
            f"{trade.entry_price:.3f} -> {trade.exit_price:.3f}; "
            f"net {trade.net_pips:.1f} pips / ¥{trade.net_yen:,.0f}"
        )


if __name__ == "__main__":
    main()
