import ollama
import streamlit as st
import json

# Đọc dữ liệu phim
with open("movies.json", "r", encoding="utf-8") as f:
    movies_data = json.load(f)

# System prompt bằng tiếng Việt, sử dụng key tiếng Anh
system_prompt = f"Bạn là trợ lý gợi ý phim. Sử dụng dữ liệu sau để đề xuất phim: {json.dumps(movies_data)}. Hiểu và trả lời các câu hỏi tự nhiên bằng tiếng Việt, dựa trên genre, rating, hoặc từ khóa. Trả lời ngắn gọn."

# Lưu lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

st.title("Chatbot Gợi Ý Phim")

# Hiển thị lịch sử chat
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input từ user
if prompt := st.chat_input("Hỏi gì về phim (VD: Gợi ý phim hành động hay):"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gọi Ollama
    # Thay "deepseek-v3.1:671b-cloud" bằng model bạn muốn sử dụng ví dụ gpt-oss:120b-cloud, gpt-oss:20b-cloud, qwen3-coder:480b-cloud
    response = ollama.chat(
        model="deepseek-v3.1:671b-cloud",
        messages=st.session_state.messages
    )
    ai_response = response['message']['content']

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)

# Chạy: streamlit run chatbot.py
