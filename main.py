"""
Defines a simple API which accepts a URL, scrapes all text from the page content of the URL, and passes off to the OpenAI API using a summarization prompt
to generate a summary of the page content. The summary is then returned to the user.

The API is defined using FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import os
import openai

from pydantic import BaseModel


class Request(BaseModel):
    url: str

app = FastAPI()


@app.post("/summarize")
async def summarize(request: Request):
    url = request.url
    print(f"Received request to summarize: {url}")
    # Configure an OpenAI client using an API key from the environment
    openai.api_key = os.getenv("OPENAI_TOKEN")
    # Get the page content from the URL
    page_content = get_page_content(url)
    # Generate a summary of the page content
    summary = generate_summary(page_content)
    # Return the summary to the user
    return JSONResponse(content=jsonable_encoder(summary))

def get_page_content(url):
    """
    Scrapes all text from the page content of the URL using the requests library.
    """
    import requests
    from bs4 import BeautifulSoup

    page = requests.get(url, headers={
        # Some websites return 403 if you try and hit it with a non-browser useragent
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    })
    soup = BeautifulSoup(page.content, "html.parser")
    page_content = soup.get_text()
    print(f"Page content: {page_content}")
    return page_content

def generate_summary(page_content):
    """
    Uses the OpenAI API to generate a summary of the page content using a summarization prompt.
    """

    # Trim the page_content to try and avoid hitting the OpenAI API limit
    page_content = page_content[:10000]
    print(f"Page content (trimmed): {page_content}")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a summarization assistant. The user provides text dumped from Python BeautifulSoup.get_text() and you summarize it. You will be as concise as possible while maintaining accuracy and grammatical correctness."},
            {"role": "user", "content": page_content},
    ])

    summary = completion.choices[0].message["content"].strip()
    return summary
