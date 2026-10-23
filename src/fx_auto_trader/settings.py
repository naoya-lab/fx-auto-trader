"""Safe runtime settings for the initial project scaffold."""

from collections.abc import Mapping
import os

_ALLOWED_MODES = frozenset({"backtest"})


def get_mode(env: Mapping[str, str] | None = None) -> str:
    """Return the configured mode; the scaffold intentionally allows backtest only."""
    source = os.environ if env is None else env
    mode = source.get("FXBOT_MODE", "backtest").strip().lower()

    if mode not in _ALLOWED_MODES:
        raise ValueError(
            f"Unsupported FXBOT_MODE {mode!r}. "
            "This starter project currently allows only 'backtest'."
        )

    return mode
