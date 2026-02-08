# 🌿 EcoScrutinize: AI-Powered Waste Intelligence

**EcoScrutinize** is a next-generation sustainability platform that leverages Computer Vision and Generative AI to solve the global waste contamination crisis. By providing instant, accurate segregation guidance, it empowers individuals to participate correctly in the circular economy.

---

## 🚀 Important: Performance Note (Cold Start)
**Please Note:** The **very first scan** performed after the server has been idle may take **60 to 120 seconds**. 
* **Why?** The backend must load the 12MB+ YOLOv8 model weights into RAM and establish a secure gRPC handshake with Google Gemini servers.
* **Subsequent Scans:** Once the model is "warmed up," subsequent scans typically process within **10-15 seconds**.

---

## ✨ Key Features
*   **Dual-Model Vision Pipeline:** Uses **Google Gemini 1.5 Pro/Flash** for deep semantic analysis and **YOLOv8** for high-speed local object detection.
*   **"Circular Evolution" Insights:** Don't just sort—learn. See what your waste becomes (e.g., plastic bottles becoming athletic wear).
*   **Contamination Guard:** Detects if organic waste is mixed with recyclables, advising the user to rinse containers to save recovery costs.
*   **Intelligent Assistant:** A voice-integrated AI chatbot to answer complex "where does this go?" questions.
*   **Impact Dashboard:** Real-time visualization of CO2 saved, water preserved, and energy recovered based on your scan history.

---

## 🛠️ Technical Stack
*   **Frontend:** React.js, Vite, Framer Motion (Animations), Lucide-Icons.
*   **Backend:** FastAPI (Python), Uvicorn.
*   **AI/ML:** 
    *   **Google Gemini AI:** Semantic image analysis & Natural Language Processing.
    *   **Ultralytics YOLOv8:** Edge-ready object detection and fallback.
*   **Styling:** Premium Glassmorphism UI with custom CSS-in-JS.

---

## ⚙️ Installation & Setup

### Backend
1. Navigate to the `backend/` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your Google API Key:
   ```env
   GEMINI_API_KEY=your_key_here
   ```
4. Start the server:
   ```bash
   python main.py
   ```

### Frontend
1. In the root directory, install npm packages:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```

---

## 📈 The Impact
As of 2025, only **6.9%** of global waste is successfully recycled. Contamination is the #1 reason why recyclables end up in landfills. **EcoScrutinize** targets this gap by providing the "Prescriptive Intelligence" needed to stop contamination at the source—the bin.

---

## 🏆 Hackathon Submission
Built with ❤️ for a cleaner planet.
**Project Name:** EcoScrutinize
**Category:** Sustainability / AI for Good
