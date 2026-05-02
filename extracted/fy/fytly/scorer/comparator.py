import logging
import re
from scorer.config import GraderConfigs
from rapidfuzz import fuzz

grader_configs = GraderConfigs()

class GraderComparator:
    def compare_resume_to_role(self, resume_text, role_keywords):
        """
        Compare resume with role keywords and return:
        - total score based on matched weights
        - list of matched keywords from role

        Args:
            resume_text (str): The resume content
            role_keywords (dict): {keyword: weight}

        Returns:
            dict: {
                'total_score': int,
                'matched_keywords': list of strings
            }
        """
        try:
            threshold = int(grader_configs.props.get('threshold', 85))  # Default threshold 85

            if not resume_text or not role_keywords:
                logging.warning("Empty resume or keywords input.")
                return {"total_score": 0, "matched_keywords": []}

            resume_text_lower = resume_text.lower()
            total_score = 0
            matched_keywords = []

            for keyword, weight in role_keywords.items():
                keyword_lower = keyword.strip().lower()

                # Exact phrase match in resume text
                if keyword_lower in resume_text_lower:
                    total_score += weight
                    matched_keywords.append(keyword_lower)
                    continue

                # Fuzzy match (if exact not found)
                score = fuzz.partial_ratio(keyword_lower, resume_text_lower)
                if score >= threshold:
                    total_score += weight
                    matched_keywords.append(keyword_lower)

            return {
                "total_score": total_score,
                "matched_keywords": matched_keywords
            }

        except Exception as e:
            logging.error(f"Comparison failed: {e}")
            raise
