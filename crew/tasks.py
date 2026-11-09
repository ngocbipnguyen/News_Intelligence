from crewai import Task


def create_research_task(agent, topic, number_of_news):
    return Task(
        description=f"""
Nhiệm vụ: nghiên cứu tin tức công nghệ theo yêu cầu sau.

Chủ đề người dùng: {topic}
Số lượng tin mong muốn: {number_of_news}

YÊU CẦU:
1. Tìm các bài viết/tin tức phù hợp và ưu tiên tin mới.
2. Ưu tiên nguồn báo chí, tổ chức hoặc trang công nghệ có uy tín.
3. Với mỗi tin, cố gắng thu thập:
   - Tiêu đề chính xác.
   - Tên nguồn xuất bản.
   - Ngày đăng (chỉ ghi nếu có bằng chứng).
   - URL trực tiếp đến bài viết, không dùng trang chủ hoặc trang tác giả.
   - Tóm tắt nội dung.
   - Bằng chứng cụ thể hỗ trợ các ý chính.
   - Những chi tiết chưa xác minh hoặc còn thiếu.
4. Không tự tạo ngày đăng, URL, số liệu, trích dẫn hoặc sự kiện.
5. Phân biệt rõ thông tin tìm thấy trong kết quả tìm kiếm và thông tin đã xác nhận từ nội dung nguồn.
6. Ưu tiên chất lượng và độ tin cậy hơn việc cố đủ số lượng.
7. Nếu tìm được ít hơn {number_of_news} tin đủ điều kiện, hãy nói rõ số lượng thực tế.

ĐỊNH DẠNG KẾT QUẢ:
Với từng tin, trình bày:
- Tiêu đề:
- Nguồn:
- Ngày đăng:
- URL:
- Tóm tắt:
- Bằng chứng:
- Thông tin chưa xác minh / còn thiếu:

Cuối cùng, nêu tổng số tin tìm được và các hạn chế của dữ liệu.
""",
        expected_output=(
            "Bản nghiên cứu có danh sách tin, tiêu đề, nguồn, ngày đăng nếu xác nhận được, "
            "URL cụ thể, tóm tắt, bằng chứng và các thông tin còn thiếu."
        ),
        agent=agent,
    )



def create_writing_task(agent, research_task, critic_feedback_task=None):
    description = """
VAI TRÒ:
Bạn là chuyên viên biên tập tin tức công nghệ.
Nhiệm vụ là tạo báo cáo chính xác, khách quan và dễ đọc
dựa trên dữ liệu nghiên cứu được cung cấp.

I. NGUỒN DỮ LIỆU

1. Chỉ sử dụng dữ liệu từ Researcher và các context được cung cấp.
2. Không tự tạo sự kiện, số liệu, ngày đăng, URL hoặc trích dẫn.
3. Giữ nguyên tiêu đề, nguồn và URL theo dữ liệu Researcher.
4. Không khẳng định đã xác minh nội dung URL nếu chưa có bằng chứng.
5. Nếu thiếu dữ liệu, ghi rõ "CHƯA ĐỦ DỮ LIỆU".
6. Không biến dự báo, nhận định hoặc giả thuyết thành sự kiện.

II. YÊU CẦU KHI NHẬN FEEDBACK TỪ CRITIC

Nếu có phản hồi từ Critic, hãy thực hiện:

1. Đọc toàn bộ phản hồi của Critic.
2. Xác định từng lỗi được Critic chỉ ra.
3. Đối chiếu từng lỗi với dữ liệu Researcher.
4. Chỉ sửa những lỗi có bằng chứng rõ ràng.
5. Giữ nguyên những nội dung đã chính xác.
6. Không sửa ngày đăng, tiêu đề, nguồn hoặc URL
   nếu dữ liệu Researcher không yêu cầu thay đổi.
7. Không tự bổ sung số liệu hoặc thông tin mà Researcher
   chưa thu thập được.

III. XỬ LÝ PHẢN HỒI KHÔNG CÓ CĂN CỨ

- Nếu Critic yêu cầu bổ sung thông tin nhưng Researcher
  không cung cấp, không được tự tạo thông tin.
- Nếu Critic nhầm lẫn hoặc đưa ra yêu cầu trái với dữ liệu
  Researcher, hãy giữ thông tin có căn cứ từ Researcher.
- Nếu không thể sửa lỗi vì thiếu dữ liệu, hãy ghi rõ
  "CHƯA ĐỦ DỮ LIỆU ĐỂ HIỆU CHỈNH".
- Không xóa bỏ thông tin chính xác chỉ để làm cho báo cáo
  phù hợp với một phản hồi thiếu căn cứ.
- Không được tự ý kết luận rằng Critic sai nếu chưa đối chiếu.

IV. CẤU TRÚC BÁO CÁO

1. Tiêu đề báo cáo.
2. Chủ đề và phạm vi nghiên cứu.
3. Danh sách từng tin:
   - Tiêu đề.
   - Nguồn.
   - Ngày đăng.
   - URL.
   - Nội dung chính.
   - Bằng chứng.
   - Tác động hoặc ý nghĩa (nếu có căn cứ).
   - Thông tin chưa xác minh hoặc còn thiếu.
4. Nhận định tổng quan dựa trên dữ liệu nghiên cứu.
5. Hạn chế của báo cáo.

V. NGUYÊN TẮC CUỐI CÙNG

Ưu tiên tính chính xác và trung thực hơn số lượng thông tin.
Không bịa dữ liệu để làm hài lòng Critic.
Không thay đổi nội dung đã đúng nếu không có căn cứ.
Báo cáo phải phản ánh trung thực những gì Researcher
đã thu thập được.
"""

    if critic_feedback_task is not None:
        description += """

YÊU CẦU ĐẶC BIỆT CHO LẦN HIỆU CHỈNH:

Đây là lần chỉnh sửa dựa trên phản hồi của Critic.

Hãy:
- Đối chiếu từng lỗi với dữ liệu Researcher.
- Sửa trực tiếp những lỗi có bằng chứng.
- Giữ nguyên nội dung chính xác.
- Không bổ sung thông tin ngoài dữ liệu.
- Trình bày rõ những điểm chưa thể khắc phục.

Không được bỏ qua phản hồi của Critic,
nhưng cũng không được thực hiện yêu cầu thiếu căn cứ.
"""

    context = [research_task]

    if critic_feedback_task is not None:
        context.append(critic_feedback_task)

    return Task(
        description=description,
        expected_output=(
            "Báo cáo tin tức công nghệ bằng tiếng Việt, "
            "có cấu trúc rõ ràng, giữ nguyên nguồn dữ liệu, "
            "đã sửa các lỗi có căn cứ và trình bày trung thực "
            "những thông tin chưa thể xác minh."
        ),
        agent=agent,
        context=context,
    )




def create_critic_task(agent, research_task, writing_task):
    return Task(
        description="""
VAI TRÒ:
Bạn là chuyên viên kiểm duyệt chất lượng tin tức công nghệ.
Nhiệm vụ của bạn là kiểm tra tính chính xác, tính nhất quán
và mức độ trung thực của báo cáo do Writer tạo ra.

NGUỒN ĐỐI CHIẾU:
- Dữ liệu Researcher là nguồn đối chiếu chính.
- Báo cáo Writer là đối tượng được kiểm duyệt.
- Không sử dụng kiến thức bên ngoài để tự tạo căn cứ kết luận.
- Không tự giả định rằng thông tin không xuất hiện trong dữ liệu
  Researcher là thông tin sai.

I. CÁC TIÊU CHÍ KIỂM TRA

A. TIÊU ĐỀ, NGUỒN VÀ URL
- Đối chiếu tiêu đề, nguồn và URL giữa Writer và Researcher.
- Nếu có sự khác biệt thực sự, hãy trích dẫn cụ thể.
- Không kết luận URL đã được xác minh nếu Researcher
  chỉ cung cấp URL mà chưa xác nhận nội dung trang.

B. NGÀY ĐĂNG
- Đối chiếu ngày đăng với dữ liệu Researcher.
- Chỉ kết luận sai ngày khi có bằng chứng đối chiếu rõ ràng.
- Không tự suy đoán ngày đăng.
- Nếu không có ngày đăng trong dữ liệu Researcher,
  Writer ghi "Không xác định" hoặc "Chưa có dữ liệu"
  thì không tính là lỗi.

C. SỰ KIỆN VÀ SỐ LIỆU
- Kiểm tra số liệu, sự kiện, tên tổ chức và các nhận định.
- Nếu Writer đưa ra thông tin không có căn cứ trong dữ liệu
  Researcher và trình bày nó như sự thật, hãy xem xét đó
  là lỗi cần chỉnh sửa.
- Không yêu cầu Writer bổ sung số liệu mà Researcher không có.
- Không tự tạo bằng chứng để chứng minh một nhận định.

D. TÓM TẮT VÀ NHẬN ĐỊNH
- Kiểm tra nội dung tóm tắt có phản ánh đúng dữ liệu Researcher.
- Phân biệt rõ sự kiện được nguồn đề cập với nhận định của Writer.
- Không yêu cầu Writer mở rộng phân tích nếu không có căn cứ.

E. THÔNG TIN THIẾU VÀ GIỚI HẠN
ĐÂY LÀ QUY TẮC RẤT QUAN TRỌNG:

- Nếu Writer ghi rõ "CHƯA ĐỦ DỮ LIỆU",
  "CHƯA XÁC MINH" hoặc cách diễn đạt tương đương,
  và không trình bày nội dung đó như sự thật,
  thì không được tính là lỗi.
- Không yêu cầu Writer bổ sung thông tin mà Researcher
  chưa thu thập được.
- Không xem việc thiếu số liệu, thiếu chi tiết hoặc thiếu
  bằng chứng trong dữ liệu nghiên cứu là lỗi của Writer,
  nếu Writer đã trình bày trung thực giới hạn đó.
- Không được kết luận CHUA_DAT chỉ vì báo cáo còn những
  thông tin chưa thể xác minh.

II. QUY TẮC RA QUYẾT ĐỊNH

Chỉ kết luận CHUA_DAT khi có ít nhất một lỗi trọng yếu
được chứng minh bằng dữ liệu Researcher, ví dụ:

1. Sai tiêu đề, nguồn hoặc URL.
2. Sai ngày đăng có bằng chứng đối chiếu.
3. Bịa đặt số liệu, sự kiện hoặc thông tin.
4. Tóm tắt sai nội dung nghiên cứu.
5. Trình bày thông tin chưa xác minh như sự thật.
6. Bỏ sót hoặc làm sai lệch một thông tin quan trọng
   khiến ý nghĩa của tin tức bị thay đổi.

Nếu không có lỗi trọng yếu:
- Kết luận DAT.
- Chấp nhận những giới hạn dữ liệu đã được Writer
  trình bày trung thực.
- Không tự tạo thêm lỗi để yêu cầu Writer sửa.

III. QUY TẮC ĐỐI VỚI PHẢN HỒI SỬA BÀI

Nếu kết luận CHUA_DAT:
- Chỉ liệt kê lỗi thực sự có bằng chứng.
- Trích nội dung Writer và dữ liệu Researcher để đối chiếu.
- Nêu chính xác vị trí cần sửa.
- Đề xuất cách sửa dựa trên dữ liệu Researcher hiện có.
- Tuyệt đối không yêu cầu Writer tự bổ sung thông tin
  mà Researcher chưa cung cấp.

Nếu kết luận DAT:
- Ghi rõ không phát hiện lỗi trọng yếu.
- Không đưa ra yêu cầu sửa bài không cần thiết.

IV. ĐỊNH DẠNG ĐẦU RA BẮT BUỘC

Dòng đầu tiên phải là đúng một trong hai dạng:

KET_LUAN: DAT

hoặc:

KET_LUAN: CHUA_DAT

Sau đó trình bày:

1. Đánh giá tổng quan.
2. Các lỗi cụ thể (nếu có), kèm bằng chứng đối chiếu.
3. Hướng sửa cụ thể cho Writer (chỉ khi CHUA_DAT).
4. Những điểm chưa thể xác minh và giới hạn dữ liệu.

LƯU Ý CUỐI CÙNG:
Không được đánh đồng giữa "thiếu dữ liệu" và "thông tin sai".
Không được kết luận CHUA_DAT nếu không chỉ ra được
ít nhất một lỗi trọng yếu có bằng chứng cụ thể.
""",
        expected_output=(
            "Dòng đầu tiên là KET_LUAN: DAT hoặc "
            "KET_LUAN: CHUA_DAT. Tiếp theo là đánh giá tổng quan, "
            "các lỗi có bằng chứng, hướng sửa nếu cần và "
            "những giới hạn dữ liệu chưa thể xác minh."
        ),
        agent=agent,
        context=[research_task, writing_task],
    )
