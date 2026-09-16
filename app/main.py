from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.pipeline import analyze_notes, SummaryOutput

app = FastAPI(title="Testing Notes Summarizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NotesRequest(BaseModel):
    notes: str

@app.post("/api/analyze", response_model=SummaryOutput)
async def analyze_endpoint(request: NotesRequest):
    if not request.notes or not request.notes.strip():
        raise HTTPException(status_code=400, detail="Notes content cannot be empty.")
    
    try:
        result = analyze_notes(request.notes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}