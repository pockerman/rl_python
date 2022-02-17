"""
Implementation of Policy iteration algorithm. In policy
iteration at each step we do one policy evaluation and one policy
improvement.

Implementation refactored from
https://github.com/udacity/deep-reinforcement-learning

"""

import numpy as np
from typing import Any
import copy

#from src.algorithms.algorithm_base import AlgorithmBase
#from src.algorithms.algo_input import AlgoInput

from src.algorithms.dp.dp_algorithm_base import DPAlgoBase, DPAlgoConfig
from src.algorithms.dp.iterative_policy_evaluation import IterativePolicyEvaluator
from src.algorithms.dp.policy_improvement import PolicyImprovement
from src.policies.policy_base import PolicyBase
from src.policies.policy_adaptor_base import PolicyAdaptorBase





class PolicyIteration(DPAlgoBase):
    """
    Policy iteration class
    """

    def __init__(self, algo_in: DPAlgoConfig,  policy_adaptor: PolicyAdaptorBase):
        super(PolicyIteration, self).__init__(algo_in=algo_in)

        self._p_eval = IterativePolicyEvaluator(algo_in=algo_in)
        self._p_imprv = PolicyImprovement(algo_in=algo_in, v=self._p_eval.v, policy_adaptor=policy_adaptor)

    @property
    def v(self) -> np.array:
        return self._p_imprv.v

    @property
    def policy(self):
        return self._p_eval.policy

    def actions_before_training_begins(self, **options) -> None:
        """
        Execute any actions the algorithm needs before
        starting the iterations
        """

        # call the base class version
        super(PolicyIteration, self).actions_before_training_begins(**options)
        self._p_eval.actions_before_training_begins(**options)
        self._p_imprv.actions_before_training_begins(**options)

    def actions_after_training_ends(self, **options) -> None:
        pass

    def on_episode(self) -> None:

        # make a copy of the policy already obtained
        old_policy = copy.deepcopy(self._p_eval.policy)

        # evaluate the policy
        self._p_eval.train()

        # update the value function to
        # improve for
        self._p_imprv.v = self._p_eval.v

        # improve the policy
        self._p_imprv.train()

        new_policy = self._p_imprv.policy

        # check of the two policies are the same
        if old_policy == new_policy:
            self.itr_control.residual = self.itr_control.tolerance*10**-1

        self._p_eval.policy = new_policy