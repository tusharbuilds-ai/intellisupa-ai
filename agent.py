import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

load_dotenv()

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.7
)

async def ask_agent(query: str, token:str) -> str:
    client = MultiServerMCPClient({
        "supabase": {
            "transport": "http",
            "url": "https://mcp.supabase.com/mcp",
            "headers": {
                "Authorization": f"Bearer {token}"
            }
        }
    })

    tools = await client.get_tools()
    print(f"Tools loaded: {len(tools)}")

    agent = create_agent(
        model=gemini_llm,
        tools=tools,
    )

    result = await agent.ainvoke({
        "messages": [("human", query)]  
    })

    last_message = result["messages"][-1]
    content = last_message.content
    if isinstance(content,list):
        return content[0].get("text",str(content))
    return str(content) 


if __name__ == "__main__":
    result = asyncio.run(
        ask_agent("What data I have in my table customer?")
    )
    print(result)