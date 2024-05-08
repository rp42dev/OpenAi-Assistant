import os
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from dotenv import load_dotenv
import time

load_dotenv()

# Set your OpenAI API key
OPENAI_API_TOKEN = os.getenv('OPENAI_API_TOKEN')

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_TOKEN)


def load_openai_assistant(assistant_id, vs_ID):
    """Load the OpenAI assistant and create a new thread for interaction."""
    assistant = client.beta.assistants.retrieve(assistant_id)
    thread = client.beta.threads.create(
        tool_resources={
            "file_search": {
                "vector_store_ids": [vs_ID]
            }
        }
    )
    return thread, assistant


def wait_on_run(run, thread):
    """Wait for the assistant run to complete or progress to next stage."""
    idx = 0
    while run.status == "queued" or run.status == "in_progress":
        
        print(f"Waiting for assistant response{'.'*idx}", end="\r")
        
        idx = (idx + 1) % 4
        
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


def get_assistant_response(thread, assistant_id, user_input):
    """Interact with the assistant by sending user input and retrieving the response."""
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

    messages = client.beta.threads.messages.list(
        thread_id=thread.id, order="asc", after=message.id
    )
    try:
        return messages.data[0].content[0].text.value
    except IndexError:
        return "No response from the assistant, please try again."


def main():
    """Main function to interact with the OpenAI assistant."""
    VS_ID = os.getenv('VS_ID_TOKEN')
    ASSISANT_ID = os.getenv('ASSISANT_ID_TOKEN')

    print("Welcome! Let's start a conversation with the OpenAI assistant. Type 'exit' to quit.\n")
    
    thread, assistant = load_openai_assistant(ASSISANT_ID, VS_ID)
    
    # Start the conversation loop
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            break
        
        try:
            response = get_assistant_response(thread, ASSISANT_ID, user_input)
            print(f"Assistant: {response}\n")
        except (APIError, APIConnectionError, RateLimitError) as e:
            print(f"An error occurred during API interaction: {e}")
            break
        
    print("Exiting...")


if __name__ == "__main__":
    main()