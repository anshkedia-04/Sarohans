from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Initialize Flask to serve static files (HTML) from the current directory
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enables the HTML file to talk to this Python script

# --- API CLIENT & KNOWLEDGE BASE ---

# Check for API key and initialize the Groq client
if not os.environ.get("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found. Please create a .env file and add your key.")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

PRODUCTS = [
    {"name": "Leheriya Silk Saree", "price": "₹3,499", "category": "Rajputana Saree", "desc": "Wave-dyed Rajasthani art"},
    {"name": "Bandhej Georgette Saree", "price": "₹2,799", "category": "Rajputana Saree", "desc": "Tie-dye masterpiece"},
    {"name": "Printed Chanderi Saree", "price": "₹1,899", "category": "Rajputana Saree", "desc": "Handblock printed elegance"},
    {"name": "Gota Patti Work Saree", "price": "₹4,299", "category": "Rajputana Saree", "desc": "Gota ribbon embellishment"},
    {"name": "Royal Ghaghra Choli Set", "price": "₹5,499", "category": "Rajputana Poshak", "desc": "Full flared ghaghra set"},
    {"name": "Odhni Bandhej Poshak", "price": "₹3,799", "category": "Rajputana Poshak", "desc": "With embroidered odhni"},
    {"name": "Designer Embroidered Poshak", "price": "₹6,999", "category": "Rajputana Poshak", "desc": "Mirror & thread work"},
    {"name": "Festive Cotton Poshak", "price": "₹2,499", "category": "Rajputana Poshak", "desc": "Lightweight festive wear"},
    {"name": "Embroidered Georgette Suit", "price": "₹3,299", "category": "Party Wear", "desc": "Sequin & bead work"},
    {"name": "Designer Lehenga Set", "price": "₹7,499", "category": "Party Wear", "desc": "Heavy embroidery lehenga"},
    {"name": "Shimmer Georgette Saree", "price": "₹2,199", "category": "Party Wear", "desc": "Party-ready shimmer drape"},
    {"name": "Net Embroidered Suit", "price": "₹4,199", "category": "Party Wear", "desc": "Layered net with lining"},
    {"name": "Banarasi Pure Silk Saree", "price": "₹12,999", "category": "Wedding Saree", "desc": "Handwoven zari work"},
    {"name": "Kanjeevaram Bridal Saree", "price": "₹15,499", "category": "Wedding Saree", "desc": "South silk masterwork"},
    {"name": "Zari & Cutwork Saree", "price": "₹8,999", "category": "Wedding Saree", "desc": "Pure gold zari weaving"},
    {"name": "Bridal Red Silk Saree", "price": "₹11,499", "category": "Wedding Saree", "desc": "Auspicious bridal red"},
]

# This string formats all your café's data into a single block for the LLM
KNOWLEDGE_BASE = f"""
- Brand Name: Sarohans Ethnic Wear
- Products: {PRODUCTS}
- Offers: Free shipping on orders above ₹1,499. Use code SAROHANS10 for 10% off first order.
- Location: Sarohans Emporium, MI Road, Jaipur, Rajasthan 302001.
- Contact: +91 98765 43210, hello@sarohans.com.
- Hours: Mon–Sat: 10am – 7pm.
- Policies: 15-day easy returns, free pickup. Pan-India delivery in 5–7 days.
"""

SYSTEM_PROMPT = f"""
You are a helpful and knowledgeable assistant for 'Sarohans', a premium ethnic wear brand.
Your goal is to answer customer questions accurately based ONLY on the information provided below.
If a user asks about products, recommend items from the list with their prices.
Do not make up information. If unsure, provide the contact phone number.

Keep your answers elegant, polite (use Namaste), and concise.

Here is the information about Sarohans:
{KNOWLEDGE_BASE}
"""

# ——— LLM-POWERED LOGIC ENGINE ———
def get_bot_response(user_msg):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.1-8b-instant",  # Updated to currently supported model
            temperature=0.7,
            max_tokens=150,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return "Namaste! I am currently experiencing high traffic. Please try again later or contact us at +91 98765 43210."

# Serve the HTML file at the root URL
@app.route('/')
def index():
    return app.send_static_file('design11.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    user_message = data.get('message', '')
    bot_reply = get_bot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"🌸 Sarohans Server Running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
