import os
from dotenv import load_dotenv
import os
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel # Import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider # Import OpenAIProvider

load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

server = MCPServerStdio(
    'cmd',
    args=[
        '/c',
        'npx',
        '-y',
        '@browsermcp/mcp@latest'
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
        result = await agent.run('goto https://voice.google.com/u/0/messages, find the previous message history for "iphone". send the message "hello world" to iphone. Continue to check the page every 2 minutes for responses and complete any requests made from iphone')
    print(result.output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())