import re
from transformers import PreTrainedTokenizer


class ManualSplitter:
    def __init__(self, tokenizer: PreTrainedTokenizer, max_nb_tokens: int)-> None:
        self.tokenizer = tokenizer
        self.max_nb_tokens = max_nb_tokens

    def get_number_tokens(self, input: str) -> int:
        return len(self.tokenizer(input)["input_ids"])

    def split_in_subsections(self, section: str) -> list[str]:
        regexp_subsection = r"((?:\n|^)#{3}\s.*?(?=\n#|\Z))"
        sub_sections = re.findall(regexp_subsection, section, re.DOTALL)
        return sub_sections
    
    def split_into_sentences(self, text: str) -> list[str]:
        normalized_text = text.replace("\n", " ").strip()
        if normalized_text is None or normalized_text == "":
            return []
        segments = re.split(r"([.!?])", normalized_text)
        sentences: list[str] = []
        for i in range(0, len(segments), 2):
            if i + 1 < len(segments):
                # Combine the text and delimiter
                candidate = (segments[i] + segments[i + 1]).strip()
            else:
                # If no delimiter segment, use the text directly
                candidate = segments[i].strip()
            if candidate:
                sentences.append(candidate)
        return sentences
     
    def split_fixed_length(self, subsection:str) -> list[str]:
        sentences = self.split_into_sentences(subsection)
        chunks: list[str] = []
        for sentence in sentences:
            nb_tokens_sentences = self.get_number_tokens(sentence)
            if len(chunks) == 0 or  self.get_number_tokens(chunks[-1]) + nb_tokens_sentences > self.max_nb_tokens:
                chunks.append([sentence])
            else: 
                chunks[-1] += sentence
        return chunks

        
    def split_section(self, section: str, ):
        list_subsections = self.split_in_subsections(section)
        section_splits = []
        for subsection in list_subsections:
            if self.get_number_tokens(subsection) > self.max_nb_tokens:
                subsections_splits = self.split_fixed_length(subsection)
                section_splits += subsections_splits
            else: 
                section_splits.append(subsection)
        return list_subsections

    def remove_pages_titles(self, text: str) -> str:

        regexp_page_title = r"((?:\n|^)#\sPage.*?(?=\n))"
        text =re.sub(regexp_page_title,'', text)
        return text
    
    def get_sections(self, text: str) -> list[str]:
        regexp_subsection = r"((?:\n|^)#{2}\s.*?(?=\n#{2}\s|\Z))"
        sections = re.findall(regexp_subsection, text, re.DOTALL)
        return sections 
    
    def load_file(self, path_manual: str) -> str:
        with open(path_manual) as f: 
            text = f.read()
        return text

    def split_manual(self, path_manual:str) -> list[str]:
        text = self.load_file(path_manual)
        text = self.remove_pages_titles(text)
        sections = self.get_sections(text)

        splitted_manual = []
        for section in sections: 
            nb_tokens  =  self.get_number_tokens(section)
            if nb_tokens > self.max_nb_tokens:
                splitted_section_parts = self.split_section(section)
                splitted_manual += splitted_section_parts
            else: 
                splitted_manual.append(section)

        return splitted_manual 
    