import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig



# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")




@cl.on_chat_start
async def start():
    #Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )
    
    
    config: RunConfig = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
    
    agent  = Agent(
          name = "Assistant" , 
        instructions= "You are a helpful assistant" ,
        model= model
    )
    cl.user_session.set("chat_history", [])  
    cl.user_session.set("config", config)
    cl.user_session.set("agent", agent)
        
    await cl.Message(content="Welcome to the Study mode Asistant AI Assistant! How can I help you with today?").send()




@cl.on_message
async def main():
    


# if __name__ == "__main__":
#     main()