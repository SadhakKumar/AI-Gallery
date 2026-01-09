from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Global client instance
client = QdrantClient(url="http://localhost:6333")

def initialize_qdrant_client():
    client.create_collection(
        collection_name="image_captions",
        vectors_config=VectorParams(size=384, distance=Distance.DOT),
    )
    
def insert_to_qdrant(id, embedding, caption, image_path):
    try:
        client.upsert(
            collection_name="image_captions",
            points=[
                PointStruct(
                    id = id,
                    vector = embedding.tolist(),
                    payload = {
                        "caption": caption,
                        "image_path": image_path
                    }
                )
            ]
        )
        print("Stored caption and embedding in Qdrant.")
    except Exception as e:
        print(f"Error inserting to Qdrant: {e}")

def query_qdrant(embedding, top_k=3):
    try:
        search_result = client.query_points(
            collection_name="image_captions",
            query=embedding.tolist(),
            with_payload=True,
            limit=top_k
        ).points

        return search_result
    except Exception as e:
        print(f"Error querying Qdrant: {e}")
        return []