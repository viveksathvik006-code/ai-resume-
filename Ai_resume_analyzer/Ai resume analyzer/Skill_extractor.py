import os
import re

import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_FILE = os.path.join(BASE_DIR, "Data", "Skill_dictionary.csv")


def load_skill_dictionary(path=SKILL_FILE):
    """
    Read the skill CSV and return a list like:
    {"skill": "Power BI", "category": "Data", "names": ["power bi", "powerbi"]}
    'names' holds every spelling we should look for (the skill + its aliases).
    """
    table = pd.read_csv(path).fillna("")
    skill_list = []

    for _, row in table.iterrows():
        names = [row["skill"]]
        for alias in row["aliases"].split("|"):
            if alias.strip():
                names.append(alias)

        skill_list.append({
            "skill": row["skill"],
            "category": row["category"],
            "names": [name.lower().strip() for name in names],
        })

    return skill_list


def appears_in(name, text):
    """
    True if 'name' appears as a whole word in the text.
    This stops 'java' from matching inside 'javascript'
    and 'sql' from matching inside 'postgresql'.
    """
    pattern = r"(?<![a-z0-9])" + re.escape(name) + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None 


def extract_skills(cleaned_text, skill_list):
    """Return the skills found in the resume, grouped by category."""
    found = {}

    for item in skill_list:
        for name in item["names"]:
            if appears_in(name, cleaned_text):
                found.setdefault(item["category"], []).append(item["skill"])
                break   # one spelling is enough

    return found


def flatten_skills(skills_by_category):
    """Turn {"Data": ["SQL"], "Tools": ["Git"]} into ["SQL", "Git"]."""
    all_skills = []
    for skills in skills_by_category.values():
        all_skills.extend(skills)
    return all_skills
