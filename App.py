import streamlit as st
from google.cloud import texttospeech
from google.oauth2 import service_account
import json

# 인증 정보 로드 함수
def get_tts_client():
    try:
        if "gcp_service_account" in st.secrets:
            # Secrets 내용을 JSON으로 변환
            info = json.loads(st.secrets["gcp_service_account"])
            credentials = service_account.Credentials.from_service_account_info(info)
            return texttospeech.TextToSpeechClient(credentials=credentials)
        else:
            return texttospeech.TextToSpeechClient()
    except Exception as e:
        st.error(f"인증 설정 중 오류가 발생했습니다: {e}")
        return None

# 음성 생성 함수
def speak(text, speed):
    client = get_tts_client()
    if not client: return None
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", 
        name="ko-KR-Neural2-A"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

# UI 구성
st.title("Google TTS Speed Control")
text = st.text_area("텍스트 입력", "테스트 중입니다.")
speed = st.slider("속도 조절", 0.5, 2.0, 1.0, 0.1)

if st.button("음성 생성"):
    audio_data = speak(text, speed)
    if audio_data:
        st.audio(audio_data, format="audio/mp3")
