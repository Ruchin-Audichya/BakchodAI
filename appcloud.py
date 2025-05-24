import streamlit as st
import requests
import random
from datetime import datetime
import re
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="BakchodAI – Meme Startup Generator", page_icon="🧠", layout="centered")

# --- UI Styles ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
body {
    font-family: 'Share Tech Mono', monospace;
    background: url('https://www.transparenttextures.com/patterns/cubes.png'), linear-gradient(135deg, #000000, #1f1c2c);
    background-blend-mode: overlay;
    background-size: cover;
    color: #00FFB3;
    cursor: crosshair;
}
.big-title {
    font-size: 3em;
    font-weight: bold;
    text-align: center;
    color: #00ff99;
    text-shadow: 0 0 6px #00ffcc, 0 0 10px #00ffcc;
    margin-bottom: 0.5em;
    animation: flicker 1.5s infinite alternate;
}
@keyframes flicker {
  from { opacity: 1; }
  to { opacity: 0.8; }
}
.subtext {
    text-align: center;
    font-size: 1.1em;
    color: #00d4ff;
    margin-bottom: 2em;
}
.animated-card {
    background: rgba(0, 255, 180, 0.05);
    border: 1px solid #00ffc8;
    box-shadow: 0 0 12px rgba(0,255,204,0.3);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 22px;
    transition: all 0.3s ease-in-out;
}
.animated-card:hover {
    transform: scale(1.02);
    box-shadow: 0 0 18px rgba(0,255,204,0.5);
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
st.markdown('<div class="big-title">🧠 BAKCHOD.AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Create hilariously fake Gen-Z startup ideas. Terminal booted. Hacker sarcasm engaged. 🤖🔥</div>', unsafe_allow_html=True)

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
        "HTTP-Referer": "http://localhost",
        "X-Title": "BakchodAI"
    }
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a savage Gen-Z AI that generates spicy, dark, absurd, and meme-worthy fake startup ideas. No filters. Full bakchodi."},
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
        idea = {key: (re.search(pattern, llm_output, re.IGNORECASE).group(1).strip()
                      if re.search(pattern, llm_output, re.IGNORECASE) else "⚠️ Could not generate.")
                for key, pattern in patterns.items()}

        # LinkedIn post generation
        linkedin_prompt = f"""
Write a witty, slightly cringe, 300-word LinkedIn-style startup launch post for a new company called "{idea['Name']}".
Include sarcasm, emojis, hashtags, fake gratitude to a made-up team, and typical founder energy. Mention the tagline "{idea['Tagline']}".
End with a call to action to support, fund, or join.
"""
        with st.spinner("📣 Writing your cringe founder launch post..."):
            linkedin_post = generate_with_openrouter(linkedin_prompt)
        st.info("📣 Founder post ready!")

        idea_text = f"""🚀 {idea['Name']}\n💬 {idea['Tagline']}\n🧄 {idea['Quote']}\n🔥 {idea['Roast']}"""
        encoded_text = urllib.parse.quote_plus(idea_text)
        twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
        linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://bakchodai.com&summary={encoded_text}"

        # ✅ GOLD LOGO FIXED HERE
        st.markdown(f"""
<div class="animated-card">
    <img src='https://via.placeholder.com/100x100/FFD700/000000?text=🔥BZ' style='border-radius:50%;margin-bottom:16px;border:3px solid #FFD700;font-family:Orbitron,monospace;'>
    <h3 style='color:#FFD700;'>🤖 {idea['Name']}</h3>
    <p><strong>💬 Tagline:</strong> {idea['Tagline']}</p>
    <p><strong>🧄 Founder Quote:</strong> {idea['Quote']}</p>
    <p><strong>🔥 Meme Roast:</strong> {idea['Roast']}</p>
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div class="button-strip">
    <a href="data:text/plain;charset=utf-8,{urllib.parse.quote(idea_text)}" download="{idea['Name'].replace(' ', '_')}.txt">⬇️ Download</a>
    <a href="{twitter_url}" target="_blank">🐦 Share on X</a>
    <a href="{linkedin_url}" target="_blank">🔗 Share on LinkedIn</a>
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
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
