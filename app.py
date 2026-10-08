import streamlit as st
from deep_translator import GoogleTranslator
import tempfile
import os
import base64
import csv
import io
from datetime import datetime
from streamlit_lottie import st_lottie
import requests
import asyncio
from streamlit_option_menu import option_menu
from streamlit_mic_recorder import speech_to_text
try:
    from langdetect import detect, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

st.set_page_config(page_title="Translator Pro", layout="wide", page_icon="🌐")

st.markdown("""
    <style>
        footer {visibility: hidden;}
        
        .main-title {
            font-size: 2.5em;
            font-weight: 800;
            text-align: center;
            margin-bottom: 5px;
            letter-spacing: -0.5px;
        }
        .subtext {
            font-size: 1.1em;
            text-align: center;
            margin-bottom: 25px;
            opacity: 0.85;
        }
        .glass-card {
            background-color: var(--secondary-background-color);
            border-radius: 12px;
            border: 1px solid rgba(128, 128, 128, 0.15);
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .glass-card:hover {
            border-color: rgba(76, 175, 80, 0.4);
        }
        .action-card {
            background-color: var(--secondary-background-color);
            border-radius: 12px;
            border: 1px solid rgba(128, 128, 128, 0.15);
            padding: 18px 20px;
            margin-bottom: 15px;
        }
        .tag-badge {
            display: inline-block;
            background: rgba(76, 175, 80, 0.12);
            color: #4CAF50;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .char-counter { font-size: 0.78em; opacity: 0.6; text-align: right; margin-top: 4px; }
        .copy-btn {
            background: rgba(76,175,80,0.12); color: #4CAF50;
            border: 1px solid rgba(76,175,80,0.3); padding: 6px 14px;
            border-radius: 8px; cursor: pointer; font-size: 0.85em;
            font-weight: 600; transition: all 0.2s;
        }
        .copy-btn:hover { background: rgba(76,175,80,0.25); }
        .history-item {
            border-left: 3px solid #4CAF50;
            padding: 10px 14px; margin-bottom: 10px;
            background: var(--secondary-background-color);
            border-radius: 0 8px 8px 0;
        }
        .lang-detected {
            display: inline-block; background: rgba(33,150,243,0.12);
            color: #2196F3; padding: 3px 10px; border-radius: 20px;
            font-size: 0.8em; font-weight: 600; margin-left: 8px;
        }
        @media (max-width: 768px) {
            .main-title { font-size: 1.8em; }
            .subtext { font-size: 0.95em; margin-bottom: 15px; }
            .glass-card { padding: 15px; margin-bottom: 15px; border-radius: 8px; }
            .action-card { padding: 12px; }
            .mobile-wrap { flex-wrap: wrap !important; gap: 10px !important; }
            .about-grid { grid-template-columns: 1fr !important; gap: 5px !important; }
            .tag-badge { font-size: 0.75em; padding: 3px 8px; }
        }
    </style>
""", unsafe_allow_html=True)

def copy_to_clipboard_js(text):
    escaped = text.replace("'", "\\'").replace("\n", "\\n")
    return f"""
    <button class="copy-btn" onclick="navigator.clipboard.writeText('{escaped}').then(()=>{{this.innerText='✅ Copied!';setTimeout(()=>this.innerText='📋 Copy Translation',1500)}})">📋 Copy Translation</button>
    """

lang_dict = {
    'English': 'en', 'Hindi': 'hi', 'Telugu': 'te', 'Tamil': 'ta', 'French': 'fr',
    'Spanish': 'es', 'German': 'de', 'Italian': 'it', 'Portuguese': 'pt',
    'Russian': 'ru', 'Japanese': 'ja', 'Korean': 'ko', 'Chinese (Simplified)': 'zh-cn',
    'Arabic': 'ar', 'Dutch': 'nl', 'Turkish': 'tr', 'Urdu': 'ur', 'Bengali': 'bn',
    'Gujarati': 'gu', 'Marathi': 'mr'
}

voice_dict = {
    "👩 Female (Aria)": "en-US-AriaNeural",
    "👩 Female (Jenny)": "en-US-JennyNeural",
    "🤖 Male Robot (Christopher)": "en-US-ChristopherNeural",
    "👦 Male (Guy)": "en-US-GuyNeural",
    "🎤 Male (Andrew)": "en-US-AndrewNeural",
    "👨 Male (William - AU)": "en-AU-WilliamNeural",
    "👨 Male (Ryan - UK)": "en-GB-RyanNeural"
}

@st.cache_data(ttl=3600, show_spinner=False)
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200: return None
        return r.json()
    except:
        return None

def get_audio_player(audio_path, download_name="audio.mp3"):
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
        b64_audio = base64.b64encode(audio_bytes).decode()
        html = f"""
            <audio controls style="width: 100%; outline: none;">
                <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            </audio>
            <div style="margin-top: 10px;">
                <a href="data:audio/mp3;base64,{b64_audio}" download="{download_name}" 
                   style="text-decoration: none; background-color: #4CAF50; color: white; padding: 8px 16px; border-radius: 5px; font-size: 14px; font-weight: bold; display: inline-block;">
                   ⬇️ Download MP3
                </a>
            </div>
        """
        return html

if "history" not in st.session_state:
    st.session_state.history = []
if "total_words" not in st.session_state:
    st.session_state.total_words = 0
if "total_chars" not in st.session_state:
    st.session_state.total_chars = 0

with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    menu = option_menu(
        "Translator Pro",
        ["Home", "Translate", "History", "Voice Styles", "About", "Feedback"],
        icons=["house", "translate", "clock-history", "mic", "person", "envelope"],
        menu_icon="globe",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#4CAF50", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "rgba(128,128,128,0.1)"},
            "nav-link-selected": {"background-color": "rgba(76, 175, 80, 0.1)", "color": "#4CAF50", "font-weight": "bold"},
        }
    )
    if st.session_state.history:
        st.markdown("---")
        st.markdown(f"📊 **{len(st.session_state.history)}** translations this session")
        st.markdown(f"✍️ **{st.session_state.total_words}** words processed")

if menu == "Home":
    st.markdown(
        '<div style="display:flex;gap:40px;align-items:center;padding:20px 0 10px;">'
        '<div style="flex:1.3;">'
        '<div style="font-size:0.82em;font-weight:700;letter-spacing:2px;color:#4CAF50;text-transform:uppercase;margin-bottom:10px;">✦ AI-Powered Translation</div>'
        '<div style="font-size:2.6em;font-weight:900;line-height:1.15;margin-bottom:14px;">Break Every<br>Language Barrier.</div>'
        '<div style="font-size:1em;opacity:0.72;line-height:1.7;margin-bottom:24px;max-width:460px;">Instantly translate text or speech across <b>20+ languages</b> with neural voice synthesis — right in your browser.</div>'
        '<div style="display:flex;gap:12px;">'
        '<div style="flex:1;background:rgba(76,175,80,0.08);border:1px solid rgba(76,175,80,0.2);border-radius:12px;padding:14px;text-align:center;"><div style="font-size:1.7em;font-weight:900;color:#4CAF50;">20+</div><div style="font-size:0.75em;opacity:0.6;margin-top:2px;">Languages</div></div>'
        '<div style="flex:1;background:rgba(76,175,80,0.08);border:1px solid rgba(76,175,80,0.2);border-radius:12px;padding:14px;text-align:center;"><div style="font-size:1.7em;font-weight:900;color:#4CAF50;">7+</div><div style="font-size:0.75em;opacity:0.6;margin-top:2px;">Neural Voices</div></div>'
        '<div style="flex:1;background:rgba(76,175,80,0.08);border:1px solid rgba(76,175,80,0.2);border-radius:12px;padding:14px;text-align:center;"><div style="font-size:1.7em;font-weight:900;color:#4CAF50;">&lt;1s</div><div style="font-size:0.75em;opacity:0.6;margin-top:2px;">Response</div></div>'
        '</div>'
        '</div>'
        '<div style="flex:1;display:flex;align-items:center;justify-content:center;">'
        '<span style="font-size:8em;line-height:1;">🌐</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")


    st.markdown('<h3 style="text-align:center; margin-bottom:20px; font-size:1.4em;">✨ What You Can Do</h3>', unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("🎙️", "Voice Input", "Speak into your mic — speech is instantly converted to text."),
        ("🌍", "20+ Languages", "European, Asian & Indian languages with high accuracy."),
        ("🎧", "Neural Voices", "Human-like voiceovers via Edge TTS & Google TTS."),
        ("📤", "Export & Share", "Copy translations or download audio as MP3 instantly."),
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(
                f'<div class="glass-card" style="text-align:center; padding:22px 14px;">'
                f'<div style="font-size:2em; margin-bottom:10px;">{icon}</div>'
                f'<div style="font-weight:700; font-size:0.95em; margin-bottom:6px;">{title}</div>'
                f'<div style="font-size:0.82em; opacity:0.7; line-height:1.5;">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    col_steps, col_langs = st.columns([1, 1.2], gap="large")

    with col_steps:
        st.markdown("### 🚀 How It Works")
        steps = [
            ("1", "Open **Translate** tab from the sidebar."),
            ("2", "Type, paste, or **speak** your text."),
            ("3", "Choose a target language & hit **Translate**."),
            ("4", "Listen to audio or **download** your MP3."),
        ]
        for num, step in steps:
            st.markdown(
                f'<div style="display:flex; align-items:flex-start; gap:14px; margin-bottom:14px;">'
                f'<div style="min-width:28px; height:28px; background:#4CAF50; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.85em;">{num}</div>'
                f'<div style="font-size:0.95em; opacity:0.9; padding-top:4px;">{step}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    with col_langs:
        st.markdown("### 🌐 Supported Languages")
        langs = [
            ("🇺🇸","English"), ("🇮🇳","Hindi"), ("🇮🇳","Telugu"), ("🇮🇳","Tamil"),
            ("🇪🇸","Spanish"), ("🇫🇷","French"), ("🇩🇪","German"), ("🇯🇵","Japanese"),
            ("🇰🇷","Korean"), ("🇨🇳","Chinese"), ("🇸🇦","Arabic"), ("🇮🇹","Italian"),
            ("🇷🇺","Russian"), ("🇵🇹","Portuguese"), ("🇳🇱","Dutch"), ("🇹🇷","Turkish"),
            ("🇵🇰","Urdu"), ("🇧🇩","Bengali"), ("🇮🇳","Gujarati"), ("🇮🇳","Marathi"),
        ]
        badges = "".join(
            f'<span style="background:rgba(128,128,128,0.12); border:1px solid rgba(128,128,128,0.15); padding:5px 11px; border-radius:20px; font-size:0.82em; margin:3px; display:inline-block;">{flag} {name}</span>'
            for flag, name in langs
        )
        st.markdown(f'<div style="display:flex; flex-wrap:wrap; gap:2px; margin-top:8px;">{badges}</div>', unsafe_allow_html=True)

elif menu == "Translate":
    st.markdown('<div class="main-title">🌍 Translation Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtext">Translate text or spoken voice across 20+ languages with neural audio playback.</div>', unsafe_allow_html=True)

    t_col1, t_col2 = st.columns([1, 1], gap="medium")
    with t_col1:
        st.markdown("<span class='tag-badge'>🌐 Source: Auto-Detect</span>", unsafe_allow_html=True)
        spoken_text = speech_to_text(language='en', start_prompt="🎙️ Speak to Input", stop_prompt="⏹️ Stop Recording", use_container_width=True, just_once=True, key='STT')
    with t_col2:
        st.markdown("<span class='tag-badge' style='background: rgba(33, 150, 243, 0.12); color: #2196F3;'>🎯 Destination Language</span>", unsafe_allow_html=True)
        target_lang = st.selectbox("Destination Language:", list(lang_dict.keys()), label_visibility="collapsed")

    with st.expander("📄 Upload a File to Translate (.txt or .pdf)", expanded=False):
        uploaded_file = st.file_uploader("Upload file", type=["txt", "pdf"], label_visibility="collapsed")
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                file_text = uploaded_file.read().decode("utf-8", errors="ignore")
            elif uploaded_file.type == "application/pdf":
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(uploaded_file)
                    file_text = " ".join(page.extract_text() or "" for page in reader.pages)
                except ImportError:
                    file_text = ""
                    st.warning("⚠️ PDF support requires PyPDF2. Install it with: pip install PyPDF2")
            if file_text.strip():
                st.session_state["file_text"] = file_text[:3000]
                st.success(f"✅ Loaded {len(file_text)} characters from **{uploaded_file.name}**")
                st.text_area("Preview (first 500 chars):", file_text[:500], height=100, disabled=True)

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("#### 📝 Original Text")
        if spoken_text:
            default_text = spoken_text
        elif "file_text" in st.session_state and st.session_state.file_text:
            default_text = st.session_state.file_text
            st.session_state.file_text = ""
        else:
            default_text = st.session_state.get("quick_text", "")

        text_input = st.text_area("Original Text", value=default_text, height=180,
                                   placeholder="Type here, use the mic, or upload a file above...",
                                   label_visibility="collapsed", key="main_text_input")

        char_count = len(text_input)
        word_count = len(text_input.split()) if text_input.strip() else 0
        st.markdown(f"<div class='char-counter'>✍️ {word_count} words &nbsp;|&nbsp; {char_count} characters</div>", unsafe_allow_html=True)

        if text_input.strip() and LANGDETECT_AVAILABLE:
            try:
                detected_code = detect(text_input)
                lang_name_map = {
                    'en':'English','hi':'Hindi','te':'Telugu','ta':'Tamil','fr':'French',
                    'es':'Spanish','de':'German','it':'Italian','pt':'Portuguese','ru':'Russian',
                    'ja':'Japanese','ko':'Korean','zh-cn':'Chinese','ar':'Arabic','nl':'Dutch',
                    'tr':'Turkish','ur':'Urdu','bn':'Bengali','gu':'Gujarati','mr':'Marathi'
                }
                detected_name = lang_name_map.get(detected_code, detected_code.upper())
                st.markdown(f"🔍 Detected language: <span class='lang-detected'>{detected_name}</span>", unsafe_allow_html=True)
            except:
                pass

        st.markdown("<small style='opacity: 0.7;'>⚡ Quick Phrases:</small>", unsafe_allow_html=True)
        q1, q2 = st.columns(2)
        with q1:
            if st.button("👋 Hello, nice to meet you!", use_container_width=True):
                st.session_state["quick_text"] = "Hello, nice to meet you!"
                st.rerun()
        with q2:
            if st.button("✈️ Where is the train station?", use_container_width=True):
                st.session_state["quick_text"] = "Where is the nearest train station?"
                st.rerun()

    with col2:
        st.markdown("#### 🎯 Translated Result")
        output_placeholder = st.empty()

    st.markdown("<br>", unsafe_allow_html=True)
    translate_btn = st.button("🚀 Translate & Synthesize Audio", use_container_width=True, type="primary")

    if translate_btn:
        if not text_input.strip():
            st.warning("⚠️ Please enter some text or use the mic before translating.")
        else:
            with st.spinner(f"🔄 Translating to {target_lang}..."):
                try:
                    translated = GoogleTranslator(source='auto', target=lang_dict[target_lang]).translate(text_input)

                    now = datetime.now()
                    st.session_state.history.append({
                        "src": text_input,
                        "tgt": translated,
                        "lang": target_lang,
                        "time": now.strftime("%I:%M %p"),
                        "date": now.strftime("%d %B %Y")
                    })
                    st.session_state.total_words += len(text_input.split())
                    st.session_state.total_chars += len(text_input)
                    st.session_state.pop("quick_text", None)

                    with col2:
                        output_placeholder.markdown(
                            f"<div class='glass-card' style='min-height: 180px;'>"
                            f"<div style='font-size:1.15em; font-weight:500; line-height:1.6;'>{translated}</div>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                        st.success(f"✅ Translated to **{target_lang}**")
                        st.markdown(copy_to_clipboard_js(translated), unsafe_allow_html=True)

                        share_text = f"🌐 Translator Pro\n\nOriginal: {text_input}\n\n{target_lang} Translation: {translated}"
                        st.download_button(
                            label="📤 Download as Text",
                            data=share_text,
                            file_name=f"translation_{lang_dict[target_lang]}.txt",
                            mime="text/plain"
                        )

                    audio_path = None
                    if lang_dict[target_lang] == 'en':
                        import edge_tts
                        async def save_edge_audio():
                            communicate = edge_tts.Communicate(translated, voice="en-US-ChristopherNeural")
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                                await communicate.save(tmpfile.name)
                                return tmpfile.name
                        try:
                            audio_path = asyncio.run(save_edge_audio())
                        except Exception:
                            from gtts import gTTS
                            tts = gTTS(text=translated, lang='en')
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                                tts.save(tmpfile.name)
                                audio_path = tmpfile.name
                    else:
                        from gtts import gTTS
                        tts = gTTS(text=translated, lang=lang_dict[target_lang])
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                            tts.save(tmpfile.name)
                            audio_path = tmpfile.name

                    if audio_path:
                        st.markdown(
                            f"<div class='action-card'>"
                            f"<h4 style='margin-top:0;'>🎧 Audio Playback ({target_lang})</h4>"
                            f"{get_audio_player(audio_path, f'translation_{lang_dict[target_lang]}.mp3')}"
                            f"</div>",
                            unsafe_allow_html=True
                        )

                except Exception as e:
                    st.error(f"❌ Translation Error: {e}")
    else:
        with col2:
            output_placeholder.markdown(
                "<div class='glass-card' style='min-height:180px; display:flex; align-items:center; justify-content:center; opacity:0.5;'>"
                "<span>✨ Translation result will appear here...</span></div>",
                unsafe_allow_html=True
            )

elif menu == "History":
    st.markdown('<div class="main-title">📜 Translation History</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtext">Your translations grouped by date — search, export, and review.</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("<br>", unsafe_allow_html=True)
        empty_col = st.columns([1, 2, 1])[1]
        with empty_col:
            lottie_empty = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_ht6ixnkm.json")
            if lottie_empty:
                st_lottie(lottie_empty, height=200, key="empty-history")
            st.markdown(
                '<div style="text-align:center; padding:20px;">'
                '<h3>No translations yet!</h3>'
                '<p style="opacity:0.7;">Go to the <b>Translate</b> tab to get started.</p>'
                '</div>',
                unsafe_allow_html=True
            )
    else:
        total = len(st.session_state.history)
        langs_used = len(set(h["lang"] for h in st.session_state.history))
        most_used_lang = max(
            set(h["lang"] for h in st.session_state.history),
            key=lambda l: sum(1 for h in st.session_state.history if h["lang"] == l)
        )

        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.metric("📄 Translations", total)
        with s2:
            st.metric("✍️ Words", st.session_state.total_words)
        with s3:
            st.metric("🌍 Languages", langs_used)
        with s4:
            st.metric("🏆 Top Language", most_used_lang)

        st.markdown("<br>", unsafe_allow_html=True)

        act_col1, act_col2, act_col3 = st.columns([2, 1, 1])
        with act_col1:
            search_query = st.text_input("", placeholder="🔍 Search by keyword or language...", label_visibility="collapsed")
        with act_col2:
            csv_buffer = io.StringIO()
            writer = csv.DictWriter(csv_buffer, fieldnames=["date", "time", "lang", "src", "tgt"])
            writer.writeheader()
            writer.writerows(st.session_state.history)
            st.download_button("⬇️ Export CSV", data=csv_buffer.getvalue(),
                               file_name="translation_history.csv", mime="text/csv",
                               use_container_width=True)
        with act_col3:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.history = []
                st.session_state.total_words = 0
                st.session_state.total_chars = 0
                st.rerun()

        st.markdown("---")

        all_items = list(reversed(st.session_state.history))
        if search_query.strip():
            q = search_query.strip().lower()
            all_items = [h for h in all_items
                         if q in h["src"].lower() or q in h["tgt"].lower() or q in h["lang"].lower()]

        if not all_items:
            st.warning(f"🔍 No results for **\"{search_query}\"**.")
        else:
            st.markdown(f"<small style='opacity:0.6;'>Showing {len(all_items)} of {total} translation(s)</small>",
                        unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            from itertools import groupby
            def get_date(item):
                return item.get("date", "Today")

            groups = {}
            for item in all_items:
                d = get_date(item)
                groups.setdefault(d, []).append(item)

            for date_label, items in groups.items():
                st.markdown(
                    f'<div style="display:flex; align-items:center; gap:12px; margin:20px 0 14px;">'
                    f'<div style="flex:1; height:1px; background:rgba(128,128,128,0.2);"></div>'
                    f'<span style="font-size:0.82em; font-weight:700; opacity:0.55; white-space:nowrap; padding:4px 12px; border:1px solid rgba(128,128,128,0.2); border-radius:20px;">📅 {date_label}</span>'
                    f'<div style="flex:1; height:1px; background:rgba(128,128,128,0.2);"></div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                for item in items:
                    idx = st.session_state.history.index(item) + 1
                    time_str = item.get("time", "")
                    src_preview = item["src"][:180] + ("..." if len(item["src"]) > 180 else "")
                    tgt_preview = item["tgt"][:180] + ("..." if len(item["tgt"]) > 180 else "")

                    card_html = (
                        f'<div class="glass-card" style="margin-bottom:10px; padding:16px 20px;">'
                        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">'
                        f'<span class="tag-badge">{item["lang"]}</span>'
                        f'<span style="font-size:0.78em; opacity:0.5;">🕒 {time_str}</span>'
                        f'</div>'
                        f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">'
                        f'<div>'
                        f'<div style="font-size:0.72em; font-weight:700; opacity:0.45; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:5px;">Original</div>'
                        f'<div style="font-size:0.93em; line-height:1.5; opacity:0.85;">{src_preview}</div>'
                        f'</div>'
                        f'<div style="border-left:2px solid rgba(76,175,80,0.35); padding-left:14px;">'
                        f'<div style="font-size:0.72em; font-weight:700; color:#4CAF50; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:5px;">{item["lang"]}</div>'
                        f'<div style="font-size:0.93em; line-height:1.5; font-weight:500;">{tgt_preview}</div>'
                        f'</div>'
                        f'</div>'
                        f'</div>'
                    )
                    st.markdown(card_html, unsafe_allow_html=True)
                    st.markdown(copy_to_clipboard_js(item["tgt"]), unsafe_allow_html=True)


elif menu == "Voice Styles":
    st.markdown('<div class="main-title">🔊 Neural Voice Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtext">Convert English text into ultra-realistic lifelike AI voiceovers.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.markdown("#### ✍️ Input Script")
        text_input = st.text_area("Input Script", height=180, placeholder="Enter English text to synthesize...", label_visibility="collapsed")
        
        st.markdown("#### 🎙️ Select Voice Model")
        selected_voice = st.selectbox("Voice Model:", list(voice_dict.keys()), label_visibility="collapsed")
        
        speak_btn = st.button("🎙️ Generate Neural Audio", use_container_width=True, type="primary")

    with col2:
        st.markdown("#### 🎧 Audio Output")
        if speak_btn:
            if not text_input.strip():
                st.warning("⚠️ Please enter some English text to synthesize.")
            else:
                with st.spinner("Synthesizing Neural Audio..."):
                    import edge_tts
                    async def speak_voice():
                        communicate = edge_tts.Communicate(text_input, voice=voice_dict[selected_voice])
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                            await communicate.save(tmpfile.name)
                            return tmpfile.name

                    try:
                        audio_path = asyncio.run(speak_voice())
                    except Exception:
                        from gtts import gTTS
                        tts = gTTS(text=text_input, lang='en')
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                            tts.save(tmpfile.name)
                            audio_path = tmpfile.name
                    
                    st.markdown(
                        f"""
                        <div class='glass-card'>
                            <span class='tag-badge'>HD Voice: {selected_voice}</span>
                            <h4 style='margin-top: 15px;'>Generated Audio Track</h4>
                            {get_audio_player(audio_path, 'neural_voice.mp3')}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    st.success("✅ Audio generated successfully!")
        else:
            st.markdown(
                """
                <div class='glass-card' style='min-height: 250px; display: flex; align-items: center; justify-content: center; opacity: 0.5;'>
                    <span>🎵 Synthesized audio player will appear here...</span>
                </div>
                """, 
                unsafe_allow_html=True
            )

elif menu == "About":
    st.markdown('<div class="main-title">👨‍💻 About the Creator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtext">Meet the developer behind Translator Pro.</div>', unsafe_allow_html=True)
    
    col_logo, col_info = st.columns([1, 2], gap="large")
    
    with col_logo:
        logo_json = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
        if logo_json:
            st_lottie(logo_json, speed=1, height=250, key="creator-logo")
            
    with col_info:
        html_content = (
            '<div class="glass-card">'
            '<h2 style="margin-top:0; color:#4CAF50;">Mohammed Farwez (Munna)</h2>'
            '<p style="font-size:1.1em; opacity:0.8; font-weight:500;">Streamlit Enthusiast | Python Developer | ECE Student</p>'
            '<hr style="opacity:0.2;">'
            '<table style="width:100%; border-collapse:collapse; margin-bottom:15px;">'
            '<tr><td style="padding:6px 10px 6px 0; white-space:nowrap; font-weight:bold;">🎓 Education:</td>'
            '<td style="padding:6px 0;">B.Tech in Electronics &amp; Communication Engineering</td></tr>'
            '<tr><td style="padding:6px 10px 6px 0; white-space:nowrap; font-weight:bold;">🛠️ Skills:</td>'
            '<td style="padding:6px 0;">'
            '<span class="tag-badge" style="margin:2px;">Python</span>'
            '<span class="tag-badge" style="margin:2px;">Streamlit</span>'
            '<span class="tag-badge" style="margin:2px;">AI/ML</span>'
            '<span class="tag-badge" style="margin:2px;">Web APIs</span>'
            '</td></tr>'
            '<tr><td style="padding:6px 10px 6px 0; white-space:nowrap; font-weight:bold;">🚀 Projects:</td>'
            '<td style="padding:6px 0;">Smart Resume Generator, Translator Pro, IoT Automation</td></tr>'
            '</table>'
            '<hr style="opacity:0.2;">'
            '<p style="font-size:0.95em; line-height:1.6;">I am passionate about building user-friendly applications that solve real-world problems. '
            'I love exploring new technologies, collaborating with fellow developers, and sharing knowledge through open-source projects.</p>'
            '<div class="mobile-wrap" style="display:flex; gap:12px; margin-top:20px; flex-wrap:wrap;">'
            '<a href="mailto:mohammadfarwez23@gmail.com" target="_blank" style="text-decoration:none;">'
            '<button style="background:#f44336;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-size:0.9em;">📧 Email Me</button></a>'
            '<a href="https://github.com/farwez" target="_blank" style="text-decoration:none;">'
            '<button style="background:#333;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-size:0.9em;">🐙 GitHub</button></a>'
            '<a href="https://www.linkedin.com/in/mohammed-farwez-76238a35a" target="_blank" style="text-decoration:none;">'
            '<button style="background:#0077b5;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-size:0.9em;">💼 LinkedIn</button></a>'
            '</div>'
            '</div>'
        )
        st.markdown(html_content, unsafe_allow_html=True)

elif menu == "Feedback":
    st.markdown('<div class="main-title">📬 Get in Touch</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtext">We value your feedback, feature requests, and bug reports!</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st_lottie(load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_kkflmtur.json"), speed=1, height=350)
        
        st.markdown("""
            <div class="glass-card" style="margin-top: 20px;">
                <h4 style="margin-top: 0;">Support & Inquiries</h4>
                <p>Have a question or need a custom feature? Reach out to us!</p>
                <p>📧 <b>Email:</b> support@translatorpro.ai</p>
                <p>🕒 <b>Response Time:</b> Within 24-48 hours</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if "feedback_sent" not in st.session_state:
            st.session_state.feedback_sent = False

        if not st.session_state.feedback_sent:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            with st.form("feedback_form", clear_on_submit=True):
                st.markdown("### 📝 Send a Message")
                
                feedback_type = st.selectbox("Feedback Type", ["General Inquiry", "Feature Request", "Bug Report", "Other"])
                name = st.text_input("Name", placeholder="Your Name")
                email = st.text_input("Email", placeholder="your.email@example.com")
                msg = st.text_area("Message", placeholder="Tell us how we can improve...", height=120)
                
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("🚀 Submit Feedback", use_container_width=True)

                if submitted:
                    if name and email and msg:
                        payload = {"name": name, "email": email, "type": feedback_type, "message": msg}
                        response = requests.post("https://formspree.io/f/xqabjlag", data=payload)
                        if response.status_code == 200:
                            st.session_state.feedback_sent = True
                            st.rerun()
                        else:
                            st.error("❌ Failed to send feedback. Please try again later.")
                    else:
                        st.warning("⚠️ Please fill out all fields before submitting.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class='glass-card' style='text-align: center; padding: 40px;'>
                    <h2 style='color: #4CAF50;'>🎉 Thank You!</h2>
                    <p>Your feedback has been successfully submitted. We appreciate your input!</p>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
            if st.button("✏️ Submit Another Response", use_container_width=True):
                st.session_state.feedback_sent = False
                st.rerun()
