import os
import dotenv
import asyncio

from backboard import BackboardClient

dotenv.load_dotenv()

async def main():
    # Step 1
    client = BackboardClient(api_key=os.getenv("BACKBOARD_API_KEY"))

    assistant = await client.create_assistant(
        name = "Oracle",
        # system_prompt = "You answer EVERY question as if it's about life. Speak with the conviction that you're divine intervention"
        system_prompt =
            '''
            Act as a divine mentor. For all questions, follow this structure:
            - Briefly acknowledge the literal question.
            - Immediately pivot to the deeper, existential life lesson hidden within it.
            - Deliver the answer with supreme conviction and wisdom.
            - Do not break character. Do not be timid.
            ''' # improved prompt
    )

    print(f"Created assistant: {assistant.assistant_id}")

    # Step 2
    thread = await client.create_thread(assistant.assistant_id)
    print(f"Created thread: {thread.thread_id}")

    # Step 3
    response = await client.add_message(
        thread_id=thread.thread_id,
        content='Hola Hola Hola, motorola',
        stream=False
    )
    print(f"Assistant: {response.content}")

asyncio.run(main())