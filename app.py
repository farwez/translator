import streamlit as st
from googletrans import Translator
import tempfile
import os
import base64
from streamlit_lottie import st_lottie
import requests
import edge_tts
import asyncio
from gtts import gTTS

st.markdown("""
    <style>
        /* Hide top-right toolbar icons */
        [title="Share"],
        [title="Edit"],
        [title="Star this app"],
        a[href*='github.com'] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Translator", layout="wide")

theme = st.sidebar.radio("🌗 Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("""
        <style>
            .main-title { color: #ffb347 !important; }
            .subtext { 
                color: #a3e4d7 !important; 
                background: rgba(0,0,0,0.4); 
                padding: 8px 0; 
                border-radius: 8px;
                font-weight: bold;
            }
            .stApp {
                background: linear-gradient(120deg, #232526 0%, #485563 100%);
                color: #f5f6fa;
            }
            textarea, .stTextArea textarea {
                background-color: #333 !important;
                color: #fff !important;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            .main-title { color: #0d47a1 !important; }
            .subtext { 
                color: #6a1b9a !important; 
                background: #f3e5f5; 
                padding: 8px 0; 
                border-radius: 8px;
                font-weight: 600;
                font-family: 'Fira Mono', 'Consolas', monospace;
                letter-spacing: 1px;
            }
            .stApp {
                background: linear-gradient(135deg, #f9fafc 0%, #ffe29f 50%, #76c7f4 100%);
                color: #22223b;
            }
            textarea, .stTextArea textarea {
                background-color: #22223b !important;
                color: #f5f6fa !important;
                border-radius: 8px !important;
                border: 1.5px solid #44475a !important;
            }
            /* Change field label font and color */
            label, .stTextInput label, .stTextArea label, .stSelectbox label {
                font-family: 'Fira Mono', 'Consolas', monospace !important;
                color: #e65100 !important;
                font-size: 1.1em !important;
                font-weight: bold !important;
                letter-spacing: 1px;
            }
        </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
        .main-title {
            font-size: 2.8em;
            font-weight: bold;
            text-align: center;
            color: #2c3e50;
            margin-top: 10px;
        }
        .subtext {
            font-size: 1.2em;
            color: #34495e;
            text-align: center;
        }
        .nav-item {
            font-weight: 600;
            font-size: 1.1em;
        }
        /* Removed .sidebar .sidebar-content as it may not exist in Streamlit */
        footer {visibility: hidden;}
        .home-section {
            text-align: center;
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
        /* ✅ Prevent horizontal scroll and content overflow */
        html, body, .stApp {
            max-width: 100vw;
            overflow-x: hidden;
        }

        /* ✅ Make containers wrap properly on small devices */
        .main-title, .subtext {
            word-wrap: break-word;
            white-space: normal;
        }

        /* ✅ Responsive font scaling for small devices */
        @media screen and (max-width: 768px) {
            .main-title {
                font-size: 1.8em !important;
                padding: 8px 0;
            }
            .subtext {
                font-size: 1em !important;
                padding: 4px 0;
            }
            .stTextInput>div>input,
            textarea,
            input,
            button {
                font-size: 1rem !important;
                width: 100% !important;
            }
        }

        /* ✅ Prevent wide Lottie overflow */
        iframe {
            max-width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

lang_dict = {
    'English': 'en',
    'Hindi': 'hi',
    'Telugu': 'te',
    'Tamil': 'ta',
    'French': 'fr',
    'Spanish': 'es',
}

voice_dict = {
    "👩 Female (Aria)": "en-US-AriaNeural",
    "🤖 MALE Robot()": 	"en-US-ChristopherNeural",
    "👦 Male (Guy)": "en-US-GuyNeural",
    "🎤 Anime-style (Jenny)": "en-US-JennyNeural"
}

menu = st.sidebar.radio("📍 Navigate", ["Home", "Translate Languages", "Voice Styles (English Only)", "About Creator", "Contact/Feedback"])

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_translation = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_2LdLki.json")

if menu == "Home":
    st.markdown('<div class="main-title">🌐 Welcome to Translator Creator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtext">Easily translate text into multiple languages and listen to it!</div>', unsafe_allow_html=True)

    if lottie_translation:
        st_lottie(lottie_translation, speed=1, height=300, key="home-anim")
    else:
        st.warning("⚠️ Unable to load animation. Check your internet or try again later.")

    st.markdown("""
    <div class='home-section'>
        <h3 style='color:#ffb347; font-size:1.5em; margin-bottom:10px;'>✨ Why to Use This Translator?</h3>
        <ul style='text-align: left; max-width: 500px; margin: auto; font-size:1em; line-height:1.6;'>
            <li>🔁 Instantly translate your text into 6+ languages</li>
            <li>🎧 Listen to your translation in different voices</li>
            <li>📅 Download your translation as an MP3</li>
            <li>📱 Works on mobile & desktop</li>
        </ul>
        <div style='margin-top:20px; text-align:center;'>
            <img src='https://cdn.pixabay.com/photo/2024/09/22/07/43/alphabet-9065307_1280.png' width='140' style='border-radius:50%; box-shadow:0 4px 16px #222;' alt='Translator Icon'/>
        </div>
    </div>
    <hr style='border:1px solid #ffe29f; margin:25px 0;'>
    <div class='home-section'>
        <p style='font-size:1em; color:#6a1b9a;'>
            💡 Use the <b>sidebar</b> to start translating and listening!
        </p>
    </div>
    <style>
        @media screen and (max-width: 600px) {
            .home-section h3 {
                font-size: 1.1em !important;
            }
            .home-section ul {
                font-size: 0.95em !important;
                padding-left: 18px !important;
            }
            .home-section img {
                width: 90px !important;
            }
            .home-section p {
                font-size: 0.95em !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

elif menu == "Translate Languages":
    st.markdown('<div class="main-title">🌍 Language Translator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtext">Translate text into multiple languages and listen to it (speech support varies).</div>', unsafe_allow_html=True)

    text_input = st.text_area("✍️ Enter text to translate:")
    target_lang = st.selectbox("🌍 Translate to:", list(lang_dict.keys()))

    if st.button("🔁 Translate & Speak"):
        if not text_input.strip():
            st.warning("⚠️ Please enter some text.")
        else:
            try:
                translator = Translator()
                translated = translator.translate(text_input, dest=lang_dict[target_lang])

                detected_lang_code = translated.src
                detected_lang = next((k for k, v in lang_dict.items() if v == detected_lang_code), detected_lang_code)

                st.success("✅ Translation Successful!")
                st.markdown(f"**Detected Language:** `{detected_lang.capitalize()}`")
                st.markdown(f"**Translated ({target_lang}):** `{translated.text}`")

                audio_path = None

                if lang_dict[target_lang] == 'en':
                    async def save_edge_audio():
                        communicate = edge_tts.Communicate(translated.text, voice="	en-US-ChristopherNeural")
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                            await communicate.save(tmpfile.name)
                            return tmpfile.name
                    audio_path = asyncio.run(save_edge_audio())

                else:
                    tts = gTTS(text=translated.text, lang=lang_dict[target_lang])
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                        tts.save(tmpfile.name)
                        audio_path = tmpfile.name

                st.markdown(f"🎧 **Speaking in {target_lang}**")
                st.audio(audio_path, format="audio/mp3")

                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()
                    b64_audio = base64.b64encode(audio_bytes).decode()
                    download_link = f'<a href="data:audio/mp3;base64,{b64_audio}" download="translated_audio.mp3">📅 Click to Download MP3</a>'
                    st.markdown(download_link, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Translation Error: {e}")

elif menu == "Voice Styles (English Only)":
    st.markdown('<div class="main-title">🔊 Voice Styles</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtext">Choose a voice style to hear English text spoken aloud.</div>', unsafe_allow_html=True)

    text_input = st.text_area("✍️ Enter English text to speak:")
    selected_voice = st.selectbox("🎤 Choose Voice Style:", list(voice_dict.keys()))

    if st.button("🎙️ Speak"):
        if not text_input.strip():
            st.warning("⚠️ Please enter some English text.")
        else:
            async def speak_voice():
                try:
                    communicate = edge_tts.Communicate(text_input, voice=voice_dict[selected_voice])
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                        await communicate.save(tmpfile.name)
                        return tmpfile.name
                except:
                    fallback_voice = "en-US-AriaNeural"
                    st.warning("⚠️ Selected voice not available. Using fallback voice.")
                    communicate = edge_tts.Communicate(text_input, voice=fallback_voice)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                        await communicate.save(tmpfile.name)
                        return tmpfile.name

            audio_path = asyncio.run(speak_voice())

            st.markdown(f"🎧 **Speaking with {selected_voice}**")
            st.audio(audio_path, format="audio/mp3")

            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
                b64_audio = base64.b64encode(audio_bytes).decode()
                download_link = f'<a href="data:audio/mp3;base64,{b64_audio}" download="voice_output.mp3">📅 Click to Download MP3</a>'
                st.markdown(download_link, unsafe_allow_html=True)

elif menu == "About Creator":
    st.markdown('<div class="main-title">👨‍💻 About the Creator</div>', unsafe_allow_html=True)

    logo_url = "https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json"  
    logo_json = load_lottieurl(logo_url)

    if logo_json:
        st_lottie(logo_json, speed=1, height=250, key="creator-logo")
    else:
        st.info("👨‍💻 [Animated logo couldn't load — check internet or URL]")

    st.markdown("""
        <div style='max-width:700px; margin:auto; font-size:1.1em;'>
        <ul>
            <li><b>Name:</b> Mohammed Farwez (Munna)</li>
            <li><b>Role:</b> Streamlit Enthusiast | Python Developer | ECE Student</li>
            <li><b>Education:</b> B.Tech in Electronics & Communication Engineering</li>
            <li><b>Projects:</b> Smart Resume Generator, Translator Creator, IoT Automation, and more</li>
            <li><b>Skills:</b> Python, Streamlit, AI/ML, Embedded Systems, Web APIs, Automation</li>
            <li><b>Achievements:</b> Built 10+ apps, Hackathon finalist, Open-source contributor</li>
            <li><b>Interests:</b> Python, AI, Electronics, UI/UX, Tech Blogging 🛠️</li>
        </ul>
        <hr>
        <p>
        <b>About Me:</b><br>
        I am passionate about building user-friendly apps that solve real-world problems. I love exploring new technologies, collaborating with fellow developers, and sharing knowledge through open-source projects and tutorials.
        </p>
        <p>
        <b>Connect with me:</b><br>
        <a href="mailto:mohammadfarwez23@gmail.com">Email</a> |
        <a href="https://www.instagram.com/i_faruuu/">Instagram</a> |
        <a href="https://github.com/farwez">GitHub</a> |
        <a href="https://www.linkedin.com/in/mohammed-farwez-76238a35a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app ">LinkedIn</a>
        </p>
        <blockquote style="color:#6a1b9a; font-style:italic;">
        💡 “Turning ideas into apps one script at a time!”
        </blockquote>
        </div>
    """, unsafe_allow_html=True)

elif menu == "Contact/Feedback":
    st.markdown('<div class="main-title">📬 Contact & Feedback</div>', unsafe_allow_html=True)
    st_lottie(load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_kkflmtur.json"), speed=1, height=250, key="contact-lottie")
    
    st.markdown("""
       We'd love to hear your thoughts!
       - 📧 Email: mohammadfarwez23@gmail.com  
       - 📱 Instagram: [@i_faruuu](https://www.instagram.com/i_faruuu/)
    """, unsafe_allow_html=True)

    lottie_submit = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_touohxv0.json")

    # Track feedback submission
    if "feedback_sent" not in st.session_state:
        st.session_state.feedback_sent = False

    # Feedback form
    if not st.session_state.feedback_sent:
        with st.form("feedback_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            msg = st.text_area("Message")
            submitted = st.form_submit_button("Submit Feedback")

            if submitted:
                if name and email and msg:
                    payload = {
                        "name": name,
                        "email": email,
                        "message": msg
                    }
                    response = requests.post("https://formspree.io/f/xqabjlag", data=payload)
                    if response.status_code == 200:
                        st.session_state.feedback_sent = True
                    else:
                        st.error("❌ Failed to send feedback.")
                else:
                    st.warning("⚠️ Please fill all fields.")
    else:
        st.success("✅ Feedback sent successfully!")
        st.balloons()
        if lottie_submit:
            st_lottie(lottie_submit, height=250)
        if st.button("✏️ Submit Another Response"):
            st.session_state.feedback_sent = False
