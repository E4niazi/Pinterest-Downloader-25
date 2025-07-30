from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# CORS settings for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use your frontend domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Pinterest Downloader API is running."}

@app.get("/api/download")
async def download_pinterest(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')

        video = soup.find('video')
        image = soup.find('img')

        if video and video.get("src"):
            return {"type": "video", "url": video['src']}
        elif image and image.get("src"):
            return {"type": "image", "url": image['src']}
        else:
            return {"error": "No downloadable media found."}
    except Exception as e:
        return {"error": str(e)}
