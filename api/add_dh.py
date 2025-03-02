from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from api.schema import DHTable
import uuid
import os
import json  # 🔹 Required for JSON conversion
import asyncpg  # PostgreSQL async client

app = FastAPI()

# Get Neon database URL from Vercel environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

@app.post("/api/add_dh")
async def add_dh_table(dh_table: DHTable):
    try:
        # Validate input using Pydantic
        dh_table = DHTable(**dh_table.dict())

        # Generate a unique ID
        dh_id = str(uuid.uuid4())

        # Convert Pydantic models to dictionaries before JSON conversion
        joints_json = json.dumps([joint.dict() for joint in dh_table.joints])  # 🔹 Fixed conversion

        # Store in PostgreSQL
        conn = await get_db_connection()
        await conn.execute(
            """
            INSERT INTO dh_tables (id, name, joints) VALUES ($1, $2, $3)
            """,
            dh_id, dh_table.name, joints_json  # 🔹 Now correctly serialized
        )
        await conn.close()

        return {"message": "DH table stored successfully", "id": dh_id}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Invalid DH table format: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))
