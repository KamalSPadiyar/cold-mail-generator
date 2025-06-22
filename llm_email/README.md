# Cold Mail Generator

A Streamlit application that generates personalized cold emails based on job descriptions and resumes.

## Features

- Upload resume (PDF or DOCX format)
- Scrape job descriptions from URLs
- Generate personalized cold emails with different tones
- Secure API key management

## Local Development

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your-groq-api-key-here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Deployment to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free)
- GROQ API key

### Steps

1. **Push your code to GitHub** (without API keys):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Connect your GitHub repository
   - Set main file path to `app.py`
   - Click "Deploy"

3. **Add secrets in Streamlit Cloud**:
   - In your Streamlit Cloud dashboard, go to your app
   - Click on "Manage app" → "Settings" → "Secrets"
   - Add your secrets in TOML format:
     ```toml
     GROQ_API_KEY = "your-actual-groq-api-key-here"
     ```
   - Save the secrets

4. **Your app will automatically redeploy** with the new secrets.

## Security Notes

- ✅ API keys are stored securely in Streamlit Cloud secrets
- ✅ `.env` file is ignored by Git (never committed)
- ✅ No hardcoded API keys in the source code
- ✅ Environment variables used for local development

## Tech Stack

- **Frontend**: Streamlit
- **LLM**: GROQ (Llama 3)
- **Document Processing**: pdfplumber, python-docx
- **Web Scraping**: BeautifulSoup, requests
- **Deployment**: Streamlit Cloud

## File Structure

```
├── app.py                 # Main Streamlit application
├── chains.py             # LLM chain logic
├── portfolio.py          # Portfolio management
├── utils.py              # Utility functions
├── my_portfolio.csv      # Portfolio data
├── requirements.txt      # Python dependencies
├── .env                  # Local environment variables (not committed)
├── .gitignore           # Git ignore file
└── .streamlit/
    ├── config.toml       # Streamlit configuration
    └── secrets_template.toml  # Template for secrets
```
