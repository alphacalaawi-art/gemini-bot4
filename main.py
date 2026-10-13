import os
import requests
import time
import datetime
import threading
from flask import Flask

app = Flask(__name__)

# --- XOGTAADA KHAASKA AH ---
# (Markaad Render gelineyso waxaad ku dari kartaa Environment Variables, ama halkaan geli Token-kaaga)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "GELI_TOKEN-KAAGA_HALKAN")
CHAT_ID = os.environ.get("CHAT_ID", "8668049857")
ASSET = "AED/CNY_otc"
WEB_APP_URL = os.environ.get("WEB_APP_URL", "https://magaca-appkaaga.vercel.app")

@app.route('/')
def home():
    return "My Gemini Bot waa uu shaqeynayaa 24/7!"

def send_signal_with_webapp(action, reason):
    """Wuxuu Telegram-kaaga ugu diraa signal wata badhanka Web App-ka"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    act_text = "🟢 **UP (BUY)**" if action == "BUY" else "🔴 **DOWN (SELL)**"
    
    msg = (
        f"⚡ *SIGNAL ALERT* ⚡\n\n"
        f"📊 *Asset:* `{ASSET}`\n"
        f"📈 *Direction:* {act_text}\n"
        f"🔍 *Sababta:* {reason}\n"
        f"⏰ *Take Trade At:* `{datetime.datetime.now().strftime('%H:%M:%S')}`"
    )
    
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "✅ GOT IT / OPEN APP", 
                    "web_app": {"url": WEB_APP_URL}
                }
            ]
        ]
    }
    
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Khalad: {e}")

def market_scanner_thread():
    """Qeybta gadaal ka shaqeyneysa ee suuqa la socota"""
    print("🤖 My Gemini Bot scanner wuxuu bilaabay shaqada...")
    while True:
        # Halkaan geli hab-raacaaga falanqaynta suuqa (Pocket Option read-only)
        # Tusaale ahaan halkaan ayaad ka diri kartaa signal marka xaaladdu buuxsanto
        time.sleep(300)  # 5 daqiiqadood mar

if __name__ == "__main__":
    # Bilow background scanner thread
    scanner_thread = threading.Thread(target=market_scanner_thread, daemon=True)
    scanner_thread.start()
    
    # Render wuxuu u baahan yahay Web Server si uusan u xirmin (Port binding)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
  
