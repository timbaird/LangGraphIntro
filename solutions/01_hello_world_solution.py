"""
=============================================================================
 Exercise 1: Hello LangGraph! — SOLUTION
=============================================================================

 This is the complete, working solution for Exercise 1.
 Compare your code in 01_hello_world/hello_langgraph.py against this
 if you get stuck.
=============================================================================
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

load_dotenv()


# STEP 1: Define your State
class State(TypedDict):
    user_input: str
    response: str


# STEP 2: Create the LLM connection
llm = ChatOpenAI(
    model="google/gemini-2.0-flash-001",
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)


# STEP 3: Define your node function
def chat_node(state: State) -> dict:
    """Send the user's input to the LLM and return the response."""
    ai_message = llm.invoke(state["user_input"])
    return {"response": ai_message.content}


# STEP 4: Build the graph
graph = StateGraph(State)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)
app = graph.compile()


# STEP 5: Run it!
if __name__ == "__main__":
    print("=" * 60)
    print("  Hello LangGraph!")
    print("  Type a message and the LLM will respond.")
    print("=" * 60)
    print()

    user_message = input("You: ")
    print()
    print("Thinking...")
    print()

    result = app.invoke({"user_input": user_message, "response": ""})
    print(f"LLM: {result['response']}")

    print()
    print("=" * 60)
    print("  Congratulations! You just ran your first LangGraph!")
    print("=" * 60)
