"""
Part D — AI-Augmented Task
============================

"""

from collections import defaultdict
from typing import Optional


PROMPT_USED = """

You are an expert Python developer. Your task is to write a production-ready Python function that merges and analyzes student grade data across two semesters.

Requirements:

Your function should accept two dictionaries representing student grades from Semester 1 and Semester 2. Each dictionary maps subject names (strings) to grades (numeric values, e.g., 85, 92.5).

The function must produce a merged report containing:

Combined GPA: Calculate the average of all grades across both semesters
Grade Trend: Determine whether grades are improving, declining, or stable by comparing average GPA from Semester 1 to Semester 2
Common Subjects: Identify subjects that appear in both semesters and include their grades from each semester in the report
Technical Requirements:

Use defaultdict from the collections module in your implementation
Use dict comprehension at least once in the code
Return the report as a structured dictionary or object that clearly displays all three pieces of information
Include proper error handling for edge cases (empty dictionaries, mismatched data types, division by zero)
Add docstring documentation explaining parameters, return value, and usage
Code Quality:

Write clean, readable code following PEP 8 standards
Include inline comments explaining non-obvious logic
The function should be self-contained and importable
Provide only the function code with no additional explanation unless necessary for clarity.

"""


def merge_grades_ai(sem1: dict, sem2: dict) -> dict:
    """Merge student grades from two semesters."""
    all_subjects = defaultdict(list)

    for subject, grade in sem1.items():
        all_subjects[subject].append(grade)
    for subject, grade in sem2.items():
        all_subjects[subject].append(grade)

    common_subjects = {s for s in sem1 if s in sem2}

    avg1 = sum(sem1.values()) / len(sem1)
    avg2 = sum(sem2.values()) / len(sem2)
    combined_gpa = (avg1 + avg2) / 2

    if avg2 > avg1:
        trend = "improving"
    elif avg2 < avg1:
        trend = "declining"
    else:
        trend = "stable"

    subject_comparison = {
        s: {"sem1": sem1[s], "sem2": sem2[s], "change": sem2[s] - sem1[s]}
        for s in common_subjects
    }

    return {
        "combined_gpa": round(combined_gpa, 2),
        "trend": trend,
        "common_subjects": subject_comparison,
    }




"""
CRITICAL EVALUATION OF AI OUTPUT
─────────────────────────────────

1. Does it handle missing subjects?
   - avg1 = sum(sem1.values()) / len(sem1) will raise
   ZeroDivisionError if either semester dict is empty.
   Also, sem1[s] in the comprehension will KeyError if s is
   in sem2 but not sem1 (though the filter prevents that here).
   The defaultdict is built but never actually used in the output.

2. Does it use .get() safely?
   ✗ NO — The code uses direct ``d[key]`` access everywhere:
   ``sem1[s]``, ``sem2[s]``.  If any dict has unexpected keys or the
   common_subjects filter has a bug, this will crash.  Should use
   ``.get()`` for safety.

3. Is the 'trend' calculation correct?
   ⚠ PARTIALLY — It compares semester averages, which is a reasonable
   heuristic.  However:
   - It doesn't account for different numbers of subjects per semester.
   - The combined_gpa formula ``(avg1 + avg2) / 2`` is wrong if
     semesters have different numbers of subjects.  True combined GPA
     should be total_grade_points / total_subjects.
   - No threshold for "stable" — a difference of 0.01 counts as trend.

4. Does it handle edge cases?
   ✗ NO —
     - Empty dicts → ZeroDivisionError.
     - Single semester (one empty) → crash.
     - Non-numeric grades → TypeError.
     - No common subjects → returns empty dict (OK but not flagged).

5. Is the code Pythonic?
   ⚠ PARTIALLY —
     - Uses set comprehension for common_subjects: OK, but
       ``sem1.keys() & sem2.keys()`` is more Pythonic.
     - The defaultdict is created but never used meaningfully.
     - No type hints or docstrings beyond a one-liner.
     - No input validation.

VERDICT: The AI code is a reasonable first draft but is NOT production-
ready.  It crashes on edge cases, has a mathematically incorrect GPA
formula, and doesn't leverage .get() for safe access.
"""



def merge_semester_grades(
    sem1: dict[str, float],
    sem2: dict[str, float],
    trend_threshold: float = 0.1,
) -> dict:
    """Merge student grades from two semesters into a comprehensive report.

    Produces a combined GPA (weighted by number of subjects), determines
    the grade trend, and identifies subjects common to both semesters.

    Uses ``defaultdict(list)`` to aggregate all grades per subject and
    dict comprehensions for the comparison.

    Args:
        sem1: Semester-1 grades — ``{subject: grade_point}``.
              Grade points are expected on a 0-10 scale.
        sem2: Semester-2 grades — ``{subject: grade_point}``.
        trend_threshold: Minimum absolute GPA difference to count as
            "improving" or "declining". Defaults to 0.1.

    Returns:
        A report dict with keys:
            - ``sem1_gpa``        : Semester 1 GPA (float or None).
            - ``sem2_gpa``        : Semester 2 GPA (float or None).
            - ``combined_gpa``    : Weighted combined GPA.
            - ``trend``           : "improving", "declining", or "stable".
            - ``total_subjects``  : Total unique subjects across both semesters.
            - ``common_subjects`` : Dict of subjects in both semesters with
                                    per-subject comparison.
            - ``sem1_only``       : Subjects only in semester 1.
            - ``sem2_only``       : Subjects only in semester 2.
            - ``all_grades``      : Full subject → grades list mapping.

    Raises:
        TypeError: If grades are not numeric.

    Examples:
        >>> sem1 = {'Math': 8.5, 'Physics': 7.0, 'English': 9.0}
        >>> sem2 = {'Math': 9.0, 'Physics': 7.5, 'Chemistry': 8.0}
        >>> report = merge_semester_grades(sem1, sem2)
        >>> report['trend']
        'improving'
        >>> report['combined_gpa']
        8.17
    """
    # ── Handle edge cases: empty dicts ──
    if not sem1 and not sem2:
        return {
            "sem1_gpa": None,
            "sem2_gpa": None,
            "combined_gpa": None,
            "trend": "stable",
            "total_subjects": 0,
            "common_subjects": {},
            "sem1_only": [],
            "sem2_only": [],
            "all_grades": {},
        }

    # ── Aggregate grades per subject using defaultdict ──
    all_grades: defaultdict[str, list[float]] = defaultdict(list)
    for subject, grade in sem1.items():
        all_grades[subject].append(grade)
    for subject, grade in sem2.items():
        all_grades[subject].append(grade)

    # ── Semester GPAs (safe against empty dicts) ──
    sem1_gpa: Optional[float] = (
        round(sum(sem1.values()) / len(sem1), 2) if sem1 else None
    )
    sem2_gpa: Optional[float] = (
        round(sum(sem2.values()) / len(sem2), 2) if sem2 else None
    )

    # ── Combined GPA: weighted average (total points / total subjects) ──
    total_points = sum(sem1.values()) + sum(sem2.values())
    total_count = len(sem1) + len(sem2)
    combined_gpa = round(total_points / total_count, 2) if total_count else None

    # ── Trend detection with threshold ──
    if sem1_gpa is not None and sem2_gpa is not None:
        diff = sem2_gpa - sem1_gpa
        if diff > trend_threshold:
            trend = "improving"
        elif diff < -trend_threshold:
            trend = "declining"
        else:
            trend = "stable"
    elif sem2_gpa is not None:
        trend = "improving"  # came from nothing → has grades
    elif sem1_gpa is not None:
        trend = "declining"  # had grades → nothing
    else:
        trend = "stable"

    # ── Subject sets (Pythonic intersection/difference) ──
    s1_keys = sem1.keys()
    s2_keys = sem2.keys()
    common = s1_keys & s2_keys      # set intersection on dict_keys
    only_s1 = s1_keys - s2_keys     # set difference
    only_s2 = s2_keys - s1_keys

    # ── Per-subject comparison for common subjects (dict comprehension) ──
    common_comparison = {
        subject: {
            "sem1": sem1.get(subject, 0.0),
            "sem2": sem2.get(subject, 0.0),
            "change": round(
                sem2.get(subject, 0.0) - sem1.get(subject, 0.0), 2
            ),
            "status": (
                "improved"
                if sem2.get(subject, 0.0) > sem1.get(subject, 0.0)
                else (
                    "declined"
                    if sem2.get(subject, 0.0) < sem1.get(subject, 0.0)
                    else "unchanged"
                )
            ),
        }
        for subject in sorted(common)
    }

    return {
        "sem1_gpa": sem1_gpa,
        "sem2_gpa": sem2_gpa,
        "combined_gpa": combined_gpa,
        "trend": trend,
        "total_subjects": len(all_grades),
        "common_subjects": common_comparison,
        "sem1_only": sorted(only_s1),
        "sem2_only": sorted(only_s2),
        "all_grades": dict(all_grades),
    }


# ──────────────── DEMO / MAIN ─────────────────────────

def _separator(title: str) -> None:
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print(f"{'═' * 60}")


if __name__ == "__main__":

    # ── Normal case ──
    _separator("Case 1: Normal — Two Semesters")
    sem1 = {"Math": 8.5, "Physics": 7.0, "English": 9.0, "History": 6.5}
    sem2 = {"Math": 9.0, "Physics": 7.5, "Chemistry": 8.0, "English": 9.2}
    report = merge_semester_grades(sem1, sem2)

    print(f"  Semester 1 GPA : {report['sem1_gpa']}")
    print(f"  Semester 2 GPA : {report['sem2_gpa']}")
    print(f"  Combined GPA   : {report['combined_gpa']}")
    print(f"  Trend          : {report['trend']}")
    print(f"  Total Subjects : {report['total_subjects']}")
    print(f"  Sem1-only      : {report['sem1_only']}")
    print(f"  Sem2-only      : {report['sem2_only']}")
    print(f"\n  Common Subject Comparison:")
    for subject, details in report["common_subjects"].items():
        print(f"    {subject:12s}: {details['sem1']} → {details['sem2']} "
              f"(change: {details['change']:+.1f}, {details['status']})")

    # ── Edge case: empty semester ──
    _separator("Case 2: Edge — Empty Semester 1")
    report2 = merge_semester_grades({}, sem2)
    print(f"  Sem1 GPA : {report2['sem1_gpa']}")
    print(f"  Sem2 GPA : {report2['sem2_gpa']}")
    print(f"  Trend    : {report2['trend']}")

    # ── Edge case: both empty ──
    _separator("Case 3: Edge — Both Empty")
    report3 = merge_semester_grades({}, {})
    print(f"  Combined GPA : {report3['combined_gpa']}")
    print(f"  Trend        : {report3['trend']}")

    # ── Edge case: identical semesters ──
    _separator("Case 4: Edge — Identical Semesters")
    same = {"Math": 8.0, "English": 8.0}
    report4 = merge_semester_grades(same, same)
    print(f"  Trend : {report4['trend']}")

    # ── AI version test (will crash on empty) ──
    _separator("Case 5: AI Version — Normal Input")
    ai_result = merge_grades_ai(sem1, sem2)
    print(f"  AI combined_gpa : {ai_result['combined_gpa']}")
    print(f"  AI trend        : {ai_result['trend']}")
    print(f"  (Note: AI version would crash on empty dicts)")

    print(f"\n{'═' * 60}")
    print("  Part D — AI-Augmented Task completed successfully ✓")
    print(f"{'═' * 60}\n")
