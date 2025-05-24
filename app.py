
import streamlit as st
import requests
import random
from datetime import datetime
import base64
import re
import urllib.parse

# Streamlit Config
st.set_page_config(page_title="BakchodAI – Meme Startup Generator", page_icon="🧠", layout="centered")

# Inject Google Fonts and Custom CSS
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&family=Urbanist:wght@400;700&display=swap" rel="stylesheet">
<style>
body {
    font-family: 'Urbanist', sans-serif;
    background: linear-gradient(145deg, #0f0c29, #302b63, #24243e);
    color: #ddd;
}
.big-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.8em;
    font-weight: bold;
    text-align: center;
    color: #FFD700;
    margin-bottom: 0.2em;
    animation: popin 0.8s;
}
.subtext {
    text-align: center;
    font-size: 1.1em;
    color: #AAAAAA;
    margin-bottom: 2em;
    animation: fadein 1.2s;
}
.animated-card {
    backdrop-filter: blur(8px);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 215, 0, 0.3);
    box-shadow: 0 6px 32px rgba(255, 215, 0, 0.15);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 22px;
    transition: transform 0.3s ease;
    animation: floatin 0.7s;
}
.animated-card:hover {
    transform: translateY(-3px) scale(1.02);
}
.votebtn {
    font-size: 0.95em;
    font-weight: 600;
    padding: 10px 28px;
    border-radius: 50px;
    border: 2px solid #FFD700;
    color: #111;
    background: #FFD700;
    transition: all 0.25s ease;
    cursor: pointer;
}
.votebtn:hover {
    background: #fff200;
    color: #000;
    transform: scale(1.08);
    box-shadow: 0 0 15px rgba(255,215,0,0.4);
}
@keyframes popin {from {transform: scale(0.8); opacity: 0;} to {transform: scale(1); opacity: 1;}}
@keyframes fadein {from {opacity:0;} to {opacity:1;}}
@keyframes floatin {from {opacity:0;transform: translateY(24px);} to {opacity:1;transform: none;}}
</style>
""", unsafe_allow_html=True)

# Branding
st.markdown('<div class="big-title">🧠 BakchodAI – The Meme Startup Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Create hilariously fake Gen-Z startup ideas. Built for bakchods. Powered 100% locally. Zero chill.</div>', unsafe_allow_html=True)

# Themes
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

# Ollama Local LLM

def generate_with_ollama(prompt: str):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral:instruct", "prompt": prompt, "stream": False}
        )
        return response.json().get("response", "⚠️ Error: No response returned")
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Generate Button
if st.button("🚀 Generate Bakchod Ideas"):
    st.markdown(f"#### 🧠 Theme selected: <b>{theme}</b>", unsafe_allow_html=True)
    
    for i in range(num_ideas):
        prompt = f"""Generate a fake Gen-Z startup idea about: {theme}
Return it in this exact format:
Name: [Startup Name]
Tagline: [Funny tagline]
Founder Quote: [A sarcastic quote]
Meme Roast: [Roast line for memes]"""

        with st.spinner("Generating ultimate bakchodi..."):
            llm_output = generate_with_ollama(prompt)

        patterns = {
            "Name": r"Name:\s*(.+)",
            "Tagline": r"Tagline:\s*(.+)",
            "Quote": r"(?:Founder Quote|Quote):\s*(.+)",
            "Roast": r"(?:Meme Roast|Roast):\s*(.+)"
        }
        idea = {key: (re.search(pattern, llm_output, re.IGNORECASE).group(1).strip() if re.search(pattern, llm_output, re.IGNORECASE) else "⚠️ Could not generate.") for key, pattern in patterns.items()}

        st.markdown(f"""
<div class=\"animated-card\">
    <img src='https://dummyimage.com/100x100/ffd700/000&text=BZ' style='border-radius:50%;margin-bottom:16px;border:3px solid #FFD700;'>
    <h3 style='color:#FFD700;'>🤤 {idea['Name']}</h3>
    <p><strong>💬 Tagline:</strong> {idea['Tagline']}</p>
    <p><strong>🧄 Founder Quote:</strong> {idea['Quote']}</p>
    <p><strong>🔥 Meme Roast:</strong> {idea['Roast']}</p>
</div>
""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<button class="votebtn">👍 I’d fund this</button>', unsafe_allow_html=True)
        with col2:
            st.markdown('<button class="votebtn">👎 Trash it</button>', unsafe_allow_html=True)

        idea_text = f"Name: {idea['Name']}\nTagline: {idea['Tagline']}\nQuote: {idea['Quote']}\nRoast: {idea['Roast']}"
        b64 = base64.b64encode(idea_text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="bakchod_idea_{i+1}.txt">🗓️ Download this idea</a>'
        st.markdown(href, unsafe_allow_html=True)

        share_text = f"{idea['Name']} - {idea['Tagline']}\nFounder Quote: {idea['Quote']}\nMeme Roast: {idea['Roast']}"
        encoded = urllib.parse.quote_plus(share_text)
        st.markdown(
            f'<a href="https://twitter.com/intent/tweet?text={encoded}" target="_blank">🕳️ Tweet</a> &nbsp; | &nbsp; '
            f'<a href="https://www.linkedin.com/sharing/share-offsite/?url=https://bakchodai.local/{urllib.parse.quote_plus(idea["Name"])}" target="_blank">💼 Share on LinkedIn</a>',
            unsafe_allow_html=True
        )

        st.caption(f"🕒 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        launch_prompt = f"""
Write a short, bold and quirky LinkedIn-style startup launch post (around 200 words) about this new fake startup:
Startup Name: {idea['Name']}
Tagline: {idea['Tagline']}
Founder Quote: {idea['Quote']}
Meme Roast: {idea['Roast']}
"""
        launch_post = generate_with_ollama(launch_prompt)
        with st.expander("📢 LinkedIn Launch Post (200 words)"):
            st.markdown(f"<div style='background:#141414;padding:16px;border-left:4px solid #FFD700;border-radius:8px;color:#ddd;font-size:0.95em;'>{launch_post}</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center;font-size:1.1em;margin-bottom:8px;">Who made this?</div>
<div style="text-align:center;">
    <a class="brandlink" href="https://www.linkedin.com/in/ruchinaudi/" target="_blank">
        <img class="social-icon" src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/linkedin.svg" style="height:20px;vertical-align:middle;margin-right:5px;" />LinkedIn</a> &nbsp;|&nbsp; 
    <a class="brandlink" href="https://github.com/Ruchin-Audichya" target="_blank">
        <img class="social-icon" src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/github.svg" style="height:20px;vertical-align:middle;margin-right:5px;" />GitHub</a> &nbsp;|&nbsp; 
    <a class="brandlink" href="https://www.instagram.com/ruchin_audichya/" target="_blank">
        <img class="social-icon" src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/instagram.svg" style="height:20px;vertical-align:middle;margin-right:5px;" />Instagram</a>
</div>
<div style="text-align:center; margin-top:10px; color:#FFD700; font-size:1.08em;">Made with 💥 by <b>Ruchin</b>. 100% local. Zero API.</div>
""", unsafe_allow_html=True)
