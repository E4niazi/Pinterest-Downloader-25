from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Pinterest Downloader is live."}

@app.get("/api/download")
async def download_pinterest(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        video = soup.find("video")
        image = soup.find("img")

        if video and video.get("src"):
            return {"type": "video", "url": video["src"]}
        elif image and image.get("src"):
            return {"type": "image", "url": image["src"]}
        else:
            return {"error": "Media not found"}
    except Exception as e:
        return {"error": str(e)}
