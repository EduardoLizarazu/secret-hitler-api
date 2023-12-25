from fastapi import FastAPI
from uvicorn import run
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Configuración de CORS para permitir todas las solicitudes desde http://127.0.0.1:5500
origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory data store
allowed_vote = False

# fake_votes_db = {
#     "allies" : 0,
#     "nazi" : 0,
# }

fake_votes_db = {}

class VoteUpdate(BaseModel):
    user: str
    vote: bool

class AllowedVote(BaseModel):
    allowed: bool

class ResetVote(BaseModel):
    reset: bool

@app.get("/votes/results")
def read_votes():
    true_count = 0
    false_count = 0

    for valor in fake_votes_db.values():
        if isinstance(valor, bool):
            if valor:
                true_count += 1
            else:
                false_count += 1
    return {"dict": fake_votes_db,"allies": true_count, "nazi": false_count}

@app.delete("/votes/reset")
def reset_vote():
    global allowed_vote
    fake_votes_db = {}
    allowed_vote = False
    return {"votes": fake_votes_db}

@app.put("/votes/start")
def started_vote(data: AllowedVote):
    global allowed_vote
    allowed_vote = bool(data.allowed)
    return {"allowed": allowed_vote}

@app.put("/votes")
def update_votes(data: VoteUpdate):
    vote_value = bool(data.vote)  # Convertir a minúsculas para manejar "True" o "False"

    if allowed_vote:
        if isinstance(vote_value, bool):
            fake_votes_db.update({str(data.user) : vote_value})
            return False
        else:
            return {"error": "El valor 'vote' debe ser 'True' o 'False'"}
    else:
        return {"error": "AUN NO SE HA INICIADO LA VOTACION!!!"}


if __name__ == "__main__":
    # , host="0.0.0.0"
    run("main:app", port=8000)
