from langchain_openai import ChatOpenAI

from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough

from langchain.memory import ChatMessageHistory

from langchain.chains.combine_documents import create_stuff_documents_chain

from config import LLM_PROVIDER, OPENAI_KEY, HUGGINFACEHUB_API_TOKEN, repo_id, vector_db_dir


embeddings = HuggingFaceHubEmbeddings()
vectorstore = Chroma(persist_directory=vector_db_dir, embedding_function=embeddings)
retriever = vectorstore.as_retriever(k=3)


if LLM_PROVIDER=="openai":
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-1106", 
        temperature=0.2, 
        openai_api_key=OPENAI_KEY)
else :
    chat = HuggingFaceEndpoint(
            repo_id=repo_id, 
            temperature =  0.8, 
            huggingfacehub_api_token=HUGGINFACEHUB_API_TOKEN
        )


prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You act as a customer service assistant working for Madkudu. Answer the user's question using exlusively the chat history and the pieces of context, if you don't know the response, kindly say so. \nContext:\n\n{context} ",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

query_transform = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="messages"),
        (
            "user",
            "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation. Only respond with the query, nothing else.",
        ),
    ]
)

retriever_chain = RunnableBranch(
    (
        lambda x: len(x.get("messages", [])) == 1,
        # If only one message, then we just pass that message's content to retriever
        (lambda x: x["messages"][-1].content) | retriever,
    ),
    # If messages, then we pass inputs to LLM chain to transform the query, then pass to retriever
    query_transform | chat | StrOutputParser() | retriever,
).with_config(run_name="chat_retriever_chain")

document_chain = create_stuff_documents_chain(chat, prompt)

conversational_retrieval_chain = RunnablePassthrough.assign(
    context=retriever_chain,
    ).assign(
    answer=document_chain,
)


class RAG():
    def __init__(self):
        self.chat_history = ChatMessageHistory()
        
    def clear_history(self):
        self.chat_history = ChatMessageHistory()
        
    def handle_user_input(self, user_input):
        changed_input = f"[INST] {user_input} [/INST]"  # since we use mistral instruct we need to and [INST] and [/INST]
        self.chat_history.add_user_message(changed_input)
        response = conversational_retrieval_chain.invoke(
            {"messages": self.chat_history.messages},
        )
        answer = response["answer"]
        context = response["context"]
        self.chat_history.add_ai_message(answer)
        return answer, context

if __name__ == "__main__":
    
    rag_chatbot = RAG()
    
    while True :
        user_input = str(input("write a msg :\n"))
        
        if user_input == 'quit' or user_input =='q':
            print('shutting down')
            break
        answer, context = rag_chatbot.handle_user_input(user_input)
        
        print(answer)
