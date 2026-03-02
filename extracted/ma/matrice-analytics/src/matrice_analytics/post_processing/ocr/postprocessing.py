import re
import logging

class TextPostprocessor:
    def __init__(self, logging_level=logging.INFO):
        """
        Initialize the text postprocessor with optional logging configuration.
        
        Args:
            logging_level: The level of logging detail. Default is INFO.
        """
        self.logger = logging.getLogger('TextPostprocessor')
        
        self.task_processors = {
            "license_plate": self._process_license_plate,
            "license_plate_india": self._process_license_plate_india,
            "license_plate_us": self._process_license_plate_us,
            "license_plate_eu": self._process_license_plate_eu,
            "license_plate_qatar": self._process_license_plate_qatar,
        }
        
        self.char_substitutions = {
            'O': '0',
            'o': '0',
            'I': '1',
            'Z': '2',
            'A': '4',
            'L': '1',
            'AV': 'AV',
            'S': '5',
            'B': '8',
            'D': '0',
            'Q': '0',
            'G': '6',
            'T': '7'
        }

    def postprocess(self, texts, confidences, task=None, confidence_threshold=0.25, cleanup=True, region=None):
        """
        Postprocesses the extracted text by cleaning and filtering low-confidence results.
        Applies task-specific processing if a task is specified.
        
        Args:
            texts (list): List of extracted text strings.
            confidences (list): List of confidence scores corresponding to each text.
            task (str): Specific task for customized postprocessing. Default is None.
            confidence_threshold (float): Minimum confidence required to keep the text. Default is 0.5.
            cleanup (bool): Whether to perform text cleanup.
            region (str): Specific region for license plate processing ('india', 'us', 'eu', 'qatar'). Default is None.
            
        Returns:
            list: List of processed texts with corresponding confidence scores and validity flags.
        """
        results = []
        
        for text, confidence in zip(texts, confidences):
            if confidence < confidence_threshold:
                self.logger.debug(f"Text '{text}' rejected: confidence {confidence} below threshold {confidence_threshold}")
                results.append((None, confidence, False))
                continue
            
            if cleanup:
                processed_text = self._clean_text(text)
            else:
                processed_text = text
            
            if task and processed_text:
                if task == "license_plate" and region:
                    region_task = f"license_plate_{region.lower()}"
                    if region_task in self.task_processors:
                        processed_text = self.task_processors[region_task](processed_text)
                    else:
                        processed_text = self.task_processors["license_plate"](processed_text)
                        self.logger.warning(f"Region '{region}' not supported, using generic license plate processor")
                elif task in self.task_processors:
                    processed_text = self.task_processors[task](processed_text)
                else:
                    self.logger.warning(f"Task '{task}' not supported, skipping task-specific processing")
            
            if processed_text:
                self.logger.debug(f"Text processed successfully: '{text}' -> '{processed_text}'")
                results.append((processed_text, confidence, True))
            else:
                self.logger.debug(f"Text '{text}' rejected during processing")
                results.append((None, confidence, False))
        
        return results
    
    def _clean_text(self, text):
        """
        Basic text cleaning operations.
        
        Args:
            text (str): Text to clean.
            
        Returns:
            str: Cleaned text.
        """
        clean_text = text.strip()
        clean_text = ''.join(char for char in clean_text if char.isprintable())
        clean_text = ' '.join(clean_text.split())
        
        return clean_text
    
    def _process_license_plate(self, text):
        """
        Generic license plate processor that respects the specified region.
        
        Args:
            text (str): License plate text to process.
            
        Returns:
            str: Processed license plate text or None if invalid.
        """
        plate_text = text.upper()
        plate_text = ''.join(plate_text.split())
        
        if self.region and self.region.lower() == 'qatar':
            return self._process_license_plate_qatar(plate_text)
        elif self.region and self.region.lower() == 'india':
            return self._process_license_plate_india(plate_text)
        elif self.region and self.region.lower() == 'us':
            return self._process_license_plate_us(plate_text)
        elif self.region and self.region.lower() == 'eu':
            return self._process_license_plate_eu(plate_text)
        else:
            if re.match(r'^[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{4}$', plate_text):
                return self._process_license_plate_india(plate_text)
            elif re.match(r'^[A-Z0-9]{1,8}$', plate_text) and len(plate_text) <= 8:
                return self._process_license_plate_us(plate_text)
            elif re.match(r'^[A-Z]{1,3}[-\s]?[A-Z0-9]{1,4}[-\s]?[A-Z0-9]{1,3}$', plate_text):
                return self._process_license_plate_eu(plate_text)
            elif re.match(r'^\d{1,6}\s*[A-Z]+?$', plate_text):
                return self._process_license_plate_qatar(plate_text)
            else:
                plate_text = ''.join(char for char in plate_text if char.isalnum())
                if 4 <= len(plate_text) <= 10:
                    return plate_text
        
        self.logger.warning(f"Could not identify license plate format: '{text}'")
        return None
    
    def _process_license_plate_india(self, text):
        plate_text = text.upper().replace(" ", "")
        plate_text = ''.join(char for char in plate_text if char.isalnum())
        for old, new in self.char_substitutions.items():
            plate_text = plate_text.replace(old, new)
        
        if len(plate_text) >= 7:
            state_code = plate_text[:2]
            rest = plate_text[2:]
            match = re.match(r'^(\d{1,2})[ -]?([A-Z]{1,2})[ -]?(\d{4})$', rest)
            if match and state_code in ['AN', 'AP', 'AR', 'AS', 'BR', 'CH', 'CG', 'DD', 'DL', 'GA', 'GJ', 'HP', 'HR', 'JH', 'JK', 'KA', 'KL', 'LA', 'LD', 'MH', 'ML', 'MN', 'MP', 'MZ', 'NL', 'OD', 'PB', 'PY', 'RJ', 'SK', 'TN', 'TR', 'TG', 'TS', 'UK', 'UP', 'WB']:
                district, series, number = match.groups()
                formatted_plate = f"{state_code}{district}{series}{number}"
                self.logger.info(f"Processed Indian license plate: '{text}' -> '{formatted_plate}'")
                return formatted_plate
        self.logger.warning(f"Invalid Indian license plate format: '{text}'")
        return None

    def _process_license_plate_us(self, text):
        plate_text = text.upper()
        plate_text = ''.join(char for char in plate_text if char.isalnum())
        
        for old, new in self.char_substitutions.items():
            plate_text = plate_text.replace(old, new)
        
        if re.match(r'^[A-Z]{3}\d{4}$', plate_text) or re.match(r'^\d{3}[A-Z]{4}$', plate_text):
            self.logger.info(f"Processed US license plate (standard format): '{text}' -> '{plate_text}'")
            return plate_text
        if 2 <= len(plate_text) <= 8 and re.match(r'^[A-Z0-9]+$', plate_text):
            self.logger.info(f"Processed US license plate (vanity/other format): '{text}' -> '{plate_text}'")
            return plate_text
        
        self.logger.warning(f"Invalid US license plate format: '{text}'")
        return None

    def _process_license_plate_eu(self, text):
        plate_text = text.upper()
        plate_text = ''.join(char for char in plate_text if char.isalnum() or char == '-')
        
        if '-' not in plate_text and len(plate_text) > 3:
            for i in range(1, 4):
                if i < len(plate_text) and plate_text[i].isdigit() and plate_text[i-1].isalpha():
                    plate_text = plate_text[:i] + '-' + plate_text[i:]
                    break
        
        for old, new in self.char_substitutions.items():
            plate_text = plate_text.replace(old, new)
        
        if re.match(r'^[A-Z]{1,3}-[A-Z]{1,2}\d{1,4}$', plate_text):
            self.logger.info(f"Processed German license plate: '{text}' -> '{plate_text}'")
            return plate_text
        if re.match(r'^[A-Z]{2}\d{2}[A-Z]{3}$', plate_text):
            self.logger.info(f"Processed UK license plate: '{text}' -> '{plate_text}'")
            return plate_text
        if re.match(r'^[A-Z]{2}-\d{3}-[A-Z]{2}$', plate_text) or re.match(r'^\d{4}[A-Z]{3}$', plate_text):
            self.logger.info(f"Processed French license plate: '{text}' -> '{plate_text}'")
            return plate_text
        if re.match(r'^[A-Z]{2}\d{3}[A-Z]{2}$', plate_text):
            self.logger.info(f"Processed Italian license plate: '{text}' -> '{plate_text}'")
            return plate_text
        if re.match(r'^\d{4}[BCDFGHJKLMNPRSTVWXYZ]{3}$', plate_text):
            self.logger.info(f"Processed Spanish license plate: '{text}' -> '{plate_text}'")
            return plate_text
        if re.search(r'[A-Z]', plate_text) and re.search(r'\d', plate_text) and 4 <= len(plate_text) <= 10:
            self.logger.info(f"Processed generic European license plate: '{text}' -> '{plate_text}'")
            return plate_text
        
        self.logger.warning(f"Invalid European license plate format: '{text}'")
        return None
    
    def _process_license_plate_qatar(self, text):
        """
        Process Qatar license plate text by converting Arabic numerals to Latin and keeping only digits.
        
        Args:
            text (str): License plate text to process.
            
        Returns:
            str: Processed license plate text or None if invalid.
        """
        # Check for Unicode escape sequences (e.g., \u0664)
        if r'\u' in str(text):
            self.logger.warning(f"Invalid Qatar license plate format: '{text}' contains Unicode escape sequence")
            return None

        # Define Arabic to Latin numeral mapping
        arabic_to_latin = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
        
        # Convert Arabic numerals to Latin and keep only alphanumeric characters
        plate_text = text.translate(arabic_to_latin)
        plate_text = ''.join(char for char in plate_text if char.isalnum())
        
        # Apply character substitutions for common OCR errors
        for old, new in self.char_substitutions.items():
            plate_text = plate_text.replace(old, new)
        
        # Keep only digits for Qatar license plates
        plate_text = ''.join(char for char in plate_text if char.isdigit())
        
        # Validate: Ensure the text is 1 to 6 digits
        if re.match(r'^\d{1,6}$', plate_text):
            self.logger.info(f"Processed Qatar license plate: '{text}' -> '{plate_text}'")
            return plate_text
        
        self.logger.warning(f"Invalid Qatar license plate format: '{text}'")
        return None
    
    def _string_similarity(self, s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        
        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2+1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        
        max_len = max(len(s1), len(s2))
        similarity = 1 - (distances[-1] / max_len if max_len > 0 else 0)
        return similarity
    
    def add_task_processor(self, task_name, processor_function):
        self.task_processors[task_name] = processor_function
        self.logger.info(f"Added new task processor: {task_name}")