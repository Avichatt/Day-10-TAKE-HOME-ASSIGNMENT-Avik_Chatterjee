# Part C — Interview Ready

## Q1 — Dictionary Complexity

Dictionary operations:

| Operation | Time Complexity |
| --------- | --------------- |
| Lookup    | O(1) average    |
| Insert    | O(1) average    |
| Delete    | O(1) average    |

Reason:
Python dictionaries use a **hash table**.

Worst case **O(n)** happens when many keys produce the **same hash collision**.

### Hash Function

* **Integers** -> hash is based on the number itself
* **Strings** -> Python computes a hash from characters

### Dict vs List

Use **dict when**

* you need **fast lookup by key**
* data has **key -> value mapping**

Use **list when**

* order matters
* you access items by **index**

---

## Q2 — Group Anagrams

```python
from collections import defaultdict

def group_anagrams(words: list[str]) -> dict[str, list[str]]:

    groups = defaultdict(list)

    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)

    return dict(groups)
```

Example:

```python
group_anagrams(['eat','tea','tan','ate','nat','bat'])
```

Result:

```
{'aet': ['eat','tea','ate'], 'ant': ['tan','nat'], 'abt':['bat']}
```

---

## Q3 — Debug Character Frequency

Original problem:

```python
freq[char] += 1
```

### Bug 1 — KeyError

Fix using `.get()`:

```python
freq[char] = freq.get(char, 0) + 1
```

### Bug 2 — Only returning keys

Correct version:

```python
def char_freq(text):

    freq = {}

    for char in text:
        freq[char] = freq.get(char, 0) + 1

    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    return sorted_freq
```

Example output:

```
[('a',3),('b',2),('c',1)]
```
