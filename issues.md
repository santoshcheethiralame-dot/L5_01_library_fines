# Lab 5: Static Code Analysis

## Project
**Project:** Library Fine and Book Renewal System  
**File analyzed:** `library_system.py`  
**Tools:** Pylint, Bandit, Flake8  
**Reports:** `lab5_reports/` (`*_before.txt`, `*_after.txt`)

## Issues Identified and Resolved

Line numbers refer to the original file.

| Issue | Type | Original line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Use of `eval` (B307, W0123) | Security, Medium | 45 | `fine_from_rule` runs `eval` on a caller-supplied string, so a rule can execute arbitrary code. | Parse with `ast` and evaluate only numbers, `days`, and `+ - *`; anything else raises `ValueError`. |
| Bare `except` with `pass` (B110, E722, W0702) | Security/Bug, Low | 21-22 | `return_book` swallows every error, including `KeyboardInterrupt`, and hides failed returns. | Catch `KeyError` and `ValueError` only and print that no such loan exists. |
| Mutable default argument (W0102) | Bug | 9 | `dates=[]` is shared across calls, so the "loan dates on record" count grows across unrelated loans. | Default to `None` and create a new list inside the function. |
| Renewal changes the global fine rate | Logic bug (no tool flags it) | 27-31 | Renewing for more than 14 days did `FINE_PER_DAY += 1`, so one renewal raised fines for every student (5 days cost 15, not 10). Also W0603. | `renew_book` no longer touches `FINE_PER_DAY`. |
| Negative fine | Logic bug (no tool flags it) | 24-25 | `calculate_fine(-3)` returned -9. | Clamp days at 0 with `max(days_overdue, 0)`. |
| Invalid loan input accepted | Logic bug (no tool flags it) | 9-13, 56 | Empty student ids were dropped silently and an int book id (`4521`) was stored. | Reject both with a message and return `False`. |
| Files opened without `with` or encoding (R1732, W1514) | Quality | 34, 40 | Handles leak if an error occurs before `close()`; encoding is platform dependent. | `with open(..., encoding="utf-8")` plus `json.load`/`json.dump`. |
| `global` statements (W0603) | Quality | 28, 35 | Rebinding module state from inside functions. | `loans.clear()` and `loans.update(...)` instead of rebinding. |
| `renewBook` naming (C0103) | Style | 27 | Not snake_case. | Renamed to `renew_book`. |
| Missing docstrings (C0114, C0116) | Style | 1, many | No module or function docs. | Added docstrings. |
| `%` formatting and string concatenation (C0209) | Style | 14, 31 | Old-style formatting. | f-strings. |
| Unused import `os` (F401, W0611) | Style | 2 | Imported but never used. | Removed. |
| Missing `__main__` guard | Quality | 68 | `main()` ran on import. | `if __name__ == "__main__":`. |
| Blank lines and long lines (E302, E305, E501) | Style | 9-68, 14, 31 | PEP 8 spacing and 79-column limit. | Two blank lines around top-level defs; wrapped long strings. |

## Verification Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.07/10 | 10.00/10 |
| Bandit | 1 Medium, 1 Low | none |
| Flake8 | 14 findings | none |
