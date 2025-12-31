import os
from dotenv import load_dotenv
load_dotenv(override=True)

print("GROQ KEY:", os.getenv("GROQ_API_KEY"))
