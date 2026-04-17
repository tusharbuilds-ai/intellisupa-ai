from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import ask_agent
import os

class QueryRequest(BaseModel):
    question:str

app = FastAPI(title="IntelliSUPA AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/")
def home():
    with open("index.html",encoding="utf-8") as f:
        return HTMLResponse(f.read())
    
@app.post('/query')
async def query(request:QueryRequest,x_supabase_token:str = Header(None)):
    if not request.question.strip():
        raise HTTPException(status_code=400,detail="Question cannot be empty")
    
    token = x_supabase_token or os.getenv('SUPABASE_ACCESS_TOKEN')

    if not token:
        raise HTTPException(
            status_code=401,
            detail="No Supabase token found.Please add your token in Settings."
        )
    try:
        result = await ask_agent(request.question,token)
        return {"status":"success","answer":result}
    except Exception as e:
        raise HTTPException(status_code=505,detail=str(e))
    
app.get("/health")
def health():
    return {"status":"IntelliSupa running"}
    
