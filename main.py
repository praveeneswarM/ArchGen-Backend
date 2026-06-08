import os
import logging
import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Database and Routing modules
from utils.db import db_manager
from routes.api import router as api_router
from routes.auth import router as auth_router
from routes.projects import router as projects_router

load_dotenv()

app = FastAPI(
    title="ArchGen AI SaaS Backend",
    description="Autonomous Agentic AI Cloud Architecture Studio Orchestrator Server",
    version="1.0.0"
)

# Enable CORS for Next.js frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Global Exception caught: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "error_message": str(exc)},
    )

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    logging.info("Request started %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
    except Exception:
        logging.exception("Unhandled exception while processing %s %s", request.method, request.url.path)
        raise
    duration_ms = (time.perf_counter() - start_time) * 1000
    logging.info(
        "Request completed %s %s %s %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response

# Startup MongoDB connection hook
@app.on_event("startup")
async def startup_db_client():
    await db_manager.connect_to_database()

# Shutdown MongoDB connection hook
@app.on_event("shutdown")
async def shutdown_db_client():
    await db_manager.close_database_connection()

# Health status check
@app.get("/")
async def health_check():
    return {
        "status": "healthy",
        "service": "ArchGen AI SaaS Orchestrator",
        "version": "1.0.0",
        "database": "connected" if db_manager.db is not None else "disconnected"
    }

# Register SaaS sub-routers under prefix
app.include_router(auth_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    print(f"Starting ArchGen AI backend on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
