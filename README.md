# AI Gallery Parser

A comprehensive solution for processing photos and generating intelligent descriptions with vector embeddings.

## 📋 Basic Plan

We have a folder with lots and lots of photos. This project processes them through the following pipeline:

### Step 1: Parse All Photos

Parse all the photos one by one from the source folder.

### Step 2: Generate Captions

Use a generative AI model to automatically generate descriptions and captions for each photo.

### Step 3: Create Vector Embeddings

Use an embeddings model to convert the text captions to vectors:

- Convert captions to vectors for semantic search
- Store vectors in a vector database
- Store the path to the actual photo alongside the embeddings
- Store in the format of
  `   
{
  "vector": [ ... ],
  "photo_path": "D:/Photos/Goa/beach_2023.jpg",
  "caption": "Friends at beach during sunset",
  "date": "2023-12-18"
  }`

### Step 4: Build API & Frontend

Create an API and frontend interface to connect everything and enable users to search and explore the photo gallery.

## Backend API's to look for:

Essentially we will have a couple of api's to feed data to our UI.

1. /gallery/images GET
2. /getPhotosBySearch?caption={caption} GET
3. /add_new_photos POST [future plan]

A fairly straight forwand and simple backend API's.
