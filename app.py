
import os
import streamlit as st
from dotenv import load_dotenv


# =========================================================
# 1. CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Technology News Intelligence",
    page_icon="📰",
    layout="wide",
)


# =========================================================
# 2. NẠP API KEYS
# =========================================================

# Chạy local: đọc API keys từ file .env
load_dotenv(override=True)

# Chạy Streamlit Cloud: đọc API keys từ Secrets
try:
    for key in ["OPENAI_API_KEY", "TAVILY_API_KEY"]:
        if key in st.secrets:
            os.environ[key] = str(st.secrets[key])

except st.errors.StreamlitSecretNotFoundError:
    pass


# =========================================================
# 3. KHỞI TẠO SESSION STATE
# =========================================================

if "report" not in st.session_state:
    st.session_state.report = ""

if "critic_status" not in st.session_state:
    st.session_state.critic_status = ""

if "critic_feedback" not in st.session_state:
    st.session_state.critic_feedback = ""

if "error_message" not in st.session_state:
    st.session_state.error_message = ""


# =========================================================
# 4. GIAO DIỆN CHÍNH
# =========================================================

st.title("📰 Technology News Intelligence")

st.caption(
    "Hệ thống nghiên cứu và biên tập tin tức công nghệ bằng AI"
)

st.divider()

st.header("Thiết lập nghiên cứu")


# Nhập chủ đề
topic = st.text_input(
    "Chủ đề muốn nghiên cứu",
    placeholder="Ví dụ: Những ứng dụng AI mới nhất",
)


# Chọn lĩnh vực
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


# Chọn số lượng tin
number_of_news = st.selectbox(
    "Số lượng tin mong muốn",
    options=[5, 10, 15, 20],
    index=0,
)


st.divider()


# =========================================================
# 5. XỬ LÝ NÚT BẮT ĐẦU NGHIÊN CỨU
# =========================================================

if st.button(
    "🚀 Bắt đầu nghiên cứu",
    type="primary",
    use_container_width=True,
):

    # Kiểm tra dữ liệu đầu vào
    if not topic.strip():
        st.warning("Vui lòng nhập chủ đề nghiên cứu.")

    elif not categories:
        st.warning("Vui lòng chọn ít nhất một lĩnh vực công nghệ.")

    else:

        # Xóa kết quả và lỗi của lần chạy trước
        st.session_state.report = ""
        st.session_state.critic_status = ""
        st.session_state.critic_feedback = ""
        st.session_state.error_message = ""

        # Chuẩn bị chủ đề nghiên cứu
        research_topic = (
            f"Chủ đề: {topic.strip()}. "
            f"Các lĩnh vực cần ưu tiên: {', '.join(categories)}."
        )

        # Thông báo ngay khi nhận yêu cầu
        st.info(
            "Đã nhận yêu cầu nghiên cứu. "
            "Hệ thống đang chuẩn bị khởi động các Agent..."
        )

        try:

            # Spinner bao gồm cả quá trình import và chạy CrewAI
            with st.spinner(
                "⏳ Các Agent đang nghiên cứu và biên tập tin tức. "
                "Vui lòng chờ..."
            ):

                # Import CrewAI khi người dùng bấm nút
                from crew.crew import create_news_crew

                # Khởi chạy quy trình nghiên cứu
                pipeline = create_news_crew(
                    topic=research_topic,
                    number_of_news=number_of_news,
                )

                result = pipeline.kickoff()

            # Lưu kết quả
            st.session_state.report = result.raw

            st.session_state.critic_status = (
                result.critic_status
            )

            st.session_state.critic_feedback = (
                result.critic_feedback
            )

            if not st.session_state.report:
                st.warning(
                    "Quy trình đã kết thúc nhưng không tạo ra báo cáo. "
                    "Vui lòng kiểm tra Logs."
                )
            else:
                st.success("🎉 Đã hoàn thành quá trình nghiên cứu!")

        except Exception as exc:

            # Lưu lỗi để hiển thị
            st.session_state.error_message = str(exc)

            st.error(
                "Không thể hoàn thành quy trình nghiên cứu."
            )

            st.exception(exc)


# =========================================================
# 6. HIỂN THỊ LỖI
# =========================================================

if st.session_state.error_message:

    st.divider()

    st.subheader("Thông tin lỗi")

    st.error(st.session_state.error_message)


# =========================================================
# 7. HIỂN THỊ KẾT QUẢ KIỂM DUYỆT
# =========================================================

if st.session_state.critic_status:

    st.divider()

    st.subheader("🔍 Trạng thái kiểm duyệt")

    if st.session_state.critic_status == "DAT":

        st.success(
            "Báo cáo đã đạt yêu cầu kiểm duyệt."
        )

    elif st.session_state.critic_status == "CHUA_DAT":

        st.warning(
            "Báo cáo chưa đạt yêu cầu sau các lượt kiểm duyệt."
        )

    else:

        st.info(
            "Không xác định được kết luận của Critic: "
            f"{st.session_state.critic_status}"
        )

    with st.expander("Xem phản hồi của Critic"):

        st.markdown(
            st.session_state.critic_feedback
        )


# =========================================================
# 8. HIỂN THỊ BÁO CÁO
# =========================================================

if st.session_state.report:

    st.divider()

    st.header("📄 Báo cáo tin tức")

    st.markdown(
        st.session_state.report
    )


# =========================================================
# 9. NÚT XÓA KẾT QUẢ
# =========================================================

if (
    st.session_state.report
    or st.session_state.error_message
):

    if st.button("🗑️ Xóa kết quả"):

        st.session_state.report = ""
        st.session_state.critic_status = ""
        st.session_state.critic_feedback = ""
        st.session_state.error_message = ""

        st.rerun()
