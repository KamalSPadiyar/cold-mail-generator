import requests
from bs4 import BeautifulSoup
import streamlit as st
from urllib.parse import quote_plus
import time

class JobSearcher:
    def __init__(self):
        self.job_sites = {
            "LinkedIn": "https://www.linkedin.com/jobs/search/?keywords={}&location={}&f_E=2,3",
            "Indeed": "https://www.indeed.com/jobs?q={}&l={}",
            "Glassdoor": "https://www.glassdoor.com/Job/jobs.htm?sc.keyword={}&locT=C&locId={}",
            "AngelList": "https://angel.co/jobs?keywords={}&location={}",
            "RemoteOK": "https://remoteok.io/remote-{}-jobs",
            "WeWorkRemotely": "https://weworkremotely.com/remote-jobs/search?term={}",        }
        
        self.domain_keywords = {
            "Data Science": ["data scientist", "machine learning engineer", "data analyst", "ML engineer", "AI researcher", "data science intern"],
            "Finance": ["financial analyst", "investment banker", "portfolio manager", "risk analyst", "quantitative analyst", "finance intern"],
            "Software Engineering": ["software engineer", "full stack developer", "backend developer", "frontend developer", "DevOps engineer", "software engineering intern"],
            "Marketing": ["digital marketing", "content marketing", "marketing manager", "SEO specialist", "social media manager", "marketing intern"],
            "Product Management": ["product manager", "product owner", "product analyst", "growth manager", "business analyst", "product management intern"],
            "Consulting": ["management consultant", "strategy consultant", "business consultant", "IT consultant", "consulting intern"],
            "Healthcare": ["healthcare analyst", "medical device", "pharmaceutical", "biotech", "clinical research", "healthcare intern"],
            "Cybersecurity": ["cybersecurity analyst", "security engineer", "penetration tester", "information security", "cybersecurity intern"],
            "UX/UI Design": ["UX designer", "UI designer", "product designer", "visual designer", "user researcher", "design intern"],            "Sales": ["sales manager", "account executive", "business development", "sales representative", "sales intern"]
        }

    def get_job_suggestions(self, domain, location="United States", experience_level="entry", job_type="Full-time"):
        """Get job suggestions based on domain and preferences"""
        if domain not in self.domain_keywords:
            return []
        
        keywords = self.domain_keywords[domain]
        
        # Filter keywords based on job type
        if job_type.lower() == "internship":
            keywords = [k for k in keywords if "intern" in k.lower()]
            if not keywords:  # If no intern-specific keywords, add "intern" to general keywords
                keywords = [f"{k} intern" for k in self.domain_keywords[domain][:3]]
        else:
            keywords = [k for k in keywords if "intern" not in k.lower()]
        
        job_suggestions = []
        
        for keyword in keywords[:3]:  # Limit to top 3 keywords
            # Add job type to search query
            search_query = keyword
            if job_type.lower() != "full-time":
                search_query += f" {job_type.lower()}"
            
            for site_name, site_url in list(self.job_sites.items())[:4]:  # Limit to top 4 sites
                try:
                    if site_name == "RemoteOK":
                        formatted_url = site_url.format(quote_plus(search_query.replace(" ", "-")))
                    elif site_name == "WeWorkRemotely":
                        formatted_url = site_url.format(quote_plus(search_query))
                    else:
                        formatted_url = site_url.format(quote_plus(search_query), quote_plus(location))
                    
                    job_suggestions.append({
                        "title": f"{keyword.title()} ({job_type}) - {site_name}",
                        "url": formatted_url,
                        "site": site_name,
                        "keyword": keyword,
                        "job_type": job_type
                    })
                except Exception as e:
                    continue
        
        return job_suggestions

    def search_specific_jobs(self, domain, company_name="", location="United States"):
        """Search for specific jobs with company filter"""
        if domain not in self.domain_keywords:
            return []
        
        keywords = self.domain_keywords[domain]
        specific_jobs = []
        
        # Create search queries
        for keyword in keywords[:2]:
            search_query = keyword
            if company_name:
                search_query += f" {company_name}"
            
            # LinkedIn search
            linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(search_query)}&location={quote_plus(location)}"
            
            # Indeed search
            indeed_url = f"https://www.indeed.com/jobs?q={quote_plus(search_query)}&l={quote_plus(location)}"
            
            specific_jobs.extend([
                {
                    "title": f"{keyword.title()}" + (f" at {company_name}" if company_name else ""),
                    "url": linkedin_url,
                    "site": "LinkedIn",
                    "keyword": keyword
                },
                {
                    "title": f"{keyword.title()}" + (f" at {company_name}" if company_name else ""),
                    "url": indeed_url,
                    "site": "Indeed", 
                    "keyword": keyword
                }
            ])
        
        return specific_jobs

    def get_trending_companies(self, domain):
        """Get trending companies for a specific domain"""
        company_mapping = {
            "Data Science": ["Google", "Meta", "Netflix", "Uber", "Airbnb", "Microsoft", "Amazon", "Apple", "Tesla", "Spotify"],
            "Finance": ["Goldman Sachs", "JPMorgan Chase", "Morgan Stanley", "BlackRock", "Citadel", "Two Sigma", "Robinhood", "Stripe"],
            "Software Engineering": ["Google", "Meta", "Amazon", "Microsoft", "Apple", "Tesla", "Stripe", "Spotify", "Netflix", "Uber"],
            "Marketing": ["HubSpot", "Salesforce", "Adobe", "Shopify", "Buffer", "Hootsuite", "Canva", "Mailchimp"],
            "Product Management": ["Google", "Meta", "Amazon", "Uber", "Airbnb", "Slack", "Zoom", "Spotify", "Pinterest", "Dropbox"],
            "Consulting": ["McKinsey", "BCG", "Bain", "Deloitte", "PwC", "EY", "KPMG", "Accenture"],
            "Healthcare": ["Johnson & Johnson", "Pfizer", "Moderna", "Roche", "Novartis", "Merck", "Gilead", "Amgen"],
            "Cybersecurity": ["CrowdStrike", "Palo Alto Networks", "Fortinet", "Okta", "Zscaler", "SentinelOne", "Rapid7", "Varonis"],
            "UX/UI Design": ["Adobe", "Figma", "Canva", "Spotify", "Airbnb", "Uber", "Pinterest", "Dribbble"],
            "Sales": ["Salesforce", "HubSpot", "Oracle", "SAP", "Zoom", "Slack", "Outreach", "Gong"]
        }
        
        return company_mapping.get(domain, [])

def display_job_search_interface():
    """Display the job search interface"""
    st.markdown("## 🔍 Job Search Assistant")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Domain selection
        selected_domain = st.selectbox(
            "🎯 Select Your Domain",
            options=list(JobSearcher().domain_keywords.keys()),
            help="Choose the field you want to search jobs in"
        )
        
        # Location input
        location = st.text_input(
            "📍 Location",
            value="United States",
            help="Enter city, state, or country"
        )
          # Experience level
        experience_level = st.selectbox(
            "💼 Experience Level",
            ["Entry Level", "Mid Level", "Senior Level", "Executive"],
            help="Select your experience level"
        )
        
        # Job type selection
        job_type = st.selectbox(
            "🎯 Job Type",
            ["Full-time", "Part-time", "Internship", "Contract"],
            help="Select the type of position you're looking for"
        )
    
    with col2:
        # Company filter (optional)
        company_filter = st.text_input(
            "🏢 Company (Optional)",
            placeholder="e.g., Google, Microsoft",
            help="Filter jobs by specific company"
        )
        
        # Remote work preference
        remote_preference = st.selectbox(
            "🏠 Work Preference",
            ["Any", "Remote Only", "Hybrid", "On-site"],
            help="Choose work arrangement preference"
        )
      # Search button
    if st.button("🔍 Find Jobs", type="primary", use_container_width=True):
        job_searcher = JobSearcher()
        
        with st.spinner("🔄 Searching for jobs..."):
            # Get job suggestions
            if company_filter:
                job_suggestions = job_searcher.search_specific_jobs(
                    selected_domain, 
                    company_filter, 
                    location
                )
            else:
                job_suggestions = job_searcher.get_job_suggestions(
                    selected_domain, 
                    location, 
                    experience_level.lower().replace(" ", "_"),
                    job_type                )
        
        if job_suggestions:
            st.success(f"✅ Found {len(job_suggestions)} job opportunities!")
            
            # Display job suggestions with helpful tip
            st.markdown("### 📋 Job Opportunities")
            st.info("💡 **Tip:** All job links below are ready to use! Click on them to view the positions or use 'Generate Email' to create a personalized cold email.")
            
            for i, job in enumerate(job_suggestions[:8]):  # Limit to 8 results
                with st.container():
                    # Create a card-like layout
                    st.markdown(f"""
                    <div style="
                        background: white;
                        padding: 1.5rem;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        margin-bottom: 1rem;
                        border-left: 4px solid #667eea;
                    ">
                        <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">
                            🔗 {job['title']}
                        </h4>
                        <p style="margin: 0.25rem 0; color: #7f8c8d;">
                            <strong>Site:</strong> {job['site']} | 
                            <strong>Keywords:</strong> {job['keyword']} | 
                            <strong>Type:</strong> {job.get('job_type', 'Full-time')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                      # Action buttons
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"**🌐 Job Link:** [Open Position]({job['url']})")
                    
                    with col2:
                        # Create a unique ID for each job URL
                        url_id = f"job_url_{i}"
                        
                        # Add hidden input field and copy button with JavaScript
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <input type="text" id="{url_id}" value="{job['url']}" style="opacity: 0; position: absolute; left: -9999px;" readonly>
                            <button onclick="copyToClipboard('{url_id}')" style="
                                background: linear-gradient(135deg, #10b981, #059669);
                                color: white;
                                border: none;
                                padding: 8px 16px;
                                border-radius: 20px;
                                cursor: pointer;
                                font-size: 0.9rem;
                                font-weight: 500;
                                transition: all 0.2s ease;
                            " onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 12px rgba(16, 185, 129, 0.3)'" 
                               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                                📋 Copy Link
                            </button>
                        </div>
                        
                        <script>
                        function copyToClipboard(elementId) {{
                            const element = document.getElementById(elementId);
                            element.select();
                            element.setSelectionRange(0, 99999);
                            
                            try {{
                                document.execCommand('copy');
                                
                                // Show success message
                                const button = event.target;
                                const originalText = button.innerHTML;
                                button.innerHTML = '✅ Copied!';
                                button.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                                
                                setTimeout(() => {{
                                    button.innerHTML = originalText;
                                    button.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                                }}, 2000);
                                
                            }} catch (err) {{
                                // Fallback for older browsers
                                navigator.clipboard.writeText(element.value).then(() => {{
                                    const button = event.target;
                                    const originalText = button.innerHTML;
                                    button.innerHTML = '✅ Copied!';
                                    
                                    setTimeout(() => {{
                                        button.innerHTML = originalText;
                                    }}, 2000);
                                }});
                            }}
                        }}
                        </script>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        if st.button(f"✉️ Generate Email", key=f"email_{i}"):
                            st.session_state['selected_job_url'] = job['url']
                            st.session_state['selected_job_title'] = job['title']
                            st.success("✅ Job selected! Switch to 'Generate Cold Email' tab.")
                            st.rerun()
              # Show trending companies
            trending_companies = job_searcher.get_trending_companies(selected_domain)
            if trending_companies:
                st.markdown("### 🏆 Trending Companies")
                
                cols = st.columns(4)
                for i, company in enumerate(trending_companies[:8]):
                    with cols[i % 4]:
                        if st.button(f"🏢 {company}", key=f"company_{i}"):
                            # Set company filter and rerun search
                            st.session_state['company_filter'] = company
                            st.rerun()
              # Add a summary section with all job links
            st.markdown("---")
            st.markdown("### 📝 Quick Copy - All Job Links")
            st.markdown("**Click any link below to copy it directly:**")
            
            # Create a container for all links with copy functionality
            for i, job in enumerate(job_suggestions[:8]):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{i+1}.** {job['title']}")
                    st.caption(f"🏢 {job['site']} | 🎯 {job.get('job_type', 'Full-time')} | 🔗 [Direct Link]({job['url']})")
                
                with col2:
                    # Quick copy button for each job
                    quick_url_id = f"quick_job_url_{i}"
                    st.markdown(f"""
                    <div style="margin-top: 8px;">
                        <input type="text" id="{quick_url_id}" value="{job['url']}" style="opacity: 0; position: absolute; left: -9999px;" readonly>
                        <button onclick="copyToClipboard('{quick_url_id}')" style="
                            background: linear-gradient(135deg, #6366f1, #8b5cf6);
                            color: white;
                            border: none;
                            padding: 6px 12px;
                            border-radius: 15px;
                            cursor: pointer;
                            font-size: 0.8rem;
                            font-weight: 500;
                            width: 100%;
                        ">
                            📋 Copy URL
                        </button>
                    </div>
                    """, unsafe_allow_html=True)
                
                if i < len(job_suggestions) - 1:
                    st.markdown("")
        
        else:
            st.warning("❌ No jobs found. Try adjusting your search criteria.")
    
    return selected_domain

def display_job_insights(domain):
    """Display insights for the selected domain"""
    insights = {
        "Data Science": {
            "avg_salary": "$95,000 - $165,000",
            "growth_rate": "22% (Much faster than average)",
            "key_skills": ["Python", "SQL", "Machine Learning", "Statistics", "Tableau"],
            "certifications": ["Google Data Analytics", "AWS Machine Learning", "Microsoft Azure AI"]
        },
        "Finance": {
            "avg_salary": "$85,000 - $150,000", 
            "growth_rate": "5% (Average)",
            "key_skills": ["Excel", "Financial Modeling", "Bloomberg Terminal", "SQL", "Python"],
            "certifications": ["CFA", "FRM", "CPA", "Financial Modeling & Valuation"]
        },
        "Software Engineering": {
            "avg_salary": "$90,000 - $180,000",
            "growth_rate": "25% (Much faster than average)",
            "key_skills": ["JavaScript", "Python", "React", "Node.js", "Cloud Services"],
            "certifications": ["AWS Solutions Architect", "Google Cloud Professional", "Microsoft Azure"]
        },
        "Marketing": {
            "avg_salary": "$65,000 - $120,000",
            "growth_rate": "10% (Faster than average)", 
            "key_skills": ["Google Analytics", "SEO", "Content Marketing", "Social Media", "PPC"],
            "certifications": ["Google Ads", "HubSpot", "Facebook Blueprint", "Google Analytics"]
        },
        "Product Management": {
            "avg_salary": "$100,000 - $170,000",
            "growth_rate": "15% (Much faster than average)",
            "key_skills": ["Product Strategy", "Data Analysis", "User Research", "Agile", "SQL"],
            "certifications": ["Product School PM", "Google Product Management", "Scrum Master"]
        }
    }
    
    if domain in insights:
        insight = insights[domain]
        
        st.markdown("### 📊 Domain Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "💰 Average Salary",
                insight["avg_salary"]
            )
        
        with col2:
            st.metric(
                "📈 Job Growth Rate",
                insight["growth_rate"]
            )
        
        with col3:
            st.metric(
                "🔧 Key Skills Count",
                len(insight["key_skills"])
            )
        
        # Skills and certifications
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🛠️ Key Skills:**")
            for skill in insight["key_skills"]:
                st.write(f"• {skill}")
        
        with col2:
            st.markdown("**🎓 Recommended Certifications:**")
            for cert in insight["certifications"]:
                st.write(f"• {cert}")
