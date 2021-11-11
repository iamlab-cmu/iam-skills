from abc import abstractmethod
import json

from pillar_skills import BaseSkill, BasePolicy

from .cmd_type import CmdType

class OneStepJointDmpPolicy(BasePolicy):

    def __init__(self, duration: float, dt: float, dmp_params: dict):
        self._duration = duration
        self._dt = dt
        self._dmp_params = dmp_params
        self._horizon = int((duration + 1) / dt)

    @property
    def dt(self):
        return self._dt

    @property
    def cmd_type(self):
        return CmdType.ONESTEPJOINTDMP

    @property
    def duration(self):
        return self._duration

    @property
    def horizon(self):
        return self._horizon

    @property
    def dmp_params(self):
        return self._dmp_params

    def __call__(self, state):
        return self._dmp_params


class BaseOneStepJointDmpSkill(BaseSkill):

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
    def make_policy(self, state, param) -> OneStepJointDmpPolicy:
        pass


class JointDmpSkill(BaseOneStepJointDmpSkill):

    def make_policy(self, state, param):
        param_dict = json.loads(param)
        return OneStepJointDmpPolicy(duration=param_dict['duration'], dt=param_dict['dt'], dmp_params=param_dict['dmp_params'])
