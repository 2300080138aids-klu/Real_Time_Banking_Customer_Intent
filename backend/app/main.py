from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(
    title="Banking Intent Triage Engine",
    description="Hybrid retrieval + transformer-based banking intent detection system",
    version="1.0.0"
)

# ---------------- CORS CONFIG ----------------
# Allow frontend (Vite) to communicate with backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROUTES ----------------

app.include_router(router)


# ---------------- ROOT ENDPOINT ----------------

@app.get("/")
def root():
    return {
        "message": "Banking Intent Triage API is running",
        "status": "OK"
    }


# ---------------- HEALTH CHECK ----------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }