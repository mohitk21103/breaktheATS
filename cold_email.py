import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

api_key = app.config["GEMINI_API_KEY"]
if not api_key:
    raise ValueError("gemini key not found")

try:
    api = genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("Gemini API configured succesfully")
except Exception as e:
    print(f"error configuring gemini API:{e}")
    model = None

@app.route('/api/generate-email', methods = ['POST'])
def generate_email():
    if not model:
        return jsonify({"error": "Gemini API not configured"}), 500
    
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    job_role = data.get('jobRole')

    if not job_role:
        return jsonify({"error": "Missing 'jobRole' in request"}),400

    prompt = f"""
        Generate 2-3 distinct cold email templates for a job seeker interested in the '{job_role}' position.
        The email should be addressed professionally to an employee (like a recruiter, hiring manager, or potential teammate) at a target company.
        The goal is to express interest in the role and the company, and request a brief informational chat or ask how best to proceed with an application for the '{job_role}' role.
        Keep the tone professional, concise, enthusiastic, and respectful.
        Do NOT include placeholders like "[Your Name]" or "[Company Name]" explicitly, but write the email as if the user will fill those details in later.
        Focus on the body of the email. Do not include subject lines unless specifically asked.
        Make each template slightly different in approach (e.g., one more direct, one focusing on company admiration, one asking for advice).

        Example structure for one template:
        Dear [Employee Name/Hiring Manager],

        I hope this email finds you well.

        I'm writing to express my strong interest in the '{job_role}' position I saw advertised [mention where, e.g., on LinkedIn/company website] OR 'I am very interested in potential '{job_role}' opportunities at [Company Name]'.

        [Briefly mention 1-2 key skills/experiences relevant to the role]. I've been following [Company Name]'s work in [mention specific area] and I'm very impressed by [mention something specific].

        Would you be open to a brief 10-15 minute chat sometime next week? I'd love to learn more about the '{job_role}' role and the team. Alternatively, I'd appreciate any advice you might have on how best to express my interest to the hiring team.

        Thank you for your time and consideration.

        Sincerely,
        [Your Name]
        Your LinkedIn Profile URL (Optional)]
        [Your Portfolio URL (Optional)]

        ---
        Now generate the 2-3 templates based on this structure and the requirements above for the '{job_role}' role. Separate the templates clearly, perhaps using '--- TEMPLATE X ---' as a separator.
        """

    try:
        response = model.generate_content(prompt)
        if not response.parts:
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                block_reason = response.prompt_feedback.block_reason
                print(f"Gemini request blocked. Reason: {block_reason}")
                return jsonify({"error": f"Content generation blocked by safety filters. Reason: {block_reason}"}), 400
            else:
                print("Gemini response has no parts")
                return jsonify({"error": "Failed to generate content from Gemini API - empty response"}), 500
        
        generated_text = response.text

        templates = [template.strip() for template in generated_text.split('---', 1)[-1].strip() for t in templates]

        if not templates:
            template = [generated_text.strip()]

        return jsonify({"generated_emails": templates})
    
    except Exception as e:
        print(f"Error calling Gemini API or processing response: {e}")
        return jsonify({"error": "Failed to generate email templates due to an internal error."}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)