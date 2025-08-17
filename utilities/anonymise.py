import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def date_mopup(text, mode='VERBOSE'):
    pattern = r'\b\d{1,4}\s*[/.\-]\s*\d{1,4}\s*[/.\-]\s*\d{1,4}\b'
    redacted_text = text

    if re.search(pattern, redacted_text):
        redacted_text = re.sub(pattern, "[REDACTED DATE]", redacted_text)
        if mode == 'VERBOSE':
            print('Date(s) redacted...')
    
    return redacted_text



def name_mopup(text, mode='VERBOSE'):
    lines = text.splitlines()
    redacted_lines = []
    i = 0

    # Updated case-sensitive patterns
    dr_name_pattern = re.compile(
        r'\bDr\.?\s+(?:[A-Z]\.?\s*){1,2}[A-Z][a-z]+(?:[-–\s.,])?'
    )

    two_part_name_pattern = re.compile(
        r'\b[A-Z](?:\.|[a-z]+)?[\s.]?[A-Z][a-z]+\b'
    )

    descriptor_pattern = re.compile(
        r'\b(Consultant|Radiologist|Radiographer|Registrar|Sonographer|ST\d{1,2})\b'
    )

    while i < len(lines):
        line = lines[i]
        redacted_line = line

        # Redact all Dr-style names
        if dr_name_pattern.search(line):
            redacted_line = dr_name_pattern.sub("[REDACTED NAME]", redacted_line)
            if mode == 'VERBOSE':
                print(f'Line {i+1}: Dr-style name(s) redacted.')

        # Redact two-part names with valid descriptors
        two_part_matches = two_part_name_pattern.findall(redacted_line)
        if two_part_matches:
            # Look ahead to next non-empty line
            descriptor_line = ''
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines):
                descriptor_line = lines[j]

            if descriptor_pattern.search(redacted_line) or descriptor_pattern.search(descriptor_line):
                for match in two_part_matches:
                    redacted_line = redacted_line.replace(match, "[REDACTED NAME]")
                if mode == 'VERBOSE':
                    print(f'Line {i+1}: Two-part name(s) with role redacted.')

        redacted_lines.append(redacted_line)
        i += 1

    return '\n'.join(redacted_lines)


def redact_names_numbers_dates(text, mode='VERBOSE'):
    doc = nlp(text)

    redacted_text = text
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            redacted_text = redacted_text.replace(ent.text, "[REDACTED NAME]")
            if mode == 'VERBOSE':
                print('Name redacted...')
        elif ent.label_ == "DATE":
            redacted_text = redacted_text.replace(ent.text, "[REDACTED DATE]")
            if mode == 'VERBOSE':
                print('Date redacted...')
        redacted_text = date_mopup(redacted_text)
        redacted_text = name_mopup(redacted_text)
        

    reg_number_pattern = r'\d{3,20}'
    if re.search(reg_number_pattern, redacted_text):
        redacted_text = re.sub(reg_number_pattern, "[REDACTED NUMBER]", redacted_text)
        if mode == 'VERBOSE':
            print('Number(s) redacted...')



    return redacted_text
