import streamlit as st
import requests
import io

# CSS VÔ HIỆU HÓA CON TRỎ VÀ CỐ ĐỊNH Ô INPUT
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
    .input-container {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: white;
        padding: 10px;
        border-top: 1px solid #ccc;
        z-index: 1000;
    }
    .chat-container {
        margin-bottom: 100px; /* Đảm bảo không bị che bởi input-container */
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

# KHỞI TẠO SESSION_STATE
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# HIỂN THỊ HỘI THOẠI
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        st.markdown(f"**Bạn:** {msg['user']}")
        st.markdown(f"**Bot:** {msg['bot']}")
        
        if msg.get("sources"):
            with st.expander("Nguồn tài liệu tham khảo"):
                st.write(msg["sources"])
        
        if msg.get("audio"):
            try:
                st.audio(msg["audio"], format="audio/wav")
            except Exception as e:
                st.error(f"Lỗi khi phát audio: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# CONTAINER CHO Ô NHẬP VÀ NÚT GỬI
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    query = st.text_input("Nhập tin nhắn:", key="query_input")
    
    if st.button("Gửi", key="send_button"):
        if query.strip():
            try:
                # Gọi API xử lý văn bản
                url = "http://127.0.0.1:8000/query"
                payload = {"query_text": query}
                response = requests.post(url, json=payload, timeout=60)
                bot_reply = "Hiện đang có lỗi hệ thống, vui lòng thử lại sau."
                sources, prompt = [], ""
                
                if response.status_code == 200:
                    data = response.json()
                    bot_reply = data.get("response", bot_reply)
                    sources = data.get("sources", [])
                    prompt = data.get("prompt", "")
                else:
                    bot_reply = f"API lỗi: {response.status_code}"
                
                # Gọi API TTS
                tts_url = "http://127.0.0.1:8000/tts"
                tts_payload = {"text": bot_reply}
                audio_response = requests.post(tts_url, json=tts_payload, timeout=60)
                
                audio_buffer = None
                if audio_response.status_code == 200:
                    audio_buffer = io.BytesIO(audio_response.content)
                    audio_buffer.seek(0)
                else:
                    bot_reply += f" (TTS lỗi: {audio_response.status_code})"

                # Lưu vào session_state
                st.session_state.messages.append({
                    "user": query,
                    "bot": bot_reply,
                    "sources": sources,
                    "prompt": prompt,
                    "audio": audio_buffer
                })
                
                # Xóa ô input sau khi gửi
                st.session_state["query_input"] = ""

            except Exception as e:
                bot_reply = f"Có lỗi xảy ra: {e}"
                st.session_state.messages.append({
                    "user": query,
                    "bot": bot_reply,
                    "sources": [],
                    "prompt": "",
                    "audio": None
                })
                st.session_state["query_input"] = ""
    
    st.markdown('</div>', unsafe_allow_html=True)

# TỰ ĐỘNG CUỘN XUỐNG DƯỚI
st.markdown(
    """
    <script>
        window.scrollTo(0, document.body.scrollHeight);
    </script>
    """,
    unsafe_allow_html=True
)