import os
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()


# Set your OpenAI API key
OPENAI_API_TOKEN = os.getenv('OPENAI_API_TOKEN') # 'your_api_key


# Initialize the OpenAI client
client = OpenAI(
    api_key = OPENAI_API_TOKEN
)


#load openAi assistant and vector store
def load_openai_assistant(assistant_id, vs_ID):
    assistant = client.beta.assistants.retrieve(assistant_id)
    thread = client.beta.threads.create(
        tool_resources={
            "file_search": {
            "vector_store_ids": [vs_ID]
            }
        }
    )
    return thread, assistant


# check in loop  if assistant ai parse our request
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


# initiate assistant ai response
def get_assistant_response(thread, assistant_id, user_input):

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    run = wait_on_run(run, thread)

    # Retrieve all the messages added after our last user message
    messages = client.beta.threads.messages.list(
        thread_id=thread.id, order="asc", after=message.id
    )

    return messages.data[0].content[0].text.value


#main function
def main():
    vs_ID = "vs_dOpDSOSZrEYh5YhGcNJS5YLX"
    assistant_id = "asst_FzT6VbdmcKBXMuG9NqHkKyLn"
    thread, assistant = load_openai_assistant(assistant_id, vs_ID)
    
    
    while True:
        user_input = input("You: ")
        if user_input == "exit":
            break
        response = get_assistant_response(thread, assistant_id, user_input)
        print("Assistant:", response)
        
    print("Exiting...")
    return
    
if __name__ == "__main__":
    main()

