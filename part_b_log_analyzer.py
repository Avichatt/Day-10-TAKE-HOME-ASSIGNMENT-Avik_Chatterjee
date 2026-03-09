"""
Part B -- Log Analyzer Using Counter and defaultdict
=====================================================

"""

from collections import Counter, defaultdict
from typing import Optional



# --------------------- Simulated Server Logs ---------------------

logs = [
    "2026-03-09 10:00:01 INFO auth User login successful",
    "2026-03-09 10:01:15 ERROR database Connection timeout",
    "2026-03-09 10:02:30 WARNING api Slow response detected",
    "2026-03-09 10:03:20 INFO auth Token refreshed",
    "2026-03-09 10:04:05 ERROR database Connection timeout",
    "2026-03-09 10:05:10 CRITICAL server System crash",
    "2026-03-09 10:06:45 INFO api Request completed",
    "2026-03-09 10:07:50 ERROR api Invalid request format",
]

RAW_LOGS: list[str] = logs


def parse_log_line(line: str) -> dict[str, str]:
    """Parse a single log line into a structured dict.

    Expected format:
        ``YYYY-MM-DD HH:MM:SS LEVEL  module  message``

    Args:
        line: A single log string.

    Returns:
        Dict with keys: ``timestamp``, ``level``, ``module``, ``message``.
        Returns a dict with ``'parse_error'`` key on malformed input.

    Example:
        >>> parse_log_line("2026-03-09 08:01:12 INFO auth User login")
        {'timestamp': '2026-03-09 08:01:12', 'level': 'INFO',
         'module': 'auth', 'message': 'User login'}
    """
    parts = line.split()
    if len(parts) < 5:
        return {"parse_error": f"Malformed log line: {line}"}

    return {
        "timestamp": f"{parts[0]} {parts[1]}",
        "level": parts[2],
        "module": parts[3],
        "message": " ".join(parts[4:]),
    }


def parse_all_logs(
    logs: Optional[list[str]] = None,
) -> list[dict[str, str]]:
    """Parse all raw log lines into a list of structured dicts.

    Args:
        logs: List of raw log strings. Defaults to ``RAW_LOGS``.

    Returns:
        List of parsed log dicts.
    """
    logs = logs if logs is not None else RAW_LOGS
    return [parse_log_line(line) for line in logs]


def analyze_logs(
    logs: Optional[list[str]] = None,
) -> dict:
    """Run full analysis on the log data.

    Uses:
        - ``Counter`` for most common errors, module activity, level distribution.
        - ``defaultdict(list)`` to group errors by module.

    Args:
        logs: List of raw log strings. Defaults to ``RAW_LOGS``.

    Returns:
        Summary dict with ``total_entries``, ``error_rate``, ``level_distribution``,
        ``top_errors``, ``busiest_module``, ``most_active_modules``,
        ``errors_by_module``.
    """
    logs = logs if logs is not None else RAW_LOGS
    parsed = parse_all_logs(logs)

    # -- Filter out parse errors --
    valid = [entry for entry in parsed if "parse_error" not in entry]

    total = len(valid)
    if total == 0:
        return {
            "total_entries": 0,
            "error_rate": "0.00%",
            "level_distribution": {},
            "top_errors": [],
            "busiest_module": "N/A",
            "most_active_modules": [],
            "errors_by_module": {},
        }

    # -- Counter: level distribution --
    level_counter: Counter = Counter(
        entry.get("level", "UNKNOWN") for entry in valid
    )

    # -- Counter: most active modules --
    module_counter: Counter = Counter(
        entry.get("module", "unknown") for entry in valid
    )

    # -- Counter: most common error messages --
    error_entries = [
        entry for entry in valid
        if entry.get("level") in ("ERROR", "CRITICAL")
    ]
    error_message_counter: Counter = Counter(
        entry.get("message", "") for entry in error_entries
    )

    # -- defaultdict(list): group errors by module --
    errors_by_module: defaultdict[str, list[str]] = defaultdict(list)
    for entry in error_entries:
        module = entry.get("module", "unknown")
        errors_by_module[module].append(entry.get("message", ""))

    # -- Build summary --
    error_count = len(error_entries)
    error_rate = round((error_count / total) * 100, 2)
    busiest = module_counter.most_common(1)[0] if module_counter else ("N/A", 0)

    summary: dict = {
        "total_entries": total,
        "error_rate": f"{error_rate}%",
        "level_distribution": dict(level_counter.most_common()),
        "top_errors": error_message_counter.most_common(5),
        "busiest_module": busiest[0],
        "most_active_modules": module_counter.most_common(),
        "errors_by_module": dict(errors_by_module),
    }

    return summary


# ---------------- DEMO / MAIN ---------------------

def _separator(title: str) -> None:
    """Print a section separator."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


if __name__ == "__main__":

    _separator("Parsed Log Entries (first 5)")
    parsed = parse_all_logs()
    for entry in parsed[:5]:
        print(f"  {entry}")

    _separator("Full Log Analysis Summary")
    summary = analyze_logs()

    print(f"\n  Total Entries    : {summary['total_entries']}")
    print(f"  Error Rate       : {summary['error_rate']}")
    print(f"  Busiest Module   : {summary['busiest_module']}")

    print(f"\n  Level Distribution:")
    for level, count in summary["level_distribution"].items():
        bar = "#" * count
        print(f"    {level:10s} : {count:3d}  {bar}")

    print(f"\n  Top Error Messages:")
    for msg, count in summary["top_errors"]:
        print(f"    [{count}x] {msg}")

    print(f"\n  Most Active Modules:")
    for module, count in summary["most_active_modules"]:
        print(f"    {module:10s} : {count}")

    print(f"\n  Errors Grouped by Module:")
    for module, messages in summary["errors_by_module"].items():
        print(f"    {module}:")
        # Show unique errors with counts
        msg_counts = Counter(messages)
        for msg, cnt in msg_counts.most_common():
            print(f"      [{cnt}x] {msg}")

    print(f"\n{'=' * 60}")
    print("  Part B Log Analyzer completed successfully [OK]")
    print(f"{'=' * 60}\n")
