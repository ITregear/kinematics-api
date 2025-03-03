from fastapi import FastAPI, HTTPException, Query
import os
import json
import asyncpg
from api.schema import DHTable

app = FastAPI()

# Get Neon database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db_connection():
    """Establish a connection to the database."""
    return await asyncpg.connect(DATABASE_URL)

@app.get("/api/get_dh")
async def get_dh_table(id: str = Query(None), name: str = Query(None)):
    """
    Retrieve DH table data based on provided id or name.

    Args:
        id (str, optional): The ID of the DH table to retrieve.
        name (str, optional): The name of the DH table to retrieve.

    Returns:
        dict: The DH table data or a list of all DH tables if no parameters are provided.
    """
    conn = await get_db_connection()

    try:
        if id:
            return await fetch_dh_table_by_id(conn, id)

        if name:
            return await fetch_dh_table_by_name(conn, name)

        return await fetch_all_dh_tables(conn)

    finally:
        await conn.close()

async def fetch_dh_table_by_id(conn, id):
    """Fetch a DH table by its ID."""
    dh_table = await conn.fetchrow("SELECT * FROM dh_tables WHERE id = $1", id)
    if not dh_table:
        raise HTTPException(status_code=404, detail="DH table not found")

    return DHTable(
        name=dh_table["name"],
        joints=json.loads(dh_table["joints"])
    ).dict()

async def fetch_dh_table_by_name(conn, name):
    """Fetch a DH table by its name."""
    dh_table = await conn.fetchrow("SELECT * FROM dh_tables WHERE name = $1", name)
    if not dh_table:
        raise HTTPException(status_code=404, detail="DH table not found")

    return DHTable(
        name=dh_table["name"],
        joints=json.loads(dh_table["joints"])
    ).dict()

async def fetch_all_dh_tables(conn):
    """Fetch all DH tables from the database."""
    dh_tables = await conn.fetch("SELECT * FROM dh_tables")
    return {
        "dh_tables": [
            DHTable(
                name=table["name"],
                joints=json.loads(table["joints"])
            ).dict()
            for table in dh_tables
        ]
    }
