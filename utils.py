import docx2txt, PyPDF2, os, spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_resume(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    elif file_path.endswith(".docx"):
        text = docx2txt.process(file_path)
    return text

def extract_skills(text):
    doc = nlp(text)
    skills = [ent.text.lower() for ent in doc.ents if ent.label_ == 'SKILL']
    return skills
def calculate_score(candidate_text, job):
    job_keywords = job.skills_required.lower().split(',')
    count = sum(1 for kw in job_keywords if kw.strip() in candidate_text.lower())
    return count / len(job_keywords) if job_keywords else 0
def rank_resume_by_keywords(resume_text, job_description):
    """Rank resume based on the match with job description keywords."""
    score = 0
    job_keywords = job_description.skills_required.lower().split(',')
    for keyword in job_keywords:
        if keyword.strip() in resume_text.lower():
            score += 1
    return score

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_job_description(resume_text, job_description):
    """Match resume to job description using TF-IDF and cosine similarity."""
    documents = [resume_text, job_description.skills_required]
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]


