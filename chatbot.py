#import requirements from libraries used in file
from dotenv import load_dotenv
from openai import OpenAI
##from termcolor import colored
import os, json

load_dotenv("api_key.env")
print(os.getenv("OPENAI_API_KEY"))

#set up connection to Open AI's API using key in environment file
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

#user prompt for speaking to chatbot
user_prompt = input("Hello I am a chatbot from OpenAI. I can assist you with\n1.Checking weather in your location\n2.Currency conversion\n3.Language translating\nWhat would you like to do? (Type your selection: 1, 2, or 3)\nYou can also type 'exit' at any time to return to this menu")

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

#define functions for tools 
#set up tools dictionary schema
#make api call w/ parameters
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=message_list,
    tool_choice="auto",
    tools=tools,
    temperature=0.0
)



