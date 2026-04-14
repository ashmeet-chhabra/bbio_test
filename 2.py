import os
import dotenv
import asyncio

from backboard import BackboardClient

dotenv.load_dotenv()

async def main():
    client = BackboardClient(api_key=os.getenv("BACKBOARD_API_KEY"))

    assistant = await client.create_assistant(
        name="Japanese Study Partner",
        system_prompt="You are a helpful Japanese learning assisitant"
    )

    document = await client.upload_document_to_assistant(
        assistant.assistant_id,
        "sample_doc.pdf"
    )

    print("Waiting for document to be indexed...")

    while True:
        status = await client.get_document_status(document.document_id)
        if status.status == 'indexed':
            print('Document indexed successfully!')
            break
        elif status.status == 'failed':
            print(f"Document indexing failed: {status.status_message}")
            return
        await asyncio.sleep(2)

    thread = await client.create_thread(assistant.assistant_id)

    async for chunk in await client.add_message(
        thread_id = thread.thread_id,
        content = 'Teach me the 5 most relevant japanese grammar points here, ranked by difficuly level in ascending order',
        stream = True
    ):
        if chunk.get('type') == 'content_streaming':
            c = chunk.get('content', "")
            if c:
                print(c, end="", flush=True)

    print()

if __name__ == "__main__":
    asyncio.run(main())