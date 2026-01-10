# AI Gallery Parser

A comprehensive system for parsing large photo collections, generating intelligent descriptions using AI, and enabling semantic search through vector embeddings.

---

## Overview

**AI Gallery Parser** processes a folder of photos and builds a searchable, AI-powered gallery. Each image is analyzed, described using a generative AI model, converted into vector embeddings, and stored in a vector database for fast semantic search. A backend API and frontend UI connect everything into a smooth end-to-end experience.

---

## Core Pipeline

### 1. Parse All Photos

- Traverse the source directory recursively
- Read and process photos one by one

### 2. Generate Captions

- Use a generative AI model to automatically generate captions and descriptions
- Captions describe the scene, people, context, and environment

### 3. Create Vector Embeddings

- Convert generated captions into vector embeddings
- Store vectors in **Qdrant** for semantic search
- Persist metadata alongside embeddings

**Stored format:**

```json
{
  "vector": [ ... ],
  "photo_path": "D:/Photos/Goa/beach_2023.jpg",
  "caption": "Friends at the beach during sunset",
  "date": "2023-12-18"
}
```

### 4. Build API & Frontend

Create an API and frontend interface to connect everything and enable users to search and explore the photo gallery.

---

## Backend APIs

The system provides a couple of straightforward APIs to feed data to the UI:

1. **`/all-images`** - `GET`  
   Retrieve all images from the gallery

2. **`/similar-images?caption={caption}&top_k={numberOfPhotos}`** - `GET`  
   Search for similar images based on caption similarity

3. **`/add-images`** - `POST` _(future plan)_  
   Add new images to the gallery

---

## Setting Up

### 1. Docker & Qdrant Setup

You will require Docker to run the Qdrant Vector DB locally.

#### a. Pull the Qdrant image

```bash
docker pull qdrant/qdrant
```

#### b. Run the service

```bash
docker run -p 6333:6333 -p 6334:6334 \
  -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
  qdrant/qdrant
```

> **Note:** `pwd` will be the path where you want to have your storage.

### 2. Clone the Repository

```bash
git clone https://github.com/SadhakKumar/AI-Gallery.git
```

### 3. Backend Setup

#### a. Create a virtual environment

It is highly advised to create a virtual environment and install all dependencies there.

```bash
python -m venv .venv
```

#### b. Activate the virtual environment

```bash
.venv\Scripts\activate.bat
```

#### c. Install dependencies

```bash
pip install -r requirements.txt
```

#### d. Configure environment variables

Create a `.env` file inside the `src` folder and add your backend URL to it. (Please refer to `.env.example`)

> **Note:** In the future, we will change this URL to the ngrok URL. For now, you can use localhost.

#### e. Create required folders

Create two folders at the root level:

- `gallery`
- `extended_gallery`

#### f. Run the backend server

```bash
uvicorn src.app.main:app --reload
```

### 4. Frontend Setup

#### a. Navigate to frontend folder

```bash
cd frontend
```

#### b. Install dependencies

```bash
npm install
```

#### c. Configure environment variables

Create a `.env` file inside the frontend folder and add the backend URL. (Please follow `.env.example` for naming conventions)

#### d. Run the frontend

```bash
npm run dev
```

---

## Technologies Used

- **Vector Database:** Qdrant
- **Backend:** FastAPI (Python)
- **Frontend:** React/Next.js (JavaScript)
- **AI Models:** Generative AI for captions, embeddings for search

---

## Future Enhancements

- Add image upload functionality via `/add-images` API
- Support for ngrok URL configuration
- Enhanced search filters and metadata
- Batch processing improvements

---

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
