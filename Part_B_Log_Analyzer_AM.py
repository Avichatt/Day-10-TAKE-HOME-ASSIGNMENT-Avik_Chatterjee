from collections import Counter, defaultdict

logs = [
"2026-03-09 10:00:01 INFO auth Login success",
"2026-03-09 10:01:10 ERROR database Connection timeout",
"2026-03-09 10:02:05 WARNING api Slow response",
"2026-03-09 10:03:00 INFO api Request finished",
"2026-03-09 10:04:20 ERROR database Connection timeout",
"2026-03-09 10:05:30 CRITICAL server System crash"
]

def parse_log(line):
    parts = line.split()
    return {
        "timestamp": parts[0] + " " + parts[1],
        "level": parts[2],
        "module": parts[3],
        "message": " ".join(parts[4:])
    }

def analyze_logs(log_lines):

    parsed = [parse_log(l) for l in log_lines]

    level_counter = Counter()
    module_counter = Counter()
    error_counter = Counter()

    errors_by_module = defaultdict(list)

    for log in parsed:

        level = log.get("level")
        module = log.get("module")
        message = log.get("message")

        level_counter[level] += 1
        module_counter[module] += 1

        if level in ["ERROR", "CRITICAL"]:
            error_counter[message] += 1
            errors_by_module[module].append(message)

    total = len(parsed)
    error_rate = (level_counter["ERROR"] + level_counter["CRITICAL"]) / total * 100

    summary = {
        "total_entries": total,
        "error_rate": round(error_rate, 2),
        "top_errors": error_counter.most_common(3),
        "busiest_module": module_counter.most_common(1)[0][0]
    }

    return summary
