from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import campaigns, insights, status

app = FastAPI(
    title="Claude VPS — Meta Ads Remote Control",
    description="API to manage and monitor Meta Ads campaigns from DaybyDay agency VPS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(status.router)
app.include_router(campaigns.router)
app.include_router(insights.router)


@app.get("/")
def root():
    return {
        "service": "claude-vps",
        "docs": "/docs",
        "health": "/status/health",
    }
