from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils import *
from schemas import *
from math import log2, floor
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

@app.get("/")
async def root():
    return {"message": "Backend is ready!"}

@app.post("/start_session")
async def start_session(data: SessionRequest):
    try:
        session_name = data.session_name
        videos = register_session(data.playlist_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch videos: {e}")
    finally:
        results = []
        final_result = []
        result_arr = []
        first_arr = videos.pop()
        second_arr = videos.pop()
        first_video = first_arr.pop()
        second_video = second_arr.pop()
        initial_message = "Say hi to the user. You are a model that discusses with user about songs and only songs. Anything that is not related to music mustn't be discussed. For now, user haven't send any messages to you, but every user's message will be in the next format: 'prompt: user message'."
        model_response = send_message_to_model(initial_message)
        chat_history = [
            {
                "role": "user",
                "content": initial_message
            },
            {
                "role": "assistant",
                "content": model_response
            }
        ]
        sessions[session_name] = {
            "videos": videos,
            "results": results,
            "final_result": final_result,
            "result_arr": result_arr,
            "first_video": first_video,
            "second_video": second_video,
            "first_arr": first_arr,
            "second_arr": second_arr,
            "chat_history": chat_history,
            "progress": 0,
            "estimated_time": len(videos) * floor(log2(len(videos))),
            "finished": False,
        }
        return {
            "message": f"Session: {session_name} is ready!",
            "first_video": first_video,
            "second_video": second_video
        }

@app.post("/ranking")
async def session_make_step(data: SessionStepRequest):
    session_name = data.session_name
    winner = data.winner
    
    if session_name not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_name]

    if session["finished"]:
        return {"message": "Session is finished!"}

    session["progress"] += 1

    if winner:
        session["result_arr"].append(session["first_video"])
        session["second_arr"].append(session["second_video"])
    else:
        session["result_arr"].append(session["second_video"])
        session["first_arr"].append(session["first_video"])

    while len(session["first_arr"]) >= 1 and len(session["second_arr"]) == 0:
        session["result_arr"].append(session["first_arr"].pop())
    while len(session["second_arr"]) >= 1 and len(session["first_arr"]) == 0:
        session["result_arr"].append(session["second_arr"].pop())

    if len(session["first_arr"]) == 0 and len(session["second_arr"]) == 0:
        session["results"].append(session["result_arr"])
        session["result_arr"] = []  # Reset for next round
        
        if len(session["videos"]) > 1:
            session["first_arr"] = session["videos"].pop()
            session["second_arr"] = session["videos"].pop()
            session["first_video"] = session["first_arr"].pop()
            session["second_video"] = session["second_arr"].pop()
        elif len(session["videos"]) == 1:
            session["first_arr"] = session["videos"].pop()
            session["second_arr"] = session["results"].pop()
            session["first_video"] = session["first_arr"].pop()
            session["second_video"] = session["second_arr"].pop()
        else:
            session["videos"] = session["results"]
            session["results"] = []
            
            if len(session["videos"]) == 1:
                session["final_result"] = session["videos"][0]
                session["finished"] = True
                return {
                    "message": "Session is finished!",
                    "final_result": session["final_result"]
                }
            else:
                session["first_arr"] = session["videos"].pop()
                session["second_arr"] = session["results"].pop()
                session["first_video"] = session["first_arr"].pop()
                session["second_video"] = session["second_arr"].pop()
    else:
        session["first_video"] = session["first_arr"].pop()
        session["second_video"] = session["second_arr"].pop()

        return {
            "first_video": session["first_video"],
            "second_video": session["second_video"]
        }

@app.post("/send_message")
async def send_message(data: MessageRequest):
    session_name = data.session_name
    message = data.message
    session = sessions[session_name]
    chat_history = session["chat_history"]
    chat_history.append({
        "role": "user",
        "content": message
    })
    model_response = send_message_to_model(message)
    chat_history.append({
        "role": "assistant",
        "content": model_response
    })
    return {
        "message": "Message sent successfully!",
        "response": model_response
    }

@app.get("/get_chat_history")
async def get_chat_history(session_name: str):
    session = sessions[session_name]
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session["chat_history"]

@app.get("/get_session")
async def get_session(session_name: str):
    session = sessions[session_name]
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "videos": session["videos"],
        "final_result": session["final_result"],
        "progress": session["progress"],
        "finished": session["finished"],
        "chat_history": session["chat_history"]
    }
