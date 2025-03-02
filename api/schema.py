from pydantic import BaseModel, Field
from typing import List, Dict

class Joint(BaseModel):
    theta: float
    d: float
    a: float
    alpha: float
    joint_type: str = Field(..., pattern="^(rotational|prismatic)$")
    limits: Dict[str, float]  # Must contain "min" and "max"

class DHTable(BaseModel):
    name: str
    joints: List[Joint]
