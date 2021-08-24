from abc import abstractmethod

from pillar_skills import BaseSkill, BasePolicy

from .cmd_type import CmdType


class OneStepForcePolicy(BasePolicy):

    def __init__(self, duration=None, record=None, block=None):

        self._force_cmd = {
            'duration': duration,
            'record': record,
            'block': block
        }

    @property
    def cmd_type(self):
        return CmdType.FORCE

    def __call__(self, state):
        return self._force_cmd


class BaseForceSkill(BaseSkill):

    def precondition_satisfied_for_state(self, state):
        return 1

    def precondition_satisfied(self, state, param):
        return 1

    def termination_condition_satisfied(self, state, param, policy, t_step):
        if t_step >= 1:
            return 1
        return 0

    def skill_execution_successful(self, state_init, state_end, param, policy, t_step):
        return 1

    def make_skill_parameter_generator(self, state, max_num_parameters):
        raise NotImplementedError()

    @abstractmethod
    def make_policy(self, state, param) -> OneStepForcePolicy:
        pass


class RecordSkill(BaseForceSkill):

    def make_policy(self, state, param):
        param_dict = json.loads(param)
        return OneStepForcePolicy(duration=param_dict['duration'], record=True, block=False)


class ZeroForceSkill(BaseForceSkill):

    def make_policy(self, state, param):
        param_dict = json.loads(param)
        return OneStepForcePolicy(duration=param_dict['duration'], record=False, block=True)

