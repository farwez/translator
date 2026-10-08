# 🌍 Translator — Multilingual Voice Assistant

<p align="center">
  <strong>Translate. Listen. Learn. Communicate.</strong>
</p>

<p align="center">
  A lightweight multilingual translation and text-to-speech web application built with Python and Streamlit.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Googletrans-Translation-4285F4?style=for-the-badge" alt="Googletrans">
  <img src="https://img.shields.io/badge/Edge--TTS-Voice-0078D4?style=for-the-badge" alt="Edge TTS">
  <img src="https://img.shields.io/badge/gTTS-TTS-34A853?style=for-the-badge" alt="gTTS">
</p>

<p align="center">
  <a href="#-live-demo">Live Demo</a> •
  <a href="#-features">Features</a> •
  <a href="#-user-flow">User Flow</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-future-roadmap">Roadmap</a>
</p>

---

## 🌐 Live Demo

<p align="center">

### 🚀 Try Translator Live

<a href="https://translator-23.streamlit.app/">
  <strong>👉 Open Translator Web App</strong>
</a>

</p>

---

# ✨ About the Project

**Translator** is a multilingual voice assistant that combines **text translation** with **text-to-speech** capabilities in a simple, interactive web interface.

The application allows users to:

```text
Enter Text
    ↓
Select Language
    ↓
Translate
    ↓
🔊 Listen to Translation
    ↓
💾 Download Audio
```

The goal is simple:

> **Make multilingual communication faster, easier, and more accessible.**

---

# 🎯 Why Translator?

Traditional translation tools often focus only on converting text from one language to another.

Translator goes one step further by combining:

- 🌍 **Translation**
- 🔊 **Text-to-Speech**
- 🎙️ **Voice Selection**
- 💾 **Audio Download**
- 🌗 **Theme Customization**
- 📱 **Responsive UI**

This makes it useful not only for translation, but also for **language learning, pronunciation practice, travel, communication, and accessibility**.

---

# ✨ Features

### 🌍 Multilingual Translation

Translate text across multiple supported languages using **Googletrans**.

### 🔊 Voice Translation

Listen to translated text using text-to-speech engines.

Supports voice generation through:

- **Edge-TTS**
- **gTTS**

### 🎙️ Voice Styles

Experiment with different voice options, including male and female voices where supported.

### 💾 Download Audio

Convert translated text into an MP3 file and download it for later use.

### 🌗 Light & Dark Themes

Switch between different visual themes for a more comfortable experience.

### 📱 Responsive Interface

Designed to work across:

- 💻 Desktop
- 💻 Laptop
- 📱 Mobile devices

### 📬 Feedback System

A built-in feedback form allows users to send suggestions and feedback through **Formspree**.

### 🎨 Interactive UI

The interface uses **Lottie animations** and custom styling to create a more engaging experience.

---

# 🧭 User Flow

```text
                    🏠 HOME
                       │
                       ▼
             Learn About Translator
                       │
                       ▼
              🌍 TRANSLATOR
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       Enter Text          Select Language
             │                   │
             └─────────┬─────────┘
                       ▼
                    Translate
                       │
              ┌────────┴────────┐
              ▼                 ▼
         🔊 Listen          💾 Download
              │                 │
              └────────┬────────┘
                       ▼
                🎙️ VOICE STYLES
                       │
                       ▼
              Explore Voice Options
                       │
                       ▼
                 👨‍💻 ABOUT
                       │
                       ▼
              📬 CONTACT / FEEDBACK
```

---

# 🏗️ Application Structure

The application is organized around several user-facing sections:

| Section | Purpose |
|---------|---------|
| 🏠 **Home** | Introduction to the application |
| 🌍 **Translate Languages** | Translate, listen, and download |
| 🎙️ **Voice Styles** | Explore text-to-speech voices |
| 👨‍💻 **About Creator** | Developer information |
| 📬 **Contact / Feedback** | Submit feedback |

---

# 🧠 How It Works

Translator follows a simple processing pipeline:

```text
              👤 USER
                 │
                 ▼
          ┌──────────────┐
          │   Text Input │
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │ Googletrans  │
          │ Translation  │
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │ Translated   │
          │    Text      │
          └──────┬───────┘
                 │
          ┌──────┴───────┐
          ▼              ▼
     ┌─────────┐    ┌─────────┐
     │ Edge-TTS│    │  gTTS   │
     └────┬────┘    └────┬────┘
          │              │
          └──────┬───────┘
                 ▼
          🔊 Audio Output
                 │
          ┌──────┴──────┐
          ▼             ▼
       ▶️ Listen     💾 Download
```

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| 🐍 **Programming Language** | Python |
| 🎨 **Frontend / UI** | Streamlit |
| 🌍 **Translation** | Googletrans |
| 🔊 **Text-to-Speech** | Edge-TTS |
| 🔊 **Fallback TTS** | gTTS |
| 📬 **Feedback** | Formspree |
| ✨ **Animations** | Lottie |
| 📦 **Media Handling** | Base64, Tempfile |
| ☁️ **Deployment** | Streamlit Community Cloud |

---

# 📁 Project Architecture

A typical project structure looks like:

```text
Translator/
│
├── 📄 app.py
├── 📄 requirements.txt
├── 📄 README.md
│
├── 📁 assets/
│   ├── animations/
│   └── images/
│
└── 📁 components/
    └── ...
```

> Adjust the structure above to match your actual repository files if your implementation uses different filenames.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/farwez/Translator.git
cd Translator
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL similar to:

```text
http://localhost:8501
```

Open it in your browser and start translating.

---

# ☁️ Deployment

Translator can be deployed using **Streamlit Community Cloud**.

Typical deployment workflow:

```text
GitHub Repository
       │
       ▼
Streamlit Community Cloud
       │
       ▼
Install requirements.txt
       │
       ▼
Run Streamlit Application
       │
       ▼
🌐 Public Web Application
```

This makes the application accessible through a public URL without requiring users to install Python locally.

---

# 📦 Dependencies

Example `requirements.txt`:

```text
streamlit
googletrans
edge-tts
gTTS
requests
```

Make sure the dependency versions match the versions used by your working project.

---

# 🎨 UI & Design

Translator focuses on creating a simple but visually engaging experience.

### Design principles

- 🎯 Minimal interaction steps
- 📱 Responsive layout
- 🌗 Theme support
- ✨ Animated visual elements
- 🔊 Clear audio controls
- 💾 Easy download workflow
- 🧭 Simple navigation

The goal is to keep the interface approachable even for users who are not technically familiar with translation tools.

---

# 🔐 Privacy & API Considerations

Translator relies on external services for translation, text-to-speech, and feedback functionality.

When deploying or modifying the application:

- Avoid exposing private API credentials.
- Keep secrets outside source code where applicable.
- Review third-party service terms and usage limits.
- Do not process sensitive personal information unnecessarily.

---

# 🔮 Future Roadmap

Possible improvements for future versions:

- [ ] 🎤 Speech-to-text input
- [ ] 🗣️ Real-time voice translation
- [ ] 🌍 Support for more languages
- [ ] 📚 Translation history
- [ ] ⭐ Favorite translations
- [ ] 📋 Copy translation button
- [ ] 🎙️ More voice options
- [ ] 🔊 Adjustable speech speed
- [ ] 📱 Progressive Web App support
- [ ] 🤖 AI-powered contextual translation
- [ ] 📴 Offline translation support
- [ ] 🗂️ Download translation history
- [ ] 🌐 Automatic source-language detection

---

# 💡 Potential Use Cases

Translator can be useful for:

### 🎓 Students

Practice foreign languages and pronunciation.

### ✈️ Travelers

Translate common phrases and listen to their pronunciation.

### 💬 Everyday Communication

Understand and communicate across different languages.

### 📚 Language Learning

Read translated text while simultaneously listening to pronunciation.

### ♿ Accessibility

Convert written translations into spoken audio.

---

# ⭐ Show Some Love

If you found **Translator** useful or interesting, consider giving the repository a ⭐.

<p align="center">

**⭐ Star the repository if you like the project!**

</p>

---

# 👨‍💻 Built With

<p align="center">

🐍 **Python**  
⚡ **Streamlit**  
🌍 **Googletrans**  
🔊 **Edge-TTS**  
🎙️ **gTTS**  
📬 **Formspree**  
✨ **Lottie**

</p>

---

<p align="center">
  <strong>🌍 Translator</strong><br>
  <em>Breaking language barriers, one translation at a time.</em>
</p>

<p align="center">
  Made with ❤️
</p>
