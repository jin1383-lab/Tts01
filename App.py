import streamlit as st
from google.cloud import texttospeech

def google_tts_advanced(text, speed):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 목소리 설정
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", 
        name="ko-KR-Neural2-A" # 고품질 신경망 목소리 선택 가능
    )

    # 속도 조절 설정
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed  # 슬라이더에서 받은 값을 여기에 적용!
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

st.title("속도 조절 TTS 설정")

# 사용자가 직접 속도를 선택할 수 있는 슬라이더 생성
speed = st.slider("읽기 속도 조절", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

text = st.text_area("내용을 입력하세요", "속도를 조절해 보세요.")

if st.button("음성 생성"):
    audio_data = google_tts_advanced(text, speed)
    st.audio(audio_data, format="audio/mp3")
