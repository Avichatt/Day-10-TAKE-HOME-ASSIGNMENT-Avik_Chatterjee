from collections import defaultdict
from typing import List, Dict


def create_student(name: str, roll: str, **marks) -> dict:
    """
    Create a student record.

    Args:
        name: student name
        roll: roll number
        **marks: subject marks

    Returns:
        dict representing a student
    """

    student = {
        "name": name,
        "roll": roll,
        "marks": marks,
        "attendance": 0.0
    }

    return student


def calculate_gpa(*marks: float, scale: float = 10.0) -> float:
    """
    Calculate GPA from marks.

    Args:
        *marks: subject marks
        scale: GPA scale

    Returns:
        GPA value
    """

    if not marks:
        return 0.0

    avg = sum(marks) / len(marks)
    gpa = (avg / 100) * scale

    return round(gpa, 2)


def get_top_performers(students: List[dict], n: int = 5, subject: str = None) -> List[dict]:
    """
    Return top students.

    Args:
        students: list of student dicts
        n: number of students
        subject: subject name

    Returns:
        list of top students
    """

    if not students:
        return []

    if subject:
        sorted_students = sorted(
            students,
            key=lambda s: s.get("marks", {}).get(subject, 0),
            reverse=True
        )
    else:
        sorted_students = sorted(
            students,
            key=lambda s: sum(s.get("marks", {}).values()) / len(s.get("marks", {})) if s.get("marks") else 0,
            reverse=True
        )

    return sorted_students[:n]


def generate_report(student: dict, **options) -> str:
    """
    Generate student report.

    Options:
        include_rank
        include_grade
        verbose
    """

    include_rank = options.get("include_rank", True)
    include_grade = options.get("include_grade", True)
    verbose = options.get("verbose", False)

    name = student.get("name")
    roll = student.get("roll")
    marks = student.get("marks", {})

    report = f"Student: {name} ({roll})\n"

    if verbose:
        report += f"Marks: {marks}\n"

    if include_grade:
        avg = sum(marks.values()) / len(marks) if marks else 0
        if avg >= 90:
            grade = "A"
        elif avg >= 75:
            grade = "B"
        elif avg >= 60:
            grade = "C"
        else:
            grade = "D"

        report += f"Grade: {grade}\n"

    if include_rank:
        report += "Rank: Not calculated\n"

    return report


def classify_students(students: List[dict]) -> Dict[str, List[str]]:
    """
    Classify students into grades.
    """

    groups = defaultdict(list)

    for student in students:

        marks = student.get("marks", {})
        avg = sum(marks.values()) / len(marks) if marks else 0

        if avg >= 90:
            groups["A"].append(student["name"])
        elif avg >= 75:
            groups["B"].append(student["name"])
        elif avg >= 60:
            groups["C"].append(student["name"])
        else:
            groups["D"].append(student["name"])

    return dict(groups)

if __name__ == "__main__":
    # Tests
    s1 = create_student("Amit", "R001", math=85, python=92, ml=78)
    s2 = create_student("Priya", "R002", math=95, python=88, ml=91)

    students = [s1, s2]

    # create_student tests
    assert s1["name"] == "Amit"
    assert s1["marks"]["math"] == 85
    assert isinstance(s1, dict)

    # calculate_gpa tests
    assert calculate_gpa(85, 92, 78) > 0
    assert calculate_gpa() == 0.0
    assert round(calculate_gpa(100, 100), 2) == 10.0

    # get_top_performers tests
    top = get_top_performers(students, 1)
    assert len(top) == 1

    top_python = get_top_performers(students, 1, "python")
    assert top_python[0]["name"] == "Amit"

    # generate_report tests
    report = generate_report(s1)
    assert "Amit" in report

    report2 = generate_report(s1, verbose=True)
    assert "Marks" in report2

    # classify_students tests
    groups = classify_students(students)
    assert isinstance(groups, dict)
    print("All Part A tests passed!")
