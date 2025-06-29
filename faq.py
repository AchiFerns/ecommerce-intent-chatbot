import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from groq.types.chat import ChatCompletionUserMessageParam
from importlib_metadata import metadata


from dotenv import load_dotenv
load_dotenv()

from groq import Groq
groq_client =Groq()

import os
os.environ['GROQ_MODEL']

faqs_path=Path(__file__).parent / "resources" / "faq_data.csv"


chroma_client= chromadb.Client()
collection_name_faq= 'faq'

ef= embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)
def ingest_faq_data(path):#Loads FAQ data into ChromaDB,,,,Only runs once (usually at startup or update)
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting FAQ data into Chromadb....")
        collection =chroma_client.get_or_create_collection(
            name=collection_name_faq,
            embedding_function=ef
        )
        df=pd.read_csv(path)
        docs=df['question'].to_list()
        metadata = [{'answers': ans} for ans in df['answer'].to_list()]
        ids=[f"id_{i}" for i in range(len(docs))]
        collection.add(
            documents=docs,
            metadatas=metadata,
            ids=ids
        )
        print(f"FAQ Data successfully ingested into Chroma collection: {collection_name_faq}")
    else:
        print(f'collection {collection_name_faq} already exists ')

def get_relevant_qa(query):#Searches for the best answers,,,Runs every time the user asks a question
    collection = chroma_client.get_collection(
        name=collection_name_faq,
        embedding_function=ef
    )
    result= collection.query(
        query_texts=[query],
        n_results=2
    )
    return result

def faq_chain(query):
    result = get_relevant_qa(query)
    context = "".join([r.get('answers','') for r in result['metadatas'][0]])
    answer = generate_answer(query, context)
    return answer


def generate_answer(query,context):
    prompt =f'''Given the following context and question, generate answer based on this context only.
    If the answer is not found in the context, kindly state "I don't know". Don't try to make up an answer.
    
    QUESTION: {query}
    
    CONTEXT: {context}
    '''
    completion = groq_client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=[
            ChatCompletionUserMessageParam(
                role="user",
                content=prompt
            )
        ]
    )

    return completion.choices[0].message.content


if __name__== "__main__":
    ingest_faq_data(faqs_path)
    query = "what are the payment option?"
    #result= get_relevant_qa(query)
    answer= faq_chain(query)
    print(answer)
