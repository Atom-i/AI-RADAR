import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class NLPProcessor:
    def __init__(self):
        logger.info("🧠 Initializing NLP Processor...")
        self.categories = [
            "Inference Optimization",
            "Model Architecture",
            "Training Methods",
            "Hardware",
            "Applications",
            "Reasoning",
            "Scaling"
        ]

    def summarize(self, text: str, max_length: int = 150) -> str:
        try:
            if len(text) > max_length:
                return text[:max_length] + "..."
            return text
        except Exception as e:
            logger.error(f"Error summarizing: {e}")
            return text

    def classify_trend(self, text: str) -> Dict:
        try:
            text_lower = text.lower()
            scores = {}
            
            category_keywords = {
                "Inference Optimization": ["inference", "optimization", "latency", "throughput"],
                "Model Architecture": ["transformer", "architecture", "layer", "attention"],
                "Training Methods": ["training", "learning", "gradient", "backprop"],
                "Hardware": ["gpu", "tpu", "hardware", "accelerator"],
                "Applications": ["application", "use case", "deployment"],
                "Reasoning": ["reasoning", "chain-of-thought", "logic", "inference"],
                "Scaling": ["scaling", "scale", "large", "distributed"]
            }
            
            for category, keywords in category_keywords.items():
                score = sum(1 for kw in keywords if kw in text_lower)
                scores[category] = score
            
            top_category = max(scores, key=scores.get)
            
            return {
                'category': top_category,
                'score': scores[top_category],
                'all_scores': scores
            }
        except Exception as e:
            logger.error(f"Error classifying: {e}")
            return {'category': 'Unknown', 'score': 0}