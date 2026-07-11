"""OBSCURA — API de génération de vidéos d'horreur françaises."""
import uuid, time, threading
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

HERE = Path(__file__).parent
STATIC = HERE / "static"
JOBS = {}

app = FastAPI(title="OBSCURA", docs_url="/api/docs")

class GenerateRequest(BaseModel):
    prompt: str
    voice: str = "fr-FR-HenriNeural"

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0"}

@app.post("/api/generate")
async def generate(req: GenerateRequest):
    if len(req.prompt.strip()) < 10:
        raise HTTPException(400, "Prompt trop court (min 10 caractères)")
    job_id = uuid.uuid4().hex[:12]
    JOBS[job_id] = {"status": "queued", "prompt": req.prompt, "voice": req.voice, "created": time.time()}
    t = threading.Thread(target=_run, args=(job_id, req.prompt, req.voice), daemon=True)
    t.start()
    return {"job_id": job_id, "status": "queued", "message": "Génération lancée"}

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(404, "Job introuvable")
    return {k: v for k, v in job.items() if k != "error"}

@app.get("/api/download/{job_id}")
async def download(job_id: str):
    job = JOBS.get(job_id)
    if not job or job.get("status") != "done":
        raise HTTPException(404, "Vidéo pas encore prête")
    path = job.get("path")
    if not path or not Path(path).exists():
        raise HTTPException(404, "Fichier introuvable")
    return FileResponse(path, media_type="video/mp4", filename=f"obscura_{job_id}.mp4")

app.mount("/static", StaticFiles(directory=str(STATIC), html=True), name="static")

@app.get("/")
async def index():
    return FileResponse(STATIC / "index.html", media_type="text/html")

def _run(job_id, prompt, voice):
    try:
        JOBS[job_id]["status"] = "generating"
        from generator import generate_video_from_prompt
        r = generate_video_from_prompt(prompt, voice)
        JOBS[job_id].update({"status": "done", "path": r["path"], "duration": r["duration_sec"]})
    except Exception as e:
        JOBS[job_id].update({"status": "error", "error": str(e)})

if __name__ == "__main__":
    import os, uvicorn
    port = int(os.environ.get("PORT", 8000))
    print("\033[91m" + "="*50)
    print(f"  OBSCURA — http://0.0.0.0:{port}")
    print("  API docs — http://0.0.0.0:{port}/api/docs")
    print("="*50 + "\033[0m")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
