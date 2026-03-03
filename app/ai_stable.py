import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("STABILITY_API_KEY")

STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/ultra"


async def generate_impressionist(image_bytes: bytes):
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            STABILITY_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Accept": "application/json"
            },
            files={
                "image": ("image.png", image_bytes, "image/png")
            },
            data={
                "model": "ultra",
                "prompt": "impressionist oil painting, artistic brush strokes, vibrant colors",
                "strength": "0.6",
                "output_format": "png"
            }
        )

        if response.status_code != 200:
            raise Exception(f"Stability API error: {response.text}")

        return response.json()