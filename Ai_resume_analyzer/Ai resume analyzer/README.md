# AI Resume Analyzer & Job Recommendation System

A small Streamlit app that helps students see how well their resume matches different job roles.
Upload a PDF or DOCX resume and the app will:

1. Read and clean the resume text
2. Find the technical skills in it
3. Score the resume against 8 job roles and recommend the top 3
4. Show which skills are missing for the role you choose
5. Suggest a simple week-by-week learning roadmap
6. Let you download the analysis as a text report

## Project structure

```
Ai resume analyzer/
├── App.py                  # Streamlit dashboard (run this)
├── Resume_parser.py        # reads PDF/DOCX files and cleans the text
├── Skill_extractor.py      # finds skills using the skill dictionary
├── Job_matcher.py          # scores and ranks job roles
├── Roadmap_generator.py    # builds the learning roadmap
├── Requirements.txt
├── README.md
├── .gitignore
├── .env                    # settings (maximum file size)
├── Data/
│   ├── Job_roles.csv       # job roles and the skills they need
│   └── Skill_dictionary.csv# skills, categories and alternate spellings
└── Sample_resumes/         # three anonymised resumes to try out
```

## How to run

 cd "Ai resume analyzer"

```bash
# 1. (optional) create a virtual environment
python -m venv .venv
.venv\Scripts\activate          


# 2. install the libraries
pip install -r Requirements.txt

# 3. start the app
streamlit run App.py
```

The app opens in your browser. Upload a file from `Sample_resumes/` to try it out.

## How the match score works

For every job role the score is:

```
match score = 70% x skill coverage  +  30% x TF-IDF similarity
```

- **Skill coverage** - the percentage of the role's required skills that were found in the resume.
  If a role needs 8 skills and the resume has 6 of them, coverage is 75%.
- **TF-IDF similarity** - the resume's skills and the role's skills are turned into vectors with
  TF-IDF, and cosine similarity measures how close they are. TF-IDF gives less weight to skills
  that nearly every role asks for (like Python or Git), so rarer skills count for more.

Roles are then ranked from highest to lowest score. The top three are shown as recommendations.

## How skills are found

`Skill_extractor.py` uses plain keyword matching. For each skill in `Data/Skill_dictionary.csv`
it checks whether the skill (or one of its alternate spellings) appears as a whole word in the
cleaned resume text. Whole-word matching stops `java` from matching inside `javascript`.
Symbols such as `C++`, `C#`, `.NET` and `CI/CD` are kept during cleaning so they can be found.

## Changing the data

**Add a skill** - add a row to `Data/Skill_dictionary.csv`:

```
skill,category,aliases
Redis,Databases,redis cache
```

Aliases are other ways people write the skill, separated by `|`.

**Add a job role** - add a row to `Data/Job_roles.csv`, separating skills with `|`:

```
role,required_skills
Data Engineer,Python|SQL|Docker|AWS|Git
```

Every skill used in a role must be spelled exactly like it is in `Skill_dictionary.csv`,
otherwise it can never be matched. The app shows a warning if it finds a mismatch.

**Add a learning tip** - add the skill and a one-line tip to `LEARNING_TIPS` in `Roadmap_generator.py`.
Skills without a tip get a general one.

## Settings (.env)

| Setting | Default | Meaning |
|---|---|---|
| `MAX_FILE_SIZE_MB` | `5` | Largest resume file the app accepts |

