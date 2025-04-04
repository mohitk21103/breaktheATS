import json
import os
import google.generativeai as genai
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

# Created Modules/Classes
from AI_Powered_Analysis import AIResumeEvaluator
from analyzer_module import ResumeAnalyzer
from text_extractor import FileTextExtractor
from Resume_categoryPredict import ResumeCategory
from JobRecommendation import JobScraper

# syntax - from "module_name" import "Class_name" [:) - written to avoid confusions]

app = Flask(__name__)
# ------------------------------ ( All Class Instances at one Place ) --------------------------------------------------
ai_analysis = AIResumeEvaluator()
analyzer = ResumeAnalyzer()
extractText = FileTextExtractor()
predictCategory = ResumeCategory()

# Configure Upload Folder
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------------------ ( Gemini-API Integration Logic ) ------------------------------------------------------
key = os.environ.get("myGemKey")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"response_mime_type": "application/json"})


# ------------------------------ (Essential Functions) ---------------------------------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def ai_feedback(job_description, filepath):
    """ Generates AI feedback for the resume based on the job description """

    # Extract text from the uploaded resume
    resume_text = extractText.extract_text(filepath)

    # Generate a prompt for AI analysis
    prompt = ai_analysis.generate_prompt(job_description, resume_text)

    try:
        # Generate response from the AI model
        response = model.generate_content(prompt)
        analysis_result = response.text

        # Convert the result into a dictionary and return it
        return json.loads(analysis_result)

    except Exception as e:
        return {"error": "Failed to analyze the resume."}  # Returning error message as a dictionary


# ---------------------- (All The Routes Are Here) -----------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        if "resume" not in request.files:
            return "No file part"

        file = request.files["resume"]
        job_description = request.form.get("job_description", "").strip()
        level = request.form.get("level").strip()

        # print(level)

        if file.filename == "":
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Analyze Resume
            results = analyzer.analyze_resume(filepath, job_description)

            # AI-Analysis
            aiFeedback = ai_feedback(job_description, filepath)

            # print(aiFeedback)

            # Predict resume category:
            resume_text = extractText.extract_text(filepath)
            predicted_category = predictCategory.predict_category(resume_text)


            return redirect(
                url_for("show_analysis_result", **results, **aiFeedback, predicated_category=predicted_category, level=level))

    return render_template("analyzer.html", results=None)


@app.route("/analysis-result", methods=["GET", "POST"])
def show_analysis_result():
    # Extracting essential details
    similarity_score = request.args.get("similarity_score", "")
    suggestions = request.args.get("suggestions", "")

    # Extracting AI feedback details
    relevance_score = request.args.get("RelevanceScore", "")
    strengths = request.args.getlist("Strengths") or []
    weaknesses = request.args.getlist("Weaknesses") or []
    additional_suggestions = request.args.getlist("Suggestions") or []
    missing_keywords = request.args.getlist("MissingKeywords") or []

    # Extracting grammar and writing quality details
    grammar_errors = request.args.getlist("GrammarAndWritingQuality.GrammarErrors") or []
    clarity_issues = request.args.getlist("GrammarAndWritingQuality.ClarityIssues") or []
    professional_tone = request.args.getlist("GrammarAndWritingQuality.ProfessionalTone") or []

    # Extracting ATS Optimization Tips
    ats_tips = request.args.getlist("ATSOptimizationTips") or []

    predicted_Category = request.args.get("predicated_category", "")
    level = request.args.get("level")

    get_job = JobScraper(predicted_Category, level)
    recommended_job = get_job.get_all_jobs()

    # print(recommended_job)

    # Storing all results in a dictionary
    results = {
        "similarity_score": similarity_score,
        "suggestions": suggestions,
        "relevance_score": relevance_score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "additional_suggestions": additional_suggestions,
        "missing_keywords": missing_keywords,
        "grammar_errors": grammar_errors,
        "clarity_issues": clarity_issues,
        "professional_tone": professional_tone,
        "ats_tips": ats_tips,
        "predicted_category": predicted_Category
    }
    # for key, value in results.items():
    #     print(f"{key}: {value}")

    return render_template("analysis_results.html", results=results, jobs=recommended_job)


if __name__ == "__main__":
    app.run(debug=True)
