document.addEventListener('DOMContentLoaded', function() {
    const signInButton = document.getElementById('signInButton');
    const signInModal = document.getElementById('signInModal');
    const closeBtn = document.querySelector('.close');
    const analyzeButton = document.getElementById('analyzeButton');
    const resumeUpload = document.getElementById('resumeUpload');
    const uploadResumeButton = document.getElementById('uploadResumeButton');
    const resumeBuilderButton = document.getElementById('resumeBuilderButton');

    resumeBuilderButton.addEventListener('click', function() {
        window.location.href = 'resume_builder.html';
    });
    
    uploadResumeButton.addEventListener('click', function() {
        window.location.href = 'upload_resume.html';
    });
    
    signInButton.addEventListener('click', function() {
        signInModal.style.display = 'flex';
    });

    closeBtn.addEventListener('click', function() {
        signInModal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === signInModal) {
            signInModal.style.display = 'none';
        }
    });

    resumeUpload.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            analyzeButton.disabled = false;
        } else {
            analyzeButton.disabled = true;
        }
    });

    analyzeButton.addEventListener('click', function() {
        // replace with actual analysis logic
        const analysisResults = {
            strengths: "Good formatting, relevant experience.",
            weaknesses: "Needs more specific skills, improve action verbs.",
            suggestions: "Tailor resume to each job, quantify achievements."
        };

        const queryString = `?strengths=${encodeURIComponent(analysisResults.strengths)}&weaknesses=${encodeURIComponent(analysisResults.weaknesses)}&suggestions=${encodeURIComponent(analysisResults.suggestions)}`;

        window.location.href = 'analysis_results.html' + queryString;
    });

    document.getElementById('resumeBuilderButton').addEventListener('click', function() {
        window.location.href = 'resume_builder.html';
    });
    document.addEventListener('DOMContentLoaded', function() {
        // ... (Your existing JavaScript code) ...
    
        // About link scroll functionality
        const aboutLink = document.querySelector('nav a[href="#aboutSection"]'); // Select the about link
        const servicesLink = document.querySelector('nav a[href="#servicesSection"]'); // select the services link
        const aboutSection = document.getElementById('aboutSection'); // Select the target section
        const servicesSection = document.getElementById('servicesSection');
    
        if (aboutLink && aboutSection) {
            aboutLink.addEventListener('click', function(event) {
                event.preventDefault(); // Prevent default link behavior
    
                aboutSection.scrollIntoView({
                    behavior: 'smooth', // Smooth scrolling animation
                    block: 'start' // Scroll to the top of the element
                });
            });
        }
    
        if (servicesLink && servicesSection) {
          servicesLink.addEventListener('click', function(event) {
            event.preventDefault();
    
            servicesSection.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
          })
        }
    
        // ... (Your existing JavaScript code) ...
    });
});