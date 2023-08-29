import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import cohere

from sklearn.neighbors import NearestNeighbors
import numpy as np

api_key = ""

co = cohere.Client(api_key=api_key)

def main():
    st.set_page_config(page_title="Ask your Resume")
    st.header("Ask your Resume")

    # upload file
    pdf = st.file_uploader("Upload your Resume", type="pdf")

    # extract the text
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # create embeddings
        try:
            embeddings = [co.embed(texts=[chunk], model='embed-english-light-v2.0').embeddings for chunk in chunks]
            embeddings_2d = np.reshape(embeddings, (len(embeddings), -1))
        except Exception as e:
            st.write(f"Error creating embeddings: {e}")
            return

        # Fit nearest neighbors model
        nn = NearestNeighbors(n_neighbors=5, metric='cosine')
        nn.fit(embeddings_2d)

        # Search for embeddings that match user's question
        user_question = st.text_input("Ask a question about the Resume")
        if user_question:
            question_embeddings = co.embed(
                texts=[user_question],
                model='embed-english-light-v2.0'
            ).embeddings
            if question_embeddings:
                question_embedding = np.array(question_embeddings[0]).reshape(1, -1)  # Assuming only one embedding is returned
                print(question_embedding.shape)
            else:
                print("No embeddings found for the question.")

            distances, indices = nn.kneighbors(question_embedding)

            # Get the chunks corresponding to the nearest neighbors
            nearest_chunks = [chunks[i] for i in indices[0]]

            # Generate response based on nearest chunks
            prompt = ' '.join(nearest_chunks)
            try:
                response = co.generate(
                    model='command-light',
                    prompt=prompt,
                    max_tokens=100
                )
                st.write(response[0].text)
            except Exception as e:
                st.write(f"Error generating response: {e}")


if __name__ == '__main__':
    main()
