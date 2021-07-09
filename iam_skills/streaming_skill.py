from abc import abstractmethod
from typing import List

from pillar_skills import BaseSkill, BasePolicy

from .cmd_type import CmdType


class StreamTrajPolicy(BasePolicy):

    def __init__(self, traj: List, dt: float, cmd_type: CmdType):
        self._traj = traj
        self._dt = dt
        self._cmd_type = cmd_type

        self._t_step = 0

    @property
    def cmd_type(self):
        return self._cmd_type

    @property
    def dt(self):
        return self._dt

    @property
    def horizon(self):
        return len(self._traj)

    def get_traj_item(self, t_step):
        t = min(t_step, len(self._traj))
        return self._traj[t]

    def __call__(self, state):
        item = self.get_traj_item(self._t_step)
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
    def make_policy(self, state, param) -> StreamTrajPolicy:
        pass
