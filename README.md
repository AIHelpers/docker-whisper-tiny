# docker-whisper-tiny

Docker Compose setup for running OpenAI Whisper with the lightweight tiny model — fast, minimal, and speech-to-text ready.

## Features

- **Lightweight Model**: Uses OpenAI Whisper's tiny model for efficient speech-to-text transcription.
- **REST API**: Simple FastAPI-based REST API for audio transcription.
- **Docker Ready**: Easy deployment with Docker and Docker Compose.
- **Fast Inference**: Optimized for quick transcription of audio files.

## Prerequisites

- Docker
- Docker Compose

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AIHelpers/docker-whisper-tiny.git
   cd docker-whisper-tiny
   ```

2. Build and start the service:
   ```bash
   docker-compose up --build
   ```

The service will be available at `http://localhost:5000`.

## Usage

To use the transcription service, send a POST request to `/transcribe` with an audio file.

### Example with curl:

```bash
curl -X POST "http://localhost:5000/transcribe" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_audio_file.wav"
```

### Response:

```json
{
  "text": "This is the transcribed text from the audio file."
}
```

## API Documentation

### POST /transcribe

Transcribes audio from an uploaded file.

- **Parameters**:
  - `file` (multipart/form-data): Audio file (supports common formats like WAV, MP3, etc.)

- **Response**:
  - `200 OK`: JSON object with `"text"` field containing the transcription.
  - `500 Internal Server Error`: JSON object with `"error"` field describing the issue.

**Supported audio formats**: Depends on underlying librsndfile, but commonly includes WAV, FLV, OGG, etc. FFmpeg is used for additional formats.

## Configuration

The application uses the following configurations:

- **Model**: OpenAI Whisper Tiny (`openai/whisper-tiny`)
- **Port**: 5000
- **Host**: 0.0.0.0 (inside container)

To modify the model or other settings, edit `app.py` directly.

## Development

### Local Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

### Dependencies

- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `torch`: Machine learning framework
- `transformers`: Hugging Face transformers for Whisper model
- `soundfile`: Audio file I/O
- `python-multipart`: File upload handling

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
