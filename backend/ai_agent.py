import os
import time
from google import genai
from dotenv import load_dotenv

# Import our prompt from the prompts.py file
from prompts import INTENT_PROMPT, DYNAMIC_PANDAS_PROMPT
from prompts import POWERBI_ROUTER_PROMPT
# 1. Load the secret variables from the .env file
load_dotenv()

# 2. Initialize the Gemini Client with your key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def classify_intent(user_question):
    """Uses Gemini to determine the category of the user's question."""
    try:
        # Replace the {user_question} placeholder in our prompt with the actual question
        prompt = INTENT_PROMPT.format(user_question=user_question)
        
        # Send it to Gemini using the explicit 8B model version
        response = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
        
        # Clean up the response (remove invisible spaces and make lowercase)
        intent = response.text.strip().lower()
        return intent
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return "unknown"

def generate_pandas_code(user_question, columns):
    """Uses Gemini to generate Pandas code based on the user's question."""
    try:
        # Inject the dataset columns and user question into the prompt
        prompt = DYNAMIC_PANDAS_PROMPT.format(columns=columns, user_question=user_question)
        
        # Ask Gemini to generate the code (with a retry loop for rate limits)
        for attempt in range(3):
            try:
                response = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
                break # If successful, break out of the loop
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    print("⏳ Rate limit reached. Waiting 25 seconds before retrying...")
                    time.sleep(25)
                else:
                    raise e
        
        # Clean up any markdown blocks if the AI decided to include them anyway
        code = response.text.strip()
        if code.startswith("```python"):
            code = code[9:]
        if code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
            
        return code.strip()
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return None

def route_powerbi_dataset(question):

    prompt = POWERBI_ROUTER_PROMPT.format(
        question=question
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text.strip().lower()

# Test Block
if __name__ == "__main__":
    print("--- PHASE 7: TESTING INTENT CLASSIFIER ---")
    print("Q: Which branches are bleeding money right now?")
    print("A:", classify_intent("Which branches are bleeding money right now?"))
    
    print("\nQ: How much did we sell on Zomato vs Swiggy?")
    print("A:", classify_intent("How much did we sell on Zomato vs Swiggy?"))
    
    print("\nQ: What is the weather like today?")
    print("A:", classify_intent("What is the weather like today?"))