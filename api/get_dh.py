from fastapi import FastAPI, HTTPException, Query
import os
import json
import asyncpg
from api.schema import DHTable  # ✅ Enforce schema validation

app = FastAPI()

# Get Neon database URL
DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

@app.get("/api/get_dh")
async def get_dh_table(id: str = Query(None), name: str = Query(None)):
    conn = await get_db_connection()

    if id:
        dh_table = await conn.fetchrow("SELECT * FROM dh_tables WHERE id = $1", id)
        await conn.close()
        if not dh_table:
            raise HTTPException(status_code=404, detail="DH table not found")

        # Deserialize and validate with Pydantic
        return DHTable(
            name=dh_table["name"],
            joints=json.loads(dh_table["joints"])
        ).dict()

    if name:
        dh_table = await conn.fetchrow("SELECT * FROM dh_tables WHERE name = $1", name)
        await conn.close()
        if not dh_table:
            raise HTTPException(status_code=404, detail="DH table not found")

        return DHTable(
            name=dh_table["name"],
            joints=json.loads(dh_table["joints"])
        ).dict()

    # Fetch all DH tables
    dh_tables = await conn.fetch("SELECT * FROM dh_tables")
    await conn.close()

    # Apply schema validation for each entry
    return {
        "dh_tables": [
            DHTable(
                name=table["name"],
                joints=json.loads(table["joints"])
            ).dict()
            for table in dh_tables
        ]
    }
