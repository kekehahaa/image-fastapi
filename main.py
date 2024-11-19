import uvicorn, os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.api.endpoints.files import file_router
from app.core.config import settings

app = FastAPI()
    
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
app.include_router(file_router)

if __name__ == "__main__":
    num_cores = os.cpu_count()
    uvicorn.run("main:app", host=settings.PROJECT_HOST, 
                port=settings.PROJECT_PORT)
    
    