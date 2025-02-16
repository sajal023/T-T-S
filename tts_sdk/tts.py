
# import torch
# import numpy as np
# import io
# import soundfile as sf
# from transformers import VitsModel, AutoTokenizer
# from langdetect import detect
# from langid.langid import classify

# # ✅ Load Multi-Language TTS Models
# supported_languages = {
#     "hi": "facebook/mms-tts-hin",
#     "en": "facebook/mms-tts-eng",
#     "ta": "facebook/mms-tts-tam",
#     "pa": "facebook/mms-tts-pan",
#     "bn": "facebook/mms-tts-ben",
#     "mr": "facebook/mms-tts-mar",
#     "gu": "facebook/mms-tts-guj",
#     "kn": "facebook/mms-tts-kan",
#     "ml": "facebook/mms-tts-mal",
#     "te": "facebook/mms-tts-tel",
# }

# # ✅ Load models dynamically
# models = {}
# tokenizers = {}
# for lang, model_name in supported_languages.items():
#     try:
#         models[lang] = VitsModel.from_pretrained(model_name)
#         tokenizers[lang] = AutoTokenizer.from_pretrained(model_name)
#     except Exception as e:
#         print(f"⚠️ Failed to load model {lang}: {e}")

# def detect_language(text):
#     """Detects the language of the given text."""
#     try:
#         lang = detect(text)
#         if lang in supported_languages:
#             return lang
#         lang, _ = classify(text)
#         return lang if lang in supported_languages else "unknown"
#     except Exception as e:
#         print(f"⚠️ Language detection failed: {e}")
#         return "unknown"

# def synthesize_audio(text, lang):
#     """Converts text to speech and returns an in-memory audio stream."""
#     if lang not in models:
#         print(f"❌ Unsupported language: {lang}")
#         return None

#     model = models[lang]
#     tokenizer = tokenizers[lang]

#     # Tokenize and generate waveform
#     inputs = tokenizer(text, return_tensors="pt")
#     with torch.no_grad():
#         output = model(**inputs).waveform

#     # Get sampling rate
#     sampling_rate = getattr(model.config, "sampling_rate", 16000)

#     # Convert waveform to float32 and store in memory
#     waveform = output.squeeze().cpu().numpy()
#     audio_buffer = io.BytesIO()
#     sf.write(audio_buffer, waveform, sampling_rate, format="WAV")
#     audio_buffer.seek(0)  # Reset buffer position

#     return audio_buffer

# def speak(text):
#     """Detects language and generates speech audio."""
#     detected_lang = detect_language(text)
#     print(f"🔍 Detected Language: {detected_lang}")

#     if detected_lang in supported_languages:
#         return synthesize_audio(text, detected_lang)
#     else:
#         print("⚠️ Language not supported.")
#         return None

# def speak_with_lang(lang, text):
#     """
#     Generates speech audio when language is pre-detected.
#     This avoids repeated language detection and speeds up processing.
    
#     :param lang: Pre-detected language code (e.g., 'en', 'hi')
#     :param text: Text to synthesize
#     :return: In-memory audio buffer
#     """
#     if lang not in supported_languages:
#         print(f"⚠️ Language '{lang}' not supported.")
#         return None

#     print(f"🎙️ Using pre-detected language: {lang}")
#     return synthesize_audio(text, lang)



import torch
import numpy as np
import io
import soundfile as sf
from transformers import VitsModel, AutoTokenizer
from langdetect import detect
from langid.langid import classify

# ✅ Lazy Load Models to Save Memory
supported_languages = {
    "hi": "facebook/mms-tts-hin",
    "en": "facebook/mms-tts-eng",
    "ta": "facebook/mms-tts-tam",
    "pa": "facebook/mms-tts-pan",
    "bn": "facebook/mms-tts-ben",
    "mr": "facebook/mms-tts-mar",
    "gu": "facebook/mms-tts-guj",
    "kn": "facebook/mms-tts-kan",
    "ml": "facebook/mms-tts-mal",
    "te": "facebook/mms-tts-tel",
}

loaded_models = {}

def get_model(lang):
    """Lazy-load model without TorchScript to avoid unsupported comprehension ifs."""
    if lang not in loaded_models:
        try:
            print(f"🚀 Loading model for {lang}...")
            model = VitsModel.from_pretrained(supported_languages[lang])
            tokenizer = AutoTokenizer.from_pretrained(supported_languages[lang])

            # ❌ Remove TorchScript Compilation
            model.eval()  # Keep only evaluation mode
            loaded_models[lang] = (model, tokenizer)
        except Exception as e:
            print(f"⚠️ Failed to load model {lang}: {e}")
            return None, None

    return loaded_models[lang]


def detect_language(text):
    """Fast language detection with fallback."""
    try:
        lang, _ = classify(text)  # Fastest method
        if lang in supported_languages:
            return lang
        return detect(text) if detect(text) in supported_languages else "unknown"
    except Exception as e:
        print(f"⚠️ Language detection failed: {e}")
        return "unknown"

def synthesize_audio(text, lang):
    """Converts text to speech using optimized model inference."""
    model, tokenizer = get_model(lang)
    if not model:
        print(f"❌ Unsupported language: {lang}")
        return None

    inputs = tokenizer(text, return_tensors="pt")

    # Use FP16 for faster inference
    with torch.no_grad():
        output = model(**inputs).waveform.float()


    # Convert to audio
    waveform = output.squeeze().cpu().numpy()
    audio_buffer = io.BytesIO()
    sf.write(audio_buffer, waveform, 16000, format="WAV")
    audio_buffer.seek(0)

    return audio_buffer

def speak(text):
    """Detects language and generates speech audio efficiently."""
    detected_lang = detect_language(text)
    print(f"🔍 Detected Language: {detected_lang}")

    if detected_lang in supported_languages:
        return synthesize_audio(text, detected_lang)
    else:
        print("⚠️ Language not supported.")
        return None

def speak_with_lang(lang, text):
    """Generate speech audio using pre-detected language for faster processing."""
    if lang not in supported_languages:
        print(f"⚠️ Language '{lang}' not supported.")
        return None

    print(f"🎙️ Using pre-detected language: {lang}")
    return synthesize_audio(text, lang)




