# GPT-3.5 Summarizer Shortcut ⚡️

This repository contains the code for a webpage summariziation app that can be deployed directly onto a serverless hosting platform, such as 
[Digital Ocean App Platform](https://www.digitalocean.com/products/app-platform) or [Heroku](https://www.heroku.com/).

## Usage

The app uses the excellent [FastAPI](https://github.com/tiangolo/fastapi) to provide a small endpoint that accepts a URL, 
uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to extract text from the webpage, and sends
that to OpenAI's [ChatCompletions](https://platform.openai.com/docs/guides/chat) service to create a succinct summary.

E.g. let's say that you have deployed this repo as an app available at `https://summaries.app.dev`, you would send requests that look like


```
POST https://summaries.app.dev/summarize

Content-Type: application/json

{
  "url": "https://github.com/stallionlabs/summarizer-app/blob/main/README.md"
}
```

The response will be string containing the summary, that's it!

## Deployment

TODO
