import os
from typing import Sequence
from dotenv import load_dotenv
import asyncio
import aiohttp
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination, MaxMessageTermination
from autogen_agentchat.messages import HandoffMessage, TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat, Swarm
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_MODEL = os.getenv("GPT_MODEL")

model_client = OpenAIChatCompletionClient(model=GPT_MODEL, api_key=OPENAI_API_KEY)

async def add_user(name: str, email: str, role: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8085/api/users", json={"name": name, "email": email, "role": role}) as response:
            return await response.text()

async def list_users() -> Sequence:
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8085/api/users") as response:
            return await response.json()


user_management_agent = AssistantAgent(
    "user_management_agent",
    model_client=model_client,
    handoffs=["user_creation_agent", "user_listing_agent", "admin"],
    system_message="""You are a user management agent.
    You are assisting an admin in managing users.
    The user_creation_agent is in charge of creating a new user.
    The user_listing_agent is in charge of listing existing users.
    If you need information from the admin, you must first send your message, then you can handoff to the admin.
    Before termination, ask the admin if they need any more assistance.
    Use TERMINATE when there are no more requests from the user.""",
)

user_creation_agent = AssistantAgent(
    "user_creation_agent",
    model_client=model_client,
    handoffs=["user_management_agent", "admin"],
    tools=[add_user],
    system_message="""You are a user creation agent.
    You have the ability to create a user using the add_user tool.
    If you need information from the admin, you must first send your message, then you can handoff to the admin.
    When the transaction is complete, handoff to the user management agent to finalize.""",
)

user_listing_agent = AssistantAgent(
    "user_listing_agent",
    model_client=model_client,
    handoffs=["user_management_agent"],
    tools=[list_users],
    system_message="""You are a user listing agent.
    You have the ability to list all users using the list_users tool.
    When the transaction is complete, handoff to the user management agent to finalize.""",
)

termination = HandoffTermination(target="admin") | TextMentionTermination("TERMINATE")
team = Swarm([user_management_agent, user_creation_agent, user_listing_agent], termination_condition=termination)

def print_messages(task_result):
    for message in task_result.messages:
      if (isinstance(message, HandoffMessage)):
        print(f" - {message.source} handed off to {message.target}: {message.content}")
      elif (isinstance(message, TextMessage)):
        print(f"{message.source}: {message.content}")
      else:
        print(f" - {message.__class__} message")

async def main() -> None:
    print("Welcome, admin!")
    print("You are now connected to the user management system.")
    print("You can add users and list users.")

    first_input = input("Enter message > ")
    task_result = await team.run(task=first_input)
    print_messages(task_result)
    last_message = task_result.messages[-1]

    while isinstance(last_message, HandoffMessage) and last_message.target == "admin":
        user_message = input("Enter message > ")
        task_result = await team.run(task=HandoffMessage(source="admin", target=last_message.source, content=user_message))
        print_messages(task_result)
        last_message = task_result.messages[-1]

asyncio.run(main())

