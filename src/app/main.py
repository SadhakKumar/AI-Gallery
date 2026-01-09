from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import Request
import os
from pathlib import Path
from src.services.gallery_service import add_images_to_gallery, get_similar_images
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()
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
    
@app.get("/add-images")
def add_images():
    """Add images from extended_gallery to gallery."""
    try:
        add_images_to_gallery()
        return {"message": "Images added successfully"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
