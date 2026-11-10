
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

load_dotenv(override=True)

try:
    for key in ["OPENAI_API_KEY", "TAVILY_API_KEY"]:
        if key in st.secrets:
            os.environ[key] = str(st.secrets[key])

except st.errors.StreamlitSecretNotFoundError:
    pass


# =========================================================
# 3. KHỞI TẠO SESSION STATE
# =========================================================

for key, default in {
    "report": "",
    "critic_status": "",
    "critic_feedback": "",
    "error_message": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# =========================================================
# 4. GIAO DIỆN CHÍNH
# =========================================================

st.title("📰 Technology News Intelligence")

st.caption(
    "Hệ thống nghiên cứu và biên tập tin tức công nghệ bằng AI"
)

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

st.divider()


# =========================================================
# 5. XỬ LÝ NGHIÊN CỨU
# =========================================================

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
        st.session_state.error_message = ""

        research_topic = (
            f"Chủ đề: {topic.strip()}. "
            f"Các lĩnh vực cần ưu tiên: {', '.join(categories)}."
        )

        status = None

        try:

            with st.status(
                "Đang chuẩn bị khởi động hệ thống...",
                expanded=True,
            ) as status:

                # BƯỚC 1: IMPORT
                st.write("📦 Đang nạp module CrewAI...")

                st.write("🔎 Kiểm tra import crewai...")
                import crewai
                st.write("✅ Import crewai thành công.")

                st.write("🔎 Kiểm tra import crewai_tools...")
                import crewai_tools
                st.write("✅ Import crewai_tools thành công.")

                st.write("🔎 Kiểm tra import crew.agents...")
                import crew.agents
                st.write("✅ Import crew.agents thành công.")

                st.write("🔎 Kiểm tra import crew.tasks...")
                import crew.tasks
                st.write("✅ Import crew.tasks thành công.")

                st.write("🔎 Kiểm tra import crew.crew...")
                from crew.crew import create_news_crew
                st.write("✅ Import crew.crew thành công.")

                st.write("✅ Nạp module CrewAI thành công.")

                # BƯỚC 2: KHỞI TẠO PIPELINE
                status.update(
                    label="Đang khởi tạo quy trình nghiên cứu...",
                    state="running",
                )

                st.write("⚙️ Đang khởi tạo các Agent và Task...")

                pipeline = create_news_crew(
                    topic=research_topic,
                    number_of_news=number_of_news,
                )

                st.write("✅ Khởi tạo quy trình thành công.")

                # BƯỚC 3: CHẠY CREWAI
                status.update(
                    label="CrewAI đang thực thi quy trình...",
                    state="running",
                )

                st.write(
                    "🔍 Đang gọi pipeline.kickoff(). "
                    "Hệ thống sẽ lần lượt thực hiện các Agent."
                )

                result = pipeline.kickoff()

                # BƯỚC 4: HOÀN THÀNH
                status.update(
                    label="Nghiên cứu và biên tập hoàn tất!",
                    state="complete",
                    expanded=False,
                )

            st.session_state.report = result.raw
            st.session_state.critic_status = result.critic_status
            st.session_state.critic_feedback = result.critic_feedback

            if not st.session_state.report:
                st.warning(
                    "Quy trình đã kết thúc nhưng không tạo ra báo cáo. "
                    "Vui lòng kiểm tra Logs."
                )
            else:
                st.success("🎉 Đã hoàn thành quá trình nghiên cứu!")

        except Exception as exc:

            st.session_state.error_message = str(exc)

            if status is not None:
                status.update(
                    label="Quy trình gặp lỗi!",
                    state="error",
                    expanded=True,
                )

            st.error("Không thể hoàn thành quy trình nghiên cứu.")
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

        st.success("Báo cáo đã đạt yêu cầu kiểm duyệt.")

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
        st.markdown(st.session_state.critic_feedback)


# =========================================================
# 8. HIỂN THỊ BÁO CÁO
# =========================================================

if st.session_state.report:

    st.divider()
    st.header("📄 Báo cáo tin tức")
    st.markdown(st.session_state.report)


# =========================================================
# 9. NÚT XÓA KẾT QUẢ
# =========================================================

if st.session_state.report or st.session_state.error_message:

    if st.button("🗑️ Xóa kết quả"):

        st.session_state.report = ""
        st.session_state.critic_status = ""
        st.session_state.critic_feedback = ""
        st.session_state.error_message = ""

        st.rerun()
