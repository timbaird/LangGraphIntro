"""
=============================================================================
 Exercise 1: Hello LangGraph!
=============================================================================

 YOUR FIRST LANGGRAPH PROGRAM

 In this exercise, you'll build the simplest possible LangGraph application:
 a single-node graph that takes your input, sends it to an LLM (Large Language
 Model), and prints the response.

 Think of it like this:

     YOU  -->  [ chat_node ]  -->  RESPONSE
                    |
                 (calls LLM)

 By the end, you'll understand these core concepts:
   1. STATE   — a dictionary that carries data through your graph
   2. NODE    — a function that does work (in this case, calling an LLM)
   3. GRAPH   — connects nodes together and runs them in order
   4. EDGES   — the arrows connecting nodes (including START and END)

 INSTRUCTIONS:
   Look for the TODO comments below. Each one tells you exactly what to write.
   The comments around each TODO explain what's happening and why.

   If you get stuck, check solutions/01_hello_world_solution.py

 PREREQUISITES:
   - You've completed the setup steps in the main README.md
   - Your .env file has a valid OPENROUTER_API_KEY
=============================================================================
"""

# ── Standard library imports ────────────────────────────────────────────────
# os lets us read environment variables (like our API key)
import os

# ── Third-party imports ─────────────────────────────────────────────────────
# dotenv loads variables from your .env file into the environment
# This keeps secrets out of your code!
from dotenv import load_dotenv

# ChatOpenAI is LangChain's interface for talking to OpenAI-compatible APIs.
# OpenRouter uses the same API format as OpenAI, so this works perfectly.
from langchain_openai import ChatOpenAI

# These are the building blocks of a LangGraph graph:
# - StateGraph: the class we use to define our graph
# - START: a special marker meaning "this is where the graph begins"
# - END: a special marker meaning "this is where the graph ends"
from langgraph.graph import StateGraph, START, END

# TypedDict lets us define a dictionary with specific named fields.
# It's like a regular Python dict, but with a fixed structure.
# Learn more: https://docs.python.org/3/library/typing.html#typing.TypedDict
from typing import TypedDict


# ── Load environment variables ──────────────────────────────────────────────
# This reads your .env file and makes OPENROUTER_API_KEY available via os.environ
load_dotenv()


# =============================================================================
# STEP 1: Define your State
# =============================================================================
#
# State is the data structure that flows through your graph. Every node
# receives the current state and returns updates to it.
#
# Think of state as a form being passed between workers in an office:
#   - Each worker (node) reads what they need from the form
#   - They fill in their section
#   - They pass the updated form to the next worker
#
# For our simple chat, we need just two fields:
#   - user_input: what the user types
#   - response:   what the LLM replies
#
# We define this using TypedDict, which is just a Python dictionary
# with named, typed fields.

class State(TypedDict):
    user_input: str   # The question or message from the user
    response: str     # The LLM's reply (starts empty, filled in by our node)


# =============================================================================
# STEP 2: Create the LLM connection
# =============================================================================
#
# We need to create an LLM object that knows how to talk to OpenRouter.
# ChatOpenAI is designed for OpenAI's API, but OpenRouter uses the same
# format, so we just point it at OpenRouter's URL instead.
#
# The three things we need to configure:
#   1. model        — which AI model to use (we'll use a free one!)
#   2. api_key      — your OpenRouter API key (loaded from .env)
#   3. base_url     — OpenRouter's API endpoint (instead of OpenAI's)
#
# TODO 1: Create the LLM object.
#   Replace the `None` below with a ChatOpenAI(...) call.
#   Use these settings:
#     - model="google/gemini-2.0-flash-001"    (a free model on OpenRouter!)
#     - api_key=os.environ["OPENROUTER_API_KEY"]
#     - base_url="https://openrouter.ai/api/v1"
#
#   Note: We use ChatOpenAI (a LangChain class designed for OpenAI's API)
#   because OpenRouter uses the same API format. We just point it at
#   OpenRouter's URL instead of OpenAI's. Handy!
#
#   Want to try a different model? See the model comparison table in the
#   main README.md, or browse https://openrouter.ai/models?pricing=free
#
#   Docs: https://python.langchain.com/docs/integrations/chat/openai/

llm = None  # <-- Replace this with your ChatOpenAI(...) call


# =============================================================================
# STEP 3: Define your node function
# =============================================================================
#
# A node is just a Python function that:
#   1. Takes the current state as input
#   2. Does some work
#   3. Returns a dictionary with the fields it wants to update
#
# Our node will:
#   - Read the user's input from state["user_input"]
#   - Send it to the LLM
#   - Return the LLM's response to update state["response"]
#
# The .invoke() method sends a message to the LLM and waits for a reply.
# It returns a message object — we use .content to get the text string.
#
# TODO 2: Complete the chat_node function.
#   Inside the function:
#     a) Call llm.invoke() with state["user_input"] as the argument
#     b) Store the result in a variable (e.g., `ai_message`)
#     c) Return a dict: {"response": ai_message.content}
#
#   The return value is a dictionary that updates the state.
#   You only need to return the fields you're changing — LangGraph
#   merges your return value into the existing state automatically.

def chat_node(state: State) -> dict:
    """Send the user's input to the LLM and return the response."""
    # TODO 2: Write your code here
    pass


# =============================================================================
# STEP 4: Build the graph
# =============================================================================
#
# Now we connect everything together. Building a graph has three steps:
#
#   1. Create a StateGraph and tell it what State looks like
#   2. Add your node(s) to the graph
#   3. Add edges to connect them (including START and END)
#
# The flow will be:
#
#   START  -->  chat_node  -->  END
#
# After defining the structure, we call .compile() to turn our graph
# definition into something we can actually run.
#
# TODO 3: Build and compile the graph.
#   a) Create the graph:    graph = StateGraph(State)
#   b) Add the node:        graph.add_node("chat", chat_node)
#   c) Connect START to it: graph.add_edge(START, "chat")
#   d) Connect it to END:   graph.add_edge("chat", END)
#   e) Compile it:          app = graph.compile()

# TODO 3: Write your code here (5 lines)


# =============================================================================
# STEP 5: Run it!
# =============================================================================
#
# To run the graph, we call app.invoke() with an initial state.
# We provide the user_input and leave response empty — our node will fill it in.
#
# The if __name__ == "__main__" guard means this code only runs when you
# execute the file directly (not when importing it as a module).

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

    # TODO 4: Invoke the graph and print the response.
    #   a) Call app.invoke() with the initial state:
    #      result = app.invoke({"user_input": user_message, "response": ""})
    #   b) Print the response:
    #      print(f"LLM: {result['response']}")

    # TODO 4: Write your code here (2 lines)

    print()
    print("=" * 60)
    print("  Congratulations! You just ran your first LangGraph!")
    print("=" * 60)
