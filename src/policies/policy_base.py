"""
Base class for deriving policies
"""

from abc import ABC, abstractmethod
import torch
import torch.nn as nn
from typing import TypeVar, Any

Env = TypeVar('Env')


class PolicyBase(ABC):
    """
    Base class for policies
    """
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        raise Exception("Must be overridden")

    def __eq__(self, other: Any) -> bool:
        """
        Equality comparison. By default returns false
        """
        return False


class PolicyTorchBase(nn.Module):

    def __init__(self, env: Any) -> None:
        super(PolicyTorchBase, self).__init__()
        self.env = env

    def forward(self, x: torch.tensor) -> torch.tensor:
        raise Exception("Must be overriden")

    def act(self, state):
        raise Exception("Must be overriden")

