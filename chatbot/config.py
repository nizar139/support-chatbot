import os

# For API keys, you can either add them in the environment variables, or add a default value for os.getenv

OPENAI_KEY = os.getenv("OPENAI_KEY", "")
HUGGINFACEHUB_API_TOKEN = os.getenv("HUGGINFACEHUB_API_TOKEN", "")


# LLM_PROVIDER = "openai"
LLM_PROVIDER = "huggingface"

# repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"


vector_db_dir = "./vector_db"
documents_parent_dir = "./"