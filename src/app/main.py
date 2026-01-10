import shutil
from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
import os
from pathlib import Path
from src.services.gallery_service import add_images_to_gallery, get_similar_images
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pathlib import Path
from typing import List

dotenv_path = Path('src/.env')

load_dotenv(dotenv_path=dotenv_path)
BASE_URL = os.getenv("BACKEND_URL")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[2]
GALLERY_PATH = BASE_DIR / "gallery"
EXTENDED_GALLERY_PATH = BASE_DIR / "extended_gallery"

# Processing status tracking
processing_status = {"status": "idle", "message": "", "error": None}

app.mount("/gallery", StaticFiles(directory=GALLERY_PATH), name="gallery")


@app.get("/all-images")
def get_gallery_images(request: Request):
    gallery_path = "gallery"
    print(gallery_path)
    """Return all image paths from the gallery folder"""
    supported_formats = {'.jpg', '.JPG', '.jpeg', '.JPEG'}
    
    if not os.path.exists(gallery_path):
        return {"error": f"Gallery folder '{gallery_path}' not found"}
    
    try:
        image_files = [
            {
                "filename": f,
                "relative_path": f"{BASE_URL}/gallery/{f}"
            }
            for f in os.listdir(gallery_path)
            if os.path.isfile(os.path.join(gallery_path, f)) 
            and Path(f).suffix.lower() in supported_formats
        ]
        
        return {
            "total": len(image_files),
            "images": image_files
        }
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/similar-images")
def get_similar_images_endpoint(caption: str, top_k: int = 3):
    """Return similar images based on the provided caption."""
    print("Received caption:", caption)
    try:
        similar_images = get_similar_images(caption, top_k)

        similar_images = [{"image_path": f"{BASE_URL}/{img['image_path']}", "caption": img['caption']} for img in similar_images]
        return {
            "caption": caption,
            "top_k": top_k,
            "relative_path": similar_images
        }
    except Exception as e:
        return {"error": str(e)}
    
def process_images_background():
    """Background task to process images."""
    global processing_status
    try:
        processing_status = {"status": "processing", "message": "Processing images...", "error": None}
        add_images_to_gallery()
        processing_status = {"status": "completed", "message": "Images processed successfully", "error": None}
    except Exception as e:
        processing_status = {"status": "error", "message": "", "error": str(e)}

@app.post("/add-images")
def add_images(files: List[UploadFile] = File(...), background_tasks: BackgroundTasks = None):
    """Add images from extended_gallery to gallery."""
    
    try:
        for file in files:
            file_path = EXTENDED_GALLERY_PATH / file.filename
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            file.file.close()
        
        background_tasks.add_task(process_images_background)
        
        return {
            "message": "Images uploaded successfully. Processing started in background.",
            "status": "processing"
        }
    except Exception as e:
        return {"error": str(e)}, 400

@app.get("/process-status")
def get_process_status():
    """Get the current processing status."""
    return processing_status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
