"""brainbolt.quizzes - 4 quiz subclasses + 1 abstract base class."""
from .base_quiz       import BaseQuiz
from .python_quiz     import PythonQuiz
from .data_science_quiz import DataScienceQuiz
from .java_quiz       import JavaQuiz
from .fullstack_quiz  import FullStackQuiz

__all__ = ["BaseQuiz", "PythonQuiz", "DataScienceQuiz", "JavaQuiz", "FullStackQuiz"]


def make_quiz(topic_key: str) -> BaseQuiz:
    """Factory - returns the right Quiz subclass for a topic key."""
    mapping = {
        "python":       PythonQuiz,
        "data_science": DataScienceQuiz,
        "java":         JavaQuiz,
        "full_stack":   FullStackQuiz,
    }
    cls = mapping.get(topic_key)
    if cls is None:
        raise ValueError(f"Unknown topic: {topic_key}")
    return cls()
