"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI, status

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-producthunt"}
