# Runnables
- Def: A unit of work which can be invoke
- Runnable is a "protocol" in langchain implemented by chat models, output parsers, prompt templates, tools, etc.
- Chains are composed of runnable components

### RunnableSequence 
Invokes a series of runnables sequentially, with one runnable's
output serving as the next's input. Construct using the `|` operator or by
passing a list of runnables to RunnableSequence.

### RunnableParallel 
Invokes runnables concurrently, providing the same input
to each. Construct it using a dict literal within a sequence or by passing a
dict to RunnableParallel.