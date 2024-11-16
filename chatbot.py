from dotenv import load_dotenv
from openai import OpenAI
import os, json

load_dotenv("api_key.env")

print(os.getenv("OPENAI_API_KEY"))

#set up connection to Open AI's API using key in environment file
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

#user prompt for speaking to chatbot
user_prompt = input("Hello I am a chatbot from OpenAI. I can assist you with\n1.Checking weather in your location\n2.Currency conversion\n3.Language translating\nWhat would you like to do? (Type your selection")

# Create a list of messages to send to the API
message_list = [
    {
        "role": "system", 
        "content": "You are an assistant used for three main functions: weather reporting by a given location, currency conversion between two currencies, and translating given text into a specified language."
        #may specify to have user select function first, ie. what would you like to do today?: 1,2, or 3"
    },
    {
        "role": "user", 
        "content": user_prompt
    }
]

#tool function definitions
#return simulated weather data temp and condition description with given location, ##celsius and fahrenheit
def get_weather(location:str, unit_f:float, unit_c:float, desc:str):
    return f"The current weather in {location} is {unit_f} degrees fahrenheit/{unit_c} degrees celsius. Throughout the day you should expect {desc}. Please continue to check the report as conditions may change"

#return converted currency given a float number amount with currency type, and desired currency type
def convert_currency(amount:float, from_currency:str, to_currency:str, conversion:float):
    return f"{amount, from_currency} is equal to {conversion, to_currency}."

#return translation given text and desired language
def translate_text(text:str, target_language:str, translation:str):
    return f"{translation}"

##variable to store available tools/functions to navigate response with error handling
available_tools = {
    "get_weather": get_weather,
    "convert_currency": convert_currency,
    "translate_text": translate_text
}

#set up tools dictionary schema with example descriptions for API chatbot
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state to get weather for e.g. San Francisco, CA"
                    },
                    "unit_f": {
                        "type": "float", #"string"
                        "enum": ["fahrenheit"]
                    },
                    "unit_c": {
                        "type": "float", #"string"
                        "enum": ["celsius"]
                    },
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert a given amount from one currency to another target currency",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "float",
                        "description": "The amount to convert"
                    },
                    "from_currency": {
                        "type": "string",
                        "description": "The currency to convert from"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "The currency to convert to"
                    }
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "translate_text",
            "description": "Translate text to a target language",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to translate"
                    },
                    "target_language": {
                        "type": "string",
                        "description": "The language to translate to"
                    }
                },
                "required": ["text", "target_language"]
            }
        }
    }
]


#make api call w/ parameters
"""
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=message_list,
    tool_choice="auto",
    tools=tools,
    temperature=0.0
)

"""

def process_user_input(user_input: str) -> str:
    """
    Process user input and return appropriate response using tool calls.
    """
    try:
        # Create chat completion with tool calls
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=message_list,
            tools=tools,
            tool_choice="auto",
            temperature=0.0
        )

        # navigate message content
        response_message = response.choices[0].message

        # Check if the model wants to call a function
        if response_message.tool_calls:
            # Process each tool call
            final_response = []
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # function call with formatted response
                if function_name in available_tools:
                    function_response = available_tools[function_name](**function_args)
                    final_response.append(f"{function_name} result: {function_response}")
                
            return "\n".join(final_response)
        else:
            return response_message.content

    except Exception as e:
        return f"Error processing request: {str(e)}"


