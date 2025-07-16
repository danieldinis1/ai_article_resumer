from fastapi import FastAPI
from agents.extract import summarize_and_review
from model.article_request import ArticleRequest
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return  [ {"id": 1, "title": "Post One"},
        {"id": 2, "title": "Post Two"}]


@app.post("/resume")
async def summarize_endpoint(request: ArticleRequest):
    result = summarize_and_review(request.url)
    return result