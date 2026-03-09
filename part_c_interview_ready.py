"""
Part C -- Interview Ready
==========================

"""

from collections import defaultdict, Counter


"""

WHY IS AVERAGE O(1)?
----------------------
Python dicts are implemented as **hash tables**. When you do ``d[key]``:

  1. Python computes ``hash(key)`` — a fixed-time operation for most
     built-in types (int, str, tuple, etc.).
  2. The hash is used to compute an **index** into the internal array:
        index = hash(key) % table_size
  3. Python looks at that slot directly — one memory access, O(1).

Because a good hash function distributes keys uniformly across the table,
each slot typically holds 0 or 1 entry, so operations take constant time
on average.

WHAT CAUSES WORST-CASE O(n)?
-----------------------------
- **Hash collisions**: If many keys map to the same index, Python must
  probe through a chain of entries (open addressing with perturbation)
  to find the right one. In the pathological worst case, ALL n keys
  collide, turning the table into a linear scan -> O(n).
- **Hash-flooding attacks**: An adversary crafts keys with identical
  hash values. Python mitigates this with hash randomisation (PEP 456).
- **Table resizing**: When the table's load factor exceeds ~2/3, Python
  allocates a bigger table and rehashes all entries — an O(n) operation.
  However, this is amortised across all prior O(1) insertions, so the
  amortised cost per insert remains O(1).

HOW DOES PYTHON'S HASH FUNCTION WORK?
──────────────────────────────────────
- **Integers**: For small ints, ``hash(n) == n``. For large ints, a
  modular hash is used. This is efficient and avoids collisions among
  sequential integers.
- **Strings**: Python uses SipHash (since 3.4+), a keyed hash function
  that takes each character into account. A per-process random seed is
  added to prevent hash-flooding attacks, so ``hash("hello")`` differs
  between Python sessions.
- **Tuples**: Hashed by combining the hashes of each element using a
  XOR-rotate scheme.
- **Custom objects**: Must define ``__hash__()`` and ``__eq__()``; by
  default, CPython uses ``id(obj)`` (memory address).

WHEN TO CHOOSE DICT OVER LIST?
-------------------------------

 Use a **dict** when you need fast name->value look-ups
  or membership testing.  Use a **list** when data is sequential and
  accessed by position.
"""


def group_anagrams(words: list[str]) -> dict[str, list[str]]:
    """Group a list of words by their anagram signature.

    Two words are anagrams if they contain the same characters in any
    order.  The *anagram key* is the characters of the word sorted
    alphabetically and joined into a string.

    Uses ``defaultdict(list)`` to collect anagrams efficiently.

    Args:
        words: List of words to group.

    Returns:
        Dict mapping the sorted-character signature -> list of words
        sharing that signature.

    Examples:
        >>> group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])
        {'aet': ['eat', 'tea', 'ate'], 'ant': ['tan', 'nat'], 'abt': ['bat']}

        >>> group_anagrams([])
        {}

        >>> group_anagrams(['a'])
        {'a': ['a']}
    """
    anagram_groups: defaultdict[str, list[str]] = defaultdict(list)

    for word in words:
        # sorted('eat') -> ['a', 'e', 't'] -> 'aet'
        key = "".join(sorted(word.lower()))
        anagram_groups[key].append(word)

    return dict(anagram_groups)


"""
BUG ANALYSIS
-------------

Bug 1 — KeyError on first occurrence
    Line:  freq[char] += 1
    Problem: When a character is encountered for the first time, it
             does not exist in ``freq``, so ``freq[char]`` raises a
             ``KeyError``.  The ``+=`` operator requires the key to
             already have a value.
    Fix:    Use ``freq[char] = freq.get(char, 0) + 1``
            - .get(char, 0) returns 0 if the key is missing,
            avoiding the KeyError.
            Alternatively, use ``collections.Counter(text)`` or
            ``collections.defaultdict(int)``.

Bug 2 — Returns keys only, not (key, count) pairs
    Line:  return sorted_freq
    Problem: ``sorted(freq, ...)`` iterates over the **keys** of the
             dict.  So ``sorted_freq`` is a list of characters only —
             the counts are lost.
    Fix:    Use ``sorted(freq.items(), key=lambda x: x[1], reverse=True)``
            - .items() yields (key, value) tuples, so the
            result preserves both characters and their counts.
"""


def char_freq(text: str) -> list[tuple[str, int]]:
    """Count character frequencies in *text*, sorted descending.

    Args:
        text: Input string.

    Returns:
        List of ``(character, count)`` tuples sorted by count descending.

    Examples:
        >>> char_freq("banana")
        [('a', 3), ('n', 2), ('b', 1)]

        >>> char_freq("")
        []
    """
    freq: dict[str, int] = {}
    for char in text:
        # FIX Bug 1: use .get() with default 0 for safe first access
        freq[char] = freq.get(char, 0) + 1

    # FIX Bug 2: sort .items() (key-value pairs), not just keys
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq


# -- Alternative concise fix using Counter (one-liner) --
def char_freq_counter(text: str) -> list[tuple[str, int]]:
    """Same as char_freq but using Counter.most_common()."""
    return Counter(text).most_common()


# ---------------- DEMO / MAIN -------------------------

def _separator(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


if __name__ == "__main__":

    # -- Q2 Demo --
    _separator("Q2: group_anagrams")
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    result = group_anagrams(words)
    print(f"  Input : {words}")
    print(f"  Output: {result}")

    # Edge cases
    print(f"\n  Edge — empty list  : {group_anagrams([])}")
    print(f"  Edge — single word : {group_anagrams(['hello'])}")
    print(f"  Edge — all same    : {group_anagrams(['abc', 'bca', 'cab'])}")

    # -- Q3 Demo --
    _separator("Q3: char_freq (fixed)")
    text = "banana"
    result = char_freq(text)
    print(f"  Input : '{text}'")
    print(f"  Output: {result}")

    print(f"\n  Counter version: {char_freq_counter(text)}")
    print(f"  Empty string   : {char_freq('')}")

    print(f"\n{'=' * 60}")
    print("  Part C -- Interview Ready completed successfully [OK]")
    print(f"{'=' * 60}\n")
