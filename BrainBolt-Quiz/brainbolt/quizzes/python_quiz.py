"""PythonQuiz - inherits from BaseQuiz."""
from .base_quiz import BaseQuiz


class PythonQuiz(BaseQuiz):
    def topic_key(self):    return "python"
    def pretty_name(self):  return "Python"
    def motivational_quote(self):
        return "Python: where simplicity meets power. Let's slither in!"
