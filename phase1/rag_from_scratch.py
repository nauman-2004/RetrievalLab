import os
from sentence_transformers import SentenceTransformer
from ollama import chat

def load_documents():
    directory = "retrievallab/phase1/data"

    text_files = [f for f in os.listdir(directory) if f.endswith(".txt")]

    documents = []

    for file in text_files:
        path = os.path.join(directory, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        documents.append({
                "filename": file,
                "text": content
            })

    return documents

def chunk_documents(documents):
    c_id = 0
    chunks = []
    for document in documents:
        filename = document["filename"]
        text = document["text"]

        c_index = 0
        paras = text.split("\n\n")
        for para in paras:
            para = para.strip()
            if not para:
                continue
            chunks.append({
                "chunk_id": c_id,
                "chunk_index": c_index,
                "source_filename": filename,
                "text": para
            })
            c_id += 1
            c_index += 1

    return chunks

def embed_chunks(chunks, model):
    for chunk in chunks:
        chunk["embedding"] = model.encode(chunk["text"])

    return chunks

def retrieve(query, chunks, model, top_k=3):
    query_embedding = model.encode(query)
    results = []
    for chunk in chunks:
        similarity = model.similarity(chunk["embedding"], query_embedding)
        results.append({
            "chunk": chunk,
            "score": similarity
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

def construct_context(results):
    context = ""
    for result in results:
        context += "Source: "
        context += result["chunk"]["source_filename"]
        context += " (Chunk "
        context += str(result["chunk"]["chunk_index"])
        context += ")\n\n"
        context += result["chunk"]["text"]
        context += "\n\n"
        context += "-" * 50
        context += "\n\n"

    return context

def construct_prompt(query, context):
    prompt = f"""You are a helpful AI assistant.
    Answer the user's question using only the information provided in the context below.

    If the answer cannot be determined from the provided context, respond exactly with:

    "I don't have enough information in the retrieved documents to answer that question."

    Context:
    {context}

    Question:
    {query}

    Answer:

    """
    return prompt

def generate_answer(prompt):
    response = chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content

def main():
    documents = load_documents()
    chunks = chunk_documents(documents)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunks = embed_chunks(chunks, model)

    query = "Who is Donald Trump"
    top_results = retrieve(query, chunks, model)

    context = construct_context(top_results)

    prompt = construct_prompt(query, context)

    answer = generate_answer(prompt)

    print("\nAnswer:\n")
    print(answer)

    print("\nSources:")

    for result in top_results:
        chunk = result["chunk"]
        print(
            f"- {chunk['source_filename']} "
            f"(Chunk {chunk['chunk_index']})"
        )

if __name__ == "__main__":
    main()
