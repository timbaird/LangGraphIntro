# LangGraph Introduction Exercise

A hands-on introduction to [LangGraph](https://langchain-ai.github.io/langgraph/) — a framework for building LLM-powered workflows as graphs.

You'll go from zero to a working multi-step AI pipeline in two exercises, using a **free** AI model — no credit card required.

---

## What You'll Build

| Exercise | What it does | Concepts |
|----------|-------------|----------|
| **01 — Hello World** | Single-node graph: send a message, get a reply | State, Node, Edge, Graph |
| **02 — Research Assistant** | 3-node pipeline: research → summarise → format | Multi-node graphs, state flow, system prompts |

---

## What is LangGraph?

LangGraph is a Python framework that lets you build LLM applications as **graphs** — a set of steps (called **nodes**) connected by arrows (called **edges**).

Why graphs? Because real-world AI tasks are rarely just "ask the LLM one question". You often want to:
- Break a big task into smaller steps
- Have different steps use different prompts or tools
- Route to different steps based on conditions

LangGraph gives you a clean way to structure this. It's built on top of [LangChain](https://www.langchain.com/), which provides the building blocks for talking to LLMs.

**Analogy:** Think of a graph like a flowchart. Each box is a node (a function that does work), and the arrows between boxes are edges (they control what runs next). Data flows through the chart in a shared "state" object.

```
┌─────────┐       ┌─────────────┐       ┌──────────┐
│  START   │──────>│  Your Node  │──────>│   END    │
└─────────┘       │  (function) │       └──────────┘
                  └─────────────┘
```

> **Want to learn more?** Search for: *"What is LangGraph and how does it compare to LangChain?"*
> or read the [official introduction](https://langchain-ai.github.io/langgraph/tutorials/introduction/).

---

## Prerequisites

Before starting, make sure you have:

- **Python 3.10 or later** — check with `python3 --version`
- **pip** — Python's package manager (comes with Python)
- **A text editor or IDE** — VS Code, PyCharm, or whatever you prefer
- **Basic Python knowledge** — variables, functions, dictionaries, f-strings

> **Don't have Python 3.10+?** Download it from [python.org/downloads](https://www.python.org/downloads/).
> On macOS you can also use `brew install python`.

---

## Setup

### Step 1: Clone the repository

If you haven't already:

```bash
git clone https://github.com/YOUR-INSTRUCTOR/LangGraphIntro.git
cd LangGraphIntro
```

### Step 2: Create a virtual environment

A virtual environment keeps this project's packages separate from your system Python. This is standard practice for Python projects.

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

You'll know it's active when you see `(venv)` at the start of your terminal prompt.

> **What's a virtual environment?** It's an isolated copy of Python where you can install packages without affecting your system. Search for: *"Python virtual environments explained simply"*

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

This installs three packages:

| Package | What it does |
|---------|-------------|
| `langgraph` | The graph framework — the star of this exercise |
| `langchain-openai` | Lets us talk to OpenAI-compatible APIs (including OpenRouter) |
| `python-dotenv` | Loads API keys from a `.env` file so they stay out of your code |

### Step 4: Verify packages installed correctly

```bash
python3 -c "from langgraph.graph import StateGraph; print('LangGraph OK')"
python3 -c "from langchain_openai import ChatOpenAI; print('LangChain OK')"
python3 -c "from dotenv import load_dotenv; print('dotenv OK')"
```

You should see three "OK" messages. If any fail, re-run `pip install -r requirements.txt`.

---

## Setting Up OpenRouter (Your AI Model Provider)

### What is OpenRouter?

To run an LLM (Large Language Model) in your code, you need access to one through an API. You *could* sign up directly with OpenAI, Google, Anthropic, etc. — but each has its own account, billing, and API format.

[OpenRouter](https://openrouter.ai/) solves this by giving you **one API key** that works with models from **all major providers**. Think of it like a universal remote control for AI models.

Even better: **OpenRouter offers many models completely free** — no credit card required. That's what we'll use for these exercises.

### Why OpenRouter?

- **Free models available** — no cost to get started
- **One API key** — access models from Google, OpenAI, Meta, and more
- **OpenAI-compatible API** — LangChain's `ChatOpenAI` works with it out of the box
- **Easy to switch models** — just change one string in your code

### Step 5: Create your OpenRouter account

1. Go to [openrouter.ai](https://openrouter.ai/)
2. Click **"Sign Up"** (top right)
3. You can sign up with:
   - **Email** — enter an email and password, then verify via the confirmation email
   - **Google account** — one-click sign in
   - **GitHub account** — one-click sign in (handy if you already have one)
4. That's it — no credit card needed!

### Step 6: Get your API key

1. Once logged in, click your **avatar/icon** in the top right corner
2. Go to **"Keys"** (or navigate directly to [openrouter.ai/keys](https://openrouter.ai/keys))
3. Click **"Create Key"**
4. Give it a name (e.g., "LangGraph Exercise") and click **Create**
5. **Copy the key immediately** — it starts with `sk-or-v1-` and you won't be able to see it again after leaving this page
6. Store it somewhere safe (a text file, password manager, or just paste it straight into your `.env` file in the next step)

### Step 7: Configure your API key

```bash
# Copy the example environment file
cp .env.example .env
```

Open the new `.env` file in your editor and paste your API key:

```
OPENROUTER_API_KEY=sk-or-v1-paste-your-actual-key-here
```

> **Security note:** The `.env` file is listed in `.gitignore` so it won't be committed to Git. This is important — never put API keys directly in your code or push them to GitHub. If you accidentally expose a key, you can revoke it and create a new one from the Keys page.

> **What's a `.env` file?** It's a simple text file that stores configuration values (like API keys) as `KEY=VALUE` pairs. The `python-dotenv` library loads these into your program at runtime. This pattern keeps secrets out of your source code. Search for: *"python dotenv explained"*

---

## Choosing Your AI Model

OpenRouter offers many models for free. For these exercises, you need a model that is:
- **Free** — no cost per request
- **Fast** — responds in a few seconds, not minutes
- **Capable enough** — can follow instructions and generate coherent text

### Recommended Free Models

Here are good choices, ranked by our recommendation for this exercise:

| Model ID | Provider | Why choose it? | Trade-offs |
|----------|----------|---------------|------------|
| `google/gemini-2.0-flash-001` | Google | **Our default.** Very fast, good quality, generous context window (1M tokens). Battle-tested and reliable. | Slightly older than newer Gemini versions |
| `google/gemini-2.5-flash` | Google | Newer than 2.0, strong across many tasks. Good all-rounder. | As a newer model, occasionally less predictable |
| `openai/gpt-4o-mini` | OpenAI | Familiar if you've used ChatGPT. Solid quality, fast responses. | Smaller context window than Gemini models |
| `openai/gpt-4.1-mini-2025-04-14` | OpenAI | Newer than gpt-4o-mini, improved instruction following. | Less community feedback available yet |
| `deepseek/deepseek-v3.2-20251201` | DeepSeek | Very capable, especially for detailed/creative responses. | Can be slightly slower than the mini/flash models |

**The exercises default to `google/gemini-2.0-flash-001`** — it's fast, free, reliable, and more than capable enough for what we're building. You can change the model later if you want to experiment.

### How to switch models

In the exercise code, you'll see a line like:

```python
model="google/gemini-2.0-flash-001"
```

To try a different model, just replace the string:

```python
model="openai/gpt-4o-mini"  # or any other model ID from the table above
```

That's it — one string change. This is one of the nice things about OpenRouter.

### Browsing all available models

To see the full list of free models (there are 20+), visit:
[openrouter.ai/models?pricing=free](https://openrouter.ai/models?pricing=free)

Each model page shows its pricing (look for **$0** on both input and output), speed benchmarks, and what it's good at.

### Free model usage limits

Free models on OpenRouter have rate limits to prevent abuse. The exact limits can change, but as a rough guide:

- **Free accounts** (no credits purchased): ~5–20 requests per day across all free models
- **Accounts with any credits purchased**: higher daily limits

**For these exercises, the free tier is more than enough.** Exercise 1 makes 1 LLM call and Exercise 2 makes 3 — so even the most conservative limit gives you plenty of room to complete both exercises and re-run them a few times.

If you hit a rate limit, just wait a few minutes and try again. The limits reset regularly.

> **Tip:** If you find yourself wanting to experiment more heavily, purchasing even a small amount of credit ($1–5) on OpenRouter significantly increases your rate limits on free models and also unlocks paid models. But this is completely optional — you do not need to spend anything for these exercises.

---

## Exercises

### Exercise 1: Hello World

**Time:** ~15 minutes

Your first LangGraph program. A single node that sends your message to an LLM and prints the reply.

```
START  -->  [ chat_node ]  -->  END
```

**Start here:** Open `01_hello_world/hello_langgraph.py` and follow the TODO comments.
Full instructions: [01_hello_world/README.md](01_hello_world/README.md)

**Run it:**
```bash
python 01_hello_world/hello_langgraph.py
```

---

### Exercise 2: Research Assistant

**Time:** ~20 minutes

A 3-node pipeline that researches a topic, summarises the findings, and formats them into a report.

```
START --> [ research ] --> [ summarise ] --> [ format ] --> END
```

**Start here:** Open `02_research_assistant/research_graph.py` and follow the TODO comments.
Full instructions: [02_research_assistant/README.md](02_research_assistant/README.md)

**Run it:**
```bash
python 02_research_assistant/research_graph.py
```

---

## Solutions

If you get stuck, complete solutions are in the `solutions/` folder:

| Exercise | Solution file |
|----------|--------------|
| 01 — Hello World | `solutions/01_hello_world_solution.py` |
| 02 — Research Assistant | `solutions/02_research_assistant_solution.py` |

Try to complete the exercises yourself first! The learning happens in the doing.

---

## Key Concepts Reference

Here's a quick reference for the core concepts used in these exercises:

### State
A Python dictionary (defined with `TypedDict`) that carries data through your graph. Every node reads from it and writes to it.

```python
class State(TypedDict):
    user_input: str    # Set at the start
    response: str      # Filled in by a node
```

### Node
A regular Python function that takes the current state and returns a dictionary of updates.

```python
def my_node(state: State) -> dict:
    # Do some work...
    return {"response": "result"}  # Updates state["response"]
```

### Edge
A connection between two nodes. `add_edge(A, B)` means "run B after A finishes".

```python
graph.add_edge("node_a", "node_b")  # node_a → node_b
```

### Graph
The overall structure. You add nodes and edges, then `.compile()` it to make it runnable.

```python
graph = StateGraph(State)
graph.add_node("my_node", my_node)
graph.add_edge(START, "my_node")
graph.add_edge("my_node", END)
app = graph.compile()            # Now you can call app.invoke(...)
```

### START and END
Special markers. `START` is where the graph begins. `END` is where it stops.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'langgraph'"
Your virtual environment isn't activated, or packages aren't installed.
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "KeyError: 'OPENROUTER_API_KEY'"
Your `.env` file is missing or doesn't contain the key. Make sure you've:
1. Copied `.env.example` to `.env`
2. Replaced `your-api-key-here` with your actual key (no quotes around the value)

### "AuthenticationError" or "401"
Your API key is invalid or expired. Go to [openrouter.ai/keys](https://openrouter.ai/keys) and check that your key is still active. Create a new one if needed.

### "429 Too Many Requests" or "Rate limit exceeded"
You've hit the free tier rate limit. Wait a few minutes and try again. If it keeps happening, you may need to wait until the next day for your limit to reset.

### "Connection error" or "timeout"
Check your internet connection. OpenRouter requires internet access to reach the AI models.

### The LLM response is empty or weird
Try running again — LLM responses can vary. If a specific model is consistently giving poor results, try switching to a different free model (see the model table above).

---

## Where to Go from Here

Now that you understand the basics, here are some next steps:

1. **Try different models** — Change the model string in your code and re-run the exercises. Compare how different models handle the same task. How does Gemini's output differ from GPT-4o-mini's?

2. **Conditional edges** — Route to different nodes based on the state. This is where graphs become more powerful than simple pipelines.
   - Search: *"LangGraph conditional edges tutorial"*
   - [Docs: Conditional Edges](https://langchain-ai.github.io/langgraph/how-tos/branching/)

3. **Human-in-the-loop** — Pause the graph to get user input mid-flow, then resume.
   - Search: *"LangGraph human in the loop"*

4. **Tool calling** — Let the LLM use tools (web search, calculators, APIs) as part of your graph.
   - Search: *"LangGraph tool calling agent"*
   - [Docs: Tool Calling](https://langchain-ai.github.io/langgraph/how-tos/tool-calling/)

5. **Memory and persistence** — Save conversation history so your graph remembers previous interactions.
   - Search: *"LangGraph memory and checkpointing"*

6. **The official LangGraph tutorials** — Work through the full tutorial series:
   - [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)

> **Tip:** When you want to understand a concept better, try asking an LLM! For example:
> *"Explain conditional edges in LangGraph with a simple example"*
> *"What's the difference between LangChain and LangGraph?"*

---

## Project Structure

```
LangGraphIntro/
├── README.md                ← You are here
├── .env.example             ← Template for your API key
├── .env                     ← Your actual API key (git-ignored, you create this)
├── .gitignore
├── requirements.txt         ← Python package dependencies
├── 01_hello_world/
│   ├── README.md            ← Exercise 1 instructions
│   └── hello_langgraph.py   ← Exercise 1 scaffolded code (edit this!)
├── 02_research_assistant/
│   ├── README.md            ← Exercise 2 instructions
│   └── research_graph.py    ← Exercise 2 scaffolded code (edit this!)
└── solutions/
    ├── 01_hello_world_solution.py
    └── 02_research_assistant_solution.py
```
