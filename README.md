# Document Information Retrieval Assistant using OpenAI GPT-3

This Python script enables interaction with the OpenAI GPT-3 assistant via the OpenAI API to retrieve information from uploaded documents using a vector store.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Required Python packages (`openai`, `python-dotenv`): Install using `pip install openai python-dotenv`

## Setup

1. **Obtain OpenAI API Key:**
   - Sign up for OpenAI and obtain your API key.
   - Set your OpenAI API key in the environment variable `OPENAI_API_TOKEN`.

2. **Assistant and Vector Store IDs:**
   - Replace `assistant_id` and `vs_ID` in the script with your specific OpenAI assistant ID and vector store ID.
   - **Setup Vector Store:**
     - Create or use an existing vector store on OpenAI.
     - Upload documents containing information you want the assistant to retrieve into the vector store.

## Usage

1. **Run the Script:**
   - Execute the script by running `python your_script_name.py` in your terminal or IDE.

2. **Start Conversation:**
   - Upon running, the script will prompt you to enter a message.
   - Type you and press `Enter` to send it to the OpenAI assistant.

3. **Exit Conversation:**
   - To exit the conversation, type `exit` and press `Enter`.

## Script Details

- `load_openai_assistant(assistant_id, vs_ID)`: Initializes the OpenAI assistant and creates a new thread for interaction.
- `wait_on_run(run, thread)`: Waits for the assistant run to complete or progress to the next stage.
- `get_assistant_response(thread, assistant_id, user_input)`: Sends user input to the assistant and retrieves the response.

## Error Handling

- The script handles API-related errors such as `APIError`, `APIConnectionError`, and `RateLimitError` gracefully.

## Notes

- Ensure your OpenAI account is properly configured with the necessary permissions and resources.
- Vector store setup is required to upload documents for information retrieval by the assistant.

## Example

```bash
$ python your_script_name.py
Welcome! Let's start a conversation with the OpenAI assistant.

You: Hello
Assistant: Hi there! How can I assist you today?

You: Retrieve information from document
Assistant: Please provide specific details or keywords from the document you need information about.

You: exit
Exiting...
