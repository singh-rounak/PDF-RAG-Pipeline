class RAGService:
    def __init__(self, embedding_service, vector_store,llm_service):
                 
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.llm_service = llm_service

    def answer(self, question: str):
        # Generate an embedding for the question using the embedding service
        embedding = self.embedding_service.get_embed(question)

        # Search for relevant context in the vector store using the generated embedding
        context = self.vector_store.search(embedding)

        prompt = f''' Answer the user's question using only the context below.
        Context:
        {context}

        Question:
        {question}
        '''

        # Generate a response using the LLM
        answer = self.llm_service.generate_response(prompt)

        return answer   