# Chains, Agents, AgentExecutors and Tools

## Chain 
Purpose - to codify a sequence of actions
- Chain refers to sequences of calls/actions - whether using an LLM, a tool, or involving a data preprocessing step. </br>
- Can be thought of as a sequence of hard coded actions.

## Agent
Purpose - to use LLM to choose a sequence of actions </br>
- Can be used to choose among multiple available sets of actions, or chains
- Agent makes the decisions regarding what sequence of actions to proceed with based on the input and intermediate steps


## AgentExecutor
Purpose - call the agent, execute the actions decided upon by the agent and pass the output of those actions back to the agent
```python
next_action = agent.get_action(...)
while next_action != AgentFinish:
    observation = run(next_action)
    next_action = agent.get_action(..., next_action, observation)
return next_action
```
Above is the pseudocode of how the AgentExecutor works.
- AgentExecutor is the runtime of the agent
- Handles possible errors caused due to following through with what the agent chose to do