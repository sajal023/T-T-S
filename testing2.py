import sounddevice as sd
import soundfile as sf
from tts_sdk import detect_language, speak_with_lang

# ✅ Text to synthesize
text = "पंजाब भारत के उत्तरी भाग में स्थित एक सुंदर और सांस्कृतिक रूप से समृद्ध राज्य है।"

# ✅ Detect the language first
detected_lang = detect_language(text)
print(f"🔍 Detected Language: {detected_lang}")

# ✅ Generate speech using detected language
audio = speak_with_lang(detected_lang, text)

# ✅ Play the generated speech in real-time
if audio:
    audio.seek(0)  # Reset buffer position
    data, samplerate = sf.read(audio, dtype="float32")  # Read audio data
    sd.play(data, samplerate)  # Play the audio
    sd.wait()  # Wait until playback is finished
    print("✅ Audio played successfully in real-time.")
else:
    print("❌ Failed to generate speech.")


