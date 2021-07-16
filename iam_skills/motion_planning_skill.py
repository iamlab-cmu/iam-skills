from motion_planning import IAMMotionPlanner
from pillar_skills import BaseSkill, BasePolicy
from .streaming_skill import BaseStreamTrajSkill, StreamTrajPolicy
from .cmd_type import CmdType
from motion_planning.planning.goals import CartesianGoal
import json

class MotionPlanningSkill(BaseStreamTrajSkill):
    def __init__(self, cfg):
        self._cfg = cfg

    def make_policy(self, state, param):
        param_dict=json.loads(param):
        ref_postion=state[param_dict["ref_obj"]+"/position"]
        ref_oreientation=state[param_dict["ref_obj"]+"/quaternion"]
        
        goal_pose=ref_postion+ref_oreientation
        # call the motion planner and return a StreamTrajPolicy
        motion_planner = IAMMotionPlanner(self._cfg)
        start = state
        goal = CartesianGoal(goal_pose)
        traj = motion_planner.replan(start, goal)
        policy = StreamTrajPolicy(traj, dt=1, cmd_type=CmdType.JOINT)


