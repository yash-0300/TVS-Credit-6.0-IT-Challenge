from openai import OpenAI
client = OpenAI(api_key = "PASTE_YOUR_KEY")

audio_file = open("/path/to/file/audio.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model = "whisper-1", 
  file = audio_file
)

print(transcription.text)