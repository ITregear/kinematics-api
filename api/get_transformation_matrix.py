from fastapi import FastAPI, HTTPException, Query
import numpy as np

app = FastAPI()


@app.get("/api/get_transformation_matrix")
async def get_transformation_matrix(
    theta: float = Query(..., description="Joint angle (radians)"),
    alpha: float = Query(..., description="Link twist angle (radians)"),
    a: float = Query(..., description="Link length (meters)"),
    d: float = Query(..., description="Joint offset (meters)"),
):
    """
    Computes the Denavit-Hartenberg transformation matrix for a given joint.

    Parameters:
    - `theta`: Joint angle (for rotational joints).
    - `alpha`: Link twist angle.
    - `a`: Link length.
    - `d`: Joint offset (for prismatic joints).

    Returns:
    - 4x4 transformation matrix as a nested list.
    """

    transformation_matrix = np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha),  np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta),  np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0,             np.sin(alpha),                  np.cos(alpha),                 d],
        [0,             0,                               0,                              1],
    ])

    return transformation_matrix.tolist()
