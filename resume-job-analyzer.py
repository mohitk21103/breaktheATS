import os
import re
import nltk
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# import textractparser as textract
# import textract  # For handling various document formats

import pdfplumber


# Download required NLTK resources (only needed once)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# Load spaCy model (you can choose a different size: en_core_web_sm, en_core_web_md, en_core_web_lg)
nlp = spacy.load("en_core_web_sm")

# --- Helper Functions ---

def parse_resume(file_path):
    """Parses a resume file (PDF, DOCX, TXT) and returns its text content."""
    try:
        # text = textract.process(file_path).decode('utf-8')
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        return text
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return ""  # Return empty string on error

def preprocess_text(text, nlp):
    """Preprocesses text using spaCy."""
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    return " ".join(tokens)

def extract_keywords_tfidf(text, top_n=10):
    """Extracts keywords using TF-IDF."""
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = tfidf_vectorizer.fit_transform([text])
    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    top_indices = tfidf_scores.argsort()[-top_n:][::-1]
    top_keywords = [(feature_names[i], tfidf_scores[i]) for i in top_indices]
    return top_keywords

def calculate_similarity_sentence_bert(resume_text, job_desc_text):
    """Calculates cosine similarity using Sentence-BERT."""
    model = SentenceTransformer('all-mpnet-base-v2')  # Or another suitable model
    resume_embedding = model.encode(resume_text)
    job_desc_embedding = model.encode(job_desc_text)
    similarity_score = cosine_similarity([resume_embedding], [job_desc_embedding])[0][0]
    return similarity_score

def generate_suggestions(resume_text, job_desc_text, nlp, similarity_threshold=0.4):
    """Generates suggestions for improving the resume based on the job description."""
    suggestions = []

    # 1. Keyword Gap Analysis
    job_keywords = [kw[0] for kw in extract_keywords_tfidf(job_desc_text, top_n=15)]
    resume_keywords = set(resume_text.split())
    missing_keywords = [kw for kw in job_keywords if kw not in resume_keywords]
    if missing_keywords:
        suggestions.append(f"Consider adding these keywords (if applicable): {', '.join(missing_keywords)}")

    # 2. Similarity Threshold
    similarity_score = calculate_similarity_sentence_bert(resume_text, job_desc_text)
    if similarity_score < similarity_threshold:
        suggestions.append(f"Your resume's similarity to the job description is low ({similarity_score:.2f}). Consider rephrasing to better match the required skills and experience.")

    # 3. Action Verbs (spaCy POS tagging)
    doc = nlp(resume_text)
    weak_verbs = ['did', 'made', 'helped', 'worked', 'was', 'had']
    for sent in doc.sents:
        if sent[0].pos_ == 'VERB' and sent[0].text.lower() in weak_verbs:
            suggestions.append(f"Consider using a stronger action verb at the beginning of this sentence: '{sent.text}'")

    # 4. Quantification
    if not any(token.like_num for token in doc):
        suggestions.append("Try to quantify your accomplishments with numbers and metrics (e.g., 'Increased sales by 15%').")

    return suggestions

# --- Main Application Logic ---

def main():
    print("Resume Analyzer")
    print("---------------")

    # 1. Get Resume Input
    while True:
        resume_path = input("Enter the path to your resume file (PDF, DOCX, or TXT), or type 'quit' to exit: ")
        if resume_path.lower() == 'quit':
            return  # Exit the program

        if not os.path.exists(resume_path):
            print("Error: File not found. Please enter a valid file path.")
            continue

        resume_text = parse_resume(resume_path)
        if not resume_text:
            print("Error: Could not extract text from the resume.  Please check the file format.")
            continue

        break  # Exit the input loop if parsing was successful

    # 2. Get Job Description Input
    print("\nPlease paste the job description text below (press Ctrl+D or Ctrl+Z then Enter to finish):\n")
    job_desc_lines = []
    while True:
        try:
            line = input()
            job_desc_lines.append(line)
        except EOFError:
            break
    job_desc_text = "\n".join(job_desc_lines)

    # 3. Preprocess the Text
    processed_resume = preprocess_text(resume_text, nlp)
    processed_job_desc = preprocess_text(job_desc_text, nlp)

    # 4. Calculate Similarity
    similarity_score = calculate_similarity_sentence_bert(processed_resume, processed_job_desc)
    print(f"\nSimilarity Score (Sentence-BERT): {similarity_score:.4f}")

    # 5. Generate Suggestions
    suggestions = generate_suggestions(processed_resume, processed_job_desc, nlp)
    print("\nSuggestions for Improvement:")
    if suggestions:
        for suggestion in suggestions:
            print(f"- {suggestion}")
    else:
        print("- No specific suggestions. Your resume appears to be a good match for this job description.")

    print("\nAnalysis Complete.")

if __name__ == "__main__":
    main()

