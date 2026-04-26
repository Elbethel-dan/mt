import re
import unicodedata
from pathlib import Path


# ==========================================================
# 1. Amharic Character Normalization
# ==========================================================

def normalize_amharic_characters(text):
    if not isinstance(text, str):
        return text
    
    text = re.sub('[ሃኅኃሐሓኻ]', 'ሀ', text)
    text = re.sub('[ሑኁዅ]', 'ሁ', text)
    text = re.sub('[ኂሒኺ]', 'ሂ', text)
    text = re.sub('[ኌሔዄ]', 'ሄ', text)
    text = re.sub('[ሕኅ]', 'ህ', text)
    text = re.sub('[ኆሖኾ]', 'ሆ', text)
    text = re.sub('[ሠ]', 'ሰ', text)
    text = re.sub('[ሡ]', 'ሱ', text)
    text = re.sub('[ሢ]', 'ሲ', text)
    text = re.sub('[ሣ]', 'ሳ', text)
    text = re.sub('[ሤ]', 'ሴ', text)
    text = re.sub('[ሥ]', 'ስ', text)
    text = re.sub('[ሦ]', 'ሶ', text)
    text = re.sub('[ዓኣዐ]', 'አ', text)
    text = re.sub('[ዑ]', 'ኡ', text)
    text = re.sub('[ዒ]', 'ኢ', text)
    text = re.sub('[ዔ]', 'ኤ', text)
    text = re.sub('[ዕ]', 'እ', text)
    text = re.sub('[ዖ]', 'ኦ', text)
    text = re.sub('[ጸ]', 'ፀ', text)
    text = re.sub('[ጹ]', 'ፁ', text)
    text = re.sub('[ጺ]', 'ፂ', text)
    text = re.sub('[ጻ]', 'ፃ', text)
    text = re.sub('[ጼ]', 'ፄ', text)
    text = re.sub('[ጽ]', 'ፅ', text)
    text = re.sub('[ጾ]', 'ፆ', text)
    text = re.sub('(ሉ[ዋአ])', 'ሏ', text)
    text = re.sub('(ሙ[ዋአ])', 'ሟ', text)
    text = re.sub('(ቱ[ዋአ])', 'ቷ', text)
    text = re.sub('(ሩ[ዋአ])', 'ሯ', text)
    text = re.sub('(ሱ[ዋአ])', 'ሷ', text)
    text = re.sub('(ሹ[ዋአ])', 'ሿ', text)
    text = re.sub('(ቁ[ዋአ])', 'ቋ', text)
    text = re.sub('(ቡ[ዋአ])', 'ቧ', text)
    text = re.sub('(ቹ[ዋአ])', 'ቿ', text)
    text = re.sub('(ሁ[ዋአ])', 'ኋ', text)
    text = re.sub('(ኑ[ዋአ])', 'ኗ', text)
    text = re.sub('(ኙ[ዋአ])', 'ኟ', text)
    text = re.sub('(ኩ[ዋአ])', 'ኳ', text)
    text = re.sub('(ዙ[ዋአ])', 'ዟ', text)
    text = re.sub('(ጉ[ዋአ])', 'ጓ', text)
    text = re.sub('(ደ[ዋአ])', 'ዷ', text)
    text = re.sub('(ጡ[ዋአ])', 'ጧ', text)
    text = re.sub('(ጩ[ዋአ])', 'ጯ', text)
    text = re.sub('(ጹ[ዋአ])', 'ጿ', text)
    text = re.sub('(ፉ[ዋአ])', 'ፏ', text)
    text = re.sub('[ቊ]', 'ቁ', text)  
    text = re.sub('[ኵ]', 'ኩ', text)  

    return text

# ==================================================
# 2. Amharic Number to Arabic Number Conversion
# ==================================================

def amharic_to_arabic_number(amharic_string):
    
    amharic_values = {
        '፩': 1, '፪': 2, '፫': 3, '፬': 4, '፭': 5,
        '፮': 6, '፯': 7, '፰': 8, '፱': 9,
        '፲': 10, '፳': 20, '፴': 30, '፵': 40, '፶': 50,
        '፷': 60, '፸': 70, '፹': 80, '፺': 90,
        '፻': 100, '፼': 10000
    }
    
    def parse_number_sequence(seq):
        """Parse a sequence of digits and tens (without ፻ or ፼) into a number"""
        total = 0
        current = 0
        
        for ch in seq:
            val = amharic_values[ch]
            if val >= 10:  # Tens digit
                if current != 0 and current < 10:
                    total += current
                    current = val
                else:
                    if current != 0:
                        total += current
                    current = val
            else:  # Units (1-9)
                if current >= 10:
                    total += current
                    current = val
                else:
                    current += val
        
        total += current
        return total
    
    total = 0
    current_number = 0
    temp_number = ""
    i = 0
    length = len(amharic_string)
    
    while i < length:
        ch = amharic_string[i]
        
        if ch == '፼':  # 10000 multiplier
            if temp_number:
                current_number = parse_number_sequence(temp_number)
                temp_number = ""
            if current_number == 0:
                current_number = 1
            total = (total + current_number) * 10000
            current_number = 0
            i += 1
        elif ch == '፻':  # 100 multiplier
            if temp_number:
                current_number = parse_number_sequence(temp_number)
                temp_number = ""
            if current_number == 0:
                current_number = 1
            total += current_number * 100
            current_number = 0
            i += 1
        else:
            temp_number += ch
            i += 1
    
    if temp_number:
        total += parse_number_sequence(temp_number)
    elif current_number != 0:
        total += current_number
    
    return total


def amharic_to_arabic_in_text(text):
    if not isinstance(text, str):
        return text

    pattern = r'[፩-፺፻፼]+'
    return re.sub(pattern, lambda m: str(amharic_to_arabic_number(m.group())), text)


# ==================================================
# 3. Remove Emojis
# ==================================================

def remove_emoji(text):
    
    # Pattern to match emojis (comprehensive Unicode emoji range)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map symbols
        "\U0001F700-\U0001F77F"  # Alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric shapes
        "\U0001F800-\U0001F8FF"  # Supplemental arrows
        "\U0001F900-\U0001F9FF"  # Supplemental symbols
        "\U0001FA00-\U0001FA6F"  # Chess symbols
        "\U0001FA70-\U0001FAFF"  # Extended symbols
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "]+",
        flags=re.UNICODE
    )
    
    return emoji_pattern.sub('', text)


# ==================================================
# 4. Remove Email Addresses
# ==================================================

def remove_email(text):
    
    # Comprehensive email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Substitute emails with empty string
    return re.sub(email_pattern, '', text)


# ==================================================
# 5. Remove URLs
# ==================================================

def remove_url(text):
    
    # Comprehensive URL regex pattern
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*\b'
    
    return re.sub(url_pattern, '', text)

# ==================================================
# 6. Remove Phone Numbers
# ==================================================

def remove_phone_numbers(text):
   
    # Pattern that matches phone numbers with or without parentheses
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9})'
    
    # Remove the phone number
    result = re.sub(phone_pattern, '', text)
    
    # Clean up orphaned parentheses
    result = re.sub(r'\(\s*\)', '', result) 
    result = re.sub(r'\(\s+', '(', result)  
    result = re.sub(r'\s+\)', ')', result)   
    
    # Remove leading/trailing spaces and extra spaces
    result = re.sub(r'\s+', ' ', result).strip()
    
    # Remove orphaned opening or closing parentheses
    result = re.sub(r'^\s*\(\s*', '', result)
    result = re.sub(r'\s*\)\s*$', '', result)
    
    return result


# ==================================================
# 7. Special Character Removal
# ==================================================

def remove_special_characters(text):
   
    if not isinstance(text, str):
        return text
    
    # Keep: letters, numbers, spaces, Amharic characters, and common punctuation
    pattern = r'[^\w\s\u1200-\u137F\.\,\!\?\:\;\"\'\-\(\)\[\]\{\}]'
    
    return re.sub(pattern, '', text)


# ==================================================
# 8. Normalize Punctuations
# ==================================================

def normalize_quotes(text):

    if not isinstance(text, str):
        return text
    
    # Convert all double quote variants to standard straight double quote
    double_quotes = ['"', '"', '"', '"', '"', '«', '»', '″']
    for quote in double_quotes:
        text = text.replace(quote, '"')
    
    # Convert all single quote variants to standard straight single quote
    single_quotes = [''', ''', ''', ''', '′', '‘', '’']
    for quote in single_quotes:
        text = text.replace(quote, "'")
    
    return text


def normalize_punctuation(text):
    
    if not isinstance(text, str):
        return text
    
    # First normalize quotes
    text = normalize_quotes(text)
    
    # Then normalize other punctuation
    text = re.sub(r'!{2,}', '!', text)       
    text = re.sub(r'\?{2,}', '?', text)      # multiple question marks -> single
    text = re.sub(r'\.{2,}', '.', text)      # multiple dots -> single dot

    return text

# =========================================================    
# 9. Remove Non-English and Non-Amharic sentences
# =========================================================

def is_pure_amharic(text, threshold=0.9):
    if not isinstance(text, str):
        return False

    words = re.findall(r"[\u1200-\u137F]+", text)
    if not words:
        return False

    valid = len(words)
    return (valid / len(words)) >= threshold

   

def is_pure_english(text, threshold=0.9):
    if not isinstance(text, str):
        return False

    words = re.findall(r"[A-Za-z]+", text)
    if not words:
        return False

    valid = sum(1 for w in words if re.fullmatch(r"[A-Za-z]+", w))
    return (valid / len(words)) >= threshold




# ==================================================
# 10. Unicode Normalization and Accent Removal
# ==================================================

def remove_accents(text):
    
    if not text:
        return text
    
    # Decompose to base characters + combining diacritics
    decomposed = unicodedata.normalize('NFD', text)
    
    # Filter out combining diacritical marks (category 'Mn')
    without_accents = ''.join(
        char for char in decomposed
        if unicodedata.category(char) != 'Mn'
    )
    
    # Return in NFC form (optional but good practice)
    return unicodedata.normalize('NFC', without_accents)


# ==================================================
# 11. Remove Extra Whitespace
# ==================================================

def remove_extra_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()


def clean_line(line: str) -> str:
    """Normalize spaces and strip."""
    line = line.strip()
    line = re.sub(r'\s+', ' ', line)
    return line


def normalize_pair(en, am):
    """
    Normalize both sides for consistent deduplication.
    """
    en = re.sub(r'\s+', ' ', en.strip().lower())
    am = re.sub(r'\s+', ' ', am.strip())
    return en, am

# =========================================================
# 12. Pipeline for Cleaning Text
# =========================================================

def clean_amharic_text(text):
    
    if not isinstance(text, str):
        return text
    
    result = text
    result = amharic_to_arabic_in_text(result)  
    result = normalize_amharic_characters(result)  
    result = remove_emoji(result)
    result = remove_email(result)
    result = remove_url(result)
    result = remove_phone_numbers(result)
    result = remove_special_characters(result)
    result = normalize_punctuation(result)
    result = remove_extra_whitespace(result)
    result = clean_line(result)
    return result


def clean_english_text(text):
   
    if not isinstance(text, str):
        return text
    
    result = text
    result = remove_accents(result)  # Remove accents from English
    result = remove_emoji(result)
    result = remove_email(result)
    result = remove_url(result)
    result = remove_phone_numbers(result)
    result = remove_special_characters(result)
    result = normalize_punctuation(result)
    result = remove_extra_whitespace(result)
    result = clean_line(result)
    
    return result


# ============================================================
# 14. FULL PREPROCESSING PIPELINE
# ============================================================

def preprocess_parallel_files(
    src_path,
    tgt_path,
    src_out,
    tgt_out,
    max_words=80,
    min_words=3
):

    Path(src_out).parent.mkdir(parents=True, exist_ok=True)

    total, kept = 0, 0

    # 🔥 stores FULL PAIRS only
    seen_pairs = set()

    with open(src_path, 'r', encoding='utf-8') as f_src, \
         open(tgt_path, 'r', encoding='utf-8') as f_tgt, \
         open(src_out, 'w', encoding='utf-8') as o_src, \
         open(tgt_out, 'w', encoding='utf-8') as o_tgt:

        for en_line, am_line in zip(f_src, f_tgt):
            total += 1

            # STEP 1: CLEAN
            en = clean_english_text(en_line.strip())
            am = clean_amharic_text(am_line.strip())

            # STEP 2: FILTER LANGUAGE QUALITY
            if not is_pure_english(en):
                continue
            if not is_pure_amharic(am):
                continue

            # STEP 3: LENGTH FILTER
            en_len = len(en.split())
            am_len = len(am.split())

            if en_len < min_words or am_len < min_words:
                continue
            if en_len > max_words or am_len > max_words:
                continue

            # STEP 4: PAIR NORMALIZATION (CRITICAL)
            en_norm, am_norm = normalize_pair(en, am)

            # single key representing BOTH files together
            pair_key = (en_norm, am_norm)

            # STEP 5: DROP DUPLICATE PAIR
            if pair_key in seen_pairs:
                continue

            seen_pairs.add(pair_key)

            # STEP 6: WRITE BOTH FILES TOGETHER
            o_src.write(en + '\n')
            o_tgt.write(am + '\n')

            kept += 1

    print("=" * 60)
    print("Preprocessing Completed")
    print(f"Total pairs: {total}")
    print(f"Kept pairs : {kept}")
    print(f"Removed    : {total - kept}")
    print("=" * 60)


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    
    src_file = "/Users/elbethelzewdie/Downloads/Telegram Lite/el-workspace/el-workspace/data/raw/English.en"
    tgt_file = "/Users/elbethelzewdie/Downloads/Telegram Lite/el-workspace/el-workspace/data/raw/Amharic.am"

    src_out = "/Users/elbethelzewdie/Downloads/Telegram Lite/el-workspace/el-workspace/data/processed/cleaned.en"
    tgt_out = "/Users/elbethelzewdie/Downloads/Telegram Lite/el-workspace/el-workspace/data/processed/cleaned.am"

    preprocess_parallel_files(
        src_file,
        tgt_file,
        src_out,
        tgt_out
    )