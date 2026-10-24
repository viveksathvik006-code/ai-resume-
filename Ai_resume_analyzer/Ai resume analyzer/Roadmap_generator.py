LEARNING_TIPS = {
    "Python": "Practise the basics (loops, functions, lists, dictionaries) and finish one small automation script.",
    "SQL": "Practise SELECT, JOIN, GROUP BY and subqueries on a sample database.",
    "Excel": "Learn formulas, lookups and pivot tables, then build one summary sheet.",
    "Pandas": "Clean and analyse a CSV file with Pandas and write down what you find.",
    "NumPy": "Practise arrays and basic maths operations with NumPy.",
    "Power BI": "Build a small dashboard from a public dataset.",
    "Tableau": "Build two or three charts and combine them into a dashboard.",
    "Statistics": "Revise mean, median, standard deviation, probability and hypothesis testing.",
    "Machine Learning": "Learn supervised learning and train a simple prediction model.",
    "scikit-learn": "Train and test a model with scikit-learn on a small dataset.",
    "Deep Learning": "Learn how neural networks work and train a small one.",
    "NLP": "Practise text cleaning and build a simple text classifier.",
    "Transformers": "Understand attention at a high level and try a pretrained transformer model.",
    "Hugging Face": "Run a pretrained model from Hugging Face on your own text.",
    "PyTorch": "Build and train a small neural network in PyTorch.",
    "OpenCV": "Load images, resize, filter and detect edges with OpenCV.",
    "CNN": "Learn how convolution layers work and train a small image classifier.",
    "YOLO": "Run a pretrained YOLO model on a few images or a video.",
    "LLM": "Learn how prompts work and build a small app that calls an LLM.",
    "RAG": "Build a small question-answering app over your own documents.",
    "LangChain": "Follow the LangChain quickstart and build a simple chain.",
    "APIs": "Learn how to call a public API and handle its JSON response.",
    "REST API": "Design a few REST endpoints and test them with Postman.",
    "FastAPI": "Build a small API with FastAPI and serve a simple model through it.",
    "Django": "Build a small CRUD web app with Django.",
    "Flask": "Build a small web app or API with Flask.",
    "JavaScript": "Practise the basics and add some interactivity to a web page.",
    "TypeScript": "Convert a small JavaScript project to TypeScript.",
    "HTML": "Build a simple multi-section web page.",
    "CSS": "Style a web page and make it responsive.",
    "React": "Build a small app with components and state, such as a to-do list.",
    "Docker": "Package one of your projects into a Docker image and run it.",
    "Kubernetes": "Learn pods and deployments and run a small app on a local cluster.",
    "AWS": "Learn the core services (EC2, S3) and deploy a small app.",
    "Linux": "Get comfortable with the terminal, file permissions and basic shell commands.",
    "CI/CD": "Set up a simple GitHub Actions workflow that runs tests on every push.",
    "Git": "Practise commits, branches and merges on a project of your own.",
}


def build_roadmap(missing_skills):
    """Return a list of weekly steps, one for each missing skill."""
    if not missing_skills:
        return ["You already cover every skill for this role. Build one bigger project to show them off."]

    roadmap = []
    for week, skill in enumerate(missing_skills, start=1):
        tip = LEARNING_TIPS.get(skill, f"Learn the basics of {skill} and use it in a small project.")
        roadmap.append(f"Week {week}: {skill} - {tip}")
    return roadmap
