import json
import os
import google.generativeai as genai
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# Created Modules/Classes
from AI_Powered_Analysis import AIResumeEvaluator
from analyzer_module import ResumeAnalyzer, nlp
from testing import suggestion_eval_model
from text_extractor import FileTextExtractor
from Resume_categoryPredict import ResumeCategory
from JobRecommendation import JobScraper
from suggestion_evaluator import SuggestionEvaluator

app = Flask(__name__)

# ------------------------------ ( All Class Instances at one Place ) --------------------------------------------------
ai_analysis = AIResumeEvaluator()
analyzer = ResumeAnalyzer()
extractText = FileTextExtractor()
predictCategory = ResumeCategory()
suggestion_evaluator = SuggestionEvaluator(spacy_nlp_model=nlp, genai_eval_model=suggestion_eval_model)


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


def ai_feedback(job_description, filepath, threshold=0.7, max_attempts=3):
    """ Generates AI feedback for the resume based on the job description,
        evaluates it, and regenerates if below threshold. """

    resume_text = extractText.extract_text(filepath)
    prompt = ai_analysis.generate_prompt(job_description, resume_text)

    for _ in range(max_attempts):
        try:
            response = model.generate_content(prompt)
            response_data = json.loads(response.text)

            # Get suggestions from the response (you can adjust this key as per actual response structure)
            suggestions = response_data.get("Suggestions", [])

            # Evaluate the suggestions
            score = suggestion_evaluator.evaluate(suggestions, job_description)

            if score >= threshold:
                return response_data

        except Exception as e:
            print(f"Error in AI feedback or evaluation: {e}")
            continue

    # Return the last response even if it’s below threshold, or handle gracefully
    return response_data if 'response_data' in locals() else {"error": "Failed to analyze the resume."}


# ------------------------------ (Route to Serve Uploaded Files) --------------------------------------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ------------------------------ (All The Routes Are Here) ---------------------------------------------------------
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
        file_name = file.filename

        if file_name == "":
            return "No selected file"

        if file and allowed_file(file_name):
            filename = secure_filename(file_name)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Analyze Resume
            results = analyzer.analyze_resume(filepath, job_description)

            # AI-Analysis
            aiFeedback = ai_feedback(job_description, filepath)

            # Predict resume category:
            resume_text = extractText.extract_text(filepath)
            predicted_category = predictCategory.predict_category(resume_text)

            # Generate resume preview URL
            resume_url = url_for("uploaded_file", filename=filename)

            return redirect(
                url_for("show_analysis_result",
                        **results,
                        **aiFeedback,
                        predicated_category=predicted_category,
                        level=level,
                        file_name=filename,
                        resume_url=resume_url)
            )

    return render_template("analyzer.html", results=None)


@app.route("/analysis-result", methods=["GET", "POST"])
def show_analysis_result():
    similarity_score = request.args.get("similarity_score", "")
    suggestions = request.args.get("suggestions", "")
    relevance_score = request.args.get("RelevanceScore", "")
    strengths = request.args.getlist("Strengths") or []
    weaknesses = request.args.getlist("Weaknesses") or []
    additional_suggestions = request.args.getlist("Suggestions") or []
    missing_keywords = request.args.getlist("MissingKeywords") or []
    grammar_errors = request.args.getlist("GrammarAndWritingQuality.GrammarErrors") or []
    clarity_issues = request.args.getlist("GrammarAndWritingQuality.ClarityIssues") or []
    professional_tone = request.args.getlist("GrammarAndWritingQuality.ProfessionalTone") or []
    ats_tips = request.args.getlist("ATSOptimizationTips") or []
    predicted_Category = request.args.get("predicated_category", "")
    level = request.args.get("level")
    resume_url = request.args.get("resume_url", "")

    get_job = JobScraper(predicted_Category, level)
    try:
        recommended_job = get_job.get_all_jobs()
    except Exception as e:
        print(f"Error occurred while fetching jobs: {e}")
        recommended_job = []

    results = {
        "suggestions": suggestions,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "missing_keywords": missing_keywords,
        "grammar_errors": grammar_errors,
        "clarity_issues": clarity_issues,
        "ats_tips": ats_tips,
        "predicted_category": predicted_Category
    }

    return render_template("analysis_results.html",
                           results=results,
                           jobs=recommended_job,
                           similarity_score=similarity_score,
                           resume_url=resume_url)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
