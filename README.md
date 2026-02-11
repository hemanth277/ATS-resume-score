# ATS Resume Score

An intelligent ATS (Applicant Tracking System) Resume Score application that analyzes resumes against job descriptions and provides comprehensive feedback including skill gap analysis.

## Features

- **ATS Compatibility Score**: Get an overall score showing how well your resume matches the job requirements
- **Keyword Analysis**: See which keywords from the job description are present or missing in your resume
- **Resume Structure Check**: Verify your resume has all essential sections
- **Skill Gap Analysis**: 
  - Identifies 70+ technical and soft skills
  - Categorizes skills (Programming Languages, Frameworks, Cloud/DevOps, etc.)
  - Shows matched vs. missing skills
  - Provides prioritized learning recommendations
- **Actionable Recommendations**: Get specific suggestions to improve your resume

## Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- PyPDF2 - PDF text extraction
- Python 3.8+

**Frontend:**
- Vanilla JavaScript
- HTML5 & CSS3
- Modern responsive design

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/hemanth277/ATS-resume-score.git
cd ATS-resume-score
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Start the backend server**
```bash
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

4. **Open the frontend**
- Simply open `frontend/index.html` in your web browser
- Or use a local server like Live Server in VS Code

## Docker Deployment (Recommended)

The easiest way to run the application is using Docker:

```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost
# Backend API: http://localhost:8000
```

For detailed Docker instructions, see [DOCKER.md](DOCKER.md)

## Usage

1. **Upload Your Resume**: Click to upload or drag and drop a PDF resume
2. **Paste Job Description**: Copy and paste the job description you're applying for
3. **Analyze**: Click "Analyze Resume" to get instant feedback
4. **Review Results**:
   - Overall ATS compatibility score
   - Keyword match analysis
   - Resume structure evaluation
   - **Skill gap analysis** with learning recommendations
   - Specific recommendations for improvement

## Skill Gap Analysis

The application analyzes 70+ skills across multiple categories:

**Technical Skills:**
- Programming Languages (Python, JavaScript, Java, etc.)
- Frameworks (React, Django, FastAPI, etc.)
- Databases (MySQL, PostgreSQL, MongoDB, etc.)
- Cloud & DevOps (AWS, Azure, Docker, Kubernetes, etc.)
- Testing Tools (Jest, Pytest, Selenium, etc.)

**Soft Skills:**
- Leadership & Management
- Communication
- Problem Solving
- Teamwork & Collaboration
- Adaptability

Each missing skill comes with:
- Priority level (High/Medium/Low)
- Category classification
- Recommended learning resources

## Project Structure

```
ATS-resume-score/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── ats.py            # ATS scoring engine with skill gap analysis
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── index.html        # Main HTML file
│   ├── app.js            # JavaScript logic
│   └── app.css           # Styling
└── README.md
```

## API Endpoints

### POST /analyze
Analyzes a resume against a job description

**Request:**
- `resume`: PDF file (multipart/form-data)
- `job_description`: Text (form field)

**Response:**
```json
{
  "overall_score": 75.5,
  "keyword_match_score": 70.0,
  "structure_score": 85.0,
  "skill_gap_analysis": {
    "skill_match_percentage": 65.0,
    "skills_matched": 13,
    "skills_missing": 7,
    "skills_by_category": {...},
    "learning_recommendations": [...]
  },
  "recommendations": [...]
}
```

### GET /health
Health check endpoint

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Hemanth - [GitHub](https://github.com/hemanth277)

## Acknowledgments

- Built with FastAPI and modern web technologies
- Designed to help job seekers optimize their resumes for ATS systems
