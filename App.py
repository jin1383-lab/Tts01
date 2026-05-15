import streamlit as st
from google.cloud import texttospeech
from google.oauth2 import service_account
import json

# 1. 인증 설정 (Streamlit Cloud의 Secrets 사용)
def get_tts_client():
    try:
        # Streamlit Cloud 배포 환경
        if "gcp_service_account" in st.secrets:
            info = json.loads(st.secrets["gcp_service_account"])
            credentials = service_account.Credentials.from_service_account_info(info)
            return texttospeech.TextToSpeechClient(credentials=credentials)
        # 로컬 테스트 환경 (JSON 파일이 있을 경우)
        else:
            return texttospeech.TextToSpeechClient()
    except Exception as e:
        st.error(f"인증 설정 오류: {e}")
        return None

def generate_speech(text, speed):
    client = get_tts_client()
    if not client:
        return None

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 목소리 설정 (한국어 고품질 Neural2 목소리)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Neural2-A" 
    )

    # 속도 및 인코딩 설정
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed  # 사용자가 조절한 속도 적용
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

# --- UI 부분 ---
st.set_page_config(page_title="Google TTS 속도 조절기", page_icon="🎙️")
st.title("🎙️ Google TTS 음성 생성기")

st.markdown("### 설정을 입력하세요")
text_input = st.text_area("읽어줄 텍스트", "안녕하세요. 구글 TTS API를 활용한 음성 생성 테스트입니다.", height=150)

col1, col2 = st.columns(2)
with col1:
    speed = st.slider("읽기 속도 (0.25 ~ 4.0)", 0.25, 2.0, 1.0, 0.1)
with col2:
    st.info(f"현재 속도: {speed}x")

if st.button("음성 파일 생성"):
    if text_input:
        with st.spinner("음성을 생성 중입니다..."):
            audio_content = generate_speech(text_input, speed)
            if audio_content:
                st.audio(audio_content, format="audio/mp3")
                st.success("생성 완료!")
    else:
        st.warning("텍스트를 입력해 주세요.")
