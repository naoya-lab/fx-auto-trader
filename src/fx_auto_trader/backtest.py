"""Small, long-only moving-average crossover backtest. No broker or order connection."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Bar:
    timestamp: str
    open: float
    high: float
    low: float
    close: float


@dataclass(frozen=True)
class Trade:
    entry_time: str
    exit_time: str
    entry_price: float
    exit_price: float
    net_pips: float


def load_csv(path: str | Path) -> list[Bar]:
    """Read OHLC rows with columns: timestamp,open,high,low,close."""
    bars: list[Bar] = []
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            bar = Bar(row["timestamp"], *(float(row[k]) for k in ("open", "high", "low", "close")))
            if min(bar.open, bar.high, bar.low, bar.close) <= 0:
                raise ValueError(f"Prices must be positive: {bar.timestamp}")
            if bar.high < max(bar.open, bar.close, bar.low) or bar.low > min(bar.open, bar.close, bar.high):
                raise ValueError(f"Invalid OHLC values: {bar.timestamp}")
            bars.append(bar)
    if len(bars) < 3:
        raise ValueError("CSV must contain at least three OHLC rows.")
    return bars


def _sma(values: list[float], end: int, period: int) -> float:
    return sum(values[end - period + 1 : end + 1]) / period


def run_sma_backtest(
    bars: list[Bar],
    fast_period: int = 3,
    slow_period: int = 5,
    pip_size: float = 0.01,
    spread_pips: float = 1.0,
    slippage_pips: float = 0.2,
) -> list[Trade]:
    """Enter/exit long at the next bar's open after a close-confirmed SMA cross."""
    if fast_period < 1 or slow_period <= fast_period:
        raise ValueError("Require 1 <= fast_period < slow_period.")
    if pip_size <= 0 or spread_pips < 0 or slippage_pips < 0:
        raise ValueError("pip_size must be positive; costs cannot be negative.")
    if len(bars) <= slow_period:
        raise ValueError("Not enough bars for the selected slow_period.")

    closes = [bar.close for bar in bars]
    position: tuple[int, float] | None = None
    trades: list[Trade] = []

    # At index i, use signals from the already closed bar i-1, then fill at open i.
    for i in range(slow_period + 1, len(bars)):
        current_end, previous_end = i - 1, i - 2
        fast_now = _sma(closes, current_end, fast_period)
        slow_now = _sma(closes, current_end, slow_period)
        fast_prev = _sma(closes, previous_end, fast_period)
        slow_prev = _sma(closes, previous_end, slow_period)
        cross_up = fast_prev <= slow_prev and fast_now > slow_now
        cross_down = fast_prev >= slow_prev and fast_now < slow_now

        if position is None and cross_up:
            position = (i, bars[i].open)
        elif position is not None and cross_down:
            entry_i, entry = position
            exit_price = bars[i].open
            net = (exit_price - entry) / pip_size - spread_pips - 2 * slippage_pips
            trades.append(Trade(bars[entry_i].timestamp, bars[i].timestamp, entry, exit_price, net))
            position = None

    if position is not None:
        entry_i, entry = position
        exit_price = bars[-1].close
        net = (exit_price - entry) / pip_size - spread_pips - 2 * slippage_pips
        trades.append(Trade(bars[entry_i].timestamp, bars[-1].timestamp, entry, exit_price, net))
    return trades


def summarize(trades: list[Trade]) -> dict[str, float | int]:
    net = [trade.net_pips for trade in trades]
    wins = [p for p in net if p > 0]
    losses = [p for p in net if p < 0]
    return {
        "trade_count": len(net),
        "win_rate_pct": round(100 * len(wins) / len(net), 2) if net else 0.0,
        "net_pips": round(sum(net), 2),
        "profit_factor": round(sum(wins) / abs(sum(losses)), 2) if losses else (float("inf") if wins else 0.0),
    }
