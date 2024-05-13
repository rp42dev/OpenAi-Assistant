from openai import OpenAI, APIError, APIConnectionError, RateLimitError
import logging
import time

class OpenAIAssistant:
    """
    A class representing an interface to interact with OpenAI's assistant service.

    Attributes:
        client (OpenAI): The OpenAI client instance.
        thread: The current thread associated with the assistant.
        assistant: The loaded assistant instance.
        logger (Logger): Logger instance for logging errors.
    """

    def __init__(self, open_ai_api_key):
        """
        Initializes the OpenAIAssistant.

        Args:
            open_ai_api_key (str): The API key for accessing OpenAI services.
        """
        self.client = OpenAI(api_key=open_ai_api_key)
        self.thread = None
        self.assistant = None
        self.logger = logging.getLogger(__name__)

    def load_openai_assistant(self, assistant_id, vs_id):
        """
        Loads the OpenAI assistant and initializes a thread.

        Args:
            assistant_id (str): The ID of the assistant to load.
            vs_id (str): The vector store ID for the assistant.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id)
            self.thread = self.client.beta.threads.create(
                tool_resources={
                    "file_search": {
                        "vector_store_ids": [vs_id]
                    }
                }
            )
            return True
        except (APIError, APIConnectionError, RateLimitError) as e:
            self.logger.error(f"An error occurred during assistant loading: {e}")
            return False

    def wait_on_run(self, run):
        """
        Waits for the assistant's run to complete.

        Args:
            run: The current run object.

        Returns:
            run: The completed run object.
        """
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
        """
        Deletes the current thread associated with the assistant.
        """
        try:
            self.client.beta.threads.delete(self.thread.id)
        except (APIError, APIConnectionError, RateLimitError) as e:
            self.logger.error(f"An error occurred during thread deletion: {e}")

    def get_assistant_response(self, user_input):
        """
        Gets a response from the OpenAI assistant for the given user input.

        Args:
            user_input (str): The user's input.

        Returns:
            str: The assistant's response or an error message.
        """
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
