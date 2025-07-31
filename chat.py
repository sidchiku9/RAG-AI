from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

# Take User Query
query = input("> ")

# Vector Similarity Search [query] in DB
search_results = vector_db.similarity_search(
    query=query
)

context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
    You are a helpful AI Assistant who answers the user query based on the provided context.
    Retrieved from a PDF file along with page_contents and page number.

    You should only answer the user based on the provided context and navigate the user
    to open the right page number to know more.

    Context:
    {context}
"""

chat_completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": query },
    ]
)

print(f"🤖: {chat_completion.choices[0].message.content}")