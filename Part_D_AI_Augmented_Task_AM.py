# Part D — AI Augmented Task

## Prompt Used

```
Write a Python function that takes two dictionaries representing
student grades from two different semesters and produces a merged
report showing combined GPA, grade trend (improving/declining/stable),
and subjects common to both semesters. Use defaultdict and dict
comprehension.
```

---

## AI Generated Code

```python
from collections import defaultdict

def semester_report(sem1, sem2):

    history = defaultdict(list)

    for s, g in sem1.items():
        history[s].append(g)

    for s, g in sem2.items():
        history[s].append(g)

    avg = {s: sum(v)/len(v) for s,v in history.items()}

    gpa1 = sum(sem1.values())/len(sem1) if sem1 else 0
    gpa2 = sum(sem2.values())/len(sem2) if sem2 else 0

    if gpa2 > gpa1:
        trend = "improving"
    elif gpa2 < gpa1:
        trend = "declining"
    else:
        trend = "stable"

    return {
        "combined_gpa": sum(avg.values())/len(avg),
        "trend": trend,
        "common_subjects": list(sem1.keys() & sem2.keys())
    }
```

---

## Critical Evaluation

Yes, the code correctly uses `defaultdict` and dict comprehension.

However some improvements are needed:

* `.get()` is not used for safe access
* empty dictionaries should be handled carefully
* result dictionary could include clearer type hints
* docstring is missing

---

## Improved Version

```python
from collections import defaultdict

def semester_report(sem1: dict, sem2: dict) -> dict:
    """Merge two semester grade dictionaries."""

    history = defaultdict(list)

    for s, g in sem1.items():
        history[s].append(g)

    for s, g in sem2.items():
        history[s].append(g)

    averages = {s: sum(v)/len(v) for s,v in history.items()}

    gpa1 = sum(sem1.values())/len(sem1) if sem1 else 0
    gpa2 = sum(sem2.values())/len(sem2) if sem2 else 0

    if gpa2 > gpa1:
        trend = "improving"
    elif gpa2 < gpa1:
        trend = "declining"
    else:
        trend = "stable"

    return {
        "combined_gpa": sum(averages.values())/len(averages) if averages else 0,
        "trend": trend,
        "common_subjects": list(sem1.keys() & sem2.keys())
    }
```
