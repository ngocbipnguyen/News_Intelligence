import argparse
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Nạp biến môi trường từ file .env
load_dotenv(override=True)


def main():
    parser = argparse.ArgumentParser(
        description="Run Technology News Intelligence automatically"
    )

    parser.add_argument(
        "--topic",
        default="Những ứng dụng AI mới nhất",
        help="Chủ đề cần nghiên cứu",
    )

    parser.add_argument(
        "--number",
        type=int,
        default=5,
        help="Số lượng tin tức cần nghiên cứu",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chạy thử mà không gọi API",
    )

    args = parser.parse_args()

    # Chế độ kiểm tra: không chạy Agent, không tốn API
    if args.dry_run:
        print("DRY RUN: Script hoạt động thành công.")
        print(f"Chủ đề: {args.topic}")
        print(f"Số lượng tin: {args.number}")
        return

    from crew.crew import create_news_crew

    print("Đang khởi động Technology News Intelligence...")

    pipeline = create_news_crew(
        topic=args.topic,
        number_of_news=args.number,
    )

    result = pipeline.kickoff()

    # Tạo thư mục lưu báo cáo nếu chưa tồn tại
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Tạo tên file theo thời gian chạy
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"report_{timestamp}.md"

    # Lưu báo cáo
    report_path.write_text(
        result.raw or "",
        encoding="utf-8",
    )

    print(f"Đã lưu báo cáo: {report_path.resolve()}")
    print(f"Critic status: {result.critic_status}")


if __name__ == "__main__":
    main()
