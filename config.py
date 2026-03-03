"""
Central configuration and validation.

All tunable parameters are read from environment variables with sensible defaults.
Call ``validate()`` on startup to catch missing/invalid configuration early.
"""
import logging
import os
import sys

logger = logging.getLogger(__name__)


def validate(*, require_telegram: bool = True) -> bool:
    """Validate required environment variables.

    Args:
        require_telegram: When *False* (e.g. ``--dry-run``), skip the check
            for ``BOT_TOKEN`` / ``CHAT_ID``.

    Returns:
        ``True`` if configuration is valid, ``False`` otherwise.
    """
    ok = True

    if require_telegram:
        for var in ("BOT_TOKEN", "CHAT_ID"):
            if not os.environ.get(var):
                logger.error("Environment variable %s is not set.", var)
                ok = False

    days_ahead = os.environ.get("DAYS_AHEAD", "45")
    if not days_ahead.isdigit() or int(days_ahead) < 1:
        logger.error("DAYS_AHEAD must be a positive integer, got %r", days_ahead)
        ok = False

    for var in ("MIN_DELAY", "MAX_DELAY"):
        val = os.environ.get(var)
        if val is not None:
            try:
                f = float(val)
                if f < 0:
                    raise ValueError
            except ValueError:
                logger.error("%s must be a non-negative number, got %r", var, val)
                ok = False

    return ok
