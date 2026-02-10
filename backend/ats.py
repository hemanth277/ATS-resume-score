"""
ATS Resume Scoring Engine
Analyzes resumes against job descriptions and provides ATS compatibility scores
"""

import re
from typing import Dict, List, Tuple
from PyPDF2 import PdfReader
import io


class ATSScorer:
    """Main class for ATS resume scoring"""
    
    def __init__(self):
        self.common_sections = [
            'experience', 'education', 'skills', 'summary', 
            'objective', 'certifications', 'projects', 'achievements'
        ]
        
        # Technical skills database
        self.technical_skills = {
            'programming_languages': [
                'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift',
                'kotlin', 'go', 'rust', 'typescript', 'scala', 'r', 'matlab', 'perl'
            ],
            'frameworks': [
                'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring',
                'express', 'node.js', 'nodejs', '.net', 'laravel', 'rails', 'nextjs',
                'nuxt', 'svelte', 'ember', 'backbone'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
                'oracle', 'sql server', 'sqlite', 'dynamodb', 'mariadb', 'couchdb'
            ],
            'cloud_devops': [
                'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins',
                'gitlab', 'github actions', 'terraform', 'ansible', 'ci/cd', 'devops'
            ],
            'tools': [
                'git', 'jira', 'confluence', 'slack', 'vscode', 'intellij', 'eclipse',
                'postman', 'swagger', 'figma', 'sketch', 'adobe xd'
            ],
            'testing': [
                'jest', 'pytest', 'junit', 'selenium', 'cypress', 'mocha', 'chai',
                'testing', 'unit testing', 'integration testing', 'tdd', 'bdd'
            ]
        }
        
        # Soft skills database
        self.soft_skills = {
            'leadership': [
                'leadership', 'team lead', 'mentoring', 'coaching', 'management',
                'project management', 'people management'
            ],
            'communication': [
                'communication', 'presentation', 'public speaking', 'writing',
                'documentation', 'collaboration', 'interpersonal'
            ],
            'problem_solving': [
                'problem solving', 'analytical', 'critical thinking', 'troubleshooting',
                'debugging', 'research'
            ],
            'teamwork': [
                'teamwork', 'team player', 'collaboration', 'cross-functional',
                'agile', 'scrum', 'kanban'
            ],
            'adaptability': [
                'adaptability', 'flexibility', 'learning', 'quick learner',
                'self-motivated', 'proactive'
            ]
        }
    
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extract text content from PDF file"""
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {str(e)}")
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        # Convert to lowercase and remove special characters
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        # Filter out stop words and short words
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords
    
    def calculate_keyword_match(self, resume_keywords: List[str], 
                               job_keywords: List[str]) -> Tuple[float, List[str], List[str]]:
        """Calculate keyword match percentage"""
        resume_set = set(resume_keywords)
        job_set = set(job_keywords)
        
        matched_keywords = list(resume_set.intersection(job_set))
        missing_keywords = list(job_set - resume_set)
        
        if len(job_set) == 0:
            match_percentage = 0
        else:
            match_percentage = (len(matched_keywords) / len(job_set)) * 100
        
        return match_percentage, matched_keywords, missing_keywords
    
    def check_resume_structure(self, resume_text: str) -> Dict[str, bool]:
        """Check if resume has proper ATS-friendly structure"""
        resume_lower = resume_text.lower()
        
        sections_found = {}
        for section in self.common_sections:
            # Check if section heading exists
            sections_found[section] = bool(re.search(rf'\b{section}\b', resume_lower))
        
        return sections_found
    
    def calculate_structure_score(self, sections_found: Dict[str, bool]) -> float:
        """Calculate structure score based on sections present"""
        essential_sections = ['experience', 'education', 'skills']
        essential_found = sum(1 for section in essential_sections if sections_found.get(section, False))
        
        total_found = sum(sections_found.values())
        
        # Essential sections are worth more
        essential_score = (essential_found / len(essential_sections)) * 60
        additional_score = (total_found / len(self.common_sections)) * 40
        
        return essential_score + additional_score
    
    def check_formatting_issues(self, resume_text: str) -> List[str]:
        """Check for common ATS formatting issues"""
        issues = []
        
        # Check for tables (difficult for ATS to parse)
        if '|' in resume_text or '\t\t' in resume_text:
            issues.append("Possible table formatting detected - may not be ATS-friendly")
        
        # Check for special characters
        special_chars = re.findall(r'[^\w\s\-.,@()\[\]\/]', resume_text)
        if len(special_chars) > 20:
            issues.append("Excessive special characters detected")
        
        # Check for very short lines (possible formatting issues)
        lines = resume_text.split('\n')
        very_short_lines = [line for line in lines if 0 < len(line.strip()) < 3]
        if len(very_short_lines) > 10:
            issues.append("Many very short lines detected - check formatting")
        
        return issues
    
    def generate_recommendations(self, keyword_match: float, structure_score: float,
                                missing_keywords: List[str], sections_found: Dict[str, bool],
                                formatting_issues: List[str]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Keyword recommendations
        if keyword_match < 50:
            recommendations.append(f"⚠️ Low keyword match ({keyword_match:.1f}%). Add more relevant keywords from the job description.")
            if missing_keywords:
                top_missing = missing_keywords[:5]
                recommendations.append(f"📝 Consider adding these keywords: {', '.join(top_missing)}")
        elif keyword_match < 70:
            recommendations.append(f"✓ Moderate keyword match ({keyword_match:.1f}%). Consider adding more specific skills and technologies.")
        else:
            recommendations.append(f"✅ Excellent keyword match ({keyword_match:.1f}%)!")
        
        # Structure recommendations
        essential_sections = ['experience', 'education', 'skills']
        missing_essential = [s for s in essential_sections if not sections_found.get(s, False)]
        
        if missing_essential:
            recommendations.append(f"⚠️ Missing essential sections: {', '.join(missing_essential).title()}")
        
        if structure_score < 50:
            recommendations.append("📋 Add clear section headings (Experience, Education, Skills, etc.)")
        
        # Formatting recommendations
        if formatting_issues:
            for issue in formatting_issues:
                recommendations.append(f"⚠️ {issue}")
        
        # General ATS tips
        if keyword_match > 70 and structure_score > 70:
            recommendations.append("✅ Your resume appears to be ATS-friendly!")
            recommendations.append("💡 Tip: Use standard fonts and avoid images/graphics for best ATS compatibility")
        
        return recommendations
    
    def extract_skills_from_text(self, text: str, skill_database: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Extract skills from text based on skill database"""
        text_lower = text.lower()
        found_skills = {}
        
        for category, skills_list in skill_database.items():
            found_in_category = []
            for skill in skills_list:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    found_in_category.append(skill)
            
            if found_in_category:
                found_skills[category] = found_in_category
        
        return found_skills
    
    def analyze_skill_gaps(self, resume_text: str, job_description: str) -> Dict:
        """Analyze skill gaps between resume and job description"""
        # Extract technical skills
        resume_tech_skills = self.extract_skills_from_text(resume_text, self.technical_skills)
        job_tech_skills = self.extract_skills_from_text(job_description, self.technical_skills)
        
        # Extract soft skills
        resume_soft_skills = self.extract_skills_from_text(resume_text, self.soft_skills)
        job_soft_skills = self.extract_skills_from_text(job_description, self.soft_skills)
        
        # Calculate gaps by category
        skills_by_category = {}
        total_required = 0
        total_matched = 0
        
        # Process technical skills
        for category in self.technical_skills.keys():
            resume_skills_set = set(resume_tech_skills.get(category, []))
            job_skills_set = set(job_tech_skills.get(category, []))
            
            if job_skills_set:  # Only include if job requires skills in this category
                matched = list(resume_skills_set.intersection(job_skills_set))
                missing = list(job_skills_set - resume_skills_set)
                
                skills_by_category[category] = {
                    'matched': matched,
                    'missing': missing,
                    'type': 'technical'
                }
                
                total_required += len(job_skills_set)
                total_matched += len(matched)
        
        # Process soft skills
        for category in self.soft_skills.keys():
            resume_skills_set = set(resume_soft_skills.get(category, []))
            job_skills_set = set(job_soft_skills.get(category, []))
            
            if job_skills_set:
                matched = list(resume_skills_set.intersection(job_skills_set))
                missing = list(job_skills_set - resume_skills_set)
                
                skills_by_category[category] = {
                    'matched': matched,
                    'missing': missing,
                    'type': 'soft'
                }
                
                total_required += len(job_skills_set)
                total_matched += len(matched)
        
        # Calculate skill match percentage
        skill_match_percentage = (total_matched / total_required * 100) if total_required > 0 else 0
        
        # Generate learning recommendations
        learning_recommendations = self.generate_learning_recommendations(skills_by_category)
        
        return {
            'total_skills_required': total_required,
            'skills_matched': total_matched,
            'skills_missing': total_required - total_matched,
            'skill_match_percentage': round(skill_match_percentage, 1),
            'skills_by_category': skills_by_category,
            'learning_recommendations': learning_recommendations
        }
    
    def generate_learning_recommendations(self, skills_by_category: Dict) -> List[Dict]:
        """Generate learning recommendations for missing skills"""
        recommendations = []
        
        # Priority mapping
        priority_categories = {
            'programming_languages': 'High',
            'frameworks': 'High',
            'cloud_devops': 'High',
            'databases': 'Medium',
            'testing': 'Medium',
            'tools': 'Low',
            'leadership': 'High',
            'communication': 'Medium',
            'problem_solving': 'High',
            'teamwork': 'Medium',
            'adaptability': 'Low'
        }
        
        # Learning resources mapping
        resource_mapping = {
            'programming_languages': ['Official Documentation', 'Codecademy', 'freeCodeCamp', 'LeetCode'],
            'frameworks': ['Official Docs', 'YouTube Tutorials', 'Udemy Courses', 'Framework-specific Bootcamps'],
            'cloud_devops': ['AWS/Azure/GCP Certifications', 'Docker Documentation', 'Kubernetes Tutorials'],
            'databases': ['Database Documentation', 'SQL Practice Sites', 'Database Design Courses'],
            'testing': ['Testing Framework Docs', 'Test Automation Courses', 'TDD/BDD Tutorials'],
            'tools': ['Tool Documentation', 'YouTube Tutorials', 'Quick Start Guides'],
            'leadership': ['Leadership Books', 'Management Courses', 'Mentorship Programs'],
            'communication': ['Public Speaking Courses', 'Writing Workshops', 'Toastmasters'],
            'problem_solving': ['Algorithm Practice', 'Case Study Analysis', 'Critical Thinking Courses'],
            'teamwork': ['Agile/Scrum Certifications', 'Team Collaboration Workshops'],
            'adaptability': ['Online Courses', 'Self-Learning Resources', 'Professional Development']
        }
        
        for category, skills_data in skills_by_category.items():
            missing_skills = skills_data.get('missing', [])
            skill_type = skills_data.get('type', 'technical')
            
            for skill in missing_skills[:3]:  # Top 3 missing skills per category
                recommendations.append({
                    'skill': skill.title(),
                    'category': category.replace('_', ' ').title(),
                    'type': skill_type,
                    'priority': priority_categories.get(category, 'Medium'),
                    'resources': resource_mapping.get(category, ['Online Courses', 'Documentation'])
                })
        
        # Sort by priority (High -> Medium -> Low)
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return recommendations[:10]  # Return top 10 recommendations
    
    def analyze_resume(self, resume_bytes: bytes, job_description: str) -> Dict:
        """Main method to analyze resume against job description"""
        try:
            # Extract text from PDF
            resume_text = self.extract_text_from_pdf(resume_bytes)
            
            if not resume_text:
                raise ValueError("Could not extract text from PDF. Please ensure it's a text-based PDF.")
            
            # Extract keywords
            resume_keywords = self.extract_keywords(resume_text)
            job_keywords = self.extract_keywords(job_description)
            
            # Calculate keyword match
            keyword_match, matched_keywords, missing_keywords = self.calculate_keyword_match(
                resume_keywords, job_keywords
            )
            
            # Check structure
            sections_found = self.check_resume_structure(resume_text)
            structure_score = self.calculate_structure_score(sections_found)
            
            # Check formatting
            formatting_issues = self.check_formatting_issues(resume_text)
            
            # Calculate overall score (weighted average)
            overall_score = (keyword_match * 0.7) + (structure_score * 0.3)
            
            # Generate recommendations
            recommendations = self.generate_recommendations(
                keyword_match, structure_score, missing_keywords, 
                sections_found, formatting_issues
            )
            
            # Perform skill gap analysis
            skill_gap_analysis = self.analyze_skill_gaps(resume_text, job_description)
            
            return {
                "success": True,
                "overall_score": round(overall_score, 1),
                "keyword_match_score": round(keyword_match, 1),
                "structure_score": round(structure_score, 1),
                "matched_keywords_count": len(matched_keywords),
                "missing_keywords_count": len(missing_keywords),
                "sections_found": sections_found,
                "recommendations": recommendations,
                "top_matched_keywords": matched_keywords[:10],
                "top_missing_keywords": missing_keywords[:10],
                "skill_gap_analysis": skill_gap_analysis
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "overall_score": 0,
                "recommendations": [f"❌ Error analyzing resume: {str(e)}"]
            }
