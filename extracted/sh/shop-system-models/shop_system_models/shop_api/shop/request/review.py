from pydantic import BaseModel


class SubmitReviewModel(BaseModel):
    score: int
    text: str
    images: list[str] | None = []
    user_id: int | None = None  # Анонимный отзыв, если None


class ReviewModel(SubmitReviewModel):
    shop_name: str
