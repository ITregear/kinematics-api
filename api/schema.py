from pydantic import BaseModel, Field
from typing import List, Dict

class Joint(BaseModel):
    """Model representing a joint in a DH table."""
    theta: float
    d: float
    a: float
    alpha: float
    joint_type: str = Field(..., pattern="^(rotational|prismatic)$")
    limits: Dict[str, float]  # Must contain "min" and "max"

class DHTable(BaseModel):
    """Model representing a Denavit-Hartenberg table."""
    name: str
    joints: List[Joint]
