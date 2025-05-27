import re

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    # Remove special characters (keep alphanumerics and basic punctuation)
    text = re.sub(r'[^a-zA-Z0-9\s.,]', '', text)

    # Remove multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    # Trim leading and trailing whitespaces
    text = text.strip()

    # Remove extra whitespaces again (optional double check)
    text = ' '.join(text.split())

    return text