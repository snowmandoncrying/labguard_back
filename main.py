from fastapi import FastAPI
from router import manual

app = FastAPI()

app.include_router(manual.router) 