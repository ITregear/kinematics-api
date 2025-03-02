from fastapi import FastAPI, HTTPException, Query
import os
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
        return dict(dh_table)

    if name:
        dh_table = await conn.fetchrow("SELECT * FROM dh_tables WHERE name = $1", name)
        await conn.close()
        if not dh_table:
            raise HTTPException(status_code=404, detail="DH table not found")
        return dict(dh_table)

    # Fetch all DH tables
    dh_tables = await conn.fetch("SELECT * FROM dh_tables")
    await conn.close()
    
    return {"dh_tables": [dict(table) for table in dh_tables]}
