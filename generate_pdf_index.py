import os
import json
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
        return text.strip()
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return ""

def main():
    repo_path = "."
    files_to_index = []
    
    # Index PDFs in the root and in Files directory
    for root, dirs, files in os.walk(repo_path):
        # Skip .git directory
        if ".git" in dirs:
            dirs.remove(".git")
        
        for file in files:
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_path)
                # Normalize path for JSON (use forward slashes)
                rel_path = rel_path.replace("\\", "/")
                files_to_index.append(rel_path)

    index = {}
    for rel_path in files_to_index:
        print(f"Indexing {rel_path}...")
        full_path = os.path.join(repo_path, rel_path)
        text = extract_text_from_pdf(full_path)
        if text:
            index[rel_path] = text

    with open("pdf_index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
