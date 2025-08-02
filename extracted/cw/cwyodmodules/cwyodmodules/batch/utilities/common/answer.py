import json
from typing import List, Optional
from .source_document import SourceDocument


class Answer:
    def __init__(
        self,
        question: str,
        answer: str,
        source_documents: List[SourceDocument] = [],
        prompt_tokens: Optional[int] = 0,
        completion_tokens: Optional[int] = 0,
    ):
        self.question = question
        self.answer = answer
        self.source_documents = source_documents
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Answer):
            return False

        return (
            self.question == value.question
            and self.answer == value.answer
            and self.source_documents == value.source_documents
            and self.prompt_tokens == value.prompt_tokens
            and self.completion_tokens == value.completion_tokens
        )

    def __str__(self) -> str:
        """Return a formatted string representation of the answer with sources."""
        result = self.answer
        
        # Add source references if available
        if self.source_documents and len(self.source_documents) > 0:
            result += "\n\nSources:"
            for i, doc in enumerate(self.source_documents):
                title = doc.title or f"Document {i+1}"
                result += f"\n[{i+1}] {title} - {doc.source}"
        
        return result

    def to_json(self):
        return json.dumps(self, cls=AnswerEncoder)

    @classmethod
    def from_json(cls, json_string):
        return json.loads(json_string, cls=AnswerDecoder)

class AnswerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Answer):
            return {
                "question": obj.question,
                "answer": obj.answer,
                "source_documents": [doc.to_json() for doc in obj.source_documents],
                "prompt_tokens": obj.prompt_tokens,
                "completion_tokens": obj.completion_tokens,
            }
        return super().default(obj)


# class AnswerDecoder(json.JSONDecoder):
#     def decode(self, s, **kwargs):
#         obj = super().decode(s, **kwargs)
#         return Answer(
#             question=obj["question"],
#             answer=obj["answer"],
#             source_documents=[
#                 SourceDocument.from_json(doc) for doc in obj["source_documents"]
#             ],
#             prompt_tokens=obj["prompt_tokens"],
#             completion_tokens=obj["completion_tokens"],
#         )
class AnswerDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        obj = super().decode(s, **kwargs)
        source_documents = []
        for doc in obj["source_documents"]:
            source_documents.append(SourceDocument.from_json(doc))
        return Answer(
            question=obj["question"],
            answer=obj["answer"],
            source_documents=source_documents,
            prompt_tokens=obj["prompt_tokens"],
            completion_tokens=obj["completion_tokens"],
        )