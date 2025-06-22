import streamlit as st

def create_sidebar():
    """Create a professional sidebar with app information and settings"""
    
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;">
            <h2 style="color: white; margin: 0;">✉️ Cold Mail Pro</h2>
            <p style="color: #f0f0f0; margin: 0; font-size: 0.9rem;">AI-Powered Email Generator</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 App Features")
        features = [
            ("🤖", "AI-Powered", "Advanced language models"),
            ("🎯", "Personalized", "Tailored to job requirements"),
            ("📄", "Resume Analysis", "Extracts relevant skills"),
            ("🔒", "Secure", "No data stored permanently"),
            ("⚡", "Fast", "Generate emails in seconds"),
            ("📱", "Responsive", "Works on all devices")
        ]
        
        for icon, title, desc in features:
            st.markdown(f"""
            <div style="background: white; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #667eea;">
                <strong>{icon} {title}</strong><br>
                <small style="color: #666;">{desc}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📈 Usage Statistics")
        # Simulated statistics (in real app, these would come from database)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Emails Generated", "1,247", "↗️ 12%")
        with col2:
            st.metric("Success Rate", "94%", "↗️ 2%")
        
        st.markdown("---")
        
        st.markdown("### 💡 Pro Tips")
        tips = [
            "Keep emails under 150 words",
            "Research the company culture",
            "Personalize the subject line",
            "Include a clear call-to-action",
            "Follow up after 1 week"
        ]
        
        for i, tip in enumerate(tips, 1):
            st.markdown(f"**{i}.** {tip}")
        
        st.markdown("---")
        
        st.markdown("### 🔗 Resources")
        st.markdown("""
        - [📚 Email Best Practices](https://example.com)
        - [🎯 Job Search Tips](https://example.com)
        - [💼 Resume Templates](https://example.com)
        - [🤝 Networking Guide](https://example.com)
        """)
        
        st.markdown("---")
        
        st.markdown("""
        <div style="text-align: center; font-size: 0.8rem; color: #666; padding: 1rem;">
            <p>Made with ❤️ by <strong>Kamal Padiyar</strong></p>
            <p>Version 2.0 • Professional Edition</p>
        </div>
        """, unsafe_allow_html=True)
