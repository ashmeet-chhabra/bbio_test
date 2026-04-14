import os
import asyncio
import requests
import dotenv

from backboard import BackboardClient

dotenv.load_dotenv()

async def main():
    client = BackboardClient(api_key=os.getenv("BACKBOARD_API_KEY"))

    assistant = await client.create_assistant(name="assistant")
    thread = await client.create_thread(assistant.assistant_id)

    response = requests.post(
        f"https://app.backboard.io/api/threads/{thread.thread_id}/messages",
        headers = {"X-API-Key": os.getenv("BACKBOARD_API_KEY")},
        json={
            "content": "I like backend more than frontend.",
            "stream": False,
            "memory": "Auto"
        }
    )

    thread_2 = await client.create_thread(assistant.assistant_id)

    response = requests.post(
        f"https://app.backboard.io/api/threads/{thread_2.thread_id}/messages",
        headers = {"X-API-Key": os.getenv("BACKBOARD_API_KEY")},
        json={
            "content": "Which part of software do I prefer and over what?",
            "stream": False,
            "memory": "Auto"
        }
    )

    result = response.json()
    print(f"Assistant: {result['content']}", flush=True)

    response = requests.get(
        f"https://app.backboard.io/api/assistants/{assistant.assistant_id}/memories",
        headers={"X-API-Key": os.getenv("BACKBOARD_API_KEY")}
    )

    memories = response.json()

    for memory in memories["memories"]:
        print(f"Memory: {memory["content"]}")

asyncio.run(main())