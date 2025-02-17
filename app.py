import streamlit as st
from openai import OpenAI  # Ensure you have installed the OpenAI library (pip install openai)
import os
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from pinecone import Pinecone, ServerlessSpec
from tqdm.notebook import tqdm
import langchain
import openai
import string
import pandas as pd
import matplotlib.pyplot as plt
from langchain_pinecone import PineconeVectorStore

# Read the OpenAI API key from the file system
with open("open_ai_key.txt", "r") as f:
    openai_key = f.read().strip()

# Read the Pinecone key from the file system (PlusOne.txt)
with open("PlusOne.txt", "r") as f:
    pinecone_key = f.read().strip()

# Initialize OpenAI client
client = OpenAI(api_key=openai_key)
openai_client = client

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_key)
index = pc.Index("plusone")
# Initialize the vectorstore with the Pinecone index and the embeddings

os.environ["OPENAI_API_KEY"] = openai_key
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = PineconeVectorStore(index=index, embedding=embeddings)
st.title("Plus One Foundation Chatbot")

#############################
## Prompt & Query Functions
#############################

def generate_prompt(user_query, context):
    return f'''
    Context:
    {context}

    Instruction:
    You are an assistant that answers user queries based on the provided context related to the Plus One Foundation website, and you answer using the first person (i.e. "We"). 
    If the user's query is a friendly greeting (such as "hello", "hi", "hey", etc.), respond with a welcome message that introduces the Plus One Foundation website and its services, speaking in the first person.
    According to the World Health Organization (WHO), neurological disorders—including epilepsy, Alzheimer’s disease, Traumatic Brain Injury, and Multiple Sclerosis—affect up to one billion people worldwide, regardless of age, sex, education, or income. More than 500 different conditions are considered neurological disorders.
    The Plus One Foundation assists children and adults with a neurological injury, disorder, or disease to achieve goals, expand opportunities, and "feed the soul" through activities that offer education, rehabilitation, and training. The foundation also aids people who have had COVID-19.
    It funds classes, workshops, and life experiences—including art and music therapy, therapeutic horseback riding, integrated movement therapy, martial arts, meditation, yoga, and aquatic therapies—that help individuals along their rehabilitation and recovery journey.
    Using the above information along with the provided context, answer the user's query in the first person:
    - If the query is relevant to the Plus One Foundation website, provide the answer strictly including the sources from the context and URLs.
    - If the query is a friendly greeting, respond with a welcoming introduction to the Plus One Foundation website.
    - Otherwise, respond with: "This query is not relevant to the Plus One Foundation website."
    User Query:
    {user_query}
    '''

def query_pinecone_vector_store(query: str, top_k: int = 10, nameSpace: str = "ns1000"):
    return vector_store.similarity_search(
        query,
        k=top_k,
        namespace=nameSpace
    )

def get_completion(prompt, model="gpt-3.5-turbo"):
    message = {"role": "user", "content": prompt}
    response = openai_client.chat.completions.create(
        model=model,
        messages=[message]
    )
    return response.choices[0].message.content

def query(user_query):
    # Query the Pinecone index in namespace "ns500"
    results = query_pinecone_vector_store(user_query, top_k=5, nameSpace="ns1000")
    context = ""
    related_urls = set()
    # Build context using metadata keys: "url" and "text"
    for result in results:
        url = result.metadata.get('url', 'N/A')
        chunk = result.metadata.get('text', 'N/A')
        context += f"URL: {url} | Chunk: {chunk}\n"
        related_urls.add(url)
    
    prompt = generate_prompt(user_query, context)
    answer = get_completion(prompt)
    urls_string = ", ".join(related_urls)
    return f"{answer}\n\n Learn More: {urls_string}"

#############################
## Streamlit Chatbot Interface
#############################

# Check for existing session state variables
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# Get new user prompt
if prompt := st.chat_input("What would you like to ask about the Plus One Foundation?"):
    # Append user message to the conversation history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Generate AI response using Pinecone context and OpenAI API
    with st.chat_message("assistant"):
        answer = query(prompt)
        st.write(answer)

    # Save the assistant response in session state
    st.session_state.messages.append({"role": "assistant", "content": answer})