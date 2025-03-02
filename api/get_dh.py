from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from db.database import DATABASE

app = FastAPI()

@app.get("/api/get_dh")
def get_dh_table(id: Optional[str] = Query(None), name: Optional[str] = Query(None)):
    # Case 1: No parameters, return all DH tables
    if id is None and name is None:
        return {"dh_tables": list(DATABASE.values())}

    # Case 2: Search by ID
    if id:
        dh_table = DATABASE.get(id)
        if dh_table:
            return dh_table
        else:
            raise HTTPException(status_code=404, detail="DH table not found with ID: " + id)

    # Case 3: Search by name
    if name:
        for dh_id, dh_table in DATABASE.items():
            if dh_table["name"] == name:
                return dh_table
        raise HTTPException(status_code=404, detail="DH table not found with name: " + name)

    raise HTTPException(status_code=400, detail="Invalid query parameters")
