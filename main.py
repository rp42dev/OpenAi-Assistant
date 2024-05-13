import os
from conversation import conversation
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve environment variables
    openai_api_token = os.getenv('OPENAI_API_TOKEN')
    assistant_id_token = os.getenv('ASSISTANT_ID_TOKEN')
    vs_id_token = os.getenv('VS_ID_TOKEN')
    
    # Check if all required environment variables are set
    if not all([openai_api_token, assistant_id_token, vs_id_token]):
        print("Error: Please set all required environment variables (OPENAI_API_TOKEN, ASSISTANT_ID_TOKEN, VS_ID_TOKEN) in the .env file.")
        return

    try:
        # Start the conversation
        conversation(openai_api_token, assistant_id_token, vs_id_token)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

