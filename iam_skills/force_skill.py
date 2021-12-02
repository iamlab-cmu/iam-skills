from abc import abstractmethod
import json

from pillar_skills import BaseSkill, BasePolicy

from .cmd_type import CmdType


class ForcePolicy(BasePolicy):

    def __init__(self, duration: float, dt: float, record: bool):
        self._duration = duration
        self._dt = dt
        self._record = record
        self._horizon = int(duration / dt)

    @property
    def dt(self):
        return self._dt

    @property
    def cmd_type(self):
        return CmdType.FORCE

    @property
    def duration(self):
        return self._duration

    @property
    def horizon(self):
        return self._horizon

    @property
    def record(self):
        return self._record

    def __call__(self, state):
        return self._force_cmd


class BaseForceSkill(BaseSkill):

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
    def make_policy(self, state, param) -> ForcePolicy:
        pass


class RecordSkill(BaseForceSkill):

    def make_policy(self, state, param):
        param_dict = json.loads(param)
        return ForcePolicy(duration=param_dict['duration'], dt=param_dict['dt'], record=True)


class ZeroForceSkill(BaseForceSkill):

    def make_policy(self, state, param):
        param_dict = json.loads(param)
        return ForcePolicy(duration=param_dict['duration'], dt=param_dict['dt'], record=False)

