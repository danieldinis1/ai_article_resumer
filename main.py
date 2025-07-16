from fastapi import FastAPI
from agents.extract import summarize_and_review
from model.article_request import ArticleRequest

app = FastAPI()

@app.post("/resume")
async def summarize_endpoint(request: ArticleRequest):
    result = summarize_and_review(request.url)
    return result