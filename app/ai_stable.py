import os
from urllib import response 
import httpx
from dotenv import load_dotenv

load_dotenv
API_KEY =  os.getenv("STABILITY_API_KEY")
STABILITY_URL = "https://api.stability.ai/v1/generation/stable-diffusion-img2img"

async def generate_impressionist(image_bytes: bytes, strength: float = 0.8):
    async with httpx.AsyncClient(timeout=120) as client:
        responce = await client.post(
            STABILITY_URL,
            headers={
                "Authorization": f"Bearer{API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "init_image": image_bytes.decode("latin1"),
                "cfg_scale": 7,
                "denoising_strength": strength,
                "samples": 1,
                "style_preset": "enhance"
            }
        )
        if response.status_code != 200:
            raise Exception(f"Stability API error:{responce.text}")
        return responce.json()