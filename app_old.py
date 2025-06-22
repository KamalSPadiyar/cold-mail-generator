import streamlit as st
import pdfplumber
from docx import Document
from chains import Chain
import os
from dotenv import load_dotenv
import base64
from io import BytesIO
from sidebar import create_sidebar
from job_search import display_job_search_interface, display_job_insights

# Load environment variables
load_dotenv()

def add_custom_css():
    """Add custom CSS for professional styling"""
    st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    /* Form container */
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Custom button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.2);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    /* File uploader */
    .uploadedFile {
        border-radius: 10px;
        border: 2px dashed #667eea;
        padding: 1rem;
    }
    
    /* Results container */
    .results-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    
    /* Progress indicators */
    .progress-text {
        text-align: center;
        color: #667eea;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
        # Original email generation functionality
        generate_cold_email_interface()
    
    with tab2:
        # New job search functionality
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
            if st.button("📝 Generate Email for This Job", type="primary"):                st.session_state['prefilled_url'] = st.session_state['selected_job_url']
                # Switch to email generation tab
                st.success("✅ Job URL copied! Please switch to 'Generate Cold Email' tab and upload your resume.")

def generate_cold_email_interface():
    """Original cold email generation interface"""
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
            accept_multiple_files=False
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
            use_container_width=True
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
                    st.success("✅ Resume analyzed successfully")
                        
                except Exception as e:
                    st.error(f"❌ Failed to process resume: {e}")
                    return

            # Step 2: Job Scraping
            with st.spinner("🌐 Fetching job description..."):
                st.markdown('<p class="progress-text">Scraping job posting details</p>', unsafe_allow_html=True)
                
                try:
                    chain = Chain(name=name, tone=tone, resume_text=resume_text, language=language)
                    job_description = chain.scrape_job_description(job_url)
                    progress_bar.progress(66)
                    st.success("✅ Job description retrieved successfully")
                except Exception as e:
                    st.error(f"❌ Failed to fetch job description: {e}")
                    st.info("💡 Please ensure the URL is accessible and contains a valid job posting")
                    return

            # Step 3: Email Generation
            with st.spinner("🤖 Generating your personalized cold email..."):
                st.markdown('<p class="progress-text">Creating personalized cold email with AI</p>', unsafe_allow_html=True)
                
                try:
                    email = chain.write_mail(job_description)
                    progress_bar.progress(100)
                    
                    # Success message
                    st.markdown('''
                    <div class="success-message">
                        🎉 Your professional cold email has been generated successfully!
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Display results
                    st.markdown("### 📧 Your Generated Cold Email")
                    
                    # Email preview with copy functionality
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.text_area(
                            "Email Content",
                            email,
                            height=400,
                            help="Copy this content to your email client"
                        )
                    
                    with col2:
                        st.markdown("### 📊 Email Analysis")
                        
                        # Simple email metrics
                        word_count = len(email.split())
                        char_count = len(email)
                        
                        st.metric("Word Count", word_count)
                        st.metric("Character Count", char_count)
                        
                        if word_count < 100:
                            st.info("💡 Consider adding more details")
                        elif word_count > 200:
                            st.warning("⚠️ Email might be too long")
                        else:
                            st.success("✅ Optimal length")
                        
                        # Download link
                        download_link = create_download_link(email, f"cold_email_{name.replace(' ', '_')}.txt")
                        st.markdown(download_link, unsafe_allow_html=True)
                    
                    # Tips section
                    st.markdown("### 💡 Professional Tips")
                    tips_col1, tips_col2 = st.columns(2)
                    
                    with tips_col1:
                        st.markdown("""
                        **✅ Before Sending:**
                        - Review and personalize further
                        - Check company name and details
                        - Verify contact information
                        - Proofread for typos
                        """)
                    
                    with tips_col2:
                        st.markdown("""
                        **🚀 Best Practices:**
                        - Send during business hours
                        - Follow up after 1 week
                        - Keep it concise and focused
                        - Include a clear call-to-action
                        """)
                    
                except Exception as e:
                    st.error(f"❌ Failed to generate email: {e}")
                    return
            
            st.markdown('</div>', unsafe_allow_html=True)
    
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
