from enum import Enum


class CmdType(Enum):
    EE=0
    JOINT=1
    GRIPPER=2
    FORCE=3