import google.generativeai as genai


class ColdEmailGenerator:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Gemini API key is missing")

        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            print("✅ Gemini API configured successfully")
        except Exception as e:
            print(f"❌ Error configuring Gemini API: {e}")
            self.model = None

    def generate_cold_emails(self, job_role):
        if not self.model:
            raise RuntimeError("Gemini API is not configured properly")

        prompt = f"""
        You are an expert email writer.

        Your task is to generate 2–3 distinct **cold email templates** for a job seeker interested in the **'{job_role}'** position.

        Each email should:
        - Be addressed professionally to an employee (e.g., recruiter, hiring manager, or potential teammate) at the target company.
        - Express interest in the role and the company.
        - Ask for a short informational chat or guidance on how to proceed with applying.
        - Be professional, concise, enthusiastic, and respectful.
        - Avoid using placeholders like "[Your Name]" or "[Company Name]". Write as if the user will fill in the specifics later.
        - Focus only on the **body** of the email (no subject line required unless asked).

        Variations to include:
        - One direct approach.
        - One with admiration for the company.
        - One politely seeking advice or guidance.

        ✅ Format:
        Return the response using clear template separation with the following format:

        --- TEMPLATE 1 ---
        [Email body 1]

        --- TEMPLATE 2 ---
        [Email body 2]

        --- TEMPLATE 3 ---
        [Email body 3]
        """

        try:
            response = self.model.generate_content(prompt)

            if not response.parts:
                if response.prompt_feedback and response.prompt_feedback.block_reason:
                    raise Exception(f"Blocked by safety filter: {response.prompt_feedback.block_reason}")
                raise Exception("Empty response from Gemini model")

            # Split by separator (e.g., "--- TEMPLATE 1 ---")
            raw_text = response.text.strip()
            templates = [t.strip() for t in raw_text.split('---') if t.strip()]

            return templates

        except Exception as e:
            raise RuntimeError(f"Error generating content: {e}")
