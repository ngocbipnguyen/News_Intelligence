# Technology News Intelligence

Ứng dụng nghiên cứu và biên tập tin tức công nghệ bằng CrewAI, Tavily, OpenAI và Streamlit.

## Yêu cầu

- Python 3.12.x (khuyến nghị Python 3.12.9)
- OpenAI API key
- Tavily API key

## Cài đặt trên Windows PowerShell

```powershell
cd đường-dẫn-đến\Technology-News-Intelligence

py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Nếu lệnh `py -3.12` không hoạt động, tạo môi trường bằng đường dẫn Python 3.12 đã cài trên máy.

## Cấu hình API Key

```powershell
Copy-Item .env.example .env
```

Mở `.env` và thay giá trị mẫu bằng API Key của bạn:

```env
OPENAI_API_KEY=your_real_openai_key
TAVILY_API_KEY=your_real_tavily_key
```

Không chia sẻ hoặc commit file `.env` lên GitHub.

## Chạy ứng dụng

```powershell
python -m streamlit run app.py
```

## Cấu trúc

```text
Technology-News-Intelligence/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── crew/
    ├── __init__.py
    ├── agents.py
    ├── tasks.py
    └── crew.py
```

## Lưu ý

- Tavily `max_results=20` là số kết quả tối đa cho một lần gọi tìm kiếm, không đảm bảo tổng số bài đạt yêu cầu.
- `max_iter` là giới hạn vòng lặp Agent, không phải số lần chạy lại pipeline.
- Pipeline hiện chạy Researcher một lần, sau đó Writer và Critic tối đa 4 lượt (1 lần viết đầu + tối đa 3 lần sửa).
- Critic đánh giá dựa trên dữ liệu Researcher cung cấp; không phải hệ thống xác minh độc lập mọi URL.
- Mỗi lần chạy có thể phát sinh chi phí OpenAI và Tavily.
