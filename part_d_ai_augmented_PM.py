# Part D — AI Augmented Task

# Prompt Used:

You are an expert Python developer tasked with building a production-ready function that merges and analyzes student grade data across two semesters.

**Your Task:**
Write a Python function that accepts two dictionaries representing student grades from different semesters and generates a comprehensive merged report. The function must:

1. Calculate combined GPA across both semesters
2. Determine grade trend (improving, declining, or stable) by comparing semester-to-semester performance
3. Identify subjects that appear in both semesters
4. Return a structured report containing all three pieces of information

**Technical Requirements:**
- Use `defaultdict` from the `collections` module to handle missing keys or aggregations where appropriate
- Use dict comprehension to filter, transform, or combine the grade data
- Assume grade input format is consistent (e.g., dictionaries with subject names as keys and numeric grades as values)
- Include clear, inline comments explaining the purpose of `defaultdict` and dict comprehension usage
- Handle edge cases gracefully (empty dictionaries, no common subjects, identical GPAs)

**Output Structure:**
The function should return a dictionary containing:
- `combined_gpa`: A single float value representing the average GPA across both semesters
- `grade_trend`: A string value ("improving", "declining", or "stable")
- `common_subjects`: A list of subject names present in both semesters

**Code Quality:**
- Include a docstring explaining parameters, return type, and expected behavior
- Write clean, readable code that follows PEP 8 conventions
- Add a few example usage cases at the bottom demonstrating how to call the function with sample input dictionaries


def analyze_text_ai(text: str, **options) -> dict:

    result = {}

    if options.get("count_words", True):
        result["word_count"] = len(text.split())

    if options.get("count_sentences", True):
        result["sentence_count"] = text.count(".") + text.count("!")

    if options.get("find_longest_word", True):
        words = text.split()
        result["longest_word"] = max(words, key=len)

    if options.get("sentiment_simple", True):
        if "good" in text:
            result["sentiment"] = "positive"
        else:
            result["sentiment"] = "neutral"

    return result


# Critical evaluation:

#1.Does it handle missing subjects?
The function does not check whether the input text is empty. If an empty string is passed, some operations may produce incorrect results 
or cause errors. Good code should always handle edge cases such as empty input to prevent crashes or misleading output.

#2. max() fails if no words exist
The function uses the max() function to find the longest word. However, if the text contains no words (for example, an empty string or only spaces), 
the list of words becomes empty. Calling max() on an empty list raises a ValueError, which causes the program to crash.

#3. Sentence counting is naive
The function counts sentences using a very simple method, usually by counting periods (.) or splitting text only by periods. This approach is inaccurate
because real sentences may end with different punctuation marks such as question marks (?) or exclamation marks (!). As a result, the sentence count may be incorrect.

#4. Function does too many tasks
The function performs multiple responsibilities at once, such as counting words, counting sentences, finding the longest word, and calculating sentiment. 
This violates the Single Responsibility Principle, which states that a function should perform only one main task. When a function does too many things, it becomes harder
to read, test, debug, and maintain.

#5. No helper functions
All the logic is written inside a single large function instead of breaking it into smaller helper functions. Helper functions improve code organization, readability,
and reusability. By separating tasks into smaller functions (for example, one for word counting and another for sentence counting), the code becomes easier to understand and maintain.

### Improved Version

from typing import Dict


def analyze_text(text: str, **options) -> Dict:

    if not text:
        return {}

    result = {}

    words = text.split()

    if options.get("count_words", True):
        result["word_count"] = len(words)

    if options.get("count_sentences", True):
        result["sentence_count"] = text.count(".") + text.count("?") + text.count("!")

    if options.get("find_longest_word", True):
        result["longest_word"] = max(words, key=len) if words else ""

    if options.get("sentiment_simple", True):

        positive_words = ["good", "great", "excellent"]

        sentiment = "neutral"

        for w in words:
            if w.lower() in positive_words:
                sentiment = "positive"

        result["sentiment"] = sentiment

    return result

if __name__ == "__main__":
    test_text = "Python is good! This is a test sentence."
    print("Analysis Results:", analyze_text(test_text))
