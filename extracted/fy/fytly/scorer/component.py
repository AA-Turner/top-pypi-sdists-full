import os
import logging
from importlib import resources
from scorer.payloadreader import GraderPayloadReader
from scorer.preprocesser import GraderPreprocessor
from scorer.comparator import GraderComparator
from scorer.config import GraderConfigs

grader_configs = GraderConfigs()

class GraderComponent:
    def read_input_payload(self, file: bytes, filename: str, role_code: str):
        try:
            # Step 1: Read file content based on extension
            extension = filename.split('.')[-1].lower()
            if extension == 'pdf':
                raw_text = GraderPayloadReader.read_pdf(file)
            elif extension == 'docx':
                raw_text = GraderPayloadReader.read_docx(file)
            else:
                raise ValueError("Unsupported file type")

            # Step 2: Preprocess text
            processed_text = GraderPreprocessor().preprocess(raw_text)

            # Step 3: Fetch keywords from the corresponding .txt file based on role_code
            if not role_code:
                raise ValueError("role_code is missing in input")

            role_to_file = {
                'pd': 'pd_keywords.txt',
                'jd': 'jd_keywords.txt',
                'pfd': 'pfd_keywords.txt',
                'jfd': 'jfd_keywords.txt',
                'ai':'ai_keywords.txt',
                'de':'de_keywords.txt',
                'da':'da_keywords.txt'
            }

            keywords_file = role_to_file.get(role_code.lower())
            if not keywords_file:
                raise ValueError(f"No keywords file mapping for role_code: {role_code}")


            # Read keyword file from package using importlib.resources
            with resources.open_text("scorer.configs", keywords_file, encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    raise ValueError(f"Keywords file {keywords_file} is empty")
                pairs = content.split(',')
                keywords_result = {
                    pair.split(':')[0].strip(): int(pair.split(':')[1])
                    for pair in pairs if ':' in pair
                }





            # Step 4: Compare resume to role
            comparison_result = GraderComparator().compare_resume_to_role(processed_text, keywords_result)

            if not isinstance(comparison_result, dict):
                raise TypeError("compare_resume_to_role must return a dictionary")

            print(f"comparison_result type: {type(comparison_result)}, value: {comparison_result}")

            total_score = comparison_result.get("total_score", 0)
            matched_keywords = comparison_result.get("matched_keywords", [])

            # Step 5: Eligibility logic
            backend_developer_score = int(grader_configs.props.get('backend_developer_score'))
            full_stack_developer_score = int(grader_configs.props.get('full_stack_developer_score'))
            data_engineer_score = int(grader_configs.props.get('data_engineer_score'))
            ai_engineer_score = int(grader_configs.props.get('ai_engineer_score'))
            data_analyst_score=int(grader_configs.props.get('data_analyst_score'))

            eligible = False
            message = "Not eligible"

            if role_code.lower() in ['pd', 'jd'] and total_score >= backend_developer_score:
                eligible = True
                message = "Eligible for this role"
            elif role_code.lower() in ['pfd', 'jfd'] and total_score >= full_stack_developer_score:
                eligible = True
                message = "Eligible for this role"
            elif role_code.lower() =='de' and total_score >= data_engineer_score:
                eligible = True
                message = "Eligible for this role"
            elif role_code.lower() =='ai' and total_score >= ai_engineer_score:
                eligible = True
                message = "Eligible for this role"
            elif role_code.lower()=='da' and total_score >= data_analyst_score:
                eligible = True
                message = "Eligible for this role"




            return {
                "role_code": role_code,
                "comparator_score": total_score,
                "matched_keywords": matched_keywords,
                "eligible": eligible,
                "message": message
            }

        except Exception as e:
            logging.error(f"read input payload failed: {e}")
            raise

    # Function to detect the programming language from given code text
    def detect_language_from_code(self,code_text):
        try:
            # Map language names to their corresponding pattern file names inside 'scorer/configs'
            language_to_file = {
                'python': 'python_patterns.txt',
                'java': 'java_patterns.txt'
            }
            # Dictionary to hold count of pattern matches for each language
            language_counts = {}
            # Loop through each language and its associated pattern file
            for lang, file_name in language_to_file.items():
                # Open the pattern file using importlib.resources (safe access inside packages)
                with resources.open_text("scorer.configs", file_name, encoding="utf-8") as f:
                    # Read and strip any leading/trailing whitespace
                    content = f.read().strip()

                    # If file is empty, raise a ValueError
                    if not content:
                        raise ValueError(f"{file_name} is empty")
                    # Split the file content into a list of non-empty, stripped patterns
                    patterns = [line.strip() for line in content.splitlines() if line.strip()]

                    # Count how many times each pattern appears in the code_text and sum the total count
                    count = sum(code_text.count(pattern) for pattern in patterns)

                    # Store the total count for this language in the dictionary
                    language_counts[lang] = count
            # Identify the language with the highest match count
            max_language = max(language_counts, key=language_counts.get)
            max_count = language_counts[max_language]

            # If no patterns were found, classify as 'Unknown'
            if max_count == 0:
                detected_language = "Unknown"
            else:
                # Otherwise, capitalize the language name (e.g., 'python' → 'Python')
                detected_language = max_language.capitalize()

            # Return the result as a dictionary:
            return {
                # Preview of code_text (first 100 characters + '...' if longer)
                #"code_text": code_text[:100] + '...' if len(code_text) > 100 else code_text,
                # Dictionary of match counts per language
                "language_counts": language_counts,
                # Final detected language name
                "detected_language": detected_language
                }

        # If any exception occurs, log the error message and re-raise the exception
        except Exception as e:
                logging.error(f"Failed to detect language: {e}")
                raise
