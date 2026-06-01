import logging
import re
import subprocess
import sys

import pymupdf as fitz
import spacy

logger = logging.getLogger(__name__)


def ensure_spacy_model():
    try:
        spacy.load("en_core_web_sm")
    except OSError:
        logger.info("Downloading spaCy model 'en_core_web_sm'...")
        try:
            subprocess.check_call([
                sys.executable,
                "-m",
                "spacy",
                "download",
                "en_core_web_sm",
            ])
        except Exception as e:
            logging.exception(f"Failed to download spaCy model: {e}")


ensure_spacy_model()
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    logging.exception(f"Could not load spaCy model: {e}")
    nlp = None


def extract_text_from_pdf(file_path: str) -> str:
    logger.info(f"Opening PDF with fitz: {file_path}")
    try:
        doc = fitz.open(file_path)
        text = ""
        page_count = doc.page_count
        logger.info(f"PDF has {page_count} pages")
        for i, page in enumerate(doc):
            page_text = page.get_text()
            logger.debug(f"Extracted {len(page_text)} chars from page {i + 1}")
            text += (
                page_text
                + """
"""
            )
        return text
    except Exception as e:
        logger.exception(f"Error reading PDF: {e}")
        return ""


def clean_text(text: str) -> str:
    return re.sub("\\s+", " ", text).strip()


def extract_email(text: str) -> str:
    email_pattern = "[\\w\\.-]+@[\\w\\.-]+\\.\\w+"
    match = re.search(email_pattern, text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    phone_pattern = "[\\+]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{4,6}"
    match = re.search(phone_pattern, text)
    return match.group(0) if match else ""


def extract_linkedin(text: str) -> str:
    """Extract LinkedIn URL with support for multiple formats and split lines."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    text_block = " ".join(lines[:50])
    text_block_lower = text_block.lower()
    standard_pattern = "linkedin\\.com/in/\\s*([\\w-]+)"
    match = re.search(standard_pattern, text_block_lower)
    if match:
        return f"https://linkedin.com/in/{match.group(1)}"
    marker_pattern = "([\\w-]+)\\s*\\(linkedin\\)"
    match = re.search(marker_pattern, text_block_lower)
    if match:
        return f"https://linkedin.com/in/{match.group(1)}"
    for i, line in enumerate(lines[:30]):
        clean_line = line.lower()
        if "linkedin.com/in/" in clean_line:
            if clean_line.endswith("/in/") and i + 1 < len(lines):
                username = lines[i + 1].split()[0]
                username = re.sub(
                    "\\(linkedin\\)", "", username, flags=re.IGNORECASE
                ).strip()
                if re.match("^[\\w-]+$", username):
                    return f"https://linkedin.com/in/{username}"
    return ""


def extract_role(text: str, name: str) -> str:
    """Extract role/title from Resume or LinkedIn PDF.

    Attempts two patterns:
    1. LinkedIn Style: Name line followed immediately by role title.
    2. Traditional Style: Professional header with role descriptors separated by pipes/slashes.
    """
    if not name:
        return ""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    name_lower = name.lower()
    name_words_count = len(name.split())
    role_keywords = [
        "engineer",
        "developer",
        "manager",
        "director",
        "consultant",
        "founder",
        "ceo",
        "cto",
        "coo",
        "cfo",
        "vp",
        "president",
        "lead",
        "head",
        "chief",
        "analyst",
        "designer",
        "architect",
        "specialist",
        "advisor",
        "partner",
        "scientist",
        "researcher",
        "professor",
        "coach",
        "strategist",
        "executive",
        "expert",
    ]
    skip_patterns = [
        "summary",
        "experience",
        "education",
        "skills",
        "contact",
        "languages",
        "publications",
        "certifications",
        "page ",
        "top skills",
    ]
    for i, line in enumerate(lines[:50]):
        line_lower = line.lower()
        line_words = line.split()
        is_standalone_name = (
            name_lower in line_lower
            and len(line_words) <= name_words_count + 1
            and (not any(skip in line_lower for skip in skip_patterns))
        )
        if is_standalone_name:
            role_parts = []
            for j in range(i + 1, min(i + 6, len(lines))):
                candidate = lines[j]
                candidate_lower = candidate.lower()
                if (
                    "area" in candidate_lower
                    or ("," in candidate and len(candidate.split(",")) == 2)
                    or any(skip in candidate_lower for skip in skip_patterns)
                ):
                    break
                if any(kw in candidate_lower for kw in role_keywords) or (
                    candidate[0].isupper() and len(candidate.split()) < 12
                ):
                    role_parts.append(candidate)
                elif role_parts:
                    break
            if role_parts:
                full_role = " ".join(role_parts)
                return re.sub("\\s+", " ", full_role).strip()
    for line in lines[:10]:
        line_lower = line.lower()
        if "|" in line or " / " in line or " • " in line:
            if any(kw in line_lower for kw in role_keywords):
                parts = re.split("\\||\\/|\\u2022", line)
                for part in parts:
                    part = part.strip()
                    if any(kw in part.lower() for kw in role_keywords):
                        return part
    return ""


def extract_name(text: str, nlp_doc) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    non_name_indicators = [
        "page",
        "curriculum",
        "resume",
        "contact",
        "mobile",
        "email",
        "linkedin",
        "publications",
        "certifications",
        "skills",
        "languages",
        "honors",
        "awards",
        "greater",
        "area",
        "region",
        "metro",
        "north",
        "south",
        "east",
        "west",
        "central",
        "bay",
        "united states",
        "kingdom",
        "canada",
        "australia",
        "software engineer",
        "software design",
        "software infrastructure",
        "software development",
        "developer",
        "manager",
        "director",
        "consultant",
        "specialist",
        "top skills",
        "summary",
    ]
    for i, line in enumerate(lines[:50]):
        if line.lower() == "summary" or line.lower().startswith("summary"):
            for j in range(i - 1, max(-1, i - 10), -1):
                candidate = lines[j]
                candidate_lower = candidate.lower()
                if len(candidate.split()) < 2:
                    continue
                if (
                    1 < len(candidate.split()) <= 4
                    and (not any(char.isdigit() for char in candidate))
                    and ("@" not in candidate)
                    and (not any(w in candidate_lower for w in non_name_indicators))
                ):
                    if candidate.istitle() or candidate.isupper():
                        return candidate.title()
    for i in range(min(5, len(lines))):
        line = lines[i]
        if (
            "@" in line
            or "phone" in line.lower()
            or "resume" in line.lower()
            or ("curriculum" in line.lower())
            or ("contact" in line.lower())
            or any(w in line.lower() for w in non_name_indicators)
        ):
            continue
        if re.match("^[A-Z][a-z]+(\\s+[A-Z][a-z]+){1,2}$", line):
            return line.title()
    if nlp_doc:
        for i in range(min(15, len(lines))):
            line = lines[i]
            if any(
                h in line.lower()
                for h in ["summary", "experience", "education", "skills", "contact"]
            ):
                continue
            doc = nlp(line)
            for ent in doc.ents:
                if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                    if ent.text.lower() not in [
                        "curriculum vitae",
                        "resume",
                        "software engineer",
                        "contact",
                        "email",
                    ] and (not any(w in ent.text.lower() for w in non_name_indicators)):
                        return ent.text.title()
    first_line = lines[0]
    if (
        1 < len(first_line.split()) < 5
        and (not any(char.isdigit() for char in first_line))
        and (not any(w in first_line.lower() for w in non_name_indicators))
    ):
        return first_line.title()
    return ""


def extract_location(text: str, nlp_doc) -> str:
    """Extract location with pattern matching and tech blacklist fallback."""
    tech_blacklist = {
        "Spark",
        "Python",
        "Java",
        "Docker",
        "Kubernetes",
        "React",
        "Elastic",
        "Spring",
        "Swift",
        "Kafka",
        "Pandas",
        "Ansible",
        "Terraform",
        "Unity",
        "AWS",
        "Azure",
        "GCP",
        "Linux",
        "Node",
        "Django",
        "Flask",
        "FastAPI",
    }
    lines = [line.strip() for line in text.splitlines() if line.strip()][:10]
    location_pattern = (
        "([A-Z][a-z]+(?:\\s[A-Z][a-z]+)*),\\s([A-Z]{2})(?:\\s*\\(Remote\\))?"
    )
    for line in lines:
        match = re.search(location_pattern, line)
        if match:
            city, state = match.groups()
            return f"{city}, {state}"
    if nlp_doc:
        for ent in nlp_doc.ents:
            if ent.label_ == "GPE":
                if ent.text not in tech_blacklist and len(ent.text) > 2:
                    return ent.text
    return ""


def extract_summary(text: str) -> str:
    headers = ["summary", "profile", "professional summary", "about me", "objective"]
    stop_headers = [
        "experience",
        "employment",
        "work history",
        "skills",
        "education",
        "projects",
        "certifications",
        "publications",
        "languages",
        "interests",
    ]
    lines = text.splitlines()
    for i, line in enumerate(lines):
        clean_header = line.strip().lower()
        clean_header = re.sub("[:\\-]+", "", clean_header).strip()
        if clean_header in headers:
            summary = []
            for j in range(i + 1, len(lines)):
                content = lines[j].strip()
                if not content:
                    continue
                clean_content = re.sub("[:\\-]+", "", content.lower()).strip()
                if clean_content in stop_headers:
                    break
                if content.isupper() and len(content) < 30 and (" " not in content):
                    break
                if re.match("^[●•\\-\\*\\u2022\\u2023\\u2043\\u204c]", content):
                    break
                summary.append(content)
                if len(summary) > 25:
                    break
            return " ".join(summary)
    return ""


def is_job_header_line(line: str) -> bool:
    """Detects lines that are likely part of a LinkedIn job history header."""
    line = line.strip()
    if not line:
        return False
    date_range_pattern = "(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\.?\\s+\\d{4}\\s*[-–]\\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\.?\\s+\\d{4})"
    if re.search(date_range_pattern, line, re.IGNORECASE):
        return True
    tenure_pattern = "^(\\(?\\d+\\s+(?:yr|yrs|year|years|mo|mos|month|months).*)|(^\\d{4}\\s*[-–]\\s*(?:Present|\\d{4}))"
    if re.match(tenure_pattern, line, re.IGNORECASE):
        return True
    titles = [
        "Engineering",
        "Software",
        "Senior",
        "Lead",
        "Staff",
        "Principal",
        "Director",
        "Manager",
        "VP",
        "CEO",
        "CTO",
        "COO",
        "CFO",
        "Founder",
        "Owner",
        "Co-Founder",
        "President",
        "Advisor",
        "Consultant",
        "Head",
        "Chief",
    ]
    title_suffixes = [
        "Manager",
        "Engineer",
        "Developer",
        "Architect",
        "Director",
        "Officer",
        "Lead",
        "Specialist",
    ]
    title_pattern = f"^(?:{'|'.join(titles)})\\s*(?:{'|'.join(title_suffixes)})?$"
    if re.match(title_pattern, line, re.IGNORECASE):
        return True
    if len(line) < 50 and (not line.startswith(("•", "-", "*"))) and ("." not in line):
        words = line.split()
        if 1 <= len(words) <= 5 and all(w[0].isupper() for w in words if w.isalpha()):
            return True
    return False


def extract_achievements(text: str) -> list[dict[str, str]]:
    achievements = []
    raw_lines = text.splitlines()
    impact_words = [
        "increased",
        "decreased",
        "improved",
        "reduced",
        "saved",
        "generated",
        "delivered",
        "led",
        "managed",
        "built",
        "launched",
        "achieved",
        "optimized",
        "streamlined",
        "developed",
        "co-developed",
        "created",
        "implemented",
        "scaled",
        "grew",
    ]
    contact_patterns = ["@", "+", "www.", "linkedin.com", "/in/", "tel:", "phone:"]
    header_patterns = [
        "\\|.*\\(",
        "\\d{4}[\\u2013\\-](?:\\d{4}|Present)",
        "[\\u2013\\-]\\s*[A-Z]{2}$",
        "^(?:Education|Experience|Skills|Summary|Objective|Awards)",
    ]
    continuation_starters = {
        "that",
        "which",
        "and",
        "but",
        "or",
        "with",
        "by",
        "for",
        "from",
        "to",
        "in",
        "of",
        "at",
        "as",
        "on",
        "while",
        "where",
        "when",
        "who",
        "whose",
    }
    merged_lines = []
    current_bullet = ""
    for line in raw_lines:
        line = line.strip().replace("\u200b", "")
        if not line:
            continue
        is_bullet_start = bool(
            re.match("^[●•\\-\\*\\u2022\\u2023\\u2043\\u204c]", line)
        )
        is_header = any(re.search(p, line) for p in header_patterns)
        is_job_meta = is_job_header_line(line)
        is_likely_new_section = (
            is_header
            or (line.isupper() and len(line) < 50)
            or "Present" in line
            or is_job_meta
        )
        if is_job_meta and current_bullet:
            merged_lines.append(current_bullet)
            current_bullet = ""
            continue
        first_word = line.split()[0].lower() if line.split() else ""
        is_continuation_line = (
            not is_bullet_start
            and (not is_likely_new_section)
            and (
                line[0].islower()
                or first_word in continuation_starters
                or line.startswith(",")
                or line.startswith("(")
            )
        )
        if is_bullet_start:
            if current_bullet:
                merged_lines.append(current_bullet)
            current_bullet = line
        elif current_bullet:
            if (
                not is_likely_new_section
                and (not any(p in line.lower() for p in contact_patterns))
                and (len(line.split()) >= 1)
            ):
                current_bullet = f"{current_bullet} {line}"
            else:
                merged_lines.append(current_bullet)
                current_bullet = line if not is_likely_new_section else ""
        elif is_continuation_line and merged_lines:
            merged_lines[-1] = f"{merged_lines[-1]} {line}"
        elif not is_likely_new_section:
            merged_lines.append(line)
    if current_bullet:
        merged_lines.append(current_bullet)
    continuation_starters.update({
        "resulting",
        "including",
        "utilizing",
        "leveraging",
        "while",
        "during",
        "within",
        "across",
        "through",
        "plus",
        "also",
        "additionally",
        "furthermore",
    })
    for line in merged_lines:
        line = re.sub("\\s+", " ", line).strip()
        if any(pattern in line.lower() for pattern in contact_patterns):
            continue
        if re.match(
            "^(?:I\\s+(?:am|was|have|had|own|lead|managed|worked|built)|My\\s+)",
            line,
            re.IGNORECASE,
        ):
            continue
        if re.match(
            "^(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\\w*\\s+\\d{4}",
            line,
            re.IGNORECASE,
        ):
            continue
        has_number = any(char.isdigit() for char in line)
        has_symbol = any(char in ["%", "$", "+"] for char in line)
        has_impact = any(word in line.lower() for word in impact_words)
        cleaned_start = re.sub("^[●•\\-\\*\\d]+\\.*\\s*", "", line)
        if not cleaned_start:
            continue
        first_word = cleaned_start.split()[0].lower()
        if (
            first_word in continuation_starters
            or cleaned_start[0].islower()
            or first_word.replace("%", "").isdigit()
        ):
            continue
        if has_number and (has_symbol or has_impact):
            cleaned = cleaned_start
            if re.match("^[\\d%]+\\s", cleaned) or cleaned.startswith("%"):
                continue
            if re.search("Page\\s+\\d+\\s+of\\s+\\d+", cleaned, re.IGNORECASE):
                continue
            metric_match = re.search(
                "(\\d+(?:\\.\\d+)?\\s*(?:%|k|M|B|\\+|years?|yrs?|users?|customers?))",
                cleaned,
                re.IGNORECASE,
            )
            metric = metric_match.group(1) if metric_match else "Key Result"
            title = "Impact Highlight"
            title_set = False
            doc = nlp(cleaned) if nlp else None
            if doc:
                first_token = doc[0]
                if (
                    first_token.pos_ == "VERB"
                    or first_token.text.lower() in impact_words
                ):
                    obj_phrase = []
                    for token in doc[1:6]:
                        if token.text.lower() in (
                            ",",
                            ".",
                            "and",
                            "with",
                            "using",
                            "by",
                            "for",
                            "of",
                            "to",
                            "in",
                            "on",
                            "at",
                            "that",
                            "which",
                        ):
                            break
                        obj_phrase.append(token.text)
                    if obj_phrase:
                        title = f"{first_token.text} {' '.join(obj_phrase)}"
                        title_set = True
            if not title_set and nlp:
                verb = ""
                words_in_line = [
                    w.strip(",.").replace("\u200b", "") for w in cleaned.split()
                ]
                if not words_in_line:
                    continue
                first_word = words_in_line[0].lower()
                if first_word in impact_words:
                    verb = words_in_line[0].capitalize()
                else:
                    for token in doc:
                        if token.text.lower() in impact_words:
                            verb = token.text.capitalize()
                            break
                if verb:
                    candidate_phrases = []
                    for chunk in doc.noun_chunks:
                        if chunk.root.pos_ == "PRON":
                            continue
                        chunk_text = chunk.text.strip()
                        chunk_text = re.sub(
                            "^(the|a|an)\\s+", "", chunk_text, flags=re.IGNORECASE
                        )
                        phrase_words = [
                            w.capitalize()
                            for w in chunk_text.split()
                            if w.lower() != verb.lower()
                        ]
                        if phrase_words:
                            candidate_phrases.append(" ".join(phrase_words))
                    if candidate_phrases:
                        generic_terms = {
                            "Activity",
                            "Project",
                            "Task",
                            "Work",
                            "Process",
                            "Initiative",
                            "Core",
                            "Role",
                            "Time",
                            "System",
                            "Systems",
                            "Team",
                            "Teams",
                            "Platform",
                            "Feature",
                            "Company",
                        }
                        best_phrase = candidate_phrases[0]
                        for phrase in candidate_phrases:
                            if len(phrase.split()) == 1 and phrase in generic_terms:
                                continue
                            if (
                                best_phrase in generic_terms
                                and phrase not in generic_terms
                            ):
                                best_phrase = phrase
                                break
                            if (
                                len(phrase.split()) > len(best_phrase.split())
                                and best_phrase in generic_terms
                            ):
                                best_phrase = phrase
                        title = f"{verb} {best_phrase}"
                        title_set = True
                    else:
                        title = f"{verb} Initiative"
                        title_set = True
                if not title_set and (
                    "co-developed" in cleaned.lower() or "developed" in cleaned.lower()
                ):
                    match = re.search(
                        "(?:co-developed|developed)\\s+([A-Z][\\w\\-]+(?:\\s+(?:(?!using|with|for|by|to|through)[A-Za-z][\\w\\-]+))*)",
                        cleaned,
                        re.IGNORECASE,
                    )
                    if match:
                        # Extract and clean the text first (f-strings can't contain backslashes)
                        cleaned_text = match.group(1).replace("\u200b", "")
                        title = f"Developed {cleaned_text}"
                        title_set = True
            filler_words = {
                "Using",
                "With",
                "And",
                "For",
                "By",
                "In",
                "To",
                "The",
                "A",
                "An",
                "Of",
                "Through",
                "At",
                "On",
                "That",
                "Which",
            }
            words = title.split()
            while words and words[-1].capitalize() in filler_words:
                words.pop()
            if len(words) <= 2 and words[0] in [
                "Led",
                "Managed",
                "Developed",
                "Built",
                "Created",
            ]:
                desc_words = [
                    w.strip(",.").replace("\u200b", "") for w in cleaned.split()
                ]
                if len(desc_words) > len(words) + 1:
                    for i in range(len(words), min(len(desc_words), 6)):
                        candidate = desc_words[i]
                        if (
                            candidate.capitalize() not in filler_words
                            and len(candidate) > 2
                        ):
                            words.append(candidate.capitalize())
                            if len(words) >= 4:
                                break
            if len(words) > 4:
                words = words[:4]
            title = " ".join(words).title()
            title_words = title.split()
            if len(title_words) >= 2 and title_words[0] == title_words[1]:
                title = " ".join(title_words[1:])
            if len(title_words) >= 4 and title_words[1] == title_words[2]:
                title_words.pop(2)
                title = " ".join(title_words)
            if "(" in title and ")" not in title:
                title = title.split("(")[0].strip()
            else:
                title = re.sub("\\([^)]*\\)", "", title).strip()
            title = title.replace(
                "Impact Highlight Impact Highlight", "Impact Highlight"
            )
            description = cleaned
            description = re.sub(
                "Page\\s+\\d+\\s+of\\s+\\d+", "", description, flags=re.IGNORECASE
            )
            tenure_patterns = [
                "\\d+\\s+(?:yr|yrs|year|years|mo|mos|month|months)(?:\\s+\\d+\\s+(?:mo|mos|month|months))?",
                "\\d{4}\\s*-\\s*\\d{4}",
                "[A-Z][a-z]+\\s*\\d{4}",
                "Present",
                "\\(.*?\\)",
            ]
            for pat in tenure_patterns:
                match = re.search(pat, description)
                if match and match.start() > 50:
                    description = description[: match.start()].strip()
            if len(description) < 80:
                continue
            if len(description) > 600:
                end_match = None
                for match in re.finditer("[.!?]\\s+[A-Z]", description[100:600]):
                    end_match = match
                if end_match:
                    description = description[: 100 + end_match.start() + 1]
                else:
                    last_space = description[:600].rfind(" ")
                    if last_space > 100:
                        description = description[:last_space] + "..."
                    else:
                        description = description[:600] + "..."
            description = description.strip()
            if not description.endswith((".", "!", "?", "...")):
                description += "."
            achievements.append({
                "title": title.strip(),
                "description": description,
                "metric": metric,
            })
            if len(achievements) >= 8:
                break
    return achievements


def extract_awards_and_honors(text: str) -> list[dict[str, str]]:
    """Extract awards and honors from LinkedIn PDF text."""
    awards = []
    lines = text.splitlines()
    awards_headers = [
        "honors-awards",
        "honors & awards",
        "awards and honors",
        "awards & honors",
        "honors and awards",
        "awards",
        "honors",
        "recognition",
        "certifications",
        "licenses & certifications",
        "licenses and certifications",
    ]
    stop_headers = [
        "experience",
        "employment",
        "education",
        "skills",
        "languages",
        "publications",
        "projects",
        "interests",
        "contact",
        "summary",
        "about",
        "recommendations",
    ]
    start_idx = -1
    end_idx = len(lines)
    for i, line in enumerate(lines):
        clean = line.strip().lower().replace(" ", "").replace("-", "")
        for header in awards_headers:
            header_clean = header.replace(" ", "").replace("-", "")
            if header_clean in clean and len(line.strip()) < 35:
                start_idx = i + 1
                break
        if start_idx > -1:
            break
    if start_idx == -1:
        return []
    for i in range(start_idx, len(lines)):
        clean_line = lines[i].strip().lower()
        if not clean_line:
            continue
        for header in stop_headers:
            if header in clean_line and len(lines[i].strip()) < 25:
                end_idx = i
                break
        if end_idx != len(lines):
            break
    award_lines = [l.strip() for l in lines[start_idx:end_idx] if l.strip()]
    award_endings = [
        "winner",
        "of the year",
        "award",
        "recognition",
        "honoree",
        "nominee",
        "prize",
        "medal",
        "fellow",
        "scholar",
        "grant",
    ]
    current_award = []
    for line in award_lines:
        current_award.append(line)
        merged = " ".join(current_award)
        if any(ending in merged.lower() for ending in award_endings):
            title = merged.replace("- ", "– ").strip()
            title = re.sub("\\s+", " ", title)
            awards.append({
                "title": title,
                "description": f"Recognized for excellence: {title}",
                "metric": "🏆 Award",
            })
            current_award = []
    if current_award:
        merged = " ".join(current_award)
        if len(merged) > 10:
            title = re.sub("\\s+", " ", merged.strip())
            awards.append({
                "title": title,
                "description": f"Recognized for excellence: {title}",
                "metric": "🏆 Award",
            })
    return awards


def parse_resume(file_path: str) -> dict[str, str | list[dict[str, str]]]:
    logger.info(f"Starting parse_resume for: {file_path}")
    raw_text = extract_text_from_pdf(file_path)
    if not raw_text:
        logger.warning("PDF extraction returned no text")
        return {}
    text_len = len(raw_text)
    logger.info(f"Successfully extracted {text_len} characters of text from PDF")
    nlp_doc = nlp(raw_text[:2000]) if nlp else None
    if not nlp_doc:
        logger.warning("spaCy NLP model was not available during parsing")
    name = extract_name(raw_text, nlp_doc)
    linkedin_url = extract_linkedin(raw_text)
    role = extract_role(raw_text, name)
    data = {
        "name": name,
        "role": role,
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "linkedin": linkedin_url,
        "location": extract_location(raw_text, nlp_doc),
        "summary": extract_summary(raw_text),
        "achievements": extract_achievements(raw_text),
        "awards": extract_awards_and_honors(raw_text),
    }
    for key, value in data.items():
        if isinstance(value, list):
            logger.info(f"Extracted {len(value)} items for key: {key}")
        else:
            status = "Found" if value else "Not Found"
            logger.info(f"Extraction for {key}: {status}")
    return data
