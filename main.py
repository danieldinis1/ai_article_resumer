from fastapi import FastAPI, HTTPException
from agents.extract import summarize_and_review
from model.article_request import ArticleRequest
from fastapi.middleware.cors import CORSMiddleware

## run -> fastapi dev main.py
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
    if not await is_valid_url(request.url):
        raise HTTPException(
            status_code=400,
            detail="Invalid URL. Please provide a valid Wikipedia URL starting with http, https, or www."
        )    
    result = summarize_and_review(request.url)
    return result


async def is_valid_url(url: str) -> bool:
    if (url.startswith("http://") or
        url.startswith("https://") or
        url.startswith("www.")) and "wikipedia" in url:
        return True
    else:
        return False