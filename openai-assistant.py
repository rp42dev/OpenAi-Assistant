import os
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from dotenv import load_dotenv
import time

load_dotenv()

class OpenAIAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_TOKEN'))
        self.thread = None
        self.assistant = None
        
    def load_openai_assistant(self, assistant_id, vs_ID):
        self.assistant = self.client.beta.assistants.retrieve(assistant_id)
        self.thread = self.client.beta.threads.create(
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vs_ID]
                }
            }
        )
        
    def wait_on_run(self, run):
        idx = 0
        while run.status == "queued" or run.status == "in_progress":
            print(f"Waiting for assistant response{'.'*idx}", end="\r")
            idx = (idx + 1) % 4
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run
    
    def delete_thread(self):
        self.client.beta.threads.delete(self.thread.id)
        
    def get_assistant_response(self, user_input):
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=user_input,
        )

        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

        run = self.wait_on_run(run)

        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id, order="asc", after=message.id
        )
        try:
            return messages.data[0].content[0].text.value
        except IndexError:
            return "No response from the assistant, please try again."
        
    def start_conversation(self):
        print("Welcome! Let's start a conversation with the OpenAI assistant. Type 'exit' to quit.\n")
        self.load_openai_assistant(os.getenv('ASSISANT_ID_TOKEN'), os.getenv('VS_ID_TOKEN'))
        # Start the conversation loop
        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                break

            try:
                response = self.get_assistant_response(user_input)
                print(f"Assistant: {response}\n")
            except (APIError, APIConnectionError, RateLimitError) as e:
                print(f"An error occurred during API interaction: {e}")
                break
            
        print("Exiting...")
        self.delete_thread()
        
    def main(self):
        self.start_conversation()
        
if __name__ == "__main__":
    assistant = OpenAIAssistant()
    assistant.main()
