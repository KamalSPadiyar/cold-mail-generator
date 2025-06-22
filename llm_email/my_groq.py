from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-70b-8192"  # or try mixtral or gemma
)

# Test only if API key is available
if os.getenv("GROQ_API_KEY"):
    response = llm.invoke("The first person to land on the moon was ...")
    print(response.content)
else:
    print("GROQ_API_KEY not found in environment variables")
