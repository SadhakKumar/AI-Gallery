from sentence_transformers import SentenceTransformer
from src.database.db import initialize_qdrant_client, client, insert_to_qdrant, query_qdrant
from src.processing.processing import generate_embedding, generate_caption_for_image
import os
import shutil
from pathlib import Path

def store_caption_and_embedding(id, image_path):
    caption = generate_caption_for_image(image_path)
    print("Generated Caption:", caption)
    embedding = generate_embedding(caption)
    print("Generated Embedding")
    # Store in Qdrant
    insert_to_qdrant(id, embedding, caption, image_path)

def get_similar_images(caption, top_k=3):
    embedding = generate_embedding(caption)
    print("Query Embedding Generated")
    array = [{"image_path": items.payload['image_path'], "caption": items.payload['caption']} for items in query_qdrant(embedding, top_k)]
    return array

def process_photos_from_gallery():
    """Process all images in the gallery folder."""
    gallery_path = "gallery"
    supported_formats = {'.jpg'}
    
    if not os.path.exists(gallery_path):
        print(f"Error: Gallery folder '{gallery_path}' not found.")
        return
    
    # Get all image files
    image_files = [
        f for f in os.listdir(gallery_path)
        if os.path.isfile(os.path.join(gallery_path, f)) and Path(f).suffix.lower() in supported_formats
    ]
    
    if not image_files:
        print(f"No images found in '{gallery_path}'.")
        return
    
    print(f"Found {len(image_files)} images. Starting processing...")
    
    for idx, filename in enumerate(image_files, start=3):
        image_path = Path(os.path.join(gallery_path, filename)).as_posix()
        print(f"\n[{idx}/{len(image_files)}] Processing: {filename}")
        try:
            store_caption_and_embedding(idx, image_path)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

def add_images_to_gallery():
    extended_gallery_path = "extended_gallery"
    gallery_path = "gallery"
    supported_formats = {'.jpg'}
    if not os.path.exists(extended_gallery_path):
        print(f"Error: Extended gallery folder '{extended_gallery_path}' not found.")
        return 
    image_files = [
        f for f in os.listdir(extended_gallery_path)
        if os.path.isfile(os.path.join(extended_gallery_path, f)) and Path(f).suffix.lower() in supported_formats
    ] 
    if not image_files:
        print(f"No images found in '{extended_gallery_path}'.")
        return
    
    for idx, filename in enumerate(image_files, start=1):
        source_path = os.path.join(extended_gallery_path, filename)
        dest_path = os.path.join(gallery_path, filename)
        
        # Move file from extended_gallery to gallery
        try:
            shutil.move(source_path, dest_path)
            print(f"Moved {filename} to gallery")
        except Exception as e:
            print(f"Error moving {filename}: {e}")
            continue
        
        # Get relative POSIX path for the moved file
        image_path = Path(dest_path).as_posix()
        
        print(f"\n[{idx}/{len(image_files)}] Processing: {filename}")
        try:
            count = len(os.listdir(gallery_path))
            store_caption_and_embedding(count, image_path)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
