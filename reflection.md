# Lab 5: Static Code Analysis Reflection

## 1. What is the purpose of static code analysis?

Static code analysis examines source code without running it to find bugs, security weaknesses and coding-standard violations early, before they reach users. Pylint checks code quality, Bandit checks security, and Flake8 checks PEP 8 style, so together they cover different parts of the same file.

## 2. What did the three tools identify?

Pylint (6.07/10 before) flagged a mutable default argument, a bare `except`, `global` statements, files opened without `with` or an encoding, `eval`, a non-snake_case function name, an unused import and missing docstrings. Bandit flagged `eval` (Medium) and a try/except/pass block (Low). Flake8 flagged 14 formatting problems: missing blank lines, two overlong lines, an unused import and a bare `except`.

## 3. How did the fixes improve the program?

`eval` on a caller-supplied rule was replaced by an AST evaluator that only allows numbers, `days` and `+ - *`, so a rule can no longer run arbitrary code. Specific exceptions replaced the silent `except: pass`. The mutable default, `global` statements and unclosed files were fixed. Pylint went from 6.07 to 10.00, and Bandit and Flake8 now report nothing. Running the program also exposed bugs the tools missed: renewing a loan raised the fine rate for every student, negative days gave a negative fine, and an integer book id was accepted. These are fixed too.

## 4. What did you learn from this lab?

A program can run without errors and still be insecure or wrong. The tools caught the unsafe `eval` and the style issues, but none of them caught the renewal bug that inflated fines, which I only found by running the program and reading its output. Rerunning the tools after each fix gave measurable proof that the findings were gone.
