from sentence_transformers import SentenceTransformer
import ollama

def generate_embedding(input_text):
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embedding = model.encode(input_text)
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None 

def generate_caption_for_image(image_path):
    try:
        response = ollama.chat(
        model='llama3.2-vision',
        messages=[
            {"role": "system", "content": "You are a captioning assistant. Respond with ONLY a single short caption (max 15 words). No punctuation at start or end. Do NOT start with phrases like 'This image shows', 'The image depicts', or 'Image:'."},
            {"role": "user", "content": "Provide a concise caption for the attached image (<=15 words)."},
            {"role": "user", "images": [image_path]}
        ])     

        return response['message']['content']
    except Exception as e:
        print(f"Error generating caption: {e}")
        return "No caption available"
    
