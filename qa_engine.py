"""
Backward compatibility wrapper for qa_engine.
Redirects to the modular implementation inside src.qa_engine.
"""

from src.qa_engine import answer_question

__all__ = ["answer_question"]
