import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# Set your OpenAI API key
OPENAI_API_TOKEN = os.getenv('OPENAI_API_TOKEN') # 'your_api_key
os.environ["OPENAI_API_KEY"] = OPENAI_API_TOKEN


# Initialize the OpenAI client
client = OpenAI(
    # Set your OpenAI API key
    api_key = OPENAI_API_TOKEN
)


#return existing assistant if it exists
def get_assistant(id):
    assistant = client.beta.assistants.retrieve(id)
    return assistant


#create thread for assistant
def create_thread(vs_ID):
    thread = client.beta.threads.create(
        messages=[ { "role": "user", "content": "what price"} ],
            tool_resources={
                "file_search": {
                "vector_store_ids": [vs_ID]
                }
            }
        )
    return thread


#main function
def main():
    vs_ID = "vs_dOpDSOSZrEYh5YhGcNJS5YLX"
    assistant_id = "asst_FzT6VbdmcKBXMuG9NqHkKyLn"
    assistant = get_assistant(assistant_id)
    thread = create_thread(vs_ID)

    # the run until it's in a terminal state.
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    print(message_content.value)
    print("\n".join(citations))


if __name__ == "__main__":
    main()

