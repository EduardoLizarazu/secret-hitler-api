from fastapi import FastAPI
from uvicorn import run
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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
fake_votes_db = {
    "allies" : 0,
    "nazi" : 0,
}

class VoteUpdate(BaseModel):
    vote: str

class AllowedVote(BaseModel):
    allowed: bool

class ResetVote(BaseModel):
    reset: bool

@app.get("/votes/results")
def read_votes():
    return {"votes": fake_votes_db}

@app.delete("/votes/reset")
def reset_vote():
    fake_votes_db["allies"] = 0
    fake_votes_db["nazi"] = 0
    allowed_vote = False
    return {"votes": fake_votes_db}


@app.put("/votes")
def update_votes(data: VoteUpdate):
    vote_value = data.vote.lower()  # Convertir a minúsculas para manejar "True" o "False"

    if allowed_vote:
        if vote_value == "true":
            fake_votes_db["allies"] += 1
        elif vote_value == "false":
            fake_votes_db["nazi"] += 1
        else:
            return {"error": "El valor 'vote' debe ser 'True' o 'False'"}
    else:
        pass
    return {"votes": fake_votes_db}

@app.put("/votes/start")
def started_vote(data: AllowedVote):
    allowed_vote = bool(data.allowed)
    return {"allowed": allowed_vote}

@app.delete("/votes/reset")
def reset_vote():
    fake_votes_db["allies"] = 0
    fake_votes_db["nazi"] = 0
    allowed_vote = False
    return {"votes": fake_votes_db}

if __name__ == "__main__":
    # , host="0.0.0.0"
    run("main:app", port=8000)
