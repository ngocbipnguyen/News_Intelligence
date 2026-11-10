
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from crew.crew import create_news_crew


app = FastAPI(
    title="Technology News Intelligence API",
    description="API nghiên cứu và biên tập tin tức công nghệ bằng CrewAI",
    version="1.0.0",
)


class ResearchRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=3,
        description="Chủ đề công nghệ cần nghiên cứu",
    )
    number_of_news: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Số lượng tin tức mong muốn",
    )


@app.get("/")
def home():
    return {
        "message": "Technology News Intelligence API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/research")
def research_news(request: ResearchRequest):
    try:
        pipeline = create_news_crew(
            topic=request.topic,
            number_of_news=request.number_of_news,
        )

        result = pipeline.kickoff()

        return {
            "topic": request.topic,
            "number_of_news": request.number_of_news,
            "report": result.raw,
            "critic_status": result.critic_status,
            "critic_feedback": result.critic_feedback,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Research pipeline failed: {str(error)}",
        )
