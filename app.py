import streamlit as st
import edge_tts
import asyncio
import os

# --- Page Configuration ---
st.set_page_config(page_title="Text to Audio Pro", page_icon="🎙️", layout="centered")
st.title("🎙️ Text to Audio Converter Pro")
st.write(
    "Convert text to speech in **Sinhala, Tamil, Hindi, and English** with custom voices, tempo, and pitch control! 🎚️")

# --- Voice Options (Restricted to Sinhala, Tamil, Hindi, English) ---
VOICE_OPTIONS = {
    # 🇱🇰 Sinhala
    "🇱🇰 Sinhala (Female - Thilini)": "si-LK-ThiliniNeural",
    "🇱🇰 Sinhala (Male - Sameera)": "si-LK-SameeraNeural",

    # 🇮🇳 Tamil
    "🇮🇳 Tamil (Female - Pallavi)": "ta-IN-PallaviNeural",
    "🇮🇳 Tamil (Male - Valluvar)": "ta-IN-ValluvarNeural",

    # 🇮🇳 Hindi
    "🇮🇳 Hindi (Female - Swara)": "hi-IN-SwaraNeural",
    "🇮🇳 Hindi (Male - Madhur)": "hi-IN-MadhurNeural",
    "🇮🇳 Hindi (Female - Ananya)": "hi-IN-AnanyaNeural",
    "🇮🇳 Hindi (Male - Rehaan)": "hi-IN-RehaanNeural",

    # 🇺🇸/🇬🇧 English
    "🇺🇸 English (Female - Jenny)": "en-US-JennyNeural",
    "🇺🇸 English (Male - Guy)": "en-US-GuyNeural",
    "🇺🇸 English (Female - Aria)": "en-US-AriaNeural",
    "🇺🇸 English (Male - Davis)": "en-US-DavisNeural",
    "🇺🇸 English (Female - Michelle)": "en-US-MichelleNeural",
    "🇺🇸 English (Male - Christopher)": "en-US-ChristopherNeural",
    "🇬🇧 English (Male - Ryan)": "en-GB-RyanNeural",
    "🇬🇧 English (Female - Sonia)": "en-GB-SoniaNeural",
}

# --- 1. User Input ---
text_input = st.text_area("📝 Enter text to convert to speech:", height=150)

# --- 2. Voice Selection ---
selected_voice_name = st.selectbox("🎤 Select Language & Voice:", list(VOICE_OPTIONS.keys()))
voice_code = VOICE_OPTIONS[selected_voice_name]

# --- 3. Tempo Control (Speed) ---
st.markdown("### 🎚️ Tempo Control")
tempo_percent = st.slider(
    "Speech Speed (%):",
    min_value=-50,
    max_value=100,
    value=0,
    step=10,
    help="-50% = very slow, 0% = normal, +100% = very fast"
)

if tempo_percent == 0:
    st.info("🎵 Normal speed")
elif tempo_percent < 0:
    st.info(f"🐢 Slowed down by {abs(tempo_percent)}%")
else:
    st.info(f"🐇 Sped up by {tempo_percent}%")

# --- 4. Pitch Control (Uses Hz) ---
pitch_hz = st.slider(
    "🎼 Voice Pitch (Hz):",
    min_value=-50,
    max_value=50,
    value=0,
    step=10,
    help="Lower pitch (e.g., -50Hz) = deeper voice, Higher pitch (e.g., +50Hz) = higher voice."
)

# --- 5. Convert Function ---
async def generate_audio(text, voice, rate, pitch, output_file):
    """Generate audio using edge-tts"""
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_file)

# --- 6. Convert Button ---
if st.button("🔄 Convert to Audio"):
    if text_input.strip():
        with st.spinner("🎙️ Generating audio... Please wait."):
            try:
                # Format rate as % and pitch as Hz (e.g., "+20%" and "-30Hz")
                rate_str = f"{tempo_percent:+}%"
                pitch_str = f"{pitch_hz:+}Hz"

                # Run the async function
                file_name = "generated_audio.mp3"
                asyncio.run(generate_audio(text_input, voice_code, rate_str, pitch_str, file_name))

                # Save state
                st.session_state['audio_file'] = file_name
                st.success("✅ Audio generated successfully!")
            except Exception as e:
                st.error(f"❌ Error generating audio: {e}")
    else:
        st.warning("⚠️ Please enter some text first!")

# --- 7. Playback and Download ---
if 'audio_file' in st.session_state and os.path.exists(st.session_state['audio_file']):
    audio_path = st.session_state['audio_file']

    st.markdown("---")
    st.subheader("🔊 Your Audio")

    # Audio Player
    st.audio(audio_path, format='audio/mp3')

    # Download Button
    with open(audio_path, "rb") as file:
        st.download_button(
            label="💾 Download Audio File",
            data=file,
            file_name="my_speech.mp3",
            mime="audio/mpeg"
        )

# --- 8. Footer ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 20px 0; color: #888;">
        <p style="font-size: 14px; margin: 0; font-family: sans-serif;">
            DEVELOPED BY 
            <a href="https://tharupamaportfolio.web.app" target="_blank" style="color: #FF4B4B; text-decoration: none; font-weight: 600;">
                THARUPAMA NAYANA
            </a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)