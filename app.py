from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    # Hier können Sie den aktuellen Status des Bots zurückgeben
    return jsonify({"status": "Bot is running"})

@app.route('/start', methods=['POST'])
def start_bot():
    os.system("python /bot.py &")
    return jsonify({"status": "Bot started"})

@app.route('/stop', methods=['POST'])
def stop_bot():
    os.system("pkill -f bot.py")
    return jsonify({"status": "Bot stopped"})

if __name__ == '__main__':
    app.run(debug=True)