class AIResumeEvaluator:

    def generate_prompt(self, job_description, resume_text):
        """Generate the structured prompt with the job description and resume."""
        prompt = f"""
            Task:
                Analyze the provided resume text in relation to the job description and generate a **comprehensive, ATS-optimized report** with the following details:

                1. **Relevance Score**: A percentage (0-100%) indicating how closely the resume matches the job description.
                2. **Strengths**: Key areas where the resume aligns well with the job description, including relevant **technical skills, soft skills, industry experience, and project impact**.
                3. **Weaknesses**: Areas where the resume lacks alignment with the job description, including missing qualifications, **outdated technologies, or insufficient quantification of achievements**.
                4. **Suggestions**: Actionable advice to improve the resume’s alignment, such as **adding metrics (e.g., "Increased efficiency by 20%"), highlighting leadership roles, or improving keyword optimization**.
                5. **Missing Keywords**: Important **ATS-relevant** keywords that are missing or underused, including **technical skills, certifications, and industry-specific terms**.
                6. **Grammar and Writing Quality**: Evaluate clarity, grammar, and **ATS compliance**:
                    - **Grammar Errors**: Identify specific issues (e.g., "Incorrect verb tense in 'Managed projects that was successful.'").
                    - **Clarity Issues**: Highlight vague or repetitive phrasing (e.g., "Avoid phrases like 'responsible for' and replace with action-driven verbs.").
                    - **Professional Tone**: Suggest tone improvements (e.g., "Use impact-driven words like 'orchestrated' instead of 'helped with'.").
                7. **ATS Optimization Tips**: Additional recommendations to **enhance ATS ranking**, including formatting adjustments, keyword placement, and the **use of job-specific action verbs**.

            Output Format:

                Relevance Score: [XX%]
                Strengths: [List key areas of alignment (skills, experiences, etc.)]
                Weaknesses: [List areas requiring improvement or lacking alignment]
                Suggestions: [Provide actionable feedback, e.g., "Add experience in X to match the requirement for Y."]
                Missing Keywords: [List ATS-critical keywords that should be added]
                Grammar and Writing Quality:
                    Grammar Errors: [List specific errors with examples]
                    Clarity Issues: [List unclear phrases and rewording suggestions]
                    Professional Tone: [Recommend improvements in tone and phrasing]
                ATS Optimization Tips: [Best practices for increasing ATS ranking]
                Job & Course Recommendations:
                    Jobs: [List relevant job titles]
                    Courses: [List suggested courses/platforms]

            Additional Considerations:
                - Ensure **feedback is ATS-compliant, actionable, and industry-relevant**.
                - Highlight **both technical and soft skills alignment separately**.
                - Provide **examples or rewritten suggestions for grammar and clarity issues**.
                - Ensure **metrics, leadership experience, and project impact are highlighted**.
                - Tailor feedback to be **constructive, supportive, and industry-aligned**.
            Provide the response in JSON format not include list inside dictionary.

        job_description = {job_description}
        resume_text = {resume_text}
        """
        return prompt
