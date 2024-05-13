from openai_assistant import OpenAIAssistant

def conversation(openai_api_token, assistant_id_token, vs_id_token):
    """
    Initiates a conversation with the OpenAI assistant.

    Args:
        openai_api_token (str): The API key for accessing OpenAI services.
        assistant_id_token (str): The ID of the assistant to use.
        vs_id_token (str): The vector store ID associated with the assistant.

    """
    assistant = OpenAIAssistant(openai_api_token)
    print("Welcome! Let's start a conversation with the OpenAI assistant. Type 'exit' to quit.\n")
    
    # Load the OpenAI assistant
    if not assistant.load_openai_assistant(assistant_id_token, vs_id_token):
        print("Failed to load the OpenAI assistant. Exiting.")
        return
    
    try:
        # Start the conversation loop
        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                break
            
            if not user_input.strip():  # Check for empty input
                print("Please provide a valid input.")
                continue

            response = assistant.get_assistant_response(user_input)
            if response is None:
                print("An error occurred during response retrieval. Please try again.")
            else:
                print(f"Assistant: {response}\n")

    except KeyboardInterrupt:
        print("\nExiting due to user interruption...")
    finally:
        print("Exiting...")
        assistant.delete_thread()
