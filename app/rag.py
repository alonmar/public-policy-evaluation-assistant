from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForCausalLM,
)
import json
import os

import time
import torch
import streamlit as st


load_dotenv()


ELASTIC_URL = os.getenv("ELASTIC_URL_LOCAL")
MODEL_NAME = os.getenv("MODEL_NAME")
INDEX_NAME = os.getenv("INDEX_NAME")
HUGGINGFACE_API = os.getenv("HUGGINGFACE_API")


if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"


@st.cache_resource
def load_model_generation():
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-3.2-1B-Instruct",
        device_map=device,
        torch_dtype="auto",
        trust_remote_code=True,
        token=HUGGINGFACE_API,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Llama-3.2-1B-Instruct",
        token=HUGGINGFACE_API,
    )
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )
    return pipe


@st.cache_resource
def load_sentence_transformer():
    return SentenceTransformer(MODEL_NAME)


pipe_generation = load_model_generation()
model = load_sentence_transformer()


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def elastic_search_knn(
    field,
    vector,
    # course,
    index_name=INDEX_NAME,
):
    es_client = Elasticsearch(ELASTIC_URL)

    knn = {
        "field": field,
        "query_vector": vector,
        "k": 5,
        "num_candidates": 10000,
        # "filter": {"term": {"course": course}},
    }

    search_query = {
        "knn": knn,
        "_source": ["doc_id", "page_num", "chunk_id", "text"],
    }

    es_results = es_client.search(index=index_name, body=search_query)

    return [hit["_source"] for hit in es_results["hits"]["hits"]]


def build_prompt(query, search_results):
    prompt_template = """
As a housing policy expert advising policymakers, answer the QUESTION below using only the verified information provided in the CONTEXT.
Maintain a neutral, factual tone, and avoid assumptions or extrapolations beyond the CONTEXT.
Structure your response with a brief summary of pros and cons to support balanced decision-making, and keep the response as concise as possible.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

    context = "\n\n".join(
        [f"doc_id: {doc['doc_id']}\nanswer: {doc['text']}" for doc in search_results]
    )
    return prompt_template.format(question=query, context=context).strip()


def llm(prompt):
    # return {"answer": "test", "time": 0.0}
    start_time = time.time()
    messages = [
        {"role": "user", "content": prompt},
    ]

    eos_token_id = pipe_generation.tokenizer.eos_token_id

    generation_args = {
        "max_new_tokens": 500,
        "return_full_text": False,
        # "temperature": 0.0,
        "do_sample": False,
        "pad_token_id": eos_token_id,
    }

    output = pipe_generation(messages, **generation_args)

    answer = output[0]["generated_text"].strip()

    end_time = time.time()
    response_time = end_time - start_time

    return {"answer": answer, "time": response_time}


def rag(query):
    search_results = elastic_search_knn("text_vector", model.encode(query))
    prompt = build_prompt(query, search_results)
    return llm(prompt)
