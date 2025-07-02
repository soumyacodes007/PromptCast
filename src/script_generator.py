# src/script_generator.py
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from . import config

def generate_podcast_script(topic_text: str, personality_prompt: str) -> str:
    """Generates a two-person podcast script using Alchemyst AI based on a selected personality."""
    print(f"Generating podcast script with selected personality...")

    system_prompt = personality_prompt

    llm = ChatOpenAI(
        api_key=config.ALCHEMYST_API_KEY,
        model="alchemyst-ai/alchemyst-c1",
        base_url="https://platform-backend.getalchemystai.com/api/v1/proxy/default",
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"The topic to discuss is:\n\n{topic_text}")
    ]

    response = llm.invoke(messages)
    print("Script generated successfully.")
    return response.content