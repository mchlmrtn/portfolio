import json
import re
from collections import Counter

# Common "useless" words (Stop words)
STOP_WORDS = {
    'the', 'with', 'and', 'for', 'that', 'this', 'from', 'your', 'will', 'have',
    'been', 'were', 'also', 'they', 'their', 'which', 'what', 'when', 'where',
    'who', 'how', 'than', 'then', 'them', 'there', 'some', 'such', 'into',
    'over', 'under', 'each', 'more', 'most', 'very', 'only', 'both', 'each',
    'other', 'another', 'could', 'would', 'should', 'about', 'above', 'below',
    'after', 'before', 'being', 'between', 'during', 'through', 'under',
    'without', 'within', 'can', 'may', 'must', 'many', 'much', 'well', 'etc',
    'also', 'used', 'using', 'study', 'work', 'data', 'information', 'report',
    'project', 'module', 'brief', 'coursework', 'academic', 'portfolio',
    'introduction', 'final', 'individual', 'group', 'year', 'level', 'based',
    'including', 'including', 'management', 'analysis', 'business', 'process',
    'system', 'result', 'results', 'different', 'various', 'provided', 'further',
    'however', 'therefore', 'although', 'even', 'while', 'since', 'because'
}

def clean_text(text):
    # Remove non-alphabetic characters and lower case
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = text.split()
    # Filter out short words and stop words
    return [w for w in words if len(w) > 3 and w not in STOP_WORDS]

def generate():
    try:
        with open('pdf_index.json', 'r') as f:
            pdf_data = json.load(f)
    except FileNotFoundError:
        print("pdf_index.json not found.")
        return

    word_map = {} # word -> list of file paths
    all_words = []

    for path, text in pdf_data.items():
        cleaned = clean_text(text)
        unique_words_in_file = set(cleaned)
        all_words.extend(cleaned)
        
        for word in unique_words_in_file:
            if word not in word_map:
                word_map[word] = []
            word_map[word].append(path)

    # Get word counts for sizing
    counts = Counter(all_words)
    
    # Take the top 100 most frequent words for the cloud
    top_words = counts.most_common(100)
    
    result = []
    for word, count in top_words:
        result.append({
            "word": word,
            "count": count,
            "files": word_map[word]
        })

    with open('word_cloud_data.json', 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Generated word_cloud_data.json with {len(result)} words.")

if __name__ == "__main__":
    generate()
