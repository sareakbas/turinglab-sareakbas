from turinglab.tm_engine import SingleTapeTM, RunResult, StepConfig, Tape
 
__all__ = ["SingleTapeTM", "RunResult", "StepConfig", "Tape"]

from .multi_tape import MultiTapeTM
 
from .ntm import NonDeterministicTM