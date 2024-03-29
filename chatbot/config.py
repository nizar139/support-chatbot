import os

# For API keys, you can either add them in the environment variables, or add a default value for os.getenv

OPENAI_KEY = os.getenv("OPENAI_KEY", "your key")                               
HUGGINFACEHUB_API_TOKEN = os.getenv("HUGGINFACEHUB_API_TOKEN", "your token")    


providers = ["openai","huggingface"]

LLM_PROVIDER = "huggingface" # use the provider that you have an API key for from the providers list

# repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"


vector_db_dir = "./vector_db"
documents_parent_dir = "./"