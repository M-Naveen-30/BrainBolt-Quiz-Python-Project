"""DataScienceQuiz - inherits from BaseQuiz."""
from .base_quiz import BaseQuiz


class DataScienceQuiz(BaseQuiz):
    def topic_key(self):    return "data_science"
    def pretty_name(self):  return "Data Science"
    def motivational_quote(self):
        return "In data we trust - facts, models and a little bit of magic."
