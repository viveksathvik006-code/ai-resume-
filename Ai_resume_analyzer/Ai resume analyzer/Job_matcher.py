import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROLES_FILE = os.path.join(BASE_DIR, "Data", "Job_roles.csv")

COVERAGE_WEIGHT = 0.7
SIMILARITY_WEIGHT = 0.3
  

def load_job_roles(path=ROLES_FILE):
    """Read the roles CSV and return a list like {"role": "Data Analyst", "skills": [...]}."""
    table = pd.read_csv(path)
    roles = []

    for _, row in table.iterrows():
        skills = [s.strip() for s in row["required_skills"].split("|") if s.strip()]
        roles.append({"role": row["role"], "skills": skills})

    return roles


def check_role_skills(roles, known_skills):
    """
    Return the role skills that are missing from the skill dictionary.
    Such skills could never be found in a resume, so it is good to warn about them.
    """
    problems = []
    for role in roles:
        for skill in role["skills"]:
            if skill not in known_skills:
                problems.append(f"{role['role']}: {skill}")
    return problems


def find_skill_gap(resume_skills, required_skills):
    """Split the required skills into the ones the resume has and the ones it lacks."""
    matched = [skill for skill in required_skills if skill in resume_skills]
    missing = [skill for skill in required_skills if skill not in resume_skills]
    return matched, missing


def to_document(skills):
    """
    Turn a skill list into one line of text for TF-IDF.
    'Power BI' becomes 'Power_BI' so it is treated as a single word.
    """
    return " ".join(skill.replace(" ", "_") for skill in skills)


def rank_roles(resume_skills, roles):
    """Score every role and return them sorted from best to worst match."""
    # TF-IDF: one document per role, plus the resume as the last one
    documents = [to_document(role["skills"]) for role in roles]
    documents.append(to_document(resume_skills))

    vectors = TfidfVectorizer(token_pattern=r"\S+").fit_transform(documents)
    similarities = cosine_similarity(vectors[-1], vectors[:-1])[0]

    results = []
    for role, similarity in zip(roles, similarities):
        matched, missing = find_skill_gap(resume_skills, role["skills"])

        coverage = len(matched) / len(role["skills"]) * 100
        score = COVERAGE_WEIGHT * coverage + SIMILARITY_WEIGHT * similarity * 100

        results.append({
            "role": role["role"],
            "score": score,
            "matched": matched,
            "missing": missing,
        })

    results.sort(key=lambda result: result["score"], reverse=True)
    return results
