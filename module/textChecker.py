import re

def detect_gap(text):
    pattern = re.compile(r'gap', re.IGNORECASE)
    matches = pattern.findall(text)
    return len(matches) > 0

