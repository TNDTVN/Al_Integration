import re

# Danh sách các quy tắc rule-based với câu trả lời chi tiết, định dạng markdown
RULES = [
    {
        "pattern": r"(?i)prompt\s*engineering\s*(là gì|nghĩa là gì|có nghĩa là gì)\??",
        "response": """
## Prompt Engineering là gì?

Prompt engineering là kỹ thuật thiết kế và tối ưu hóa các câu lệnh (prompt) để tương tác hiệu quả với các mô hình AI, đặc biệt là các mô hình ngôn ngữ lớn (LLM) như GPT, Llama, hoặc Ollama. Mục tiêu là tạo ra các câu hỏi hoặc chỉ dẫn rõ ràng, chính xác, và có cấu trúc để AI trả lời phù hợp với nhu cầu của người dùng, giảm thiểu hiểu lầm hoặc kết quả không mong muốn.

### Tại sao Prompt Engineering quan trọng?
- **Tăng độ chính xác**: Prompt tốt giúp AI hiểu rõ ý định, giảm thiểu hiện tượng "hallucination" (tạo thông tin sai lệch).
- **Tiết kiệm tài nguyên**: Prompt tối ưu giảm số lần thử nghiệm, tiết kiệm token hoặc thời gian xử lý.
- **Tùy chỉnh kết quả**: Cho phép định dạng đầu ra (ví dụ: JSON, danh sách, hoặc văn bản ngắn gọn).

### Các nguyên tắc cơ bản
1. **Rõ ràng và cụ thể**:
   - Tránh các câu hỏi chung chung như "Nói về AI."
   - Ví dụ tốt: "Giải thích cách tích hợp mô hình AI vào ứng dụng web bằng Python trong 3 bước ngắn gọn."
2. **Cung cấp bối cảnh**:
   - Bao gồm thông tin nền hoặc yêu cầu cụ thể, ví dụ: "Tôi là lập trình viên Python, giải thích tích hợp API AI cho người mới bắt đầu."
3. **Định dạng đầu ra**:
   - Yêu cầu AI trả lời theo cấu trúc, như danh sách, bảng, hoặc JSON.
   - Ví dụ: "Trả lời dưới dạng danh sách 5 bước để tích hợp OpenAI API."
4. **Thử nghiệm và tinh chỉnh**:
   - Thử nhiều cách diễn đạt khác nhau để tìm prompt hiệu quả nhất.

### Ví dụ thực tế
- **Prompt kém**: "AI là gì?"
- **Prompt tốt**: "Giải thích khái niệm trí tuệ nhân tạo (AI) trong 3 câu, tập trung vào ứng dụng trong thương mại điện tử."
- **Kết quả mong đợi**: "Trí tuệ nhân tạo (AI) là lĩnh vực phát triển các hệ thống mô phỏng trí thông minh con người. Trong thương mại điện tử, AI được sử dụng để cá nhân hóa đề xuất sản phẩm, tự động hóa dịch vụ khách hàng qua chatbot, và tối ưu hóa quy trình kho bãi. Các thuật toán AI như machine learning giúp phân tích dữ liệu khách hàng để tăng doanh số."

### Mẹo nâng cao
- **Chain-of-Thought (CoT)**: Yêu cầu AI "suy nghĩ từng bước" để giải quyết vấn đề phức tạp, ví dụ: "Hãy giải bài toán tích hợp API bằng cách phân tích từng bước."
- **Few-shot prompting**: Cung cấp 1-2 ví dụ về câu hỏi và câu trả lời mong muốn để AI học theo.
- **Zero-shot prompting**: Dựa vào khả năng của mô hình để trả lời mà không cần ví dụ, nhưng cần prompt rất rõ ràng.

**Tài liệu tham khảo**: Xem thêm tại [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering).
"""
    },
    {
        "pattern": r"(?i)(cách|làm sao|how to|hướng dẫn)\s*(tích hợp|integrate)\s*ollama\??",
        "response": """
## Hướng dẫn tích hợp Ollama vào ứng dụng

Ollama là một công cụ mã nguồn mở cho phép chạy các mô hình ngôn ngữ lớn (LLM) như Llama, Mistral, hoặc Gemma trên máy cục bộ hoặc server. Tích hợp Ollama vào ứng dụng giúp bạn tận dụng sức mạnh của AI mà không phụ thuộc vào dịch vụ đám mây, tiết kiệm chi phí và tăng tính riêng tư.

### Các bước tích hợp Ollama
1. **Cài đặt Ollama**:
   - Tải Ollama từ [https://ollama.ai](https://ollama.ai) và cài đặt trên hệ thống (Windows, macOS, hoặc Linux).
   - Chạy lệnh để tải mô hình, ví dụ: `ollama pull llama3.1` để sử dụng Llama 3.1.
   - Khởi động server Ollama: `ollama serve`.

2. **Cài đặt thư viện Python**:
   - Cài đặt package `ollama` bằng lệnh: `pip install ollama`.
   - Thư viện này cung cấp giao diện để gửi yêu cầu API đến server Ollama.

3. **Gửi yêu cầu API**:
   - Sử dụng thư viện `ollama` để gửi tin nhắn hoặc xử lý stream response.
   - Ví dụ mã Python cơ bản:
     ```python
     import ollama
     response = ollama.chat(
         model='llama3.1',
         messages=[
             {'role': 'system', 'content': 'Bạn là trợ lý AI hữu ích.'},
             {'role': 'user', 'content': 'Giải thích AI trong 3 câu.'}
         ]
     )
     print(response['message']['content'])
     ```
   - Kết quả: AI sẽ trả về câu trả lời như văn bản thông thường.

4. **Xử lý stream response (nâng cao)**:
   - Để tạo trải nghiệm tương tác mượt mà, bạn có thể sử dụng stream để nhận phản hồi theo thời gian thực.
   - Ví dụ mã stream:
     ```python
     import ollama
     stream = ollama.chat(
         model='llama3.1',
         messages=[{'role': 'user', 'content': 'Xin chào, Ollama!'}],
         stream=True
     )
     for chunk in stream:
         print(chunk['message']['content'], end='', flush=True)
     ```

5. **Triển khai trong ứng dụng web**:
   - Kết hợp với Flask hoặc FastAPI để tạo endpoint nhận câu hỏi từ người dùng và trả về phản hồi từ Ollama.
   - Ví dụ endpoint Flask:
     ```python
     from flask import Flask, request, Response
     import ollama
     app = Flask(__name__)
     @app.route('/chat', methods=['POST'])
     def chat():
         prompt = request.json.get('prompt')
         stream = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': prompt}], stream=True)
         def generate():
             for chunk in stream:
                 yield chunk['message']['content'].encode('utf-8')
         return Response(generate(), mimetype='text/plain')
     if __name__ == '__main__':
         app.run()
     ```

### Lưu ý khi tích hợp
- **Cấu hình server**: Đảm bảo server Ollama chạy trên `localhost:11434` hoặc cấu hình endpoint phù hợp.
- **Hiệu suất**: Chạy mô hình lớn như Llama 3 cần GPU mạnh hoặc RAM tối thiểu 16GB để đạt hiệu suất tốt.
- **Bảo mật**: Nếu triển khai trên server công cộng, thêm xác thực API để bảo vệ endpoint.
- **Tài liệu tham khảo**: Xem chi tiết tại [Ollama Documentation](https://ollama.ai/docs).

### Mẹo tối ưu
- Sử dụng mô hình nhỏ hơn (như `gemma2:2b`) để tiết kiệm tài nguyên.
- Lưu trữ lịch sử hội thoại trong session để duy trì ngữ cảnh.
- Kiểm tra trạng thái server Ollama trước khi gửi yêu cầu để tránh lỗi kết nối.
"""
    },
    {
        "pattern": r"(?i)ai\s*safety\s*(là gì|quan trọng|nghĩa là gì)\??",
        "response": """
## AI Safety là gì?

AI Safety (an toàn AI) là tập hợp các phương pháp, kỹ thuật, và quy trình nhằm đảm bảo các hệ thống trí tuệ nhân tạo hoạt động đúng mục đích, không gây hại, và đáng tin cậy. Nó tập trung vào việc giảm thiểu các rủi ro như bias (thiên vị), hallucination (tạo thông tin sai lệch), và các hành vi không mong muốn từ AI.

### Các rủi ro chính trong AI Safety
1. **Bias (Thiên vị)**:
   - Xảy ra khi mô hình AI đưa ra kết quả thiên lệch do dữ liệu huấn luyện không công bằng.
   - Ví dụ: Một mô hình tuyển dụng AI có thể ưu ái nam giới nếu dữ liệu huấn luyện chủ yếu từ hồ sơ nam.
   - **Giải pháp**: Làm sạch dữ liệu, sử dụng kỹ thuật như fairness-aware training, và kiểm tra định kỳ kết quả AI.

2. **Hallucination (Tạo thông tin sai lệch)**:
   - AI tạo ra thông tin không chính xác hoặc không có thật, đặc biệt khi trả lời câu hỏi ngoài phạm vi kiến thức.
   - Ví dụ: AI có thể "phát minh" một sự kiện lịch sử không tồn tại.
   - **Giải pháp**: Sử dụng prompt rõ ràng, yêu cầu AI trích dẫn nguồn, hoặc giới hạn phạm vi trả lời.

3. **Bảo mật và lạm dụng**:
   - AI có thể bị lợi dụng để tạo nội dung độc hại, như tin giả hoặc mã độc.
   - **Giải pháp**: Thêm bộ lọc nội dung, giới hạn truy cập API, và giám sát hành vi người dùng.

### Tại sao AI Safety quan trọng?
- **Độ tin cậy**: Đảm bảo AI cung cấp kết quả chính xác và công bằng.
- **Hậu quả xã hội**: Giảm thiểu tác động tiêu cực đến người dùng, doanh nghiệp, hoặc xã hội.
- **Tuân thủ pháp lý**: Nhiều quốc gia đang áp dụng quy định nghiêm ngặt về AI, như GDPR ở châu Âu.

### Ví dụ thực tế
- **Bias**: Một chatbot AI trả lời thiên vị về giới tính khi được hỏi về nghề nghiệp kỹ thuật. Để khắc phục, cần huấn luyện lại với dữ liệu đa dạng hơn.
- **Hallucination**: Một mô hình trả lời "Năm 2023, Việt Nam tổ chức Thế vận hội" (sai sự thật). Prompt như "Chỉ trả lời dựa trên dữ liệu thực tế" có thể giảm thiểu vấn đề.

### Cách triển khai AI Safety
1. **Kiểm tra dữ liệu huấn luyện**:
   - Loại bỏ dữ liệu thiên vị hoặc không chính xác.
   - Sử dụng công cụ như `pandas` để phân tích dữ liệu:
     ```python
     import pandas as pd
     data = pd.read_csv('training_data.csv')
     print(data['gender'].value_counts())  # Kiểm tra phân bố giới tính
     ```
2. **Thêm bộ lọc nội dung**:
   - Sử dụng thư viện như `detoxify` để phát hiện nội dung độc hại:
     ```python
     from detoxify import Detoxify
     model = Detoxify('original')
     result = model.predict('This content is harmful')
     print(result)  # Kiểm tra mức độ độc hại
     ```
3. **Giám sát và đánh giá**:
   - Ghi log các phản hồi của AI và kiểm tra định kỳ để phát hiện bias hoặc lỗi.
   - Ví dụ: Lưu phản hồi vào database SQLite (như trong ứng dụng của bạn).

**Tài liệu tham khảo**: Xem thêm tại [AI Safety Institute](https://www.aisafetyinstitute.org).
"""
    },
    {
        "pattern": r"(?i)(xin chào|hi|hello)\??",
        "response": """
## Xin chào!

Tôi là trợ lý AI Integration, được thiết kế để hỗ trợ bạn về các chủ đề liên quan đến tích hợp trí tuệ nhân tạo vào ứng dụng. Dù bạn là người mới bắt đầu hay lập trình viên có kinh nghiệm, tôi sẽ cung cấp câu trả lời rõ ràng, ngắn gọn, và thực tế.

### Bạn có thể hỏi gì?
- **Tích hợp AI**: Cách tích hợp các mô hình như Ollama, OpenAI API, hoặc các framework như Semantic Kernel.
- **Prompt Engineering**: Làm thế nào để viết prompt hiệu quả để nhận được kết quả tốt nhất từ AI.
- **AI Safety**: Các kỹ thuật để giảm thiểu bias, hallucination, hoặc rủi ro bảo mật.
- **Quản lý chi phí**: Cách tối ưu hóa chi phí khi sử dụng dịch vụ AI.
- **Chatbot đơn giản**: Hướng dẫn xây dựng chatbot cơ bản với Python hoặc JavaScript.

### Ví dụ câu hỏi
- "Làm sao để tích hợp Ollama vào ứng dụng Flask?"
- "Prompt engineering là gì và cách áp dụng?"
- "Làm thế nào để xây dựng một chatbot đơn giản?"

### Bắt đầu ngay
Hãy nhập câu hỏi của bạn vào ô chat, hoặc thử một trong các gợi ý sau:
- **Cách tích hợp OpenAI API?**
- **AI safety quan trọng thế nào?**
- **Hướng dẫn viết prompt hiệu quả.**

**Mẹo**: Nếu bạn muốn câu trả lời chi tiết hơn hoặc có ví dụ mã, hãy nói rõ trong câu hỏi, ví dụ: "Giải thích tích hợp Ollama với mã Python chi tiết."
"""
    },
    {
        "pattern": r"(?i)(tích hợp|integrate)\s*openai\s*api\??",
        "response": """
## Hướng dẫn tích hợp OpenAI API

OpenAI API là một dịch vụ mạnh mẽ để tích hợp trí tuệ nhân tạo vào ứng dụng, cho phép tạo chatbot, phân tích văn bản, hoặc tự động hóa nhiều tác vụ. Dưới đây là hướng dẫn chi tiết để tích hợp OpenAI API vào ứng dụng của bạn.

### Các bước tích hợp OpenAI API
1. **Đăng ký và lấy API Key**:
   - Truy cập [https://platform.openai.com](https://platform.openai.com) và tạo tài khoản.
   - Vào phần "API Keys" để tạo một key mới. Lưu key này an toàn, không chia sẻ công khai.
   - Ví dụ: `sk-abc123...` (key mẫu).

2. **Cài đặt thư viện OpenAI**:
   - Cài đặt package Python: `pip install openai`.
   - Đảm bảo sử dụng phiên bản mới nhất để hỗ trợ các tính năng mới.

3. **Gửi yêu cầu API**:
   - Sử dụng thư viện `openai` để gửi tin nhắn đến mô hình như `gpt-3.5-turbo` hoặc `gpt-4`.
   - Ví dụ mã Python cơ bản:
     ```python
     from openai import OpenAI
     client = OpenAI(api_key='sk-abc123...')
     response = client.chat.completions.create(
         model="gpt-3.5-turbo",
         messages=[
             {"role": "system", "content": "Bạn là trợ lý AI hữu ích."},
             {"role": "user", "content": "Giải thích AI trong 3 câu."}
         ]
     )
     print(response.choices[0].message.content)
     ```
   - Kết quả: AI sẽ trả về câu trả lời như văn bản thông thường.

4. **Xử lý stream response (nâng cao)**:
   - OpenAI hỗ trợ stream để nhận phản hồi theo thời gian thực, phù hợp cho ứng dụng chat.
   - Ví dụ mã stream:
     ```python
     from openai import OpenAI
     client = OpenAI(api_key='sk-abc123...')
     stream = client.chat.completions.create(
         model="gpt-3.5-turbo",
         messages=[{"role": "user", "content": "Xin chào, OpenAI!"}],
         stream=True
     )
     for chunk in stream:
         if chunk.choices[0].delta.content:
             print(chunk.choices[0].delta.content, end='', flush=True)
     ```

5. **Tích hợp vào ứng dụng web**:
   - Kết hợp với Flask hoặc FastAPI để tạo giao diện chat.
   - Ví dụ endpoint Flask:
     ```python
     from flask import Flask, request, Response
     from openai import OpenAI
     app = Flask(__name__)
     client = OpenAI(api_key='sk-abc123...')
     @app.route('/chat', methods=['POST'])
     def chat():
         prompt = request.json.get('prompt')
         stream = client.chat.completions.create(
             model="gpt-3.5-turbo",
             messages=[{"role": "user", "content": prompt}],
             stream=True
         )
         def generate():
             for chunk in stream:
                 if chunk.choices[0].delta.content:
                     yield chunk.choices[0].delta.content.encode('utf-8')
         return Response(generate(), mimetype='text/plain')
     if __name__ == '__main__':
         app.run()
     ```

### Quản lý chi phí
- **Theo dõi token usage**: Mỗi phản hồi từ OpenAI API bao gồm thông tin `usage` (prompt_tokens, completion_tokens).
- Ví dụ kiểm tra chi phí:
  ```python
  response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": "Xin chào"}]
  )
  tokens_used = response.usage.total_tokens
  cost = tokens_used * 0.000002  # Giả sử $0.002/1000 tokens
  print(f"Chi phí: ${cost:.6f}")
  ```
- **Mẹo tiết kiệm**:
  - Sử dụng mô hình rẻ hơn như `gpt-3.5-turbo` thay vì `gpt-4`.
  - Viết prompt ngắn gọn để giảm số token.

### Lưu ý
- **Bảo mật**: Lưu API Key trong biến môi trường (`.env`) thay vì hardcode.
- **Xử lý lỗi**: Kiểm tra các lỗi như `RateLimitError` hoặc `AuthenticationError`:
  ```python
  try:
      response = client.chat.completions.create(...)
  except openai.RateLimitError:
      print("Đã vượt quá giới hạn, thử lại sau.")
  except openai.AuthenticationError:
      print("API Key không hợp lệ.")
  ```
- **Tài liệu tham khảo**: Xem chi tiết tại [OpenAI API Documentation](https://platform.openai.com/docs).

### Mẹo nâng cao
- Sử dụng `max_tokens` để giới hạn độ dài phản hồi.
- Thêm lịch sử hội thoại vào `messages` để duy trì ngữ cảnh.
- Kiểm tra trạng thái API bằng endpoint `/health` nếu bạn tự triển khai server proxy.
"""
    },
    {
        "pattern": r"(?i)quản lý\s*chi phí\s*(dịch vụ)?\s*ai\??",
        "response": """
## Quản lý chi phí dịch vụ AI

Khi sử dụng các dịch vụ AI như OpenAI, Google Cloud AI, hoặc chạy mô hình cục bộ như Ollama, quản lý chi phí là yếu tố quan trọng để đảm bảo hiệu quả tài chính, đặc biệt trong các dự án lớn hoặc triển khai lâu dài. Dưới đây là hướng dẫn chi tiết để tối ưu hóa chi phí khi sử dụng AI.

### Các yếu tố ảnh hưởng đến chi phí
1. **Số token sử dụng**:
   - Hầu hết dịch vụ AI tính phí dựa trên số token (prompt + completion).
   - Ví dụ: Với OpenAI, `gpt-3.5-turbo` có chi phí khoảng $0.002/1000 tokens (giá tham khảo).
2. **Loại mô hình**:
   - Mô hình lớn hơn như `gpt-4` tốn nhiều chi phí hơn so với `gpt-3.5-turbo` hoặc `gemma2:2b`.
   - Mô hình mã nguồn mở như Ollama có thể miễn phí nếu chạy cục bộ, nhưng cần đầu tư phần cứng.
3. **Tần suất sử dụng**:
   - Các ứng dụng có lượng truy vấn lớn (như chatbot công cộng) sẽ tiêu tốn nhiều token hơn.
4. **Hạ tầng triển khai**:
   - Chạy mô hình cục bộ (như Ollama) cần chi phí phần cứng (GPU, RAM).
   - Dịch vụ đám mây (như AWS, Azure) tính phí theo giờ sử dụng.

### Cách tối ưu hóa chi phí
1. **Theo dõi và ghi log token usage**:
   - Sử dụng dashboard hoặc database (như SQLite trong ứng dụng của bạn) để ghi lại số token và chi phí.
   - Ví dụ mã Python để ghi log:
     ```python
     import sqlite3
     def log_usage(model_name, prompt_tokens, completion_tokens):
         conn = sqlite3.connect('cost_management.db')
         c = conn.cursor()
         c.execute('SELECT cost_per_token FROM models WHERE name = ?', (model_name,))
         cost_per_token = c.fetchone()[0]
         total_tokens = prompt_tokens + completion_tokens
         cost = total_tokens * cost_per_token
         c.execute('INSERT INTO usage_logs (model_id, prompt_tokens, completion_tokens, total_tokens, cost) VALUES (?, ?, ?, ?, ?)',
                   (1, prompt_tokens, completion_tokens, total_tokens, cost))
         conn.commit()
         conn.close()
     ```

2. **Chọn mô hình phù hợp**:
   - Sử dụng mô hình nhỏ hơn cho các tác vụ đơn giản (như `gpt-3.5-turbo` hoặc `gemma2:2b`).
   - Ví dụ: Đối với chatbot cơ bản, `gpt-3.5-turbo` thường đủ hiệu quả và rẻ hơn `gpt-4`.

3. **Tối ưu hóa prompt**:
   - Viết prompt ngắn gọn, tránh lặp lại thông tin không cần thiết.
   - Ví dụ:
     - **Prompt kém**: "Hãy giải thích chi tiết về trí tuệ nhân tạo, bao gồm lịch sử, ứng dụng, và tương lai của nó trong 1000 từ."
     - **Prompt tốt**: "Giải thích trí tuệ nhân tạo trong 3 câu, tập trung vào ứng dụng trong thương mại điện tử."
   - Sử dụng `max_tokens` để giới hạn độ dài phản hồi.

4. **Chạy mô hình cục bộ**:
   - Sử dụng Ollama để chạy mô hình như Llama hoặc Gemma trên máy cục bộ, tránh chi phí API đám mây.
   - Yêu cầu: Máy tính có GPU (ít nhất 8GB VRAM) hoặc RAM lớn (16GB+).

5. **Tận dụng bộ nhớ đệm (cache)**:
   - Lưu trữ các phản hồi phổ biến để tái sử dụng, giảm số lần gọi API.
   - Ví dụ: Nếu người dùng thường hỏi "AI là gì?", lưu câu trả lời vào database và trả về ngay.

### Ví dụ thực tế
- **Theo dõi chi phí với OpenAI**:
  ```python
  from openai import OpenAI
  client = OpenAI(api_key='sk-abc123...')
  response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": "Xin chào"}]
  )
  tokens_used = response.usage.total_tokens
  cost = tokens_used * 0.000002  # Giả sử $0.002/1000 tokens
  print(f"Chi phí: ${cost:.6f}")
  log_usage('gpt-3.5-turbo', response.usage.prompt_tokens, response.usage.completion_tokens)
  ```

- **Chạy Ollama cục bộ**:
  ```python
  import ollama
  response = ollama.chat(model='gemma2:2b', messages=[{'role': 'user', 'content': 'Xin chào'}])
  print(response['message']['content'])
  # Chi phí: 0 (nếu chạy cục bộ)
  ```

### Mẹo nâng cao
- **Dùng mô hình mã nguồn mở**: Các mô hình như Llama, Mistral, hoặc Gemma trên Ollama giúp tiết kiệm chi phí dài hạn.
- **Tự động hóa giám sát**: Tạo script kiểm tra chi phí định kỳ và gửi cảnh báo nếu vượt ngưỡng.
- **Tài liệu tham khảo**: Xem [OpenAI Pricing](https://openai.com/pricing) hoặc [Ollama Documentation](https://ollama.ai/docs) để biết thêm chi tiết.
"""
    },
    {
        "pattern": r"(?i)(chatbot|simple chatbot)\s*(tạo|làm|implement)\??",
        "response": """
## Hướng dẫn xây dựng chatbot đơn giản

Chatbot là một ứng dụng AI có thể tương tác với người dùng qua văn bản hoặc giọng nói, thường được sử dụng trong dịch vụ khách hàng, thương mại điện tử, hoặc hỗ trợ kỹ thuật. Dưới đây là hướng dẫn chi tiết để xây dựng một chatbot đơn giản bằng Python và Flask, tích hợp với mô hình AI như Ollama.

### Các bước xây dựng chatbot
1. **Cài đặt môi trường**:
   - Cài Python và các thư viện: `pip install flask ollama`.
   - Cài đặt Ollama và tải mô hình (ví dụ: `ollama pull llama3.1`).

2. **Tạo server Flask**:
   - Tạo một ứng dụng Flask để xử lý yêu cầu từ người dùng và trả về phản hồi từ AI.
   - Ví dụ mã `server.py`:
     ```python
     from flask import Flask, request, Response
     import ollama
     app = Flask(__name__)
     @app.route('/chat', methods=['POST'])
     def chat():
         prompt = request.json.get('prompt')
         stream = ollama.chat(
             model='llama3.1',
             messages=[{'role': 'user', 'content': prompt}],
             stream=True
         )
         def generate():
             for chunk in stream:
                 yield chunk['message']['content'].encode('utf-8')
         return Response(generate(), mimetype='text/plain')
     if __name__ == '__main__':
         app.run(debug=True)
     ```

3. **Tạo giao diện người dùng**:
   - Sử dụng HTML, CSS, và JavaScript để tạo giao diện chat.
   - Ví dụ `index.html`:
     ```html
     <!DOCTYPE html>
     <html>
     <head>
         <title>Chatbot</title>
         <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
     </head>
     <body>
         <div id="chat"></div>
         <input id="user-input" type="text" placeholder="Nhập câu hỏi...">
         <button onclick="sendMessage()">Gửi</button>
         <script>
         async function sendMessage() {
             const input = document.getElementById('user-input').value;
             const chat = document.getElementById('chat');
             chat.innerHTML += `<p>User: ${input}</p>`;
             const response = await axios.post('/chat', { prompt: input }, { responseType: 'stream' });
             const reader = response.data.getReader();
             const decoder = new TextDecoder();
             let result = '';
             while (true) {
                 const { done, value } = await reader.read();
                 if (done) break;
                 result += decoder.decode(value);
                 chat.innerHTML += `<p>AI: ${result}</p>`;
             }
         }
         </script>
     </body>
     </html>
     ```

4. **Xử lý lịch sử hội thoại**:
   - Lưu trữ lịch sử trong session hoặc database để duy trì ngữ cảnh.
   - Ví dụ thêm lịch sử vào `server.py`:
     ```python
     from flask import session
     @app.route('/chat', methods=['POST'])
     def chat():
         prompt = request.json.get('prompt')
         if 'messages' not in session:
             session['messages'] = [{'role': 'system', 'content': 'Bạn là trợ lý AI.'}]
         session['messages'].append({'role': 'user', 'content': prompt})
         stream = ollama.chat(model='llama3.1', messages=session['messages'], stream=True)
         def generate():
             response = ''
             for chunk in stream:
                 response += chunk['message']['content']
                 yield chunk['message']['content'].encode('utf-8')
             session['messages'].append({'role': 'assistant', 'content': response})
             session.modified = True
         return Response(generate(), mimetype='text/plain')
     ```

5. **Triển khai và kiểm tra**:
   - Chạy server: `python server.py`.
   - Truy cập `http://localhost:5000` để kiểm tra giao diện chat.
   - Thử nhập câu hỏi như "Xin chào" để xem phản hồi từ AI.

### Mẹo nâng cao
- **Tùy chỉnh giao diện**: Sử dụng Bootstrap hoặc Tailwind CSS để làm giao diện đẹp hơn.
- **Bảo mật**: Thêm xác thực người dùng để giới hạn quyền truy cập chatbot.
- **Tối ưu hóa hiệu suất**: Sử dụng mô hình nhỏ hơn (như `gemma2:2b`) để tăng tốc độ.
- **Tài liệu tham khảo**: Xem [Flask Documentation](https://flask.palletsprojects.com) và [Ollama Documentation](https://ollama.ai/docs).

### Lưu ý
- Đảm bảo server Ollama đang chạy trên `localhost:11434`.
- Kiểm tra tài nguyên máy (CPU/GPU) để chạy mô hình AI hiệu quả.
- Nếu muốn sử dụng OpenAI thay vì Ollama, thay `ollama.chat` bằng `openai.chat.completions.create` như trong ví dụ tích hợp OpenAI API.
"""
    },
    {
        "pattern": r"(?i)semantic\s*kernel\s*(là gì|introduction|giới thiệu)\??",
        "response": """
## Semantic Kernel là gì?

Semantic Kernel là một framework mã nguồn mở của Microsoft, được thiết kế để tích hợp trí tuệ nhân tạo vào ứng dụng một cách dễ dàng. Nó cung cấp các công cụ để kết hợp mô hình AI (như OpenAI, Hugging Face) với dữ liệu bên ngoài, bộ nhớ ngữ cảnh, và logic lập trình truyền thống.

### Các thành phần chính
1. **Kernel**:
   - Lõi trung tâm của Semantic Kernel, quản lý các plugin, mô hình AI, và ngữ cảnh.
   - Ví dụ: Tạo một kernel để kết nối với OpenAI:
     ```python
     from semantic_kernel import Kernel
     from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion
     kernel = Kernel()
     kernel.add_text_completion_service("openai", OpenAITextCompletion("gpt-3.5-turbo", api_key="sk-abc123..."))
     ```

2. **Plugins**:
   - Các hàm hoặc công cụ mà AI có thể sử dụng, như truy vấn database, gọi API, hoặc xử lý file.
   - Ví dụ plugin để tra cứu thời tiết:
     ```python
     from semantic_kernel import sk_function
     class WeatherPlugin:
         @sk_function(description="Lấy thông tin thời tiết")
         def get_weather(self, city: str) -> str:
             return f"Thời tiết ở {city}: 25°C, nắng."
     kernel.import_plugin(WeatherPlugin(), plugin_name="weather")
     ```

3. **Memory**:
   - Lưu trữ ngữ cảnh hoặc thông tin từ các tương tác trước để cải thiện phản hồi.
   - Ví dụ: Lưu trữ lịch sử hội thoại trong vector database.

4. **Planners**:
   - Tự động tạo kế hoạch để thực hiện nhiệm vụ phức tạp bằng cách kết hợp nhiều plugin và AI.
   - Ví dụ: "Lập kế hoạch viết email dựa trên dữ liệu khách hàng."

### Lợi ích của Semantic Kernel
- **Tích hợp dễ dàng**: Kết nối nhiều mô hình AI (OpenAI, Hugging Face) và dịch vụ bên ngoài.
- **Tính linh hoạt**: Kết hợp AI với lập trình truyền thống (như Python, C#).
- **Bộ nhớ ngữ cảnh**: Duy trì lịch sử hội thoại để trả lời nhất quán.
- **Mã nguồn mở**: Miễn phí và có cộng đồng hỗ trợ lớn.

### Ví dụ tích hợp đơn giản
- Tạo một chatbot sử dụng Semantic Kernel và OpenAI:
  ```python
  from semantic_kernel import Kernel
  from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion
  async def main():
      kernel = Kernel()
      kernel.add_text_completion_service("openai", OpenAITextCompletion("gpt-3.5-turbo", api_key="sk-abc123..."))
      prompt = "Giải thích AI trong 3 câu."
      result = await kernel.run_function(prompt)
      print(result)
  if __name__ == "__main__":
      import asyncio
      asyncio.run(main())
  ```

### Cách bắt đầu
1. Cài đặt Semantic Kernel: `pip install semantic-kernel`.
2. Tạo kernel và kết nối với mô hình AI (như OpenAI hoặc Hugging Face).
3. Thêm plugin tùy chỉnh để mở rộng chức năng.
4. Sử dụng planners để tự động hóa các tác vụ phức tạp.

### Lưu ý
- **Yêu cầu kỹ thuật**: Cần hiểu cơ bản về Python hoặc C# và cách gọi API.
- **Chi phí**: Nếu dùng mô hình như OpenAI, cần quản lý chi phí API.
- **Tài liệu tham khảo**: Xem chi tiết tại [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel).

### Mẹo nâng cao
- Kết hợp với vector database như Chroma để lưu trữ ngữ cảnh dài hạn.
- Sử dụng planners để tự động hóa quy trình như tạo báo cáo hoặc phân tích dữ liệu.
- Tích hợp với các dịch vụ đám mây như Azure để triển khai quy mô lớn.
"""
    }
]
