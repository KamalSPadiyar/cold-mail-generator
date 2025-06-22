import streamlit as st
import pdfplumber
from docx import Document
from chains import Chain
import os
from dotenv import load_dotenv
import base64
from sidebar import create_sidebar
from job_search import display_job_search_interface, display_job_insights

# Load environment variables
load_dotenv()

def add_custom_css():
    """Add custom CSS for professional styling"""
    st.markdown("""    <style>    /* Main app styling with light background */
    .stApp {
        background: #f8f9fa;
    }
    
    /* Header styling */
    .main-header {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    
    .main-title {
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    /* Form container */
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
        border: 1px solid #e5e7eb;
    }
    
    /* Results container */
    .results-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 2rem;
        border: 1px solid #e5e7eb;
    }
    
    /* Job search results */
    .job-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    
    .job-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    .job-title {
        color: #1f2937;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .job-company {
        color: #4f46e5;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .job-location {
        color: #6b7280;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .job-link {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 500;
        display: inline-block;
        transition: all 0.2s ease;
    }
    
    .job-link:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        text-decoration: none;
        color: white !important;
    }
    
    /* Progress text */
    .progress-text {
        color: #6b7280;
        font-style: italic;
        margin-top: 0.5rem;
    }
    
    /* Email output styling */
    .email-output {
        background: #f8fafc;
        border-left: 4px solid #4f46e5;
        padding: 1.5rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        line-height: 1.6;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
    }
    
    /* Download link styling */
    .download-link {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        margin-top: 1rem;
        transition: transform 0.2s;
        font-weight: 500;
    }
    
    .download-link:hover {
        transform: translateY(-2px);
        text-decoration: none;
        color: white !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    .stSelectbox > div > div > select {
        border: 1px solid #d1d5db;
        border-radius: 8px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        border-color: transparent;
    }
    
    /* Hide Streamlit elements */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Copy button styling */
    .copy-button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        padding: 8px 16px !important;
        border-radius: 20px !important;
        cursor: pointer !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        margin: 4px 0 !important;
    }
    
    .copy-button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
    }
    
    .copy-success {
        background: linear-gradient(135deg, #059669, #047857) !important;
    }
    
    /* Job summary section styling */
    .job-summary {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .job-summary h3 {
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    .job-link-item {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.2s ease;
    }
    
    .job-link-item:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* ...existing code... */
    </style>
    """, unsafe_allow_html=True)

def create_download_link(content, filename):
    """Create a download link for the generated email"""
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}" class="download-link">📥 Download Email</a>'
    return href

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def generate_cold_email_interface():
    """Cold email generation interface"""
    
    # Main Form Container
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 👤 Personal Information")
            name = st.text_input(
                "Full Name",
                placeholder="Enter your full name (e.g., John Smith)",
                help="This will be used to personalize your email",
                key="email_name"
            )
            
            st.markdown("### 🎯 Job Details")
            # Check if URL was pre-filled from job search
            default_url = st.session_state.get('prefilled_url', '')
            job_url = st.text_input(
                "Job Posting URL",
                value=default_url,
                placeholder="https://company.com/careers/job-posting",
                help="Paste the complete URL of the job posting",
                key="email_job_url"
            )
            
        with col2:
            st.markdown("### ⚙️ Configuration")
            tone = st.selectbox(
                "Email Tone",
                ["Professional", "Formal", "Friendly", "Casual"],
                help="Choose the tone that matches the company culture",
                key="email_tone"
            )
            
            language = st.selectbox(
                "Language",
                ["English"],
                help="Currently supporting English language",
                key="email_language"
            )
            
            # Add some features showcase
            st.markdown("### ✨ Features")
            features = [
                "🎯 AI-Powered Personalization",
                "📄 Resume Analysis", 
                "🌐 URL Scraping",
                "💼 Professional Templates"
            ]
            for feature in features:
                st.markdown(f"**{feature}**")
        
        st.markdown("### 📄 Resume Upload")
        resume_file = st.file_uploader(
            "Upload Your Resume",
            type=["pdf", "docx"],
            help="Upload your resume in PDF or DOCX format. The AI will analyze your experience and skills.",
            accept_multiple_files=False,
            key="email_resume"
        )
        
        if resume_file:
            st.success(f"✅ Resume uploaded: {resume_file.name}")
            file_size = len(resume_file.getvalue()) / 1024  # Size in KB
            st.caption(f"File size: {file_size:.1f} KB")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate Button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button(
            "🚀 Generate Professional Cold Email",
            type="primary",
            use_container_width=True,
            key="generate_email_btn"
        )
    
    # Processing and Results
    if generate_button:
        if not name.strip():
            st.error("❌ Please enter your full name")
            return
        if not job_url.strip():
            st.error("❌ Please enter a valid job posting URL")
            return
        if resume_file is None:
            st.error("❌ Please upload your resume")
            return

        # Show progress
        progress_container = st.container()
        
        with progress_container:
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            
            # Step 1: Resume Processing
            with st.spinner("📄 Analyzing your resume..."):
                progress_bar = st.progress(0)
                st.markdown('<p class="progress-text">Extracting and analyzing resume content</p>', unsafe_allow_html=True)
                
                try:
                    if resume_file.type == "application/pdf":
                        resume_text = extract_text_from_pdf(resume_file)
                    elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        resume_text = extract_text_from_docx(resume_file)
                    else:
                        st.error("❌ Unsupported file format. Please upload PDF or DOCX.")
                        return
                    
                    if not resume_text.strip():
                        st.error("❌ Could not extract text from your resume. Please check the file.")
                        return
                    
                    progress_bar.progress(33)
                        
                except Exception as e:
                    st.error(f"❌ Failed to extract resume text: {e}")
                    return

            # Step 2: Job Description Scraping
            with st.spinner("🌐 Analyzing job posting..."):
                st.markdown('<p class="progress-text">Scraping and processing job description</p>', unsafe_allow_html=True)
                
                try:
                    chain = Chain(name=name, tone=tone, resume_text=resume_text, language=language)
                    job_description = chain.scrape_job_description(job_url)
                    progress_bar.progress(66)
                    
                except Exception as e:
                    st.error(f"❌ Failed to scrape job URL: {e}")
                    st.info("💡 Make sure the URL is accessible and contains a job description")
                    return

            # Step 3: Email Generation
            with st.spinner("🤖 Generating personalized cold email..."):
                st.markdown('<p class="progress-text">Creating your personalized cold email</p>', unsafe_allow_html=True)
                
                try:
                    email = chain.write_mail(job_description)
                    progress_bar.progress(100)
                    
                    # Success message
                    st.success("✅ Your professional cold email is ready!")
                    
                    # Display the email
                    st.markdown("### 📧 Generated Cold Email")
                    st.markdown('<div class="email-output">', unsafe_allow_html=True)
                    st.write(email)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download link
                    download_link = create_download_link(email, f"cold_email_{name.replace(' ', '_')}.txt")
                    st.markdown(download_link, unsafe_allow_html=True)
                    
                    # Copy to clipboard
                    st.code(email, language=None)
                    
                    # Additional tips
                    with st.expander("💡 Email Sending Tips", expanded=False):
                        st.markdown("""
                        **Best Practices for Cold Emails:**
                        - Send between 9 AM - 11 AM or 2 PM - 4 PM
                        - Follow up after 5-7 business days
                        - Keep subject line under 50 characters
                        - Personalize the email for each recipient
                        - Include a clear call-to-action
                        - Keep it concise (under 150 words)
                        """)
                    
                except Exception as e:
                    st.error(f"❌ Failed to generate email: {e}")
                    return
            
            st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Page configuration
    st.set_page_config(
        page_title="Professional Cold Mail Generator",
        page_icon="📧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS
    add_custom_css()
    
    # Create professional sidebar
    create_sidebar()
    
    # Header Section
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">✉️ Professional Cold Mail Generator</h1>
        <p class="subtitle">Create compelling, personalized cold emails that get responses</p>
        <p style="color: #888; font-size: 0.9rem;">Powered by Advanced AI • Secure • Professional</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for API key
    if not os.getenv("GROQ_API_KEY") and "GROQ_API_KEY" not in st.secrets:
        st.error("🔐 API Configuration Required")
        st.info("💡 Please configure your GROQ API key in environment variables or Streamlit secrets")
        st.markdown("**For local development:** Add `GROQ_API_KEY` to your `.env` file")
        return

    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["✉️ Generate Cold Email", "🔍 Job Search Assistant"])
    
    with tab1:
        # Cold email generation functionality
        generate_cold_email_interface()
    
    with tab2:
        # Job search functionality
        st.markdown("### 🎯 Find Jobs in Your Domain")
        selected_domain = display_job_search_interface()
        
        # Show domain insights
        if selected_domain:
            display_job_insights(selected_domain)
        
        # Check if a job URL was selected from job search
        if 'selected_job_url' in st.session_state:
            st.markdown("---")
            st.markdown("### ✉️ Generate Email for Selected Job")
            st.info(f"🎯 **Selected Job:** {st.session_state.get('selected_job_title', 'Unknown')}")
            st.write(f"**URL:** {st.session_state['selected_job_url']}")
            
            # Pre-fill the email generation form
            if st.button("📝 Generate Email for This Job", type="primary"):
                st.session_state['prefilled_url'] = st.session_state['selected_job_url']
                # Clear the selection
                del st.session_state['selected_job_url']
                if 'selected_job_title' in st.session_state:
                    del st.session_state['selected_job_title']
                st.success("✅ Job URL copied! Please switch to 'Generate Cold Email' tab and upload your resume.")
                st.rerun()

    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.8rem; padding: 2rem;">
        Made with ❤️ using Streamlit & AI • Secure & Professional • 
        <a href="https://github.com/KamalSPadiyar/cold-mail-generator" target="_blank" style="color: #667eea;">View Source Code</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
