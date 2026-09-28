from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="PointAI Backend Test")

# Request
class ImagePayload(BaseModel):
    image: str  # Expecting Base64 encoded string

@app.post("/process-image", status_code=status.HTTP_200_OK)
async def process_image(payload: ImagePayload):
    """
    Accepts a POST request with a Base64 encoded image.
    Returns a success message.
    """
    if not payload.image:
        raise HTTPException(status_code=400, detail="Image payload cannot be empty")
    
    # NOTE: If actual image processing is required (e.g., saving to disk, ML inference),
    # it should be offloaded to a background task (BackgroundTasks) or a task queue 
    # (Celery/RabbitMQ) to prevent blocking the event loop.
    
    return {"message": "accepted"}