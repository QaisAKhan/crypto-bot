from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = "8107754002:AAG047aeYSIgBiUkUpxMHbTBGplIZbxuRKU"  # توکن ربات خود را اینجا قرار دهید

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '').lower()

    if 'قیمت' in text or 'price' in text:
        coin = text.split()[-1]
        price = get_price(coin)  # تابع دریافت قیمت (مقدار واقعی را جایگزین کنید)
        response = f"قیمت {coin}: ${price}" if 'قیمت' in text else f"{coin} price: ${price}"
        
    elif text == '/start':
        response = "سلام! برای قیمت ارزها 'قیمت bitcoin' ارسال کنید"
    
    else:
        response = "دستور نامعتبر!"

    send_message(chat_id, response)
    return jsonify({"status": "success"})

def get_price(coin):
    # مثال: دریافت قیمت از API (در واقعیت از CoinGecko/Binance استفاده کنید)
    return round(50000 * (1 + hash(coin) % 0.2), 2)  # مقدار تصادفی برای تست

def send_message(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
