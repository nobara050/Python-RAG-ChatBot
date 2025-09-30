from transformers import VitsModel, AutoTokenizer
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import APIRouter
import scipy.io.wavfile
import torch
import io

model = VitsModel.from_pretrained("facebook/mms-tts-vie")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-vie")
model.eval()

class TTSRequest(BaseModel):
    text: str

router = APIRouter(tags=["Text-to-Speech"])
@router.post("/tts")
async def text_to_speech(request: TTSRequest):
    try:
        # Tokenize văn bản
        inputs = tokenizer(request.text, return_tensors="pt")
        
        # Tạo audio trong RAM
        with torch.no_grad():
            output = model(**inputs).waveform
        
        # Lưu audio vào buffer trong RAM
        audio_buffer = io.BytesIO()
        scipy.io.wavfile.write(audio_buffer, rate=model.config.sampling_rate, data=output.squeeze().cpu().numpy())
        audio_buffer.seek(0)
        
        # Trả về luồng âm thanh
        return StreamingResponse(audio_buffer, media_type="audio/wav")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing TTS: {str(e)}")
