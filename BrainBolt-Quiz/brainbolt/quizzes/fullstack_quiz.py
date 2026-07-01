"""FullStackQuiz - inherits from BaseQuiz."""
from .base_quiz import BaseQuiz


class FullStackQuiz(BaseQuiz):
    def topic_key(self):    return "full_stack"
    def pretty_name(self):  return "Full Stack"
    def motivational_quote(self):
        return "Front, back, middle - own the entire stack!"
