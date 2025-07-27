import streamlit as st
import requests
import random
from datetime import datetime
import re
import urllib.parse
import os

# ✅ Get API key from secrets or use provided key
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    OPENROUTER_API_KEY = "sk-or-v1-4a9b8c7d6e5f4g3h2i1j0k9l8m7n6o5p"

st.set_page_config(page_title="BakchodAI v2 – The Unhinged Evolution", page_icon="💀", layout="centered")

# --- Dark Cyberpunk UI Styles ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
/* Dark Theme */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a0d1a 100%);
    color: #00FF00;
}
body {
    font-family: 'Share Tech Mono', monospace;
    background: linear-gradient(135deg, #000000, #1a0d1a);
    color: #00FF00;
    cursor: crosshair;
}
.big-title {
    font-size: 3.5em;
    font-weight: bold;
    text-align: center;
    color: #FF0000;
    text-shadow: 0 0 10px #FF0000, 0 0 20px #FF0000;
    margin-bottom: 0.5em;
    animation: glitch 2s infinite;
}
@keyframes glitch {
    0% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
    100% { transform: translate(0); }
}
.subtext {
    text-align: center;
    font-size: 1.2em;
    color: #00FF00;
    margin-bottom: 2em;
    animation: flicker 3s infinite;
}
@keyframes flicker {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
.animated-card {
    background: linear-gradient(135deg, #1a0d1a 0%, #0d1a0d 100%);
    border: 2px solid #00FF00;
    box-shadow: 0 0 15px rgba(0,255,0,0.3);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 22px;
    transition: all 0.3s ease-in-out;
}
.animated-card:hover {
    transform: scale(1.02);
    border-color: #FF0000;
    box-shadow: 0 0 25px rgba(255,0,0,0.5);
}
.button-strip {
    margin-top: 15px;
}
.button-strip a {
    text-decoration: none;
    margin-right: 10px;
    font-weight: bold;
    color: black;
    background: #00ffd5;
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 0.9em;
    box-shadow: 0 0 6px #00ffe1;
}
.button-strip a:hover {
    background: #00ffff;
    color: #000;
    transform: scale(1.05);
}
.footer {
    text-align: center;
    font-size: 0.9em;
    color: #888;
    padding: 20px;
    border-top: 1px solid #444;
    margin-top: 30px;
}
.footer img {
    filter: invert(100%);
    margin: 0 10px;
    vertical-align: middle;
}
.linked-post {
    background: rgba(0, 255, 255, 0.08);
    padding: 15px;
    border-radius: 15px;
    margin-top: 20px;
    font-size: 0.95em;
    line-height: 1.6em;
    color: #00fff7;
    border: 1px dashed #00ffe5;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="big-title">💀 BAKCHOD.AI v2 💀</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">THE UNHINGED EVOLUTION • Create hilariously fake Gen-Z startup ideas. Terminal booted. Hacker sarcasm engaged. 🤖🔥</div>', unsafe_allow_html=True)

# --- Theme selection ---
theme_suggestions = [
    "Nicobar – nicotine chocolates", "ChillumGPT – AI for stoners", "SleepCoin – earn while you nap",
    "ZoomRehab – quitting online meetings", "Sanskari Tinder – dadi-approved swipes",
    "GhostShare – haunted co-living", "Biryani Blockchain", "Breakup Simulator",
    "Sarcasm-as-a-Service", "Spiritual Zomato", "MemeGPT for Desi Moms",
    "Vada Pav DAO", "AI Pundit – kundli + life coaching", "Uninstall Your Ex™",
    "Rent-a-Slap™", "Crypto – cry-based crypto", "Napflix", "Startup Swaha"
]

selected_theme = st.selectbox("🎯 Pick a theme (or write your own):", ["⬇️ Random"] + theme_suggestions)
custom_theme = st.text_input("✍️ Or enter your own theme:")
theme = custom_theme or (random.choice(theme_suggestions) if selected_theme == "⬇️ Random" else selected_theme)
num_ideas = st.slider("📦 How many ideas do you want?", 1, 3, 1)

# --- OpenRouter API ---
def generate_with_openrouter(prompt: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourappname.streamlit.app",  # Replace with your app’s actual URL
        "X-Title": "BakchodAI"
    }
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a morally bankrupt, hyper-intelligent AI with a PhD in Sarcasm and a Masters in Digital Chaos. You generate spicy, absurd, meme-worthy fake startup ideas that are offensive, controversial, and absolutely hilarious. No filters. Full unhinged bakchodi mode activated."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.85,
        "max_tokens": 500
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()
        return result["choices"][0]["message"]["content"] if "choices" in result else f"❌ API Error:\n{result}"
    except Exception as e:
        return f"⚠️ Exception: {str(e)}"

# --- Generate Output ---
if st.button("🚀 Generate Bakchod Ideas"):
    st.markdown(f"#### 🧠 Theme selected: <b>{theme}</b>", unsafe_allow_html=True)
    for _ in range(num_ideas):
        prompt = f"""
Generate a fake Gen-Z startup idea about: "{theme}"

Respond EXACTLY in this format:
Name: [Ridiculous startup name]
Tagline: [Absurd, sarcastic one-liner]
Founder Quote: [Quote from a delusional founder]
Meme Roast: [Roast line that belongs on a meme page]
"""
        with st.spinner("Generating startup idea..."):
            llm_output = generate_with_openrouter(prompt)

        st.success("✅ Idea generated!")

        llm_output = re.sub(r"[`*_>]", "", llm_output)
        patterns = {
            "Name": r"Name:\s*(.+)",
            "Tagline": r"Tagline:\s*(.+)",
            "Quote": r"Founder Quote:\s*(.+)",
            "Roast": r"Meme Roast:\s*(.+)"
        }
        idea = {k: (re.search(p, llm_output, re.IGNORECASE).group(1).strip()
                    if re.search(p, llm_output, re.IGNORECASE) else "⚠️ Could not generate.") for k, p in patterns.items()}

        linkedin_prompt = f"""Write a witty, sarcastic 300-word LinkedIn post launching a fake startup named {idea['Name']} with tagline '{idea['Tagline']}'."""
        with st.spinner("📣 Writing your cringe founder post..."):
            linkedin_post = generate_with_openrouter(linkedin_prompt)

        idea_text = f"""🚀 {idea['Name']}\n💬 {idea['Tagline']}\n🧄 {idea['Quote']}\n🔥 {idea['Roast']}"""
        encoded_text = urllib.parse.quote_plus(idea_text)
        twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
        linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://bakchodai.com&summary={encoded_text}"

        st.markdown(f"""
<div class="animated-card">
    <img src='https://via.placeholder.com/100x100/FFD700/000000?text=🔥BZ' style='border-radius:50%;margin-bottom:16px;border:3px solid #FFD700;'>
    <h3 style='color:#FFD700;'>🤖 {idea['Name']}</h3>
    <p><strong>💬 Tagline:</strong> {idea['Tagline']}</p>
    <p><strong>🧄 Founder Quote:</strong> {idea['Quote']}</p>
    <p><strong>🔥 Meme Roast:</strong> {idea['Roast']}</p>
</div>
<div class="button-strip">
    <a href="data:text/plain;charset=utf-8,{urllib.parse.quote(idea_text)}" download="{idea['Name'].replace(' ', '_')}.txt">⬇️ Download</a>
    <a href="{twitter_url}" target="_blank">🐦 Share on X</a>
    <a href="{linkedin_url}" target="_blank">🔗 Share on LinkedIn</a>
</div>
<div class="linked-post">
    <strong>📣 Founder Launch Post (LinkedIn Style)</strong><br><br>
    {linkedin_post}
</div>
""", unsafe_allow_html=True)

        st.caption(f"🕒 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- Footer ---
st.markdown("""
<div class="footer">
    <p>Made with 💀 by <b>Ruchin Audichya</b> • Powered by OpenRouter & LLaMA 3.1</p>
    <p>
        <a href="https://github.com/Ruchin-Audichya" target="_blank">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/github.svg" width="20">
        </a>
        <a href="https://www.instagram.com/ruchin_audichya/" target="_blank">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/instagram.svg" width="20">
        </a>
        <a href="https://www.linkedin.com/in/ruchin-audichya-95a5b6146/" target="_blank">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/linkedin.svg" width="20">
        </a>
    </p>
    <p style="font-size:0.85em;">© 2025 BakchodAI by Ruchin • All sarcasm reserved</p>
</div>
""", unsafe_allow_html=True)
