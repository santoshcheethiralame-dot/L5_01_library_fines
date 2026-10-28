# Reflection

1. **Which tool found the most issues, and which was most useful?**
   Pylint found the most (21 messages), mostly docstrings and style. Bandit found the fewest (2) but they mattered most: `eval` on caller input is a code-execution hole.

2. **Did any tool report something that was not worth fixing, or miss something real?**
   Missing-docstring warnings are low value on a small script. All three tools missed the logic bugs: renewals raising everyone's fine, negative fines, and an int book id being accepted. I found those by running the program and reading its output.

3. **How did fixing one issue affect others?**
   Replacing `global` with `loans.clear()`/`update()` and `with open` removed several Pylint messages at once. The mutable default fix changed the printed loan counts, which showed the old numbers were wrong.

4. **How would you use static analysis in a real project?**
   Run Flake8 and Pylint in a pre-commit hook and in CI, with Bandit as a blocking check for Medium and above. Static analysis catches whole classes of mistakes cheaply but does not replace tests or reading the output.
