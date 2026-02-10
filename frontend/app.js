/**
 * ATS Resume Score - Frontend JavaScript
 * Handles form submission, file upload, and results display
 */

// API Configuration
const API_URL = 'http://localhost:8000';

// DOM Elements
const analysisForm = document.getElementById('analysisForm');
const resumeFile = document.getElementById('resumeFile');
const fileLabel = document.getElementById('fileLabel');
const fileInfo = document.getElementById('fileInfo');
const jobDescription = document.getElementById('jobDescription');
const charCount = document.getElementById('charCount');
const submitBtn = document.getElementById('submitBtn');

const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

/**
 * Setup all event listeners
 */
function setupEventListeners() {
    // File input change
    resumeFile.addEventListener('change', handleFileSelect);

    // Job description character count
    jobDescription.addEventListener('input', updateCharCount);

    // Form submission
    analysisForm.addEventListener('submit', handleFormSubmit);

    // New analysis button
    newAnalysisBtn.addEventListener('click', resetForm);

    // Drag and drop
    const fileUploadWrapper = document.querySelector('.file-upload-wrapper');
    fileUploadWrapper.addEventListener('dragover', handleDragOver);
    fileUploadWrapper.addEventListener('dragleave', handleDragLeave);
    fileUploadWrapper.addEventListener('drop', handleDrop);
}

/**
 * Handle file selection
 */
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        displayFileInfo(file);
    }
}

/**
 * Display selected file information
 */
function displayFileInfo(file) {
    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);

    // Validate file type
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        fileInfo.innerHTML = `
            <div class="file-error">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                    <path fill-rule="evenodd" d="M8 15A7 7 0 108 1a7 7 0 000 14zm0-1A6 6 0 108 2a6 6 0 000 12zm1-6a1 1 0 11-2 0 1 1 0 012 0zM8 4a.905.905 0 00-.9.995l.35 3.507a.552.552 0 001.1 0l.35-3.507A.905.905 0 008 4z"/>
                </svg>
                Only PDF files are supported
            </div>
        `;
        resumeFile.value = '';
        return;
    }

    // Validate file size
    if (file.size > 10 * 1024 * 1024) {
        fileInfo.innerHTML = `
            <div class="file-error">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                    <path fill-rule="evenodd" d="M8 15A7 7 0 108 1a7 7 0 000 14zm0-1A6 6 0 108 2a6 6 0 000 12zm1-6a1 1 0 11-2 0 1 1 0 012 0zM8 4a.905.905 0 00-.9.995l.35 3.507a.552.552 0 001.1 0l.35-3.507A.905.905 0 008 4z"/>
                </svg>
                File size must be less than 10MB
            </div>
        `;
        resumeFile.value = '';
        return;
    }

    // Display file info
    fileInfo.innerHTML = `
        <div class="file-success">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path fill-rule="evenodd" d="M10.97 4.97a.75.75 0 011.071 1.05l-3.992 4.99a.75.75 0 01-1.08.02L4.324 8.384a.75.75 0 111.06-1.06l2.094 2.093 3.473-4.425a.236.236 0 01.02-.022z"/>
            </svg>
            <span>${file.name} (${fileSizeMB} MB)</span>
        </div>
    `;
}

/**
 * Update character count for job description
 */
function updateCharCount() {
    const count = jobDescription.value.length;
    charCount.textContent = `${count} characters`;
}

/**
 * Handle drag over
 */
function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('drag-over');
}

/**
 * Handle drag leave
 */
function handleDragLeave(event) {
    event.currentTarget.classList.remove('drag-over');
}

/**
 * Handle file drop
 */
function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('drag-over');

    const files = event.dataTransfer.files;
    if (files.length > 0) {
        resumeFile.files = files;
        displayFileInfo(files[0]);
    }
}

/**
 * Handle form submission
 */
async function handleFormSubmit(event) {
    event.preventDefault();

    const file = resumeFile.files[0];
    const jobDesc = jobDescription.value.trim();

    // Validation
    if (!file) {
        showError('Please select a resume file');
        return;
    }

    if (!jobDesc || jobDesc.length < 10) {
        showError('Please enter a detailed job description (at least 10 characters)');
        return;
    }

    // Show loading state
    showLoading();

    // Prepare form data
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDesc);

    try {
        // Send request to backend
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to analyze resume');
        }

        const result = await response.json();

        // Display results
        displayResults(result);

    } catch (error) {
        console.error('Error analyzing resume:', error);
        console.error('Error details:', {
            message: error.message,
            stack: error.stack
        });

        // Show detailed error message
        let errorMessage = error.message || 'Failed to analyze resume. Please try again.';

        // Add helpful hints based on error type
        if (error.message && error.message.includes('Failed to fetch')) {
            errorMessage += '\n\n🔧 Troubleshooting:\n';
            errorMessage += '• Make sure the backend server is running (uvicorn main:app --reload)\n';
            errorMessage += '• Check that the server is running on http://localhost:8000\n';
            errorMessage += '• Look at the browser console (F12) for more details';
        }

        showError(errorMessage);
        showUploadSection();
    }
}

/**
 * Show loading state
 */
function showLoading() {
    uploadSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    loadingSection.classList.remove('hidden');
}

/**
 * Show upload section
 */
function showUploadSection() {
    loadingSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    uploadSection.classList.remove('hidden');
}

/**
 * Display analysis results
 */
function displayResults(result) {
    // Hide loading, show results
    loadingSection.classList.add('hidden');
    uploadSection.classList.add('hidden');
    resultsSection.classList.remove('hidden');

    // Animate score
    animateScore(result.overall_score);

    // Update breakdown scores
    updateBreakdownScore('keyword', result.keyword_match_score);
    updateBreakdownScore('structure', result.structure_score);

    // Display recommendations
    displayRecommendations(result.recommendations);

    // Display keywords
    displayKeywords(
        result.top_matched_keywords || [],
        result.top_missing_keywords || [],
        result.matched_keywords_count || 0,
        result.missing_keywords_count || 0
    );

    // Display skill gap analysis
    if (result.skill_gap_analysis) {
        displaySkillGapAnalysis(result.skill_gap_analysis);
    }

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Animate score display
 */
function animateScore(targetScore) {
    const scoreNumber = document.getElementById('scoreNumber');
    const scoreRing = document.getElementById('scoreRing');

    let currentScore = 0;
    const duration = 2000; // 2 seconds
    const steps = 60;
    const increment = targetScore / steps;
    const stepDuration = duration / steps;

    const interval = setInterval(() => {
        currentScore += increment;

        if (currentScore >= targetScore) {
            currentScore = targetScore;
            clearInterval(interval);
        }

        scoreNumber.textContent = Math.round(currentScore);

        // Update ring
        const circumference = 2 * Math.PI * 85;
        const offset = circumference - (currentScore / 100) * circumference;
        scoreRing.style.strokeDashoffset = offset;

        // Update color based on score
        if (currentScore >= 70) {
            scoreRing.style.stroke = '#10b981'; // green
        } else if (currentScore >= 50) {
            scoreRing.style.stroke = '#f59e0b'; // orange
        } else {
            scoreRing.style.stroke = '#ef4444'; // red
        }
    }, stepDuration);
}

/**
 * Update breakdown score bar
 */
function updateBreakdownScore(type, score) {
    const bar = document.getElementById(`${type}Bar`);
    const scoreElement = document.getElementById(`${type}Score`);

    setTimeout(() => {
        bar.style.width = `${score}%`;
        scoreElement.textContent = `${Math.round(score)}%`;

        // Update color
        if (score >= 70) {
            bar.style.background = 'linear-gradient(90deg, #10b981, #059669)';
        } else if (score >= 50) {
            bar.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
        } else {
            bar.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
        }
    }, 300);
}

/**
 * Display recommendations
 */
function displayRecommendations(recommendations) {
    const list = document.getElementById('recommendationsList');
    list.innerHTML = '';

    recommendations.forEach((rec, index) => {
        const li = document.createElement('li');
        li.className = 'recommendation-item';
        li.style.animationDelay = `${index * 0.1}s`;
        li.textContent = rec;
        list.appendChild(li);
    });
}

/**
 * Display keywords
 */
function displayKeywords(matched, missing, matchedCount, missingCount) {
    // Update counts
    document.getElementById('matchedCount').textContent = matchedCount;
    document.getElementById('missingCount').textContent = missingCount;

    // Display matched keywords
    const matchedContainer = document.getElementById('matchedKeywords');
    matchedContainer.innerHTML = '';

    if (matched.length === 0) {
        matchedContainer.innerHTML = '<p class="no-keywords">No matched keywords found</p>';
    } else {
        matched.forEach((keyword, index) => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag matched';
            tag.style.animationDelay = `${index * 0.05}s`;
            tag.textContent = keyword;
            matchedContainer.appendChild(tag);
        });
    }

    // Display missing keywords
    const missingContainer = document.getElementById('missingKeywords');
    missingContainer.innerHTML = '';

    if (missing.length === 0) {
        missingContainer.innerHTML = '<p class="no-keywords">Great! No critical keywords missing</p>';
    } else {
        missing.forEach((keyword, index) => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag missing';
            tag.style.animationDelay = `${index * 0.05}s`;
            tag.textContent = keyword;
            missingContainer.appendChild(tag);
        });
    }
}

/**
 * Show error message
 */
function showError(message) {
    // Log to console
    console.error('Showing error to user:', message);

    // Create a better error display
    const errorHTML = `
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #1e293b;
            border: 2px solid #ef4444;
            border-radius: 16px;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            z-index: 9999;
            color: #f1f5f9;
        ">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <svg width="32" height="32" viewBox="0 0 32 32" fill="#ef4444">
                    <path d="M16 2C8.3 2 2 8.3 2 16s6.3 14 14 14 14-6.3 14-14S23.7 2 16 2zm0 26c-6.6 0-12-5.4-12-12S9.4 4 16 4s12 5.4 12 12-5.4 12-12 12z"/>
                    <path d="M16 10c-.6 0-1 .4-1 1v8c0 .6.4 1 1 1s1-.4 1-1v-8c0-.6-.4-1-1-1zM16 22c-.6 0-1 .4-1 1s.4 1 1 1 1-.4 1-1-.4-1-1-1z"/>
                </svg>
                <h3 style="margin: 0; font-size: 1.25rem; color: #ef4444;">Error</h3>
            </div>
            <p style="margin: 0 0 1.5rem 0; white-space: pre-wrap; line-height: 1.6;">${message}</p>
            <button onclick="this.parentElement.remove()" style="
                width: 100%;
                padding: 0.75rem;
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
            ">Close</button>
        </div>
        <div onclick="this.nextElementSibling.remove(); this.remove()" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: 9998;
        "></div>
    `;

    document.body.insertAdjacentHTML('beforeend', errorHTML);
}

/**
 * Display skill gap analysis
 */
function displaySkillGapAnalysis(skillGap) {
    // Update summary cards
    document.getElementById('skillMatchPercentage').textContent = `${skillGap.skill_match_percentage}%`;
    document.getElementById('skillsMatched').textContent = skillGap.skills_matched;
    document.getElementById('skillsMissing').textContent = skillGap.skills_missing;

    // Display skills by category
    displaySkillsByCategory(skillGap.skills_by_category);

    // Display learning recommendations
    displayLearningRecommendations(skillGap.learning_recommendations);
}

/**
 * Display skills organized by category
 */
function displaySkillsByCategory(skillsByCategory) {
    const container = document.getElementById('skillsByCategory');
    container.innerHTML = '';

    if (!skillsByCategory || Object.keys(skillsByCategory).length === 0) {
        container.innerHTML = '<p class="no-skills">No specific skill requirements detected in the job description.</p>';
        return;
    }

    for (const [category, data] of Object.entries(skillsByCategory)) {
        const matched = data.matched || [];
        const missing = data.missing || [];
        const skillType = data.type || 'technical';

        // Create category card
        const categoryCard = document.createElement('div');
        categoryCard.className = 'category-card';
        categoryCard.style.animationDelay = `${Object.keys(skillsByCategory).indexOf(category) * 0.1}s`;

        const categoryName = category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        const typeIcon = skillType === 'technical' ? '💻' : '🤝';

        categoryCard.innerHTML = `
            <div class="category-header">
                <span class="category-icon">${typeIcon}</span>
                <h5 class="category-name">${categoryName}</h5>
                <span class="category-badge">${matched.length}/${matched.length + missing.length}</span>
            </div>
            <div class="category-skills">
                ${matched.length > 0 ? `
                    <div class="category-skills-group">
                        <div class="skills-group-label">✅ Matched</div>
                        <div class="skills-tags">
                            ${matched.map(skill => `<span class="skill-tag matched">${skill}</span>`).join('')}
                        </div>
                    </div>
                ` : ''}
                ${missing.length > 0 ? `
                    <div class="category-skills-group">
                        <div class="skills-group-label">❌ Missing</div>
                        <div class="skills-tags">
                            ${missing.map(skill => `<span class="skill-tag missing">${skill}</span>`).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;

        container.appendChild(categoryCard);
    }
}

/**
 * Display learning recommendations
 */
function displayLearningRecommendations(recommendations) {
    const container = document.getElementById('learningCards');
    container.innerHTML = '';

    if (!recommendations || recommendations.length === 0) {
        container.innerHTML = '<p class="no-recommendations">Great! You have all the required skills.</p>';
        return;
    }

    recommendations.forEach((rec, index) => {
        const card = document.createElement('div');
        card.className = 'learning-card';
        card.style.animationDelay = `${index * 0.05}s`;

        // Priority badge color
        const priorityColors = {
            'High': '#ef4444',
            'Medium': '#f59e0b',
            'Low': '#6b7280'
        };

        card.innerHTML = `
            <div class="learning-card-header">
                <div class="learning-skill-info">
                    <h5 class="learning-skill-name">${rec.skill}</h5>
                    <span class="learning-skill-category">${rec.category}</span>
                </div>
                <span class="priority-badge" style="background: ${priorityColors[rec.priority] || '#6b7280'}">
                    ${rec.priority}
                </span>
            </div>
            <div class="learning-resources">
                <div class="resources-label">📚 Learning Resources:</div>
                <ul class="resources-list">
                    ${rec.resources.map(resource => `<li>${resource}</li>`).join('')}
                </ul>
            </div>
        `;

        container.appendChild(card);
    });
}

/**
 * Reset form for new analysis
 */
function resetForm() {
    analysisForm.reset();
    fileInfo.innerHTML = '';
    charCount.textContent = '0 characters';
    showUploadSection();
}
