from typing import Any, List, Union
from openai import OpenAI
from openai.types.responses import Response as OpenAIResponse, ResponseOutputItem as OpenAIResponseOutputItem, ResponseOutputMessage as OpenAIResponseOutputMessage
from matrx_utils import vcprint, clear_terminal
from dotenv import load_dotenv
from matrx_ai.config.unified_config import UnifiedMessage

load_dotenv()
clear_terminal()

client = OpenAI()

# Use the streaming context manager to get both events and final response
with client.responses.stream(
    model="gpt-5-mini",
    reasoning={
        "effort": "medium",
        "summary": "detailed"
    },
    tools=[{ "type": "web_search_preview" }],
    include=["reasoning.encrypted_content"],
    input="What was a positive news story from today?",
) as stream:
    # Process streaming events in real-time
    for event in stream:
        event_type = event.type
        
        # Handle different event types for streaming display
        if event_type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
        elif event_type == "response.reasoning_summary_text.delta":
            print(f"{event.delta}", end="", flush=True)
        elif event_type == "response.created":
            vcprint("Stream started", color="cyan")
        elif event_type == "response.completed":
            vcprint("\nStream completed", color="green")
    
    # Get the final complete response with full content and usage data
    response: OpenAIResponse = stream.get_final_response()

print("\n" + "="*50)
vcprint(response, "Final Complete Response", color="green")


# Output is a list of items that can be messages, reasoning, web_search_call, etc.
output: List[OpenAIResponseOutputItem] = response.output

for item in output:
    item_type: str = item.type
    if item_type == "message":
        pass
    elif item_type == "reasoning":
        pass
    elif item_type == "web_search_call":
        pass
    else:
        vcprint(item, "Unknown Item", color="red")

unified_message: UnifiedMessage = UnifiedMessage.from_openai(output)
vcprint(unified_message, "Unified Message", color="magenta")

sample_output: List[OpenAIResponseOutputItem] = [
        {
            "id": "ws_0a12a58b7b1fca6000695550b609b88193a3323f0785901b3d",
            "action": {
                "query": "positive news story today",
                "type": "search",
                "sources": None
            },
            "status": "completed",
            "type": "web_search_call"
        },
        {
            "id": "msg_0a12a58b7b1fca6000695550b710b081938dae0143aaf39048",
            "content": [
                {
                    "annotations": [
                        {
                            "end_index": 495,
                            "start_index": 303,
                            "title": "School assembly news headlines, December 31: Top India, world, sports, business news - India Today",
                            "type": "url_citation",
                            "url": "https://www.indiatoday.in/amp/education-today/news/story/school-assembly-news-headlines-december-31-top-india-world-sports-business-news-2844210-2025-12-31?utm_source=openai"
                        },
                        {
                            "end_index": 950,
                            "start_index": 865,
                            "title": "2025 in science",
                            "type": "url_citation",
                            "url": "https://en.wikipedia.org/wiki/2025_in_science?utm_source=openai"
                        }
                    ],
                    "text": "On December 31, 2025, a notable positive development was the strong performance of global stock markets. European indices reached record highs, and there were significant gains in both Asian and U.S. markets. This resilience reflects investor confidence and sets a promising tone for the upcoming year. ([indiatoday.in](https://www.indiatoday.in/amp/education-today/news/story/school-assembly-news-headlines-december-31-top-india-world-sports-business-news-2844210-2025-12-31?utm_source=openai))\n\nAdditionally, in the realm of science, UK company Space Forge achieved a milestone in space-based manufacturing by successfully demonstrating a 1,000 \u00b0C furnace aboard an orbital micro-factory. This advancement is designed to produce semiconductor materials in microgravity, potentially resulting in materials up to 4,000 times purer than those manufactured on Earth. ([en.wikipedia.org](https://en.wikipedia.org/wiki/2025_in_science?utm_source=openai))\n\nThese developments highlight significant progress in both economic and technological fields as the year concludes. ",
                    "type": "output_text",
                    "logprobs": []
                }
            ],
            "role": "assistant",
            "status": "completed",
            "type": "message"
        }
    ]

full_response_example: OpenAIResponse = {
    "id": "resp_0a16d8c172123aeb006955587f41f481a0b884a4f06bedc90c",
    "created_at": 1767200895.0,
    "error": None,
    "incomplete_details": None,
    "instructions": None,
    "metadata": {},
    "model": "gpt-5.1-2025-11-13",
    "object": "response",
    "output": [
        {
            "id": "rs_0a16d8c172123aeb006955587ff73081a099639e7f57bdd432",
            "summary": [
                {
                    "text": "**Searching for positive news**\n\nI need to find a positive news story from today, December 31, 2025. The user is looking for something uplifting, possibly related to science, the environment, or medicine. I'll use the web tool to execute a search query focusing on today's date for recent and relevant news. I\u2019ll make sure to pull just one great story that fits what the user is interested in! Let's see what we can find.",
                    "type": "summary_text"
                }
            ],
            "type": "reasoning",
            "content": None,
            "encrypted_content": None,
            "status": None
        },
        {
            "id": "ws_0a16d8c172123aeb006955588402c481a096d2645bee7a9be5",
            "action": {
                "query": "good news positive news December 31 2025 breakthrough discovery",
                "type": "search",
                "sources": None
            },
            "status": "completed",
            "type": "web_search_call"
        },
        {
            "id": "rs_0a16d8c172123aeb00695558935a0881a0bf1a647cc846ee99",
            "summary": [
                {
                    "text": "**Searching for positive news**\n\nI need to find a positive story specifically from today, December 31, 2025. I've noticed some general \"year in review\" articles and positive science updates, but the user asked for something published today. I should refine my search for \"December 31, 2025 good news.\" I\u2019ll aim for a mainstream piece, possibly something like an article about a malaria vaccine cost drop or conservation success. I\u2019ll focus on getting a concrete story.",
                    "type": "summary_text"
                }
            ],
            "type": "reasoning",
            "content": None,
            "encrypted_content": None,
            "status": None
        },
        {
            "id": "ws_0a16d8c172123aeb00695558953d2081a0b5781268222e73c8",
            "action": {
                "query": "\"December 31, 2025\" \"good news\" \"breakthrough\"",
                "type": "search",
                "sources": None
            },
            "status": "completed",
            "type": "web_search_call"
        },
        {
            "id": "rs_0a16d8c172123aeb00695558a09c5881a0a02af404b0d209f2",
            "summary": [
                {
                    "text": "**Summarizing conservation success**\n\nThere\u2019s a recent article titled \"DEC completes spruce grouse restoration effort\" published on December 31, 2025, detailing the successful conservation of the endangered spruce grouse in New York. This counts as positive news since it highlights a successful effort in wildlife restoration in the user's state. I should summarize the key points briefly, providing just enough context to explain why it\u2019s a good development, and cite the source as FingerLakes1.com.",
                    "type": "summary_text"
                },
                {
                    "text": "**Finalizing spruce grouse summary**\n\nI\u2019m reviewing the details of the article to ensure I have everything right. The New York State Department of Environmental Conservation has completed its 13-year spruce grouse recovery program in the Adirondacks, releasing a total of 363 adults and 711 chicks. Their final release included 50 adults in summer 2025, and now they're focusing on monitoring and habitat management. This is a major milestone for conservation, showing a shift from decline to hope for this endangered species.",
                    "type": "summary_text"
                },
                {
                    "text": "**Defining spruce grouse**\n\nI'll quickly define the spruce grouse as a rare bird found in cold forests, situated near the southern edge of its range in New York. This is positive news as it represents a long-term investment in wildlife conservation and showcases cross-border cooperation efforts for species protection. Overall, this achievement is significant for restoring populations. I'll make sure to include the explicit date of December 31, 2025, in my response.",
                    "type": "summary_text"
                }
            ],
            "type": "reasoning",
            "content": None,
            "encrypted_content": None,
            "status": None
        },
        {
            "id": "msg_0a16d8c172123aeb00695558a8999481a0ba1cf75662ed604e",
            "content": [
                {
                    "annotations": [
                        {
                            "end_index": 796,
                            "start_index": 669,
                            "title": "DEC completes spruce grouse restoration effort",
                            "type": "url_citation",
                            "url": "https://www.fingerlakes1.com/2025/12/31/dec-completes-spruce-grouse-restoration-effort/?utm_source=openai"
                        }
                    ],
                    "text": "One uplifting story from today (December 31, 2025):\n\nNew York\u2019s Department of Environmental Conservation announced it has completed the release phase of a 13\u2011year program to rescue the endangered spruce grouse, one of the state\u2019s rarest birds, in the Adirondacks. \n\nSince 2013, biologists and partners in Canada and Maine have moved hundreds of adult birds and chicks into carefully selected forest habitats to rebuild the population. With the final group of birds released this past summer, officials say the focus can now shift from emergency releases to long\u2011term monitoring and habitat protection\u2014meaning the species is no longer in immediate freefall in New York. ([fingerlakes1.com](https://www.fingerlakes1.com/2025/12/31/dec-completes-spruce-grouse-restoration-effort/?utm_source=openai))\n\nSo, today\u2019s good news: a long, patient conservation effort has reached a major milestone, giving a threatened species a real chance to recover.",
                    "type": "output_text",
                    "logprobs": []
                }
            ],
            "role": "assistant",
            "status": "completed",
            "type": "message"
        }
    ],
    "parallel_tool_calls": True,
    "temperature": 1.0,
    "tool_choice": "auto",
    "tools": [
        {
            "type": "web_search_preview",
            "search_context_size": "medium",
            "user_location": {
                "type": "approximate",
                "city": None,
                "country": "US",
                "region": None,
                "timezone": None
            }
        }
    ],
    "top_p": 1.0,
    "background": False,
    "conversation": None,
    "max_output_tokens": None,
    "max_tool_calls": None,
    "previous_response_id": None,
    "prompt": None,
    "prompt_cache_key": None,
    "reasoning": {
        "effort": "high",
        "generate_summary": None,
        "summary": "detailed"
    },
    "safety_identifier": None,
    "service_tier": "default",
    "status": "completed",
    "text": {
        "format": {
            "type": "text"
        },
        "verbosity": "medium"
    },
    "top_logprobs": 0,
    "truncation": "disabled",
    "usage": {
        "input_tokens": 12296,
        "input_tokens_details": {
            "cached_tokens": 0
        },
        "output_tokens": 1076,
        "output_tokens_details": {
            "reasoning_tokens": 893
        },
        "total_tokens": 13372
    },
    "user": None,
    "billing": {
        "payer": "developer"
    },
    "completed_at": 1767200936,
    "prompt_cache_retention": None,
    "store": True
}