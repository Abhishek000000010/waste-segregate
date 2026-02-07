from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import io
import logging
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

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
    # Load model with absolute path for cloud stability
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "yolov8n.pt")
    model = YOLO(model_path)
    print(f"✅ YOLOv8 model loaded successfully from {model_path}.")
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
# Google Gemini Setup (with Multi-Key Rotation)
# ─────────────────────────────────────────────────────────────
from dotenv import load_dotenv
import random

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
# Support multiple keys separated by commas
RAW_KEYS = GEMINI_API_KEY.split(",")
GEMINI_KEYS = [k.strip() for k in RAW_KEYS if k.strip() and k.strip() != "YOUR_API_KEY_HERE"]
print(f"🔑 Loaded {len(GEMINI_KEYS)} Gemini keys from .env")
current_key_index = 0

def init_gemini_with_key(index):
    """Initializes the Gemini model with a specific key from the pool."""
    if index >= len(GEMINI_KEYS): return None
    key = GEMINI_KEYS[index]
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        
        # Determine the best model for this key
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Preference order for modern models
        preferences = [
            'models/gemini-1.5-flash', 
            'models/gemini-1.5-pro', 
            'models/gemini-pro',
            'models/gemini-2.0-flash-exp'
        ]
        
        selected_model = None
        for pref in preferences:
            for m in all_models:
                if pref == m:
                    selected_model = m
                    break
            if selected_model: break
            
        # Last resort fallback: any model with 'gemini' in its name
        if not selected_model:
            for m in all_models:
                if 'gemini' in m.lower():
                    selected_model = m
                    break
        
        if not selected_model:
            selected_model = 'models/gemini-1.5-flash' # Final hard fallback
            
        logger.info(f"📡 Selected model '{selected_model}' for Key #{index+1}")
        return genai.GenerativeModel(selected_model)
    except Exception as e:
        logger.error(f"⚠️ Initialization of Key #{index+1} failed: {e}")
        return None

# Initial Setup
gemini_model = init_gemini_with_key(current_key_index)

async def call_gemini_robust(prompt_data):
    """
    Tries to call Gemini's generate_content using all available keys.
    prompt_data can be a string (for chat) or a list (for detection with image).
    """
    global current_key_index, gemini_model
    
    last_error = ""
    # We will try every key in the list exactly once
    for _ in range(len(GEMINI_KEYS)):
        if not gemini_model:
            gemini_model = init_gemini_with_key(current_key_index)
            
        if gemini_model:
            try:
                # Actual call
                logger.info(f"🛰️ Calling Gemini with Key #{current_key_index+1}...")
                response = gemini_model.generate_content(prompt_data)
                return response.text
            except Exception as e:
                err_str = str(e).lower()
                last_error = f"Key #{current_key_index+1} error: {str(e)}"
                
                # Check for rate limit OR forbidden OR permission issues OR not found
                should_rotate = any(x in err_str for x in ["429", "quota", "exhausted", "403", "forbidden", "permission", "404", "not found", "invalid"])
                
                if should_rotate:
                    logger.warning(f"🔄 Rotating due to: {last_error}")
                    current_key_index = (current_key_index + 1) % len(GEMINI_KEYS)
                    gemini_model = init_gemini_with_key(current_key_index)
                else:
                    # If it's a completely different error, log it and try to rotate anyway just in case
                    logger.error(f"⚠️ Unexpected error with key #{current_key_index+1}: {str(e)}")
                    current_key_index = (current_key_index + 1) % len(GEMINI_KEYS)
                    gemini_model = init_gemini_with_key(current_key_index)
        else:
            # Current key failed init, move to next
            current_key_index = (current_key_index + 1) % len(GEMINI_KEYS)
            gemini_model = init_gemini_with_key(current_key_index)

    raise Exception(f"All Gemini API keys failed or are exhausted. Last error: {last_error}")

# ─────────────────────────────────────────────────────────────
# Smart Fallback Metadata for YOLO (Prevents repetitive text)
# ─────────────────────────────────────────────────────────────
FALLBACK_INSIGHTS = {
    "bottle": {
        "transformation": "Shredded into high-performance polyester fibers for eco-apparel and athletic wear.",
        "impact": "Recycling 1 ton of PET saves 3.8 barrels of oil.",
        "fun_fact": "It takes just 5 bottles to make the fiber for one XL t-shirt!"
    },
    "can": {
        "transformation": "Melted and rolled into infinite cycles of new aluminum sheets for beverages.",
        "impact": "Uses 95% less energy than producing from raw bauxite ore.",
        "fun_fact": "A recycled can could be back on a store shelf in just 60 days."
    },
    "phone": {
        "transformation": "Dismantled to recover precious gold, silver, and copper for new high-tech circuitry.",
        "impact": "Prevents toxic heavy metals from leaching into groundwater.",
        "fun_fact": "One ton of old phones contains more gold than many gold mines!"
    },
    "default": {
        "transformation": "Processed through advanced sorting to reclaim raw material for sustainable manufacturing.",
        "impact": "Reduces landfill strain and preserves natural habitats for future generations.",
        "fun_fact": "Most modern materials can be reborn multiple times if sorted correctly."
    }
}

def get_fallback_metadata(class_name):
    name = class_name.lower()
    for key, data in FALLBACK_INSIGHTS.items():
        if key in name:
            return data
    return FALLBACK_INSIGHTS["default"]


@app.post("/detect", response_model=DetectionResponse)
async def detect_waste(image: UploadFile = File(...)):
    """
    Detect waste items using Gemini (primary) or YOLO (fallback).
    """
    global current_key_index, gemini_model
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
            
            # Use the robust caller to handle rotation across ALL keys
            content = await call_gemini_robust([prompt, pil_image])
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
            error_msg = f"❌ Gemini Error: {str(e)}"
            print(error_msg)
            logger.error(error_msg)
            # Proceed to YOLO fallback
            pass


    # ─── STRATEGY 2: YOLOv8 (Fallback) ───
    if model:
        try:
            print("🚀 Starting YOLOv8 fallback...")
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
                        
                        # Enrich with SMART metadata for YOLO findings
                        item_meta = get_fallback_metadata(class_name)

                        detected_items.append(DetectedItem(
                            id=len(detected_items) + 1,
                            itemType=class_name.capitalize(),
                            bin=get_bin_for_item(class_name),
                            contaminated=is_contaminated(class_name),
                            confidence=conf,
                            bbox=BoundingBox(x=int(x1), y=int(y1), w=int(x2-x1), h=int(y2-y1)),
                            metadata=item_meta
                        ))
                    except Exception as box_err:
                        print(f"⚠️ Box processing error: {box_err}")
                        continue
            
            if detected_items:
                detected_items.sort(key=lambda x: x.confidence, reverse=True)
                print(f"✅ YOLO Found: {[d.itemType for d in detected_items]}")
                return DetectionResponse(items=detected_items[:3])
            
            print("🚀 YOLO found nothing.")
            
        except Exception as e:
            print(f"❌ YOLO Error: {e}")
            logger.error(f"YOLO fallback failed: {e}")

    if DEMO_MODE:
        print("🎁 Returning FALLBACK_DEMO_RESPONSE")
        return FALLBACK_DEMO_RESPONSE
    return DetectionResponse(items=[])


@app.post("/chat", response_model=ChatResponse)
async def chat_assistant(request: ChatRequest):
    """
    AI Assistant to answer waste related questions using Gemini.
    """
    global current_key_index, gemini_model
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
        
        # Use the robust caller to handle rotation across ALL keys
        content = await call_gemini_robust(prompt)
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
