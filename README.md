# Supoort Chatbot

This is a python project for a support chatbot, that uses knowledge from severel pages of Madkudu's support website : https://support.madkudu.com/hc/en-us

## How Does it work :

### The RAG approach :

Retrieval augmented generation, or RAG, is an architectural approach that can improve the efficacy of large language model (LLM) applications by leveraging custom data. This is done by retrieving data/documents relevant to a question or task and providing them as context for the LLM.


![image](https://github.com/nizar139/support-chatbot/assets/93913464/03b6b43a-fa43-4810-9c9b-4de5df2cebae)


In our context, the RAG apprach can enable us to create a support chatbot that can answer the user accurately using Madkudu's knowledge and documentation in the [support website](https://support.madkudu.com/hc/en-us)

### The vector store :

We use a static vector store, created using the script create_vector_store, where chunks are stored as Embeddings (vectors), for that purpose we use HuggingFace embeddings, which are easy to access and use.

## How to run the files

### Preparations

This project uses poetry for dependency management, please refer to their [website](https://python-poetry.org/docs/) in order to install it.

Once poetry is installed, from the root directory of the project ,use the following command to prepare and activate a virtual environment  :

```
poetry install
poetry shell
```

Before being able to run the code, you need to either have an OPENAI API KEY or a HUGGINGFACE API TOKEN.

You can either add these in your environment variables, using the names `OPENAI_KEY` or `HUGGINFACEHUB_API_TOKEN`
or you can put them in config.py in the designated place :

```
OPENAI_KEY = os.getenv("OPENAI_KEY", "your key")                               
HUGGINFACEHUB_API_TOKEN = os.getenv("HUGGINFACEHUB_API_TOKEN", "your token") 
```

For each provider, you need to change `LLM_PROVIDER` in `config.py` accordinly 
```
providers = ["openai","huggingface"]
LLM_PROVIDER = "your provider from the list"
``` 

### run the streamlit app 

in a terminal where the poetry env is activated, make sure that you are in the root directory of the project, some directory names variables won't work otherwise, then :
```
streamlit run  .\chatbot\front.py
```
to stop the app you need to press `ctrl+c` in the used terminal

### run a console chatbot

in a terminal where the poetry env is activated, make sure that you are in the root directory of the project, some directory names variables won't work otherwise, then :
```
python  .\chatbot\chatbot.py
```
to stop the app you can either input `q` or `quit`.

### Update the vector database 

This project uses a Chroma vector database that includes relevant knowledge from Madkudu's support website. the vector database is in the directory vector_db

the script `create_vector_database.py` takes all the pdf files in the documents directory, and recreates a vector database using the knowledge in these documents.
in order to run it, make sure you placed to pdf files you want to be included in documents directory.

in a terminal where the poetry env is activated, make sure that you are in the root directory of the project, some directory names variables won't work otherwise, then :
```
python  .\chatbot\create_vector_store.py
```

