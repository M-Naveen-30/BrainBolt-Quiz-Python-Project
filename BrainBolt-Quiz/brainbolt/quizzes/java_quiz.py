"""JavaQuiz - inherits from BaseQuiz."""
from .base_quiz import BaseQuiz


class JavaQuiz(BaseQuiz):
    def topic_key(self):    return "java"
    def pretty_name(self):  return "Java"
    def motivational_quote(self):
        return "Write once, run anywhere - and ace this quiz everywhere!"
