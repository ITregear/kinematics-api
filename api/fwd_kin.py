from fastapi import FastAPI, HTTPException, Query
import os
import httpx
import numpy as np
import logging
from typing import List

app = FastAPI()

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

API_BASE_URL = os.getenv("API_BASE_URL")


@app.get("/api/fwd_kin")
async def fwd_kin(
    id: str = Query(None, description="ID of the stored DH table"),
    name: str = Query(None, description="Name of the stored DH table"),
    joint_values: List[float] = Query(..., description="Repeated query parameter for joint values"),
):
    """
    Computes forward kinematics for a given manipulator using its stored DH table.

    Parameters:
    - `id` or `name`: Identifier for the stored DH table (only one is required).
    - `joint_values`: List of joint positions (repeated parameter format).

    Returns:
    - 4x4 transformation matrix representing the end-effector's pose.
    """

    logging.info(f"Received request for fwd_kin with name={name}, id={id}, joint_values={joint_values}")

    if not id and not name:
        raise HTTPException(status_code=400, detail="Must provide either 'id' or 'name'.")

    # Retrieve DH table
    async with httpx.AsyncClient() as client:
        params = {"id": id} if id else {"name": name}
        dh_response = await client.get(f"{API_BASE_URL}/api/get_dh", params=params)

    if dh_response.status_code != 200:
        logging.error(f"Failed to retrieve DH table: {dh_response.text}")
        raise HTTPException(status_code=dh_response.status_code, detail="Failed to retrieve DH table.")

    dh_table = dh_response.json()
    joints = dh_table.get("joints", [])

    if len(joint_values) != len(joints):
        raise HTTPException(status_code=400, detail="Number of joint values must match the number of joints.")

    # Validate joint limits
    for i, (joint, value) in enumerate(zip(joints, joint_values)):
        limit_min, limit_max = joint["limits"]["min"], joint["limits"]["max"]
        if not (limit_min <= value <= limit_max):
            raise HTTPException(
                status_code=400,
                detail=f"Joint {i} value {value} out of limits [{limit_min}, {limit_max}].",
            )

    # Compute transformation matrices
    transformation_matrices = []
    async with httpx.AsyncClient() as client:
        for i, (joint, value) in enumerate(zip(joints, joint_values)):
            theta = value if joint["joint_type"] == "rotational" else joint["theta"]
            d = value if joint["joint_type"] == "prismatic" else joint["d"]

            logging.info(f"Requesting transformation matrix for joint {i}: theta={theta}, alpha={joint['alpha']}, a={joint['a']}, d={d}")

            response = await client.get(
                f"{API_BASE_URL}/api/get_transformation_matrix",
                params={"theta": theta, "alpha": joint["alpha"], "a": joint["a"], "d": d},
            )

            if response.status_code != 200:
                logging.error(f"Error in transformation matrix request: {response.text}")
                raise HTTPException(status_code=response.status_code, detail="Failed to compute transformation matrix.")

            transformation_matrices.append(np.array(response.json()))

    # Compute the final transformation matrix
    final_matrix = np.eye(4)
    for matrix in transformation_matrices:
        try:
            final_matrix = np.dot(final_matrix, matrix)
        except Exception as e:
            logging.error(f"Matrix multiplication error: {str(e)}")
            raise HTTPException(status_code=500, detail="Matrix multiplication failed.")

    return {"end_effector_transform": final_matrix.tolist()}
