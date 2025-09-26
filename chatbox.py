import ollama
import streamlit as st

# System prompt cho chủ đề AI Integration (bằng tiếng Việt)
system_prompt = """
Bạn là trợ lý tư vấn về AI Integration. Hãy giải thích rõ ràng, ngắn gọn bằng tiếng Việt các khái niệm liên quan như:
- Basic Ollama model integration: Tích hợp mô hình Ollama cơ bản.
- Prompt engineering fundamentals: Nguyên tắc cơ bản về kỹ thuật viết prompt.
- AI safety considerations cơ bản: Các lưu ý an toàn AI cơ bản (như bias, hallucination).
- Cost management cho AI services: Quản lý chi phí dịch vụ AI (ví dụ: token usage, chọn model rẻ).
- OpenAI API integration cơ bản: Tích hợp OpenAI API đơn giản.
- Các chủ đề khác như Simple chatbot implementation, Semantic Kernel introduction, hoặc bất kỳ câu hỏi liên quan đến AI Integration.
Trả lời dựa trên kiến thức chung, giữ ngắn gọn và hữu ích. Nếu câu hỏi không liên quan, lịch sự từ chối.
"""

# Lưu lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

st.title("Chatbot Tư Vấn AI Integration")

# Hiển thị lịch sử chat
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input từ user
if prompt := st.chat_input("Hỏi về AI Integration (VD: Giải thích OpenAI API integration cơ bản là gì?):"):
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

# Chạy: streamlit run E:\Cong_nghe_web\Al_Integration\chatbot.py
