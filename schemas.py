from pydantic import BaseModel

class SessionRequest(BaseModel):
    playlist_id: str
    session_name: str

class RankingRequest(BaseModel):
    session_name: str
    winner: int

class MessageRequest(BaseModel):
    message: str
    session_name: str
