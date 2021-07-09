from abc import ABC, abstractmethod
from enum import Enum
from pillar_skills import BaseSkill, BasePolicy


class StreamCmdType(Enum):
    EE=0
    JOINT=1


class BaseStreamTrajPolicy(BasePolicy, ABC):

    def __init__(self, traj):
        self._traj = traj
        self._t_step = 0

    @property
    @abstractmethod
    def cmd_type(self) -> StreamCmdType:
        pass

    @property
    @abstractmethod
    def dt(self) -> float:
        pass

    @property
    def horizon(self):
        return len(self._traj)

    def __call__(self, state):
        t = min(self._t_step, len(self._traj))
        item = self._traj[t]

        self._t_step += 1

        return item


class BaseStreamTrajSkill(BaseSkill):

    def precondition_satisfied_for_state(self, state):
        return 1

    def precondition_satisfied(self, state, param):
        return 1

    def termination_condition_satisfied(self, state, param, policy, t_step):
        if t_step >= policy.horizon:
            return 1
        return 0

    def skill_execution_successful(self, state_init, state_end, param, policy, t_step):
        return 1

    def make_skill_parameter_generator(self, state, max_num_parameters):
        raise NotImplementedError()

    @abstractmethod
    def make_policy(self, state, param) -> BaseStreamTrajPolicy:
        pass
