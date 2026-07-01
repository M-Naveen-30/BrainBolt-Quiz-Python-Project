"""
quiz_runner.py
~~~~~~~~~~~~~~
Drives a single quiz attempt in the terminal.
"""
import time

from .quizzes import BaseQuiz


class QuizRunner:
    """Owns the run-loop for one BaseQuiz instance."""

    def __init__(self, quiz: BaseQuiz):
        self._quiz = quiz

    # ----------------------------------------------------------------
    def run(self):
        print("\n" + "=" * 60)
        print(" " * 18 + f"  {self._quiz.pretty_name().upper()} QUIZ  STARTS")
        print("=" * 60)
        print(" Tip: type A, B, C or D and press Enter.\n")

        for idx, q in self._quiz.iter_questions():
            self._ask_one(idx, q)

        # ----- results -----
        total = self._quiz.total()
        score = self._quiz.score
        emoji = self._quiz.result_emoji()
        print("\n" + "=" * 60)
        print(f"   Congratulations - you scored  {score} / {total}   {emoji}")
        print("=" * 60)

    # ----------------------------------------------------------------
    def _ask_one(self, idx, q):
        print(f"\n Q{idx}. {q['q']}")
        for i, opt in enumerate(q["options"]):
            letter = chr(ord("A") + i)
            print(f"   {letter}.  {opt}")

        while True:
            ans = input(" Your answer (A/B/C/D) : ").strip().upper()
            if ans in {"A", "B", "C", "D"}:
                break
            print("   Type only A, B, C or D.")

        ok = (ans == q["answer"])
        self._quiz.record(q, ans, ok)

        if ok:
            print("   Correct!")
        else:
            print(f"   Wrong. Correct answer was: {q['answer']}")

    # ----------------------------------------------------------------
    def review_answers(self):
        """Show every question with the user's pick + correct + explanation."""
        print("\n" + "=" * 60)
        print(" " * 18 + "  ANSWER REVIEW")
        print("=" * 60)

        for i, rec in enumerate(self._quiz.answers, start=1):
            tag = "OK " if rec["ok"] else "X  "
            print(f"\n {tag} Q{i}. {rec['q']}")
            for j, opt in enumerate(rec["options"]):
                letter   = chr(ord("A") + j)
                marker = ""
                if letter == rec["correct"]:
                    marker += "  <- correct"
                if letter == rec["picked"] and not rec["ok"]:
                    marker += "  (you picked)"
                print(f"     {letter}. {opt}{marker}")
            if rec["explain"]:
                print(f"     Why: {rec['explain']}")
            time.sleep(0.02)
