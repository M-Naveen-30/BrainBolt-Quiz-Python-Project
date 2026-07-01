"""
base_quiz.py
~~~~~~~~~~~~
Abstract base class for every quiz topic.

OOP showcase
------------
* ABSTRACTION  -> ABC + abstractmethod
* INHERITANCE  -> PythonQuiz / JavaQuiz / DataScienceQuiz / FullStackQuiz
                  all extend this class.
* POLYMORPHISM -> Every subclass overrides topic_key() and pretty_name();
                  callers use BaseQuiz reference without caring which one.
* ENCAPSULATION-> All question data hidden behind self._questions.
"""
import os
import json
import random
from abc import ABC, abstractmethod

from ..config import QUESTIONS_FILE, QUESTIONS_PER_QUIZ


class BaseQuiz(ABC):
    """Abstract quiz - subclasses just declare the topic key."""

    # cache loaded once for all subclasses
    _bank_cache = None

    def __init__(self):
        self._questions = self.__load()
        self.score   = 0
        self.answers = []   # list of dicts: {q, options, picked, correct, ok, explain}

    # ----------- subclass MUST override these -----------
    @abstractmethod
    def topic_key(self) -> str: ...

    @abstractmethod
    def pretty_name(self) -> str: ...

    # ----------- POLYMORPHIC default (can be overridden) -----------
    def motivational_quote(self) -> str:
        """Each subclass can change this if it wants."""
        return "Great minds discuss ideas. Let's go!"

    # ----------- loaders -----------
    @classmethod
    def _bank(cls):
        if cls._bank_cache is None:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
                cls._bank_cache = json.load(f)
        return cls._bank_cache

    def __load(self):
        bank = self._bank()[self.topic_key()]
        questions = [self.__shuffle_options(dict(q)) for q in bank]
        random.shuffle(questions)
        return questions[:QUESTIONS_PER_QUIZ]

    @staticmethod
    def __shuffle_options(qdict):
        """Shuffle options - track which letter is the new correct one."""
        original_letter = qdict["answer"]
        original_correct_text = qdict["options"][ord(original_letter) - ord("A")]

        opts = list(qdict["options"])
        random.shuffle(opts)
        new_idx = opts.index(original_correct_text)
        qdict["options"] = opts
        qdict["answer"]  = chr(ord("A") + new_idx)
        return qdict

    # ----------- runtime API -----------
    def total(self):
        return len(self._questions)

    def iter_questions(self):
        for idx, q in enumerate(self._questions, start=1):
            yield idx, q

    def record(self, q, picked_letter, ok):
        self.answers.append({
            "q": q["q"],
            "options": q["options"],
            "picked": picked_letter,
            "correct": q["answer"],
            "ok": ok,
            "explain": q.get("explain", ""),
        })
        if ok:
            self.score += 1

    # ----------- result summary string (polymorphic) -----------
    def result_emoji(self) -> str:
        pct = self.score / self.total()
        if pct == 1.0:
            return ""
        if pct >= 0.85:
            return ""
        if pct >= 0.6:
            return ""
        if pct >= 0.4:
            return ""
        return ""
