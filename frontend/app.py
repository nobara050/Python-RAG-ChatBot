import streamlit as st
import requests
import io

# CSS VÔ HIỆU HÓA CON TRỎ
st.markdown(
    """
    <style>
    
    input, textarea {
        user-select: auto !important;
        pointer-events: auto !important;
        caret-color: auto !important;
    }
    
    button {
        pointer-events: auto !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# TIÊU ĐỀ ỨNG DỤNG
st.title("FPT Policy ChatBot")

# DIV CẢNH BÁO
st.markdown(
    """
    <div style="background-color:#f9a371; padding:10px; border-radius:8px; border:1px solid #ffeeba;">
        <strong>Lưu ý:</strong> ChatBot đang trong giai đoạn thử nghiệm. Các thông tin được cung cấp có thể không hoàn toàn chính xác và chỉ mang tính tham khảo.
    </div>
    """,
    unsafe_allow_html=True
)

# Ô NHẬP CÂU HỎI
query = st.text_input("Nhập tin nhắn:")

# KHỞI TẠO SESSION_STATE
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# NÚT GỬI
if st.button("Gửi"):
    if query.strip() != "":
        try:
            # Gọi API xử lý văn bản
            url = "http://127.0.0.1:8000/query"
            payload = {"query_text": query}
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                bot_reply = data.get("response", "Hiện đang có lỗi hệ thống, vui lòng thử lại sau.")
                sources = data.get("sources", [])
                prompt = data.get("prompt", "")
            else:
                bot_reply = f"API lỗi: {response.status_code}"
                context, sources, query_back = "", [], ""
            
            # Gọi API TTS
            tts_url = "http://127.0.0.1:8000/tts"
            tts_payload = {"text": bot_reply}
            audio_response = requests.post(tts_url, json=tts_payload, timeout=60)
            
            if audio_response.status_code == 200:
                audio_buffer = io.BytesIO(audio_response.content)
                audio_buffer.seek(0)
            else:
                audio_buffer = None
                bot_reply += f" (TTS lỗi: {audio_response.status_code})"

            # Lưu vào session_state
            st.session_state.messages.append({
                "user": query,
                "bot": bot_reply,
                "sources": sources,
                "prompt": prompt,
                "audio": audio_buffer
            })

        except Exception as e:
            bot_reply = f"Có lỗi xảy ra: {e}"
            context, sources, query_back, audio_buffer = "", [], "", None
            st.session_state.messages.append({
                "user": query,
                "bot": bot_reply,
                "sources": sources,
                "prompt": query_back,
                "audio": audio_buffer
            })

# HỘI THOẠI VÀ GIỌNG NÓI
for msg in st.session_state.messages:
    st.markdown(f"**Bạn:** {msg['user']}")
    st.markdown(f"**Bot:** {msg['bot']}")

    if msg.get("sources"):
        with st.expander("Nguồn tài liệu tham khảo"):
            st.text(msg["sources"])

    # Phát audio từ buffer
    if msg.get("audio"):
        st.audio(msg["audio"], format="audio/wav")