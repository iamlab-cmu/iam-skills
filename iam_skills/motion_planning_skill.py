from motion_planning import IAMMotionPlanner
from pillar_skills import BaseSkill, BasePolicy
from .streaming_skill import BaseStreamTrajSkill, StreamTrajPolicy
from .cmd_type import CmdType


class MotionPlanningSkill(BaseStreamTrajSkill):
    def __init__(self, cfg):
        self._cfg = cfg

    def make_policy(self, state, param):
        # call the motion planner and return a StreamTrajPolicy
        motion_planner = IAMMotionPlanner(self._cfg)
        start = state
        goal = None
        traj = motion_planner.replan(start, goal)
        policy = StreamTrajPolicy(traj, dt=1, cmd_type=CmdType.JOINT)


