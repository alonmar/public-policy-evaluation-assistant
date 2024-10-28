from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import json
import os

from tqdm.auto import tqdm


load_dotenv()


ELASTIC_URL = os.getenv("ELASTIC_URL_LOCAL")
MODEL_NAME = os.getenv("MODEL_NAME")
INDEX_NAME = os.getenv("INDEX_NAME")
HUGGINGFACE_API = os.getenv("HUGGINGFACE_API")


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def load_mode():
    print(f"Loading model: {MODEL_NAME}")
    return SentenceTransformer(MODEL_NAME)


def fetch_documents():
    print("Fetching documents...")

    directory_path = "json_data"

    # List all files in the directory
    files = os.listdir(directory_path)

    documents = []
    for file in files:
        print(f"Reading file: {file}")
        data = read_json(f"{directory_path}/{file}")
        documents.extend(data)
        print(f"Fetched {len(documents)} documents")
    return documents


def setup_elasticsearch(model):
    print("Setting up Elasticsearch...")
    es_client = Elasticsearch(ELASTIC_URL)

    index_settings = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "doc_id": {"type": "keyword"},
                "page_num": {"type": "integer"},
                "chunk_id": {"type": "keyword"},
                "text": {"type": "text"},
                "text_vector": {
                    "type": "dense_vector",
                    "dims": model.get_sentence_embedding_dimension(),
                    "index": True,
                    "similarity": "cosine",
                },
            }
        },
    }

    es_client.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    es_client.indices.create(index=INDEX_NAME, body=index_settings)
    print(f"Elasticsearch index '{INDEX_NAME}' created")
    return es_client


def index_documents(es_client, documents, model):
    print("Indexing documents...")
    for doc in tqdm(documents):
        doc["text_vector"] = model.encode(doc["text"]).tolist()
        es_client.index(index=INDEX_NAME, document=doc)
    print(f"Indexed {len(documents)} documents")


def init_elasticsearch():
    model = load_mode()
    documents = fetch_documents()
    es_client = setup_elasticsearch(model)
    index_documents(es_client, documents, model)


if __name__ == "__main__":
    init_elasticsearch()
