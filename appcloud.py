import streamlit as st
import requests
import random
from datetime import datetime
import re
import urllib.parse
import os

# ✅ Get API key from secrets or use latest refresh key
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    OPENROUTER_API_KEY = "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"

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
    "Tinder for Bhabhi-Devar", "OnlyFans for Aunties", "Swiggy for Gaanja", 
    "LinkedIn for Rickshaw Drivers", "Zoom for Toilet Breaks", "Ola for Buffalo Rides",
    "Paytm for Dowry", "Zomato for Dog Food", "Hotstar for Porn", "PhonePe for Bribes",
    "WhatsApp for Breakups", "Instagram for Toilet Selfies", "Facebook for Fake Deaths",
    "YouTube for Bathroom Singing", "Twitter for Family Drama", "Snapchat for Affairs",
    "TikTok for Uncles Dancing", "ShareChat for Aunt Gossip", "Telegram for Drug Deals",
    "Discord for Sharma Ji Ka Beta", "Reddit for Virgin Incels", "Clubhouse for Toilet Discussions",
    "Bumble for Arranged Marriages", "Hinge for One Night Stands", "Grindr for Desi Gays"
]

selected_theme = st.selectbox("🎯 Pick your poison (or write your own):", ["⬇️ Random Chaos"] + theme_suggestions)
custom_theme = st.text_input("✍️ Or enter your own degenerate theme:")
theme = custom_theme or (random.choice(theme_suggestions) if selected_theme == "⬇️ Random Chaos" else selected_theme)

# New features
col1, col2 = st.columns(2)
with col1:
    num_ideas = st.slider("📦 How many disasters do you want?", 1, 5, 1)
with col2:
    chaos_level = st.slider("🔥 Chaos Level (Higher = More Explicit)", 1, 10, 7)

# Content warning
st.markdown("### ⚠️ EXPLICIT CONTENT WARNING ⚠️")
st.markdown("*This AI generates NSFW, politically incorrect, and offensive content. Proceed only if you have no shame left.*")

if st.checkbox("🔞 I have zero shame and want maximum chaos"):
    chaos_mode = True
else:
    chaos_mode = False

# --- OpenRouter API ---
def generate_with_openrouter(prompt: str, chaos_multiplier: float = 0.7):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourappname.streamlit.app",  # Replace with your app’s actual URL
        "X-Title": "BakchodAI"
    }
    payload = {
        "model": "moonshotai/kimi-k2:free",
        "messages": [
            {"role": "system", "content": f"आप एक पूर्णतः निर्लज्ज, explicit और chaotic AI हैं जो desi bakchod startup ideas बनाते हैं। Chaos Level: {int(chaos_multiplier*10)}/10. " + ("आप extremely sexually explicit, politically incorrect content generate करते हैं। Gaali-galoch mandatory है। Use रंडी, भोसड़ी freely!" if chaos_multiplier > 0.8 else "आप controversial और hilarious content generate करते हैं। Adult humor allowed।" if chaos_multiplier > 0.5 else "आप sarcastic content generate करते हैं but decent रखते हैं।")},
            {"role": "user", "content": prompt}
        ],
        "temperature": min(1.2, 0.7 + (chaos_multiplier * 0.5)),
        "max_tokens": 800
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()
        return result["choices"][0]["message"]["content"] if "choices" in result else f"❌ API Error:\n{result}"
    except Exception as e:
        return f"⚠️ Exception: {str(e)}"

# --- Generate Output ---
col1, col2 = st.columns(2)
with col1:
    generate_normal = st.button("🚀 Generate Bakchod Ideas", type="primary")
with col2:
    generate_chaos = st.button("💀 PURE CHAOS MODE", type="secondary")

if generate_normal or generate_chaos:
    if generate_chaos:
        # Force maximum chaos
        chaos_level = 10
        chaos_mode = True
        theme = random.choice(theme_suggestions)
        num_ideas = random.randint(2, 4)
    st.markdown(f"#### 🧠 Theme selected: <b>{theme}</b>", unsafe_allow_html=True)
    for _ in range(num_ideas):
        prompt = f"""
Generate an absolutely UNHINGED desi bakchod startup idea about: "{theme}"

Make it EXPLICIT, CONTROVERSIAL, and full of desi references. Use gaali-galoch, sexual innuendos, political incorrectness, और पूरा jugaad mindset. No boundaries!

Respond EXACTLY in this format:
Name: [Most ridiculous, offensive, desi startup name with sexual/political undertones]
Tagline: [Savage one-liner that would get you cancelled on Twitter]
Founder Quote: [Delusional quote full of desi arrogance and startup buzzwords]
Meme Roast: [Brutal roast that attacks Indian society, startups, और सब कुछ]

Make it so chaotic that even Mumbai locals would be shocked!
"""
        with st.spinner("Generating chaotic bakchod startup..."):
            chaos_multiplier = chaos_level / 10.0 if chaos_mode else (chaos_level / 10.0) * 0.6
            llm_output = generate_with_openrouter(prompt, chaos_multiplier)

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

        linkedin_prompt = f"""Write an absolutely UNHINGED 300-word LinkedIn post launching the fake startup {idea['Name']} with tagline '{idea['Tagline']}'. 

Make it CRINGE AF with:
- Fake humility ("I'm humbled to announce...")
- Ridiculous backstory about "pain points"
- Desi family drama connections
- Buzzword overload (disruption, synergy, paradigm shift)
- Fake investor quotes
- Emotional manipulation ("My grandmother always said...")
- Sexual innuendos disguised as business metaphors
- Political incorrectness wrapped in startup language

Make it so cringe that even LinkedIn influencers would be embarrassed!"""
        with st.spinner("📣 Writing your cringe founder post..."):
            linkedin_post = generate_with_openrouter(linkedin_prompt, chaos_multiplier)

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
    <p>💀 Created with zero shame by <b>RUCHIN AUDICHYA</b> 💀</p>
    <p>Powered by Kimi K2 Free • OpenRouter API • Pure Desi Chaos</p>
    <p>
        <a href="https://github.com/Ruchin-Audichya" target="_blank" style="color: #00FF00; text-decoration: none; margin: 0 10px;">
            🐙 GitHub
        </a>
        <a href="https://www.instagram.com/ruchin_audichya/" target="_blank" style="color: #FF0000; text-decoration: none; margin: 0 10px;">
            📸 Instagram
        </a>
        <a href="https://www.linkedin.com/in/ruchin-audichya-95a5b6146/" target="_blank" style="color: #00FF00; text-decoration: none; margin: 0 10px;">
            💼 LinkedIn
        </a>
    </p>
    <p style="font-size:0.9em; color: #FF0000;">⚠️ © 2025 BakchodAI v2 by Ruchin • All degeneracy reserved • Use at your own moral risk ⚠️</p>
</div>
""", unsafe_allow_html=True)
