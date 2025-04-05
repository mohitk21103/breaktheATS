document.addEventListener('DOMContentLoaded', function() {
    const useTemplateButtons = document.querySelectorAll('.use-template');
    const resumeFormArea = document.getElementById('resumeFormArea');
    const resumeForm = document.getElementById('resumeForm');
    const generateResumeButton = document.getElementById('generateResume');
    const generatedResumeDiv = document.getElementById('generatedResume');
    const resumeOutputDiv = document.getElementById('resumeOutput');

    useTemplateButtons.forEach(button => {
        button.addEventListener('click', function() {
            resumeFormArea.classList.remove('resume-form-area-hidden');
        });
    });

    generateResumeButton.addEventListener('click', function() {
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const experience = document.getElementById('experience').value;
        const education = document.getElementById('education').value;
        const skills = document.getElementById('skills').value;

        // replace with actual resume generation logic
        const resumeContent = `
            <h2>${name}</h2>
            <p>Email: ${email}</p>
            <p>Phone: ${phone}</p>
            <h3>Experience</h3>
            <p>${experience}</p>
            <h3>Education</h3>
            <p>${education}</p>
            <h3>Skills</h3>
            <p>${skills}</p>
        `;

        resumeOutputDiv.innerHTML = resumeContent;
        generatedResumeDiv.classList.remove('generated-resume-hidden');
    });
});