from fastapi import FastAPI
import json

app = FastAPI()

@app.get('/api/hello')
def read_root():
    return {"message": "Hello Robot Nerd!"}