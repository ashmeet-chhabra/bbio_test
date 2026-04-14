import os
import asyncio
import requests
import dotenv

from backboard import BackboardClient

dotenv.load_dotenv()

async def main():
    client = BackboardClient(api_key=os.getenv("BACKBOARD_API_KEY"))

    assistant = await client.create_assistant(
        name="Web Search assistant",
        system_prompt="You are a helpful assistant with web search."
    )

    thread = await client.create_thread(assistant.assistant_id)

    response = requests.post(
        f"https://app.backboard.io/api/threads/{thread.thread_id}/messages",
        headers = {"X-API-Key": os.getenv("BACKBOARD_API_KEY")},
        json={
            "content": "What are some VERY recent films you'd recommend that got swept outta most people's radar but are great?",
            "web_search": "auto"
        }
    )

    result = response.json()
    print(f"Assistant: {result['content']}", flush=True)

asyncio.run(main())