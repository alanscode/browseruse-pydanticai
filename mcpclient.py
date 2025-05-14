import os
from dotenv import load_dotenv
import os
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel # Import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider # Import OpenAIProvider
import asyncio
import time

load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

server = MCPServerStdio(
    'cmd',
    args=[
        '/c',
        'npx',
        '-y',
        '@browsermcp/mcp'
    ]
)

# Initialize Agent with OpenAIModel and OpenAIProvider
agent = Agent(
    model=OpenAIModel(
        "google/gemini-2.5-flash-preview", # Model name as expected by OpenRouter
        provider=OpenAIProvider(
            base_url='https://openrouter.ai/api/v1',
            api_key=openrouter_api_key
        )
    ),
    mcp_servers=[server]
)


async def main():
    async with agent.run_mcp_servers():
        while True:
            result = await agent.run('goto https://voice.google.com/u/0/messages, find the previous message history for "iphone". check for new messages and try to complete any and all tasks that are requested by iphone.')
            print(result.output)
            for i in range(120, 0, -1):
                print(f"Next run in {i} seconds...", end='\r')
                await asyncio.sleep(1)
            print("Running again...")
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())