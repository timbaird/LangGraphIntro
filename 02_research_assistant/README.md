# Exercise 2: Research Assistant

## Goal

Build a 3-node pipeline that researches a topic, summarises the findings, and formats them into a clean report.

```
START  -->  [ research ]  -->  [ summarise ]  -->  [ format ]  -->  END
                |                    |                  |
          Generates 5          Condenses to        Formats as
          key facts           2-3 sentences       bullet points
```

## What You'll Learn

| Concept | What it means |
|---------|--------------|
| **Multi-node graphs** | Chaining multiple nodes together in a pipeline |
| **State accumulation** | Each node adds data to the state — later nodes can read earlier nodes' outputs |
| **System messages** | Giving the LLM a role/persona to guide its behaviour |
| **Separation of concerns** | Each node has ONE job — research, summarise, or format |

## How Data Flows Through the Pipeline

Watch how the state grows at each step:

| After Node | Fields filled in state |
|---|---|
| *Start* | `topic` only |
| `research` | `topic` + `research_notes` |
| `summarise` | `topic` + `research_notes` + `summary` |
| `format` | `topic` + `research_notes` + `summary` + `formatted_output` |

## Instructions

1. Open `research_graph.py` in your editor
2. Complete the 6 TODOs
3. Run it:

```bash
python 02_research_assistant/research_graph.py
```

4. Try different topics! Compare how the raw research notes differ from the final formatted output.

## If You Get Stuck

- Check `solutions/02_research_assistant_solution.py`
- Make sure Exercise 1 works first — the LLM connection is the same

## Quick Concept Check

After completing this exercise, you should be able to answer:

1. Why does the `summarise_node` read from `state["research_notes"]` instead of `state["topic"]`?
2. What would happen if you swapped the order of the `summarise` and `format` edges?
3. Could you add a 4th node? What would it do?

## Want to Learn More?

- [LangGraph Core Concepts](https://langchain-ai.github.io/langgraph/concepts/) — state, nodes, and edges explained
- [LangChain Messages](https://python.langchain.com/docs/concepts/messages/) — SystemMessage, HumanMessage, and more
- Try asking an LLM: *"What is the difference between a linear pipeline and a graph with conditional edges in LangGraph?"*
- **Next step: Conditional edges** — LangGraph can route to different nodes based on the state. Search for *"LangGraph conditional edges tutorial"* to explore this.
