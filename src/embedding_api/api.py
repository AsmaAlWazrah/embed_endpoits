from fastapi import FastAPI, HTTPException
import numpy as np
import re
import pyarabic.araby as arab
from transformers import pipeline
from sentence_transformers import SentenceTransformer

from src.utils.payloads import EmbeddingPayload


app = FastAPI()

# Initialize the feature extraction pipelines
electrapipeline = pipeline('feature-extraction', model='aubmindlab/araelectra-base-generator')
arabertpipeline = pipeline('feature-extraction', model='aubmindlab/bert-base-arabertv2')
camelpipeline = pipeline('feature-extraction', model='CAMeL-Lab/bert-base-arabic-camelbert-msa')
e5pipeline = pipeline('feature-extraction', model='intfloat/e5-large')

# Initialize SBERT models
sbert_models = {
    'electra': SentenceTransformer('aubmindlab/araelectra-base-generator'),
    'arabert': SentenceTransformer('aubmindlab/bert-base-arabertv2'),
    'camelbert': SentenceTransformer("CAMeL-Lab/bert-base-arabic-camelbert-msa"),
    'e5': SentenceTransformer('intfloat/e5-large')
}


def process_input(payload: EmbeddingPayload):
    text = payload.text
    model_choice = payload.model
    method = payload.method

    # Keep only Arabic characters and spaces
    token = re.sub(r"[^\u0600-\u06ff ]", "", text)
    # Remove diacritics (Tashkeel)
    token = arab.strip_tashkeel(token)

    embeddings = None
    if method == 'word' and len(text.split()) == 1:
        if model_choice == 'electra':
            embeddings = electrapipeline(token)[0][1]
        elif model_choice == 'arabert':
            embeddings = arabertpipeline(token)[0][1]
        elif model_choice == 'camelbert':
            embeddings = camelpipeline(token)[0][1]
        elif model_choice == 'e5':
            embeddings = e5pipeline(token)[0][1]
        else:
            raise HTTPException(status_code=400, detail="Invalid model choice for word method")
    elif method == 'average':
        if model_choice == 'electra':
            emb = electrapipeline(token)[0][1:-1]
            embeddings = np.mean(emb, axis=0).tolist()
        elif model_choice == 'arabert':
            emb = arabertpipeline(token)[0][1:-1]
            embeddings = np.mean(emb, axis=0).tolist()
        elif model_choice == 'camelbert':
            emb = camelpipeline(token)[0][1:-1]
            embeddings = np.mean(emb, axis=0).tolist()
        elif model_choice == 'e5':
            emb = e5pipeline(token)[0][1:-1]
            embeddings = np.mean(emb, axis=0).tolist()
        else:
            raise HTTPException(status_code=400, detail="Invalid model choice for average method")
    elif method == 'sbert':
        if model_choice in sbert_models:
            model = sbert_models[model_choice]
            embeddings = model.encode(text).tolist()
        else:
            raise HTTPException(status_code=400, detail="Invalid model choice for sbert method")
    else:
        if method == 'word' and len(text.split()) != 1:
            raise HTTPException(status_code=400, detail="Invalid text input choice for word method as its len is greater than one")
        raise HTTPException(status_code=400, detail="Invalid method")

    return {"text": text, "model": model_choice, "method": method, "embeddings": embeddings}


@app.post("/generate_embedding")
def generate_embedding(payload: EmbeddingPayload):
    try:
        result = process_input(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))