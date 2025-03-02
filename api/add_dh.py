from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from api.schema import DHTable
import uuid
import os
import asyncpg

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")


async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)


@app.post("/api/add_dh")
async def add_dh_table(dh_table: DHTable):
    try:
        # Validate the input using Pydantic
        dh_table = DHTable(**dh_table.dict())

        # Generate a unique ID
        dh_id = str(uuid.uuid4())

        # Convert to dictionary and add ID
        dh_data = dh_table.dict()
        dh_data["id"] = dh_id

        # Store in PostgreSQL
        conn = await get_db_connection()
        await conn.execute(
            """
            INSERT INTO dh_tables (id, name, joints) VALUES ($1, $2, $3)
            """,
            dh_id, dh_table.name, dh_data["joints"]
        )
        await conn.close()

        return {"message": "DH table stored successfully", "id": dh_id}

    except ValidationError as e:
        raise HTTPException(
            status_code=400, detail="Invalid DH table format: " + str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred: " + str(e))
