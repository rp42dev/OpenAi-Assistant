from openai import OpenAI, APIError, APIConnectionError, RateLimitError
import logging
import time

class OpenAIAssistant:
    def __init__(self, open_ai_api_key):
        self.client = OpenAI(api_key=open_ai_api_key)
        self.thread = None
        self.assistant = None
        self.logger = logging.getLogger(__name__)

    def load_openai_assistant(self, assistant_id, vs_id):
        try:     
            self.assistant = self.client.beta.assistants.retrieve(assistant_id)
            self.thread = self.client.beta.threads.create(
                tool_resources={
                    "file_search": {
                        "vector_store_ids": [vs_id]
                    }
                }
            )
        except (APIError, APIConnectionError, RateLimitError) as e:
            self.logger.error(f"An error occurred during assistant loading: {e}")
            return None

    def wait_on_run(self, run):
        idx = 0
        while run.status in ["queued", "in_progress"]:
            print(f"Waiting for assistant to load...", end="\r")
            idx = (idx + 1) % 4
            time.sleep(0.5)
            try:
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id,
                )
            except (APIError, APIConnectionError, RateLimitError) as e:
                self.logger.error(f"An error occurred during run retrieval: {e}")
                return None
        return run

    def delete_thread(self):
        try:
            self.client.beta.threads.delete(self.thread.id)
        except (APIError, APIConnectionError, RateLimitError) as e:
            self.logger.error(f"An error occurred during thread deletion: {e}")

    def get_assistant_response(self, user_input):
        try:
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
            if not run:
                return "No response from the assistant, please try again."
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id, order="asc", after=message.id
            )
            return messages.data[0].content[0].text.value
        except (APIError, APIConnectionError, RateLimitError, IndexError) as e:
            self.logger.error(f"An error occurred during assistant response retrieval: {e}")
            return "An error occurred, please try again later."

