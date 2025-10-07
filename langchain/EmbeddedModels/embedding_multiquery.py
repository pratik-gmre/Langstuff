from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()



embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=32)

documents = [
    "Kathmandu is the capital of Nepal",
    "Tokyo is the capital of Japan",
    "Washington is the capital of the United States"
]
  
  
  
result=embedding.embed_documents(documents)

print(str(result))
