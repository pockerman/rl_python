"""
Helper class for iterative algorithms
"""

from enum import Enum
import abc
from abc import abstractmethod, ABC
from typing import Any, TypeVar

from src.utils.wrappers import time_fn
from src.utils.iteration_controller import ItrControlResult, IterationController
from src.utils import INFO


Env = TypeVar("Env")



class AlgorithmBase(ABC):
    """
    Base class for deriving algorithms
    """

    def __init__(self, n_episodes: int, tolerance: float, env: Env, render_env: bool = False) -> None:
        super(AlgorithmBase, self).__init__()
        self._itr_ctrl = IterationController(tol=tolerance, n_max_itrs=n_episodes)
        self._train_env = env
        self._state = None
        self.render_env = render_env
        self.output_msg_frequency: int = 100

    def __call__(self, **options) -> ItrControlResult:
        """
        Make the module callable
        """
        return self.train(**options)

    @property
    def state(self) -> Any:
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def train_env(self) -> Any:
        """
        Returns the environment used for training
        """
        return self._train_env

    @train_env.setter
    def train_env(self, value: Any) -> None:
        self._train_env = value

    @property
    def itr_control(self) -> IterationController:
        return self._itr_ctrl

    @property
    def n_episodes(self) -> int:
        return self.itr_control.n_max_itrs

    @property
    def current_episode_index(self) -> int:
        return self._itr_ctrl.current_itr_counter

    def reset(self) -> None:
        """
        Reset the underlying data
        """
        self._state = self.train_env.reset()
        self._itr_ctrl.reset()

    @time_fn
    def train(self, **options) -> ItrControlResult:

        """
        Iterate to train the agent
        """

        itr_ctrl_rsult = ItrControlResult(tol=self._itr_ctrl.tolerance,
                                          residual=self._itr_ctrl.residual,
                                          n_itrs=0, n_max_itrs=self._itr_ctrl.n_max_itrs,
                                          n_procs=1)

        self.actions_before_training_begins(**options)

        while self._itr_ctrl.continue_itrs():

            if self._itr_ctrl.current_itr_counter % self.output_msg_frequency   == 0:
                print("{0}: Episode {1} of {2}, ({3}% done)".format(INFO, self._itr_ctrl.current_itr_counter,
                                                                    self.itr_control.n_max_itrs,
                                                                    (self._itr_ctrl.current_itr_counter / self.itr_control.n_max_itrs)*100.0))
            self.actions_before_episode_begins(**options)
            self.step(**options)
            self.actions_after_episode_ends(**options)

        self.actions_after_training_ends(**options)

        # update the control result
        itr_ctrl_rsult.n_itrs = self._itr_ctrl.current_itr_counter
        itr_ctrl_rsult.residual = self._itr_ctrl.residual

        return itr_ctrl_rsult

    def actions_before_episode_begins(self, **options) -> None:
        """
        Execute any actions the algorithm needs before
        starting the episode
        :param options:
        :return: None
        """
        self._state = self.train_env.reset()

    def actions_after_episode_ends(self, **options):
        """
        Execute any actions the algorithm needs before
        starting the episode
        :param options:
        :return:
        """
        pass

    def actions_before_training_begins(self, **options) -> None:
        """
        Execute any actions the algorithm needs before
        starting the training
        """
        self.reset()

    @abstractmethod
    def actions_after_training_ends(self, **options) -> None:
        """
        Execute any actions the algorithm needs after
        the iterations are finished
        """
        raise NotImplementedError("The function must be overridden")

    @abstractmethod
    def step(self, **options) -> None:
        """
        Do one step of the algorithm
        """
        raise NotImplementedError("The function must be overridden")





