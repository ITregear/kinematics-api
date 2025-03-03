from fastapi import FastAPI

app = FastAPI()

@app.get('/api/hello')
def read_root():
    """Return a greeting message."""
    return {"message": "Hello Robot Nerd!"}