import pickle
import re
import nltk

# nltk.download('punkt')
# nltk.download('stopwords')

# Load the model and vectorizer
clf = pickle.load(open('model.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))


class ResumeCategory:
    def __init__(self):
        self.category_mapping = {
            6: 'Data Science',
            12: 'HR',
            0: 'Advocate',
            1: 'Arts',
            24: 'Web Designing',
            16: 'Mechanical Engineer',
            22: 'Sales',
            14: 'Health and fitness',
            5: 'Civil Engineer',
            15: 'Java Developer',
            4: 'Business Analyst',
            21: 'SAP Developer',
            2: 'Automation Testing',
            11: 'Electrical Engineering',
            18: 'Operations Manager',
            20: 'Python Developer',
            8: 'DevOps Engineer',
            17: 'Network Security Engineer',
            19: 'PMO',
            7: 'Database',
            13: 'Hadoop',
            10: 'ETL Developer',
            9: 'DotNet Developer',
            3: 'Blockchain',
            23: 'Testing'
        }

    def clean_resume(self, txt):
        clean_text = re.sub('http\S+\s', ' ', txt)
        clean_text = re.sub('RT|cc', ' ', clean_text)
        clean_text = re.sub('#\S+\s', ' ', clean_text)
        clean_text = re.sub('@\S+', '  ', clean_text)
        clean_text = re.sub(r'[^\w\s]', ' ', clean_text)
        clean_text = re.sub(r'[^\x00-\x7f]', ' ', clean_text)
        clean_text = re.sub('\s+', ' ', clean_text).strip()
        return clean_text

    def predict_category(self, resume_text):
        cleaned_resume = self.clean_resume(resume_text)
        transformed_text = tfidf.transform([cleaned_resume])
        prediction_id = clf.predict(transformed_text)[0]
        return self.category_mapping.get(prediction_id, "Unknown")