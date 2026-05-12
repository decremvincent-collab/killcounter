from flask import Flask, jsonify
from TikTokLive import TikTokLiveClient
from TikTokLive.events import GiftEvent
import threading

app = Flask(__name__)
kill_count = 0

# Compte TikTok de 징니ゃ♡
client = TikTokLiveClient(unique_id="im_jingni_ya")

# Configuration des cadeaux (+ / -)
gift_actions = {
    "불렛": 30,
    "홈": 3,
    "금": 3,
    "카우보이": 3,
    "하트": -3,
    "티켓": 15,
    "고글": -15,
    "블루": 30,
    "골드": -30,
    "크리스탈": 150,
    "크리스탈": -150,
    "방종": 0,
    "방종쉴드": 0
}

@client.on("gift")
async def on_gift(event: GiftEvent):
    global kill_count
    name = event.gift.name
    if name in gift_actions:
        kill_count += gift_actions[name]

@app.route("/kills")
def kills():
    return jsonify({"kills": kill_count})

def run_tiktok():
    client.run()

threading.Thread(target=run_tiktok).start()

if __name__ == "__main__":
    # Flask écoute sur toutes les interfaces (Render exige host=0.0.0.0)
    app.run(host="0.0.0.0", port=5000)

