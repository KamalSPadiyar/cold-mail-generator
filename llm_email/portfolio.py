class Portfolio:
    def __init__(self):
        # Predefined portfolio links with associated tags/skills
        self.projects = [
            {
                "title": "AI Resume Analyzer",
                "url": "https://github.com/username/ai-resume-analyzer",
                "tags": ["AI", "machine learning", "NLP", "resume"]
            },
            {
                "title": "Personal Website",
                "url": "https://username.github.io",
                "tags": ["web development", "portfolio", "React"]
            },
            {
                "title": "Chatbot Assistant",
                "url": "https://github.com/username/chatbot-assistant",
                "tags": ["chatbot", "AI", "dialogue systems"]
            },
            {
                "title": "Grammar Scoring Engine",
                "url": "https://github.com/username/grammar-scoring",
                "tags": ["NLP", "grammar", "scoring"]
            },
        ]

    def load_portfolio(self):
        # Placeholder for loading from file/db if needed in future
        pass

    def query_links(self, skills):
        # Given a list of skills, return matching project links as a comma-separated string
        matched_links = []
        skills_lower = set(skill.lower() for skill in skills)

        for project in self.projects:
            project_tags = set(tag.lower() for tag in project["tags"])
            if skills_lower & project_tags:
                matched_links.append(f"[{project['title']}]({project['url']})")

        if not matched_links:
            # Return some default links if no match found
            matched_links = [f"[{p['title']}]({p['url']})" for p in self.projects[:2]]

        return ", ".join(matched_links)
