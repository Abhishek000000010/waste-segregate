from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import io
import logging
import os

# Setup logging
logging.basicConfig(
    filename='backend.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Waste Segregate API", version="1.0.0")

# ─────────────────────────────────────────────────────────────
# Demo Mode Flag
# ─────────────────────────────────────────────────────────────

DEMO_MODE = False  # Changed to False to debug real detection


# ─────────────────────────────────────────────────────────────
# CORS enabled for frontend
# ─────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────
# Load YOLOv8 Model (with fallback)
# ─────────────────────────────────────────────────────────────

model = None

try:
    from ultralytics import YOLO
    model = YOLO("yolov8n.pt")
    print("✅ YOLOv8 model loaded successfully.")
except Exception as e:
    print(f"⚠️ Failed to load YOLOv8 model: {e}")
    pass  # Model will be None, DEMO_MODE will handle it


# ─────────────────────────────────────────────────────────────
# Bin Mapping Rules (Dry, Wet, Hybrid/Hazardous)
# ─────────────────────────────────────────────────────────────

BIN_MAPPING = {
    # ─── Dry / Recyclable ───
    "bottle": "Recycle",
    "can": "Recycle",
    "cup": "Recycle",
    "wine glass": "Recycle",
    "vase": "Recycle",
    "book": "Recycle",
    "paper": "Recycle",

    # ─── Wet / Organic ───
    "banana": "Organic",
    "apple": "Organic",
    "orange": "Organic",
    "broccoli": "Organic",
    "carrot": "Organic",
    "hot dog": "Organic",
    "pizza": "Organic",
    "donut": "Organic",
    "cake": "Organic",
    "sandwich": "Organic",
    "food": "Organic",
    "potted plant": "Organic",

    # ─── Dry / Non-Recyclable (Landfill) ───
    "plastic bag": "Landfill",
    "handbag": "Landfill",
    "backpack": "Landfill",
    "suitcase": "Landfill",
    "umbrella": "Landfill",
    "tie": "Landfill",

    # ─── Hazardous / Hybrid (E-waste) ───
    "cell phone": "Hazardous",
    "laptop": "Hazardous",
    "mouse": "Hazardous",
    "keyboard": "Hazardous",
    "remote": "Hazardous",
    "microwave": "Hazardous",
    "oven": "Hazardous",
    "toaster": "Hazardous",
    "tv": "Hazardous",
    "refrigerator": "Hazardous",
    "scissors": "Hazardous", # Sharp object
    "knife": "Hazardous",    # Sharp object
}

# Items that indicate wet waste / contamination for dry bins
CONTAMINATION_ITEMS = {
    "banana", "apple", "orange", "broccoli", "carrot",
    "hot dog", "pizza", "donut", "cake", "sandwich", "food",
    "potted plant"
}


# ─────────────────────────────────────────────────────────────
# Pydantic Models
# ─────────────────────────────────────────────────────────────

class BoundingBox(BaseModel):
    x: int
    y: int
    w: int
    h: int


class DetectedItem(BaseModel):
    id: int
    itemType: str
    bin: str
    contaminated: bool
    confidence: float
    bbox: BoundingBox
    metadata: dict = {}


class DetectionResponse(BaseModel):
    items: list[DetectedItem]


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str
    binSuggestion: str = "Landfill" # Default


# ─────────────────────────────────────────────────────────────
# Fallback Demo Data
# ─────────────────────────────────────────────────────────────

FALLBACK_DEMO_RESPONSE = DetectionResponse(
    items=[
        DetectedItem(
            id=1,
            itemType="Plastic Bottle",
            bin="Recycle",
            contaminated=False,
            confidence=0.95,
            bbox=BoundingBox(x=50, y=80, w=100, h=180),
            metadata={
                "transformation": "Shredded into flakes and spun into high-performance polyester fibers for sustainable apparel.",
                "impact": "Recycling one ton of PET bottles saves 3.8 barrels of oil.",
                "fun_fact": "It takes about 5 plastic bottles to make enough fiber for one extra-large T-shirt."
            }
        ),
        DetectedItem(
            id=2,
            itemType="Banana Peel",
            bin="Organic",
            contaminated=True,
            confidence=0.88,
            bbox=BoundingBox(x=200, y=120, w=120, h=80),
            metadata={
                "transformation": "Heated in an anaerobic digester to produce methane gas for green electricity and nutrient-rich bio-fertilizer.",
                "impact": "Organic waste in landfills is a major source of methane; composting reduces this 100%.",
                "fun_fact": "Banana peels can be used to polish leather shoes and silver jewelry!"
            }
        ),
    ]
)


# ─────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────

def get_bin_for_item(class_name: str) -> str:
    return BIN_MAPPING.get(class_name.lower(), "Landfill")


def is_contaminated(class_name: str) -> bool:
    return class_name.lower() in CONTAMINATION_ITEMS


# ─────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    """Health check endpoint - always returns ok"""
    return {"status": "ok"}


# ─────────────────────────────────────────────────────────────
# Google Gemini Setup
# ─────────────────────────────────────────────────────────────

from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY, transport='rest')
    
    # Dynamically find the best working model for this specific key
    print("📡 Discovering available Gemini models...")
    available_models = []
    try:
        # Sort models to prefer flash/pro first in the discovery loop
        all_models = list(genai.list_models())
        preferences = ['2.5-flash', '2.0-flash', '1.5-flash', 'pro', 'flash']
        all_models.sort(key=lambda x: next((i for i, p in enumerate(preferences) if p in x.name.lower()), 999))
        
        for m in all_models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"🔬 Testing candidate: {m.name}...")
                try:
                    import time
                    time.sleep(0.5) # Avoid hitting discovery API rate limits
                    test_m = genai.GenerativeModel(m.name)
                    # Very tiny test to verify key permissions for this model
                    test_m.generate_content("hi") 
                    print(f"✅ Verified working: {m.name}")
                    available_models.append(m.name)
                    # Once we find a good flash or pro model, we can stop to save time
                    if "flash" in m.name or "pro" in m.name:
                        break
                except Exception as test_err:
                    print(f"❌ {m.name} failed verification: {test_err}")
                    continue
    except Exception as e:
        print(f"⚠️ Could not list models: {e}")
        available_models = ['models/gemini-1.5-flash', 'models/gemini-pro', 'gemini-1.5-flash']

    model_to_use = available_models[0] if available_models else None
        
    if model_to_use:
        gemini_model = genai.GenerativeModel(model_to_use)
        print(f"🚀 Eco-Scrutinize AI ACTIVE using: {model_to_use}")
    else:
        gemini_model = None
        print("❌ CRITICAL: No working AI models found for this API key.")
    
except Exception as e:
    gemini_model = None
    logger.error(f"❌ Gemini Discovery Failed: {str(e)}")
    print(f"❌ Gemini Discovery Error: {e}")


@app.post("/detect", response_model=DetectionResponse)
async def detect_waste(image: UploadFile = File(...)):
    """
    Detect waste items using Gemini (primary) or YOLO (fallback).
    """
    print(f"📥 Received detection request: {image.filename} ({image.content_type})")
    
    # Read image
    try:
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        logger.info(f"Image read successful: {image.filename}")
    except Exception as e:
        logger.error(f"Image read failed: {e}")
        if DEMO_MODE: return FALLBACK_DEMO_RESPONSE
        return DetectionResponse(items=[])

    # ─── STRATEGY 1: GEMINI AI (Accurate) ───
    if gemini_model and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
        try:
            logger.info("🧠 Requesting Gemini Pro analysis...")
            prompt = """
            Look at this image. Identify all visible waste items.
            
            Act as a Sustainability Expert. Categorize each item into Recycle, Organic, Hazardous, or Landfill.
            
            Return a JSON object with this EXACT structure:
            {
                "items": [
                    {
                        "itemType": "Name (e.g. Plastic Water Bottle)",
                        "bin": "Recycle" or "Organic" or "Hazardous" or "Landfill",
                        "contaminated": boolean,
                        "confidence": 0.95,
                        "metadata": {
                            "transformation": "One sentence on what this becomes after recycling.",
                            "impact": "One specific impact statistic.",
                            "fun_fact": "A short, interesting fact about this material."
                        }
                    }
                ]
            }
            
            IMPORTANT:
            - Identify EVERY item visible if possible.
            - If no waste is visible, return an empty items list.
            - Even if multiple items of same type exist (like 3 bottles), list them as separate items or a single aggregate item with count.
            - BE BOLD: If it looks like plastic, it's a plastic item for recycling.
            - Always prefer the full JSON structure.
            """
            
            response = gemini_model.generate_content([prompt, pil_image])
            content = response.text
            print(f"📄 Detection Raw Gemini: {content}")
            
            # Robust extraction
            import json
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(content)
            
            # Convert to our internal model
            detected_items = []
            for i, item in enumerate(data.get("items", [])):
                meta = item.get("metadata", {})
                
                detected_items.append(DetectedItem(
                    id=i+1,
                    itemType=item["itemType"],
                    bin=item["bin"],
                    contaminated=item.get("contaminated", False),
                    confidence=item.get("confidence", 0.9),
                    bbox=BoundingBox(x=0, y=0, w=0, h=0),
                    metadata=meta
                ))
            
            if detected_items:
                print(f"✅ Gemini Found: {[d.itemType for d in detected_items]}")
                return DetectionResponse(items=detected_items)
            else:
                print("🧠 Gemini returned empty items list.")
                
        except Exception as e:
            print(f"❌ Gemini Error type: {type(e).__name__}")
            print(f"❌ Gemini Error message: {str(e)}")
            # If it's a safety filter or quota error, we want to know


    # ─── STRATEGY 2: YOLOv8 (Fallback) ───
    if model:
        try:
            print("🚀 Starting YOLOv8 inference...")
            results = model(pil_image, device="cpu", verbose=False)
            
            detected_items = []
            for result in results:
                for box in result.boxes:
                    try:
                        conf = float(box.conf[0])
                        if conf < 0.25: continue
                        
                        class_id = int(box.cls[0])
                        class_name = model.names[class_id]

                        # 🛑 EXPLICIT FILTER: Ignore people
                        if class_name.lower() in ['person', 'face', 'hand', 'man', 'woman']:
                            continue
                        
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        
                        # Enrich with basic metadata for YOLO findings
                        item_meta = {
                            "transformation": f"Can be processed into raw material for new {class_name} manufacturing.",
                            "impact": f"Recycling {class_name} saves energy compared to producing from virgin materials.",
                            "fun_fact": f"High quality {class_name} recovery is essential for a circular economy."
                        }

                        detected_items.append(DetectedItem(
                            id=len(detected_items) + 1,
                            itemType=class_name.capitalize(),
                            bin=get_bin_for_item(class_name),
                            contaminated=is_contaminated(class_name),
                            confidence=conf,
                            bbox=BoundingBox(x=int(x1), y=int(y1), w=int(x2-x1), h=int(y2-y1)),
                            metadata=item_meta
                        ))
                    except: continue
            
            if detected_items:
                detected_items.sort(key=lambda x: x.confidence, reverse=True)
                return DetectionResponse(items=detected_items[:3])
            
            print("🚀 YOLO found nothing.")
            
        except Exception as e:
            print(f"❌ YOLO Error: {e}")

    if DEMO_MODE:
        print("🎁 Returning FALLBACK_DEMO_RESPONSE")
        return FALLBACK_DEMO_RESPONSE
    return DetectionResponse(items=[])


@app.post("/chat", response_model=ChatResponse)
async def chat_assistant(request: ChatRequest):
    """
    AI Assistant to answer waste related questions using Gemini.
    """
    if not gemini_model or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        return ChatResponse(
            response="I'm currently in offline mode. Please check my API configuration.",
            binSuggestion="Landfill"
        )

    try:
        prompt = f"""
        You are 'Eco-Scrutinize AI', a friendly and expert sustainability assistant.
        The user is asking: "{request.query}"
        
        Provide a concise, helpful answer (max 3 sentences). 
        Identify if they are asking about a specific item and suggest the correct bin.
        
        Return your answer in this JSON format:
        {{
            "response": "Your helpful advice here.",
            "binSuggestion": "Recycle" or "Organic" or "Hazardous" or "Landfill"
        }}
        """
        
        response = gemini_model.generate_content(prompt)
        content = response.text
        print(f"📄 Raw Gemini Response: {content}")
        
        # Robust JSON extraction
        import json
        import re
        
        try:
            # Try to find JSON block
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(content)
        except Exception as json_err:
            print(f"⚠️ JSON Parse Error: {json_err}")
            # Fallback if AI didn't return JSON
            return ChatResponse(
                response=content.strip()[:200], # Just return raw text if small
                binSuggestion="Landfill"
            )
        
        return ChatResponse(
            response=data.get("response", "I'm here to help!"),
            binSuggestion=data.get("binSuggestion", "Landfill")
        )
    except Exception as e:
        error_str = str(e)
        print(f"❌ Chat Assistant Error: {error_str}")
        
        if "429" in error_str or "ResourceExhausted" in error_str:
            friendly_err = "I'm a bit overwhelmed with requests right now. Please wait about 60 seconds and try again!"
        elif "404" in error_str:
            friendly_err = "I'm having trouble finding my knowledge base. (Error 404)"
        else:
            friendly_err = f"I'm having trouble connecting to my brain. (Detail: {error_str[:50]})"
            
        return ChatResponse(
            response=friendly_err,
            binSuggestion="Landfill"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
