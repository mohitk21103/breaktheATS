
# beat_the_ATS

## Overview

The Smart Resume Analyzer is a Python-based tool designed to help job applicants optimize their resumes for specific job descriptions. It leverages Natural Language Processing (NLP) techniques to analyze resume content, identify key skills and keywords, and provide actionable suggestions for improvement. This tool aims to bridge the gap between a candidate's qualifications and the specific requirements of a job, increasing the likelihood of passing initial Applicant Tracking System (ATS) screening and ultimately improving job search effectiveness.

## Features

* **Resume Parsing:** Extracts text content from resume files (currently supports PDF format).
* **Text Preprocessing:** Cleans and normalizes text from both the resume and the job description to ensure accurate analysis.
* **Keyword Extraction:** Employs TF-IDF (Term Frequency-Inverse Document Frequency) to identify the most relevant keywords within the job description.
* **Semantic Similarity Analysis:** Utilizes Sentence-BERT embeddings to calculate the semantic similarity between the resume and the job description, capturing the underlying meaning of the text.
* **Suggestion Generation:** Provides targeted suggestions for resume improvement, including:
    * Identifying missing keywords and skills.
    * Assessing overall resume-job description alignment.
    * Recommending stronger action verbs.
    * Encouraging the quantification of achievements.
* **Similarity Scoring:** Quantifies the similarity between the resume and the job description, providing a numerical score for easy interpretation.

## Technologies Used

* Python
* NLTK
* spaCy
* Gemini API
* Sentence Transformers
* scikit-learn (for TF-IDF and cosine similarity)
* pdfplumber
* Flask
* React.js

## Installation

1.  **Prerequisites:**
    * Python 3.9 and above
    * pip (Python package installer)

2.  **Installation Steps:**
    * Clone the repository: `git clone https://github.com/arvinder004/breaktheATS`
    * Navigate to the project directory: `cd breaktheATS`
    * Install the required Python packages: `pip install -r requirements.txt`
    * Download the necessary NLTK data:
        ```python
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        ```
    * Download the spaCy English language model: `python -m spacy download en_core_web_sm`

## Usage

1.  **Command-Line Interface (CLI):**
    * Run the main script: `python main.py`
    * Follow the prompts to enter the resume file path and paste the job description.

2.  **Web Application (If applicable):**
    * Start the Flask backend: `python app.py`
    * Open the React frontend in your web browser (usually `http://localhost:3000`).
    * Upload your resume file and paste the job description.
    * Click the "Analyze" button to view the results.


## Team

Arvinder Singh Dhoul

* Email: asdhoul004@gmail.com
* LinkedIn: [linkedin.com/in/arvinder004](https://www.linkedin.com/in/arvinder004)
* GitHub: [github.com/arvinder004](https://github.com/arvinder004)
* Portfolio: [arvinder-portfolio.netlify.app/](https://arvinder-portfolio.netlify.app/)

Mohit Kanojiya

* Email: mohitk21103@gmail.com
* LinkedIn: [https://www.linkedin.com/in/mohit-kanojiya](https://www.linkedin.com/in/mohit-kanojiya)
* GitHub: [github.com/mohitk21103](https://github.com/mohitk21103)

Burhanuddin Saifee

* Email: burhansaifee2003@gmail.com
* LinkedIn: [https://www.linkedin.com/in/burhanuddin-saifee-6aa15b255](https://www.linkedin.com/in/burhanuddin-saifee-6aa15b255)
* GitHub: [https://github.com/burhansaifee](https://github.com/burhansaifee)


## License

MIT License

Copyright (c) 2025 Arvinder Singh Dhoul