from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

stored_word = {"value": None}

class WordRequest(BaseModel):
    word: str

@app.post("/set-word")
def set_word(req: WordRequest):
    word = req.word.strip()
    if len(word) < 3:
        raise HTTPException(status_code=400, detail="Word must be at least 3 letters.")
    stored_word["value"] = word
    return {"message": "Word saved", "word": word}

@app.get("/jumble")
def jumble(seed: int = 0):
    word = stored_word["value"]
    if word is None:
        raise HTTPException(status_code=400, detail="No word has been set yet.")
    chars = list(word)
    random.seed(seed)
    random.shuffle(chars)
    return {"original": word, "jumbled": ''.join(chars)}
