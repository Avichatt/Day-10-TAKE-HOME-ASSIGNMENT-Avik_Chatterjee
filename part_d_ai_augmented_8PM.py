# Part D — AI Augmented Task

# Prompt Used:
# Write a Python function called analyze_text(text: str, **options).
# Options include: count_words, count_sentences, find_longest_word, sentiment_simple.
# Use type hints and Google style docstrings.
# Return a dictionary containing the analysis results.

### AI Generated Code (Initial Simplified Version)

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


### Critical Evaluation

# Problems identified:
# 1. Does not handle empty text
# 2. max() fails if no words
# 3. Sentence counting is naive
# 4. Function does too many tasks
# 5. No helper functions


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
