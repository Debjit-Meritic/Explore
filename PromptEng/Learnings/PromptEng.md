# Prompt Engineering
### Types of LLM

| Base LLM | Instruction Tuned LLM |
| ----- | ---- |
| Predicts next word | Tries to follow instructions |

The type of LLM affects the prompting practices to keep in mind

## Principles of Prompting
1. Write clear and specific instructions
   #### Tactics
   - Use delimiters: triple quotes, triple backticks, triple dashes, angle brackets, xml tags
     - Useful for preventing prompt injection
   - Ask for structured output
   - Ask the model to validate
   - Few shot prompting
        
2. Give the model time to "think"
   #### Tactics
   - Specify steps required to complete the task.
   - Ask for output in specific format
   - Instruct the model to work out its own solution before rushing to a conclusion


## Empirical Heuristics
- User prompt written in human like language rather than json formatted string gives much better output for instruction following tasks.
- While the prompt in human lang performs better, additional data passed in the data should be semi structured or structured like json for better output.
- With json formatted inputs, word counting abilities seem to be off by a factor of 0.7 to 0.8; so if asking for 50 words, llm returns 38.  
