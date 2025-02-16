# Multi-Language Text-to-Speech (TTS) System

This project provides a **multi-language text-to-speech (TTS) system** using Facebook's MMS-TTS models. The system can automatically detect the language of the input text and generate speech in that language.

## 🚀 Features
- **Supports multiple languages:** Hindi, English, Tamil, Punjabi, Bengali, Marathi, Gujarati, Kannada, Malayalam, and Telugu.
- **Automatic language detection** using `langdetect` and `langid`.
- **On-the-fly model loading** to generate high-quality speech.
- **Outputs WAV audio format** stored in memory for easy playback or saving.

## 📌 Supported Languages
| Language | Code |
|----------|------|
| Hindi    | hi   |
| English  | en   |
| Tamil    | ta   |
| Punjabi  | pa   |
| Bengali  | bn   |
| Marathi  | mr   |
| Gujarati | gu   |
| Kannada  | kn   |
| Malayalam| ml   |
| Telugu   | te   |

## 🛠 Installation
### 1️⃣ Prerequisites
Ensure you have **Python 3.8+** installed along with `pip`.

### 2️⃣ Install Required Dependencies
```sh
pip install torch numpy soundfile transformers langdetect langid
```

## 📜 Usage
```python
from your_tts_module import speak

text = "Hello, how are you?"
audio_stream = speak(text)

if audio_stream:
    with open("output.wav", "wb") as f:
        f.write(audio_stream.read())
    print("✅ Audio saved as output.wav")
else:
    print("❌ Failed to generate speech.")
```

## 📌 How It Works
1. **Detects the language** of the given text.
2. **Loads the appropriate TTS model** based on the detected language.
3. **Generates speech audio** and returns it as an in-memory WAV file.

## ⚠️ Error Handling
- If a language is not supported, it prints a warning.
- If a model fails to load, it skips that language.

## 📜 License
This project is open-source and available under the MIT License.

