from siri_question_answer import EstimatedTableConsumer

def on_message(message: str, _type: str, id: str) -> None:
    print(f"Id {id}")
    print(f"Type {_type}")
    print(f"Message {message}")

# Create a new EstimatedTableConsumer
consumer = EstimatedTableConsumer(url="https://api.ginko.voyage/Siri/Siri.do?apiKey=API_KEY")
consumer.listen_estimated_timetable(60, on_message)

# For demonstration - use any appropriate way to keep the program alive
import time
while True:
    time.sleep(1)