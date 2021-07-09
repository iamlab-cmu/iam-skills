from abc import abstractmethod

from pillar_skills import BaseSkill, BasePolicy

from .cmd_type import CmdType


class OneStepGripperPolicy(BasePolicy):

    def __init__(self, target_width=None, close_gripper=None, open_gripper=None):
        n_nones = 0
        if target_width is None:
            n_nones += 1
        if close_gripper is None:
            n_nones += 1
        if open_gripper is None:
            n_nones += 1

        assert n_nones == 2, 'Must provide only 1 gripper command'

        self._gripper_cmd = {
            'target_width': target_width,
            'close_gripper': close_gripper,
            'open_gripper': open_gripper
        }

    @property
    def cmd_type(self):
        return CmdType.GRIPPER

    def __call__(self, state):
        return self._gripper_cmd


class BaseGripperSkill(BaseSkill):

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
    def make_policy(self, state, param) -> OneStepGripperPolicy:
        pass


class OpenGripperSkill(BaseGripperSkill):

    def make_policy(self, state, param):
        return OneStepGripperPolicy(open_gripper=True)


class CloseGripperSkill(BaseGripperSkill):

    def make_policy(self, state, param):
        return OneStepGripperPolicy(close_gripper=True)


class GotoGripperWidthSkill(BaseGripperSkill):

    def make_policy(self, state, param):
        return OneStepGripperPolicy(target_width=param)
