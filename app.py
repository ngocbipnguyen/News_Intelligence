
import os
import streamlit as st
from dotenv import load_dotenv

# 1. Cấu hình trang
st.set_page_config(
    page_title="Technology News Intelligence",
    page_icon="📰",
    layout="wide",
)

# 2. Nạp biến môi trường từ .env khi chạy local
load_dotenv(override=True)

# 3. Đọc API keys từ Streamlit Secrets khi chạy trên Cloud
try:
    for key in ["OPENAI_API_KEY", "TAVILY_API_KEY"]:
        if key in st.secrets:
            os.environ[key] = str(st.secrets[key])
except st.errors.StreamlitSecretNotFoundError:
    pass

# 4. Hiển thị giao diện
st.title("📰 Technology News Intelligence")
st.caption("Hệ thống nghiên cứu và biên tập tin tức công nghệ bằng AI")
st.divider()

st.header("Thiết lập nghiên cứu")

topic = st.text_input(
    "Chủ đề muốn nghiên cứu",
    placeholder="Ví dụ: Những ứng dụng AI mới nhất",
)

categories = st.multiselect(
    "Lĩnh vực công nghệ",
    options=[
        "Trí tuệ nhân tạo (AI)",
        "An ninh mạng",
        "Điện toán đám mây",
        "Phần mềm",
        "Phần cứng",
    ],
    default=["Trí tuệ nhân tạo (AI)"],
)

number_of_news = st.selectbox(
    "Số lượng tin mong muốn",
    options=[5, 10, 15, 20],
    index=0,
)

# 5. Khởi tạo session state
if "report" not in st.session_state:
    st.session_state.report = ""

if "critic_status" not in st.session_state:
    st.session_state.critic_status = ""

if "critic_feedback" not in st.session_state:
    st.session_state.critic_feedback = ""

# 6. Nút chạy Agent
if st.button(
    "🚀 Bắt đầu nghiên cứu",
    type="primary",
    use_container_width=True,
):
    if not topic.strip():
        st.warning("Vui lòng nhập chủ đề nghiên cứu.")

    elif not categories:
        st.warning("Vui lòng chọn ít nhất một lĩnh vực công nghệ.")

    else:
        st.session_state.report = ""
        st.session_state.critic_status = ""
        st.session_state.critic_feedback = ""

        research_topic = (
            f"Chủ đề: {topic.strip()}. "
            f"Các lĩnh vực cần ưu tiên: {', '.join(categories)}."
        )

        try:
            # Import CrewAI khi người dùng thực sự chạy Agent
            from crew.crew import create_news_crew

            with st.spinner(
                "Các Agent đang nghiên cứu và biên tập tin tức..."
            ):
                result = create_news_crew(
                    topic=research_topic,
                    number_of_news=number_of_news,
                ).kickoff()

            st.session_state.report = result.raw
            st.session_state.critic_status = result.critic_status
            st.session_state.critic_feedback = result.critic_feedback

        except Exception as exc:
            st.error("Không thể hoàn thành quy trình.")
            st.exception(exc)

# 7. Hiển thị kết quả kiểm duyệt
if st.session_state.critic_status:
    st.divider()
    st.subheader("Trạng thái kiểm duyệt")

    if st.session_state.critic_status == "DAT":
        st.success("Báo cáo đã đạt yêu cầu kiểm duyệt.")

    elif st.session_state.critic_status == "CHUA_DAT":
        st.warning("Báo cáo chưa đạt yêu cầu sau các lượt kiểm duyệt.")

    else:
        st.info(
            f"Không xác định được kết luận của Critic: "
            f"{st.session_state.critic_status}"
        )

    with st.expander("Xem phản hồi của Critic"):
        st.markdown(st.session_state.critic_feedback)

# 8. Hiển thị báo cáo
if st.session_state.report:
    st.divider()
    st.header("📄 Báo cáo tin tức")
    st.markdown(st.session_state.report)
