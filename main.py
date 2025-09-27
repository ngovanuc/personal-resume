import os
import sys
import warnings
import uuid
import traceback
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from argon2 import PasswordHasher

import fastapi
from fastapi import FastAPI, Depends, Form, HTTPException, status, Request, Cookie, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse, Response, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import time


# warnings.filterwarnings("ignore")
# os.system("cls")
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Personal Resume Website",
    description="AI Engineer & Researcher Portfolio",
    version="1.0.0",
    # Optimization for high concurrency
    docs_url="/docs" if os.getenv("ENV") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENV") != "production" else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} | Time: {process_time:.4f}s")
    
    response.headers["X-Process-Time"] = str(process_time)
    return response


templates = Jinja2Templates(directory=["templates"])
app.mount("/public", StaticFiles(directory="public"), name="public")
app.mount("/me", StaticFiles(directory="me"), name="me")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """ Home Page """
    return templates.TemplateResponse(
        "/resume/home.html", 
        {
            "request": request
        }
    )

@app.get("/resume", response_class=HTMLResponse)
async def resume(request: Request):
    """ Resume Page """
    return templates.TemplateResponse(
        "/resume/resume.html", 
        {
            "request": request
        }
    )

@app.get("/health")
async def health_check():
    """ Health check endpoint for Docker """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "uptime": time.time()
    }

@app.get("/api/info")
async def app_info():
    """ Application information endpoint """
    return {
        "name": "Personal Resume Website",
        "version": "1.0.0",
        "author": "NGO Van Uc",
        "description": "AI Engineer & Researcher Portfolio",
        "docker": True,
        "environment": os.getenv("ENV", "development")
    }

@app.get("/api/stats")
async def get_stats(request: Request):
    """ Get basic application stats """
    return {
        "timestamp": datetime.now().isoformat(),
        "client_ip": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "referer": request.headers.get("referer"),
        "host": request.headers.get("host"),
        "instance_id": os.getenv("INSTANCE_ID", "main"),
        "workers": os.getenv("WORKERS", 1)
    }

@app.get("/metrics")
async def metrics():
    """ Prometheus metrics endpoint """
    import psutil
    import os
    
    # Basic system metrics
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    
    return {
        "cpu_usage_percent": cpu_percent,
        "memory_usage_percent": memory.percent,
        "memory_available_mb": memory.available / 1024 / 1024,
        "instance_id": os.getenv("INSTANCE_ID", "main"),
        "pid": os.getpid(),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    workers = int(os.getenv("WORKERS", 4))  # Tăng workers
    instance_id = os.getenv("INSTANCE_ID", "main")
    
    print(f"Starting server [{instance_id}] on {host}:{port} with {workers} workers")
    
    # High-performance configuration
    uvicorn.run(
        "main:app",
        host=host, 
        port=port,
        workers=workers,
        access_log=True,
        reload=False,
        # High concurrency settings
        limit_concurrency=1000,  # Max concurrent connections
        limit_max_requests=1000000,  # Max requests before restart
        timeout_keep_alive=5,
        timeout_graceful_shutdown=30,
    )