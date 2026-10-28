"""Campus library tracker: loans, overdue fines, renewals and persistence."""
import ast
import json
import operator
from datetime import datetime

# Global state
loans = {}
FINE_PER_DAY = 2

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul}


def add_book_loan(student_id, book_id, dates=None):
    """Record a loan; reject empty student ids and non-string book ids."""
    if not student_id or not isinstance(book_id, str):
        print(f"Rejected loan: student={student_id!r} book={book_id!r}")
        return False
    if dates is None:
        dates = []
    dates.append(str(datetime.now()))
    loans.setdefault(student_id, []).append(book_id)
    print(f"{student_id} borrowed {book_id} "
          f"(loan dates on record: {len(dates)})")
    return True


def return_book(student_id, book_id):
    """Remove a loan; report when no such loan exists."""
    try:
        loans[student_id].remove(book_id)
        if len(loans[student_id]) == 0:
            del loans[student_id]
    except (KeyError, ValueError):
        print(f"No loan of {book_id} for {student_id}")
        return False
    return True


def calculate_fine(days_overdue):
    """Return the fine for days_overdue; never negative."""
    return max(days_overdue, 0) * FINE_PER_DAY


def renew_book(student_id, book_id, extra_days):
    """Renew a loan without touching the fine rate."""
    print(f"Renewed {book_id} for {student_id} by {extra_days} days")


def load_records(file="loans.json"):
    """Replace the in-memory loans with the contents of file."""
    with open(file, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    loans.clear()
    loans.update(data)


def save_records(file="loans.json"):
    """Write the in-memory loans to file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(loans, handle)


def _eval_node(node, days):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, days)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id == "days":
        return days
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left, days),
                                   _eval_node(node.right, days))
    raise ValueError("unsupported fine rule")


def fine_from_rule(rule, days):
    """Evaluate a +, -, * arithmetic rule in terms of days, without eval."""
    return _eval_node(ast.parse(rule, mode="eval"), days)


def print_report():
    """Print every student and their borrowed books."""
    print("Loan Report")
    for student, books in loans.items():
        print(student, "->", books)


def main():
    """Run the demo scenario."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", 4521)  # book id should be a string
    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)
    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))
    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    print("S102 owes:", calculate_fine(int(days)))
    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
