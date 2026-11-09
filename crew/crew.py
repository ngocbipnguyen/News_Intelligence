import re
from dataclasses import dataclass

from crewai import Crew, Process

from crew.agents import (
    create_researcher_agent,
    create_writer_agent,
    create_critic_agent,
)
from crew.tasks import (
    create_research_task,
    create_writing_task,
    create_critic_task,
)


@dataclass
class NewsPipelineResult:
    raw: str
    tasks_output: list
    critic_status: str
    critic_feedback: str

    def __str__(self):
        return self.raw


import re
import unicodedata

def get_critic_verdict(critic_text):
    clean_text = unicodedata.normalize("NFKC", str(critic_text))
    clean_text = clean_text.replace("*", "").replace("#", "")
    clean_text = clean_text.strip()

    first_line = clean_text.splitlines()[0].strip().upper()
    first_line = re.sub(r"\s+", " ", first_line)

    if "CHUA_DAT" in first_line or "CHƯA ĐẠT" in first_line:
        return "CHUA_DAT"

    if re.search(r"KET_LUAN:\s*DAT$", first_line):
        return "DAT"

    return "KHONG_XAC_DINH"


class NewsCrewRunner:
    def __init__(self, topic, number_of_news):
        self.topic = topic
        self.number_of_news = number_of_news

    def kickoff(self):
        researcher = create_researcher_agent()
        writer = create_writer_agent()
        critic = create_critic_agent()

        all_task_outputs = []

        # Researcher chạy một lần để tạo dữ liệu nền.
        research_task = create_research_task(
            researcher,
            self.topic,
            self.number_of_news,
        )
        research_crew = Crew(
            agents=[researcher],
            tasks=[research_task],
            process=Process.sequential,
            verbose=True,
        )

        print("\n========== RESEARCHER BAT DAU ==========\n")
        research_result = research_crew.kickoff()
        all_task_outputs.extend(research_result.tasks_output)
        print("\n========== RESEARCHER HOAN THANH ==========\n")

        critic_feedback_task = None
        final_report = ""
        final_critic_feedback = ""
        critic_status = "CHUA_KIEM_DUYET"

        # 4 lượt tối đa: 1 lần viết đầu + tối đa 3 lần sửa.
        for attempt in range(4):
            if attempt == 0:
                print("\n========== WRITER VIET LAN DAU ==========\n")
            else:
                print(f"\n========== WRITER SUA LAN {attempt} ==========\n")

            writing_task = create_writing_task(
                writer,
                research_task,
                critic_feedback_task,
            )
            critic_task = create_critic_task(
                critic,
                research_task,
                writing_task,
            )

            review_crew = Crew(
                agents=[writer, critic],
                tasks=[writing_task, critic_task],
                process=Process.sequential,
                verbose=True,
            )
            review_result = review_crew.kickoff()
            all_task_outputs.extend(review_result.tasks_output)

            writer_output = review_result.tasks_output[0]
            critic_output = review_result.tasks_output[1]

            final_report = writer_output.raw
            final_critic_feedback = critic_output.raw
            critic_status = get_critic_verdict(final_critic_feedback)

            print("\n========== KET QUA KIEM DUYET ==========\n")
            print("Ket luan:", critic_status)

            if critic_status == "DAT":
                print("\nBAO CAO DA DUOC DUYET!\n")
                break

            if attempt == 3:
                print("\nBAO CAO VAN CHUA DAT SAU 3 LAN SUA.\n")
                break

            critic_feedback_task = critic_task
            print("\nCritic yeu cau Writer chinh sua bao cao.\n")

        return NewsPipelineResult(
            raw=final_report,
            tasks_output=all_task_outputs,
            critic_status=critic_status,
            critic_feedback=final_critic_feedback,
        )


def create_news_crew(topic, number_of_news):
    return NewsCrewRunner(topic=topic, number_of_news=number_of_news)
