from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, Response
import numpy as np
import cv2
import base64

from .styles import (
    outline_style,
    pencil_style,
    shadow_style,
    bold_style
)
from .utils import adjust_brightness_contrast, image_to_bytes
from .ai_stable import generate_impressionist

app = FastAPI(title="AI Stencil Generator")


# 🔥 Map Figma UI labels → backend function keys
STYLE_MAP = {
    "outline": "outline",
    "pencil sketch": "pencil",
    "pencil": "pencil",
    "shadows": "shadows",
    "shadow": "shadows",
    "bold": "bold",
    "impressionist": "impressionist"
}


@app.post("/generate-stencil")
async def generate_stencil(
    file: UploadFile = File(...),
    style: str = Form(...),
    brightness: float = Form(0),
    contrast: float = Form(1.0)
):
    try:
        # Normalize style string
        style_clean = style.strip().lower()
        style_key = STYLE_MAP.get(style_clean)

        if not style_key:
            return JSONResponse(
                {"error": f"Style '{style}' not supported"},
                status_code=400
            )

        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return JSONResponse(
                {"error": "Invalid image file"},
                status_code=400
            )

        # Apply brightness & contrast
        image = adjust_brightness_contrast(image, brightness, contrast)

        # ===== LOCAL STYLES =====
        if style_key == "outline":
            result = outline_style(image)
            return Response(
                content=image_to_bytes(result),
                media_type="image/png"
            )

        elif style_key == "pencil":
            result = pencil_style(image)
            return Response(
                content=image_to_bytes(result),
                media_type="image/png"
            )

        elif style_key == "shadows":
            result = shadow_style(image)
            return Response(
                content=image_to_bytes(result),
                media_type="image/png"
            )

        elif style_key == "bold":
            result = bold_style(image)
            return Response(
                content=image_to_bytes(result),
                media_type="image/png"
            )

        # ===== AI STYLE (Stability AI) =====
        elif style_key == "impressionist":
            _, buffer = cv2.imencode(".png", image)
            image_bytes = buffer.tobytes()

            api_response = await generate_impressionist(image_bytes)

            img_b64 = api_response["image"]
            result_bytes = base64.b64decode(img_b64)

        return Response(
        content=result_bytes,
        media_type="image/png"
    )

    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )