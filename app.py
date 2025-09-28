# app.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import soundfile as sf
import io
import tempfile
import os

# Load model + processor globally (to avoid reload for each request)
MODEL_ID = "openai/whisper-tiny"
processor = AutoProcessor.from_pretrained(MODEL_ID)
model = AutoModelForSpeechSeq2Seq.from_pretrained(MODEL_ID)
model.eval()

app = FastAPI()

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        # Load audio into numpy
        audio_bytes = await file.read()

        # Debug: Print file info
        print(f"File name: {file.filename}")
        print(f"Content type: {file.content_type}")
        print(f"File size: {len(audio_bytes)} bytes")

        # Try to read audio data
        audio_io = io.BytesIO(audio_bytes)

        # Save to temporary file first, as soundfile may not recognize format from BytesIO
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename or 'audio.wav')[1]) as temp_file:
            temp_file.write(audio_bytes)
            temp_file_path = temp_file.name

        try:
            audio_data, samplerate = sf.read(temp_file_path)
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)

        print(f"Audio shape: {audio_data.shape}")
        print(f"Sample rate: {samplerate}")

        # Preprocess
        inputs = processor(audio_data, sampling_rate=samplerate, return_tensors="pt")

        with torch.no_grad():
            generated_ids = model.generate(**inputs)
            transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return JSONResponse({"text": transcription})

    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse({"error": f"Audio processing failed: {str(e)}"}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000)
