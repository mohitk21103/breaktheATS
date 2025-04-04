import os
import re
import nltk
import spacy
import pdfplumber
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Download necessary NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


class ResumeAnalyzer:
    def __init__(self):
        self.model = SentenceTransformer('all-mpnet-base-v2')

    def parse_resume(self, file_path):
        """Parses a resume file (PDF) and returns its text content."""
        try:
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            return text
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return ""

    def preprocess_text(self, text):
        """Preprocesses text using spaCy."""
        doc = nlp(text)
        tokens = [token.lemma_.lower() for token in doc if
                  not token.is_stop and not token.is_punct and not token.is_space]
        return " ".join(tokens)

    def extract_keywords_tfidf(self, text, top_n=10):
        """Extracts keywords using TF-IDF."""
        tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        tfidf_matrix = tfidf_vectorizer.fit_transform([text])
        feature_names = tfidf_vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        top_indices = tfidf_scores.argsort()[-top_n:][::-1]
        return [(feature_names[i], tfidf_scores[i]) for i in top_indices]

    def calculate_similarity(self, resume_text, job_desc_text):
        """Calculates cosine similarity using Sentence-BERT."""
        resume_embedding = self.model.encode(resume_text)
        job_desc_embedding = self.model.encode(job_desc_text)
        return cosine_similarity([resume_embedding], [job_desc_embedding])[0][0]

    def generate_suggestions(self, resume_text, job_desc_text, similarity_threshold=0.4):
        """Generates suggestions for improving the resume."""
        suggestions = []
        job_keywords = [kw[0] for kw in self.extract_keywords_tfidf(job_desc_text, top_n=15)]
        resume_keywords = set(resume_text.split())
        missing_keywords = [kw for kw in job_keywords if kw not in resume_keywords]

        if missing_keywords:
            suggestions.append(f"Consider adding these keywords: {', '.join(missing_keywords)}")

        similarity_score = self.calculate_similarity(resume_text, job_desc_text)
        if similarity_score < similarity_threshold:
            suggestions.append(
                f"Your resume's similarity to the job description is low ({similarity_score:.2f}). Consider improving alignment.")

        return suggestions

    def analyze_resume(self, resume_path, job_desc_text):
        """Runs the full resume analysis and returns results."""
        resume_text = self.parse_resume(resume_path)
        if not resume_text:
            return {"error": "Could not extract text from resume."}

        processed_resume = self.preprocess_text(resume_text)
        processed_job_desc = self.preprocess_text(job_desc_text)
        similarity_score = self.calculate_similarity(processed_resume, processed_job_desc)
        suggestions = self.generate_suggestions(processed_resume, processed_job_desc)

        return {
            "similarity_score": round(similarity_score*100, 2),
            "suggestions": suggestions
        }
