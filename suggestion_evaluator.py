import random
import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

TOP_N_KEYWORDS = 10
STRONG_VERBS = ['achieved', 'led', 'managed', 'developed', 'created', 'implemented', 'spearheaded', 'orchestrated',
                'drove', 'innovated']


class SuggestionEvaluator:
    def __init__(self, spacy_nlp_model, genai_eval_model):
        self.nlp = spacy_nlp_model
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        self.eval_model = genai_eval_model

    def _preprocess_text(self, text):
        if not text:
            return ""
        doc = self.nlp(text.lower())
        tokens = [token.lemma_ for token in doc if token.is_alpha and token.text not in self.stopwords]
        return " ".join(tokens)

    def _extract_keywords_tfidf(self, text, top_n=TOP_N_KEYWORDS):
        processed_text = self._preprocess_text(text)
        if not processed_text:
            return []
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
            tfidf_matrix = vectorizer.fit_transform([processed_text])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray().flatten()
            top_indices = scores.argsort()[-top_n:][::-1]
            keywords = [feature_names[i] for i in top_indices if scores[i] > 0]
            return keywords
        except Exception as e:
            print(f"Error extracting keywords with TF-IDF: {e}")
            return []

    def generate_specific_suggestions(self, resume_text, job_desc_text, attempt=1):
        suggestions = []
        processed_resume = self._preprocess_text(resume_text)
        processed_job_desc = self._preprocess_text(job_desc_text)

        if job_desc_text:
            job_keywords = self._extract_keywords_tfidf(job_desc_text)
            resume_words = set(processed_resume.split())
            missing_keywords = [kw for kw in job_keywords if kw not in resume_words]
            if missing_keywords:
                suggestions.append(
                    f"Consider incorporating relevant keywords from the job description, such as: {', '.join(missing_keywords[:5])}.")

        try:
            doc = self.nlp(resume_text)
            weak_verb_sentences = []
            for sent in doc.sents:
                first_verbs = [token for token in sent if token.pos_ == 'VERB'][:2]
                for verb in first_verbs:
                    if verb.text.lower() not in STRONG_VERBS and verb.dep_ != 'aux':
                        sentence_preview = sent.text[:100] + ('...' if len(sent.text) > 100 else '')
                        weak_verb_sentences.append(f"'{sentence_preview}' (starts with '{verb.text}')")
                        break
            if weak_verb_sentences:
                suggestions.append(
                    f"Review sentences starting with weaker verbs ({', '.join(weak_verb_sentences[:2])}). Try stronger action verbs like: {random.choice(STRONG_VERBS)}, {random.choice(STRONG_VERBS)}.")
        except Exception as e:
            print(f"Error analyzing action verbs: {e}")

        try:
            doc = self.nlp(resume_text)
            if not any(token.like_num for token in doc):
                suggestions.append(
                    "Quantify achievements where possible. Use numbers to show impact (e.g., 'Increased sales by 15%').")
        except Exception as e:
            print(f"Error checking for quantification: {e}")

        return suggestions

    def evaluate_suggestions_with_llm(self, job_description, resume_text, suggestions):
        if not suggestions:
            return 5

        prompt = f"""
        You are an expert resume reviewer.
        Job Description:
        ---
        {job_description if job_description else "No job description provided."}
        ---
        Resume Text:
        ---
        {resume_text[:2000]}
        ---
        Generated Suggestions for Improvement:
        ---
        {suggestions}
        ---
        On a scale of 1 to 5 (1=Not helpful, 3=Somewhat helpful, 5=Very helpful and relevant), how helpful are THESE SPECIFIC SUGGESTIONS for improving the resume based on the job description?

        Provide ONLY the integer score (1, 2, 3, 4, or 5). Do not add any explanation or other text.
        """

        try:
            response = self.eval_model.generate_content(prompt)
            score_text = ''.join(filter(str.isdigit, response.text.strip()))
            if score_text:
                return max(1, min(5, int(score_text)))
            else:
                print(f"LLM did not return a clear score. Response: {response.text}")
                return 3
        except Exception as e:
            print(f"Error evaluating suggestions with LLM: {e}")
            return 3
