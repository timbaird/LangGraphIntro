"""
=============================================================================
 Exercise 2: Research Assistant — SOLUTION
=============================================================================

 This is the complete, working solution for Exercise 2.
 Compare your code in 02_research_assistant/research_graph.py against this
 if you get stuck.
=============================================================================
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


# STEP 1: Define your State
class State(TypedDict):
    topic: str
    research_notes: str
    summary: str
    formatted_output: str


# STEP 2: Create the LLM connection
llm = ChatOpenAI(
    model="google/gemini-2.0-flash-001",
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)


# STEP 3: Node 1 — The Researcher
def research_node(state: State) -> dict:
    """Node 1: Research the topic and produce raw notes."""
    messages = [
        SystemMessage(content="You are a research assistant. Given a topic, "
                              "provide 5 key facts or points about it. "
                              "Be concise but informative."),
        HumanMessage(content=f"Research this topic: {state['topic']}"),
    ]
    ai_message = llm.invoke(messages)
    return {"research_notes": ai_message.content}


# STEP 4: Node 2 — The Summariser
def summarise_node(state: State) -> dict:
    """Node 2: Summarise the research notes into a concise overview."""
    messages = [
        SystemMessage(content="You are a summariser. Take the research notes "
                              "provided and condense them into a clear, "
                              "2-3 sentence summary."),
        HumanMessage(content=f"Summarise these research notes:\n\n"
                             f"{state['research_notes']}"),
    ]
    ai_message = llm.invoke(messages)
    return {"summary": ai_message.content}


# STEP 5: Node 3 — The Formatter
def format_node(state: State) -> dict:
    """Node 3: Format the summary into a clean, readable report."""
    messages = [
        SystemMessage(content="You are a formatter. Take the summary provided "
                              "and format it as a clean report with:\n"
                              "- A title\n"
                              "- 3-5 bullet points\n"
                              "- A one-sentence conclusion\n"
                              "Use markdown formatting."),
        HumanMessage(content=f"Format this summary into a report:\n\n"
                             f"{state['summary']}"),
    ]
    ai_message = llm.invoke(messages)
    return {"formatted_output": ai_message.content}


# STEP 6: Build the graph
graph = StateGraph(State)
graph.add_node("research", research_node)
graph.add_node("summarise", summarise_node)
graph.add_node("format", format_node)
graph.add_edge(START, "research")
graph.add_edge("research", "summarise")
graph.add_edge("summarise", "format")
graph.add_edge("format", END)
app = graph.compile()


# STEP 7: Run it!
if __name__ == "__main__":
    print("=" * 60)
    print("  Research Assistant — 3-Node LangGraph Pipeline")
    print("=" * 60)
    print()

    topic = input("Enter a topic to research: ")
    print()

    print("Processing... (this may take a moment — 3 LLM calls)")
    print()

    result = app.invoke({
        "topic": topic,
        "research_notes": "",
        "summary": "",
        "formatted_output": "",
    })

    print("─" * 60)
    print("STAGE 1 — Raw Research Notes:")
    print("─" * 60)
    print(result["research_notes"])
    print()
    print("─" * 60)
    print("STAGE 2 — Summary:")
    print("─" * 60)
    print(result["summary"])
    print()
    print("─" * 60)
    print("STAGE 3 — Formatted Report:")
    print("─" * 60)
    print(result["formatted_output"])
    print()
    print("=" * 60)
    print("  Done! Your research assistant processed the topic through")
    print("  3 nodes, each building on the previous node's work.")
    print("=" * 60)
