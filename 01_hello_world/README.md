# Exercise 1: Hello LangGraph!

## Goal

Build the simplest possible LangGraph application — a single-node graph that sends your message to an LLM and prints the reply.

```
START  -->  [ chat_node ]  -->  END
                 |
           (calls the LLM)
```

## What You'll Learn

| Concept | What it means |
|---------|--------------|
| **State** | A dictionary that carries data through your graph. Every node can read from it and write to it. |
| **Node** | A Python function that does one piece of work. It receives the current state and returns updates. |
| **Edge** | An arrow connecting two nodes. Tells LangGraph what order to run things in. |
| **Graph** | The overall structure — nodes + edges. You `.compile()` it to make it runnable. |

## Instructions

1. Open `hello_langgraph.py` in your editor
2. Read through the comments — they explain every concept as you go
3. Complete the 4 TODOs (each one is clearly marked and explained)
4. Run it:

```bash
python 01_hello_world/hello_langgraph.py
```

5. Type a message when prompted and watch the LLM respond!

## If You Get Stuck

- Check `solutions/01_hello_world_solution.py` for the complete working code
- The most common issue is a missing or incorrect API key — make sure your `.env` file is set up

## Quick Concept Check

After completing this exercise, you should be able to answer:

1. What does `StateGraph(State)` do?
2. Why does `chat_node` return a dictionary instead of a string?
3. What do `START` and `END` represent?

## Want to Learn More?

- [LangGraph Quick Start](https://langchain-ai.github.io/langgraph/tutorials/introduction/) — official tutorial
- [What is a Graph?](https://en.wikipedia.org/wiki/Directed_graph) — the computer science concept behind LangGraph
- Try asking an LLM: *"Explain the concept of a directed graph in simple terms with examples"*
