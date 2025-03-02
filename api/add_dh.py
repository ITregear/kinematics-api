from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from api.schema import DHTable
from db.database import DATABASE
import uuid

app = FastAPI()

@app.post("/api/add_dh")
def add_dh_table(dh_table: DHTable):
    try:
        # Validate the input using Pydantic
        dh_table = DHTable(**dh_table.dict())

        # Generate a unique ID
        dh_id = str(uuid.uuid4())

        # Convert to dictionary and add ID
        dh_data = dh_table.dict()
        dh_data["id"] = dh_id

        # Store in "database"
        DATABASE[dh_id] = dh_data

        return {"message": "DH table stored successfully", "id": dh_id}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Invalid DH table format: " + str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))
