from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from datasets import load_dataset

# 🔹 Load and preview dataset
path = "models/datasets.json"
dataset = load_dataset("json", data_files=path)
samples = dataset["train"]
# 🔹 Initialize Ollama model
llm = ChatOllama(model="my-chatbot", temperature=0.9)

# 🔹 Set up memory
memory = ConversationBufferMemory(return_messages=True)
for sample in samples:
     question = sample["input"]
     answer = sample["output"]
     memory.save_context({"input": question}, {"output": answer})

# 🔹 Define prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Tum ek helpful assistant ho jo hamesha Hindlish (Hindi + English) mein jawab deta hai. Tumhara tone friendly aur desi hona chahiye, bina overly Western enthusiasm ke."),
    ("human", "{input}")
])

# 🔹 Function to get streamed answer
def getAnswer(question: str) -> str:
    # Retrieve previous chat history 
    history = memory.buffer_as_messages
    formatted_history = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in history])
    # Build prompt
    full_prompt = f"{formatted_history}\nUser: {question}\nBot:"
    response = ""
    # Stream response from Ollama
    for chunk in llm.stream(full_prompt):
        response += chunk.content 

    # Save to memory
    memory.save_context({"input": question}, {"output": response})
    return response

# 🔹 CLI loop for testing
if __name__ == "__main__":
    print("🤖 Ollama Chatbot is ready! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        answer = getAnswer(user_input)
        print("Bot:", answer)

 