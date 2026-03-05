"""
=============================================================================
 Exercise 2: Research Assistant — A 3-Node Graph
=============================================================================

 BUILDING ON WHAT YOU LEARNED

 In Exercise 1, you built a single-node graph. Now you'll build something
 more realistic: a 3-node graph where each node does a different job,
 and data flows through the pipeline.

 Your Research Assistant will work like this:

     START
       |
       v
   [ research ]     Node 1: Generate key facts about a topic
       |
       v
   [ summarise ]    Node 2: Condense the research into a summary
       |
       v
   [ format ]       Node 3: Format the summary as clean bullet points
       |
       v
      END

 This is a PIPELINE — each node builds on the previous node's work.
 The state carries data forward from one node to the next, like a
 relay race passing a baton.

 NEW CONCEPTS YOU'LL LEARN:
   - Multi-node graphs (chaining nodes together)
   - How state accumulates as it passes through nodes
   - Using different prompts for different tasks
   - System messages vs user messages in LangChain

 INSTRUCTIONS:
   Complete the TODOs below. There are 6 this time.
   If you get stuck, check solutions/02_research_assistant_solution.py

 PREREQUISITES:
   - You've completed Exercise 1
   - Your .env file has a valid OPENROUTER_API_KEY
=============================================================================
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# LangChain message types — these let us send structured messages to the LLM.
#
# When talking to a chat LLM, messages have roles:
#   - SystemMessage: Instructions that set the LLM's behaviour
#                    (e.g., "You are a research assistant")
#   - HumanMessage:  The user's input (what they're asking about)
#
# This is more powerful than sending a plain string because it lets us
# guide the LLM's behaviour with a system prompt PLUS give it the data
# to work with as a human message.
#
# Docs: https://python.langchain.com/docs/concepts/messages/
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()


# =============================================================================
# STEP 1: Define your State
# =============================================================================
#
# This time, our state has MORE fields because data accumulates as it
# passes through the pipeline:
#
#   topic            — what the user wants to research (set at the start)
#   research_notes   — raw research from Node 1 (filled by research node)
#   summary          — condensed summary from Node 2 (filled by summarise node)
#   formatted_output — final formatted result from Node 3 (filled by format node)
#
# Notice how each node fills in one field, building on the previous work.
# This is the power of state: it's the shared workspace that all nodes
# can read from and write to.

class State(TypedDict):
    topic: str
    research_notes: str
    summary: str
    formatted_output: str


# =============================================================================
# STEP 2: Create the LLM connection
# =============================================================================
#
# Same as Exercise 1 — we create our OpenRouter connection.
#
# TODO 1: Create the LLM object (same as Exercise 1).
#   llm = ChatOpenAI(
#       model="google/gemini-2.0-flash-001",
#       api_key=os.environ["OPENROUTER_API_KEY"],
#       base_url="https://openrouter.ai/api/v1",
#   )

llm = None  # <-- Replace with ChatOpenAI(...)


# =============================================================================
# STEP 3: Define Node 1 — The Researcher
# =============================================================================
#
# This node takes the topic and asks the LLM to generate research notes.
#
# We use SystemMessage + HumanMessage instead of a plain string so we can:
#   - Give the LLM a ROLE (via SystemMessage) — "You are a research assistant"
#   - Give it the TASK (via HumanMessage) — "Research this topic: ..."
#
# The invoke() method accepts a list of messages. The LLM reads them all
# and generates a response that considers both the system instructions
# and the human message.
#
# TODO 2: Complete the research_node function.
#   a) Create a list of messages:
#      messages = [
#          SystemMessage(content="You are a research assistant. Given a topic, "
#                                "provide 5 key facts or points about it. "
#                                "Be concise but informative."),
#          HumanMessage(content=f"Research this topic: {state['topic']}"),
#      ]
#   b) Call the LLM: ai_message = llm.invoke(messages)
#   c) Return the update: return {"research_notes": ai_message.content}

def research_node(state: State) -> dict:
    """Node 1: Research the topic and produce raw notes."""
    # TODO 2: Write your code here
    pass


# =============================================================================
# STEP 4: Define Node 2 — The Summariser
# =============================================================================
#
# This node reads the research_notes from Node 1 and condenses them
# into a shorter summary.
#
# KEY INSIGHT: This node doesn't know anything about the original topic
# directly — it reads the RESEARCH NOTES from state, which were produced
# by the previous node. This is how data flows through a pipeline.
#
# TODO 3: Complete the summarise_node function.
#   a) Create messages that ask the LLM to summarise the research:
#      messages = [
#          SystemMessage(content="You are a summariser. Take the research notes "
#                                "provided and condense them into a clear, "
#                                "2-3 sentence summary."),
#          HumanMessage(content=f"Summarise these research notes:\n\n"
#                               f"{state['research_notes']}"),
#      ]
#   b) Call the LLM and return: {"summary": ai_message.content}

def summarise_node(state: State) -> dict:
    """Node 2: Summarise the research notes into a concise overview."""
    # TODO 3: Write your code here
    pass


# =============================================================================
# STEP 5: Define Node 3 — The Formatter
# =============================================================================
#
# This node takes the summary and formats it nicely with a title and
# bullet points. It's the final step in our pipeline.
#
# TODO 4: Complete the format_node function.
#   a) Create messages that ask the LLM to format the output:
#      messages = [
#          SystemMessage(content="You are a formatter. Take the summary provided "
#                                "and format it as a clean report with:\n"
#                                "- A title\n"
#                                "- 3-5 bullet points\n"
#                                "- A one-sentence conclusion\n"
#                                "Use markdown formatting."),
#          HumanMessage(content=f"Format this summary into a report:\n\n"
#                               f"{state['summary']}"),
#      ]
#   b) Call the LLM and return: {"formatted_output": ai_message.content}

def format_node(state: State) -> dict:
    """Node 3: Format the summary into a clean, readable report."""
    # TODO 4: Write your code here
    pass


# =============================================================================
# STEP 6: Build the graph
# =============================================================================
#
# Now we connect our three nodes in sequence. The pattern is the same
# as Exercise 1, but with more nodes and more edges:
#
#   START --> research --> summarise --> format --> END
#
# Each add_edge(A, B) call means "after A finishes, run B next".
#
# TODO 5: Build and compile the graph.
#   a) Create the graph:       graph = StateGraph(State)
#   b) Add all three nodes:    graph.add_node("research", research_node)
#                               graph.add_node("summarise", summarise_node)
#                               graph.add_node("format", format_node)
#   c) Connect them in order:  graph.add_edge(START, "research")
#                               graph.add_edge("research", "summarise")
#                               graph.add_edge("summarise", "format")
#                               graph.add_edge("format", END)
#   d) Compile:                app = graph.compile()

# TODO 5: Write your code here (8 lines)


# =============================================================================
# STEP 7: Run it!
# =============================================================================
#
# This time we'll show the output of each stage so you can see
# how data accumulates in the state as it passes through the pipeline.

if __name__ == "__main__":
    print("=" * 60)
    print("  Research Assistant — 3-Node LangGraph Pipeline")
    print("=" * 60)
    print()

    topic = input("Enter a topic to research: ")
    print()

    # TODO 6: Invoke the graph and display results.
    #   a) Run the graph:
    #      result = app.invoke({
    #          "topic": topic,
    #          "research_notes": "",
    #          "summary": "",
    #          "formatted_output": "",
    #      })
    #   b) Print each stage of the pipeline (this is done for you below,
    #      just uncomment it after you create the `result` variable):

    # TODO 6: Invoke the graph here (1 call to app.invoke)

    # Uncomment the lines below after completing TODO 6:
    # print("─" * 60)
    # print("STAGE 1 — Raw Research Notes:")
    # print("─" * 60)
    # print(result["research_notes"])
    # print()
    # print("─" * 60)
    # print("STAGE 2 — Summary:")
    # print("─" * 60)
    # print(result["summary"])
    # print()
    # print("─" * 60)
    # print("STAGE 3 — Formatted Report:")
    # print("─" * 60)
    # print(result["formatted_output"])
    # print()
    # print("=" * 60)
    # print("  Done! Your research assistant processed the topic through")
    # print("  3 nodes, each building on the previous node's work.")
    # print("=" * 60)
