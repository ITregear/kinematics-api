from fastapi import FastAPI, HTTPException, Query
import os
import json  # 🔹 Required for JSON deserialization
import asyncpg  # PostgreSQL async client

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
        return {
            "id": dh_table["id"],
            "name": dh_table["name"],
            "joints": json.loads(dh_table["joints"])  # 🔹 Convert JSON string back to list
        }

    if name:
        dh_table = await conn.fetchrow("SELECT * FROM dh_tables WHERE name = $1", name)
        await conn.close()
        if not dh_table:
            raise HTTPException(status_code=404, detail="DH table not found")
        return {
            "id": dh_table["id"],
            "name": dh_table["name"],
            "joints": json.loads(dh_table["joints"])  # 🔹 Convert JSON string back to list
        }

    # Fetch all DH tables
    dh_tables = await conn.fetch("SELECT * FROM dh_tables")
    await conn.close()

    return {
        "dh_tables": [
            {
                "id": table["id"],
                "name": table["name"],
                "joints": json.loads(table["joints"])  # 🔹 Convert JSON string back to list
            }
            for table in dh_tables
        ]
    }
