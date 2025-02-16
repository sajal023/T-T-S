# from tts_sdk import speak

# # Test the function
# audio = speak("पंजाब भारत के उत्तरी भाग में स्थित एक सुंदर और सांस्कृतिक रूप से समृद्ध राज्य है। यह राज्य अपनी उपजाऊ भूमि, कृषि और सामाजिक एकता के लिए प्रसिद्ध है।")

# # Save the output if it's valid
# if audio:
#     with open("output.wav", "wb") as f:
#         f.write(audio.read())
#     print("✅ Audio saved as output.wav")


import sounddevice as sd
import numpy as np
from tts_sdk import speak
import soundfile as sf

# Generate the speech audio
audio = speak("पंजाब भारत के उत्तरी भाग में स्थित एक सुंदर और सांस्कृतिक रूप से समृद्ध राज्य है।")

# Play the audio in real-time
if audio:
    audio.seek(0)  # Reset buffer position
    data, samplerate = sf.read(audio, dtype="float32")  # Read audio data
    sd.play(data, samplerate)  # Play the audio
    sd.wait()  # Wait until playback is finished
    print("✅ Audio played successfully in real-time.")
else:
    print("❌ Failed to generate speech.")
