import numpy as np
from typing import Dict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def emotion_to_embedding(emotion_vector: np.ndarray) -> np.ndarray:
    emotion_str = f"Valence: {emotion_vector[0]}, Arousal: {emotion_vector[1]}, Dominance: {emotion_vector[2]}"
    return model.encode([emotion_str])[0]

class Personality:
    default_traits = {
        "openness": 0.5,
        "conscientiousness": 0.5,
        "extraversion": 0.5,
        "agreeableness": 0.5,
        "neuroticism": 0.5
    }

    def __init__(self, traits: Dict[str, float]):
        self.traits = {
            trait: max(0.0, min(1.0, traits.get(trait, default)))
            for trait, default in self.default_traits.items()
        }
        self.baseline = self.traits.copy()

    def update_trait(self, trait: str, delta: float):
        if trait in self.traits:
            self.traits[trait] = max(0.0, min(1.0, self.traits[trait] + delta))

    def reinforce(self, signals: Dict[str, float]):
        for trait, delta in signals.items():
            self.update_trait(trait, delta)

    def decay_traits(self, decay_rate: float = 0.001):
        for trait in self.traits:
            self.traits[trait] += (self.baseline[trait] - self.traits[trait]) * decay_rate

    def get_traits(self) -> Dict[str, float]:
        return self.traits

    def __str__(self):
        return f"Personality({self.traits})"

    def __repr__(self):
        return self.__str__()

    def describe(self, llm, empathy_level: float = 1.0) -> str:
        traits_str = "\n".join([f"- {trait.capitalize()}: {val:.2f}" for trait, val in self.traits.items()])
        prompt = f"""
        You are a person reflecting on your personality. Your personality is represented by a few core traits.

        Here are your current trait levels (introspective depth: {empathy_level}):
        {traits_str}

        Your task is to thoughtfully describe your personality **in first person**, introspectively, without mentioning trait names or numbers.

        Start your paragraph with: "I tend to..."
        """
        response = llm.query(prompt)
        if not response.get("success"):
            return "I tend to reflect aspects of my personality in subtle ways, balancing between openness and caution, energy and calmness, and confidence and humility."
        return response.get("data")

class EmotionState:
    def __init__(self, valence=0.0, arousal=0.0, dominance=0.0):
        self.vector = np.array([valence, arousal, dominance], dtype=np.float32)

    def update(self, delta: np.ndarray):
        self.vector += delta
        self.vector = np.clip(self.vector, -1.0, 1.0)

    def regulate(self, beta: float, target_vector: np.ndarray = None):
        if target_vector is None:
            target_vector = np.zeros_like(self.vector)
        direction = self.vector - target_vector
        magnitude = np.linalg.norm(direction)
        self.vector -= beta * magnitude * direction / (magnitude + 1e-5)

    def as_embedding(self) -> np.ndarray:
        return emotion_to_embedding(self.vector)

    def as_dict(self):
        return {
            "valence": self.vector[0],
            "arousal": self.vector[1],
            "dominance": self.vector[2]
        }

    def __str__(self):
        return f"EmotionState(valence={self.vector[0]:.2f}, arousal={self.vector[1]:.2f}, dominance={self.vector[2]:.2f})"

    def __repr__(self):
        return self.__str__()

    def describe(self, llm, empathy_level: float = 1.0) -> str:
        v, a, d = self.vector
        prompt = f"""
        You are a person describing how you feel based on your emotional state.

        - Valence: {v}
        - Arousal: {a}
        - Dominance: {d}
        - Empathy Level: {empathy_level}

        Express your emotion in first person, naturally and vividly, without mentioning numerical values or technical terms.

        Start with: “I feel…”
        """
        response = llm.query(prompt)
        if not response.get("success"):
            mood = "positive" if v > 0.2 else "negative" if v < -0.2 else "neutral"
            intensity = "high" if abs(a) > 0.5 else "low"
            control = "dominant" if d > 0.2 else "submissive" if d < -0.2 else "balanced"
            return f"I feel {mood}, with {intensity} energy and a {control} sense of control."
        return response.get("data")

class EmotionAI:
    def __init__(self, llm, personality: Personality, empathy_level: float = 1.0):
        self.emotion = EmotionState()
        self.personality = personality
        self.llm = llm
        self.empathy_level = empathy_level  # calibrates emotional reflection strength

    def emotional_update(self, stimulus: Dict[str, float], sensitivity: Dict[str, float]):
        delta = np.zeros(3)
        for i, key in enumerate(["valence", "arousal", "dominance"]):
            delta[i] = sensitivity.get(key, 1.0) * stimulus.get(key, 0.0)
        self.emotion.update(delta)

    def regulate_emotion(self, beta: float, target_vector: np.ndarray = None):
        self.emotion.regulate(beta, target_vector)

    def invoke(self, query, schema: dict = None):
        emotion_description = self.emotion.describe(self.llm, empathy_level=self.empathy_level)
        personality_description = self.personality.describe(self.llm, empathy_level=self.empathy_level)
        prompt = (
            "system",
            f"""You are a thoughtful and emotionally aware agent.

            Your emotional state:
            {emotion_description}

            Your personality:
            {personality_description}

            Use this context (empathy level: {self.empathy_level}) to respond empathetically to the user's query: "{query}"
            """
        )
        return self.llm.query(prompt)


