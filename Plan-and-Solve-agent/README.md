Plan-and-Solve decouples the entire process into two core stages:

- Planning Phase: First, the agent receives the user's complete question. Its first task is not to directly solve the problem or call tools, but to decompose the problem and formulate a clear, step-by-step action plan. This plan itself is the product of a large language model call.
- Solving Phase: After obtaining the complete plan, the agent enters the execution phase. It will strictly execute according to the steps in the plan, one by one. Each step's execution may be an independent LLM call or processing of the previous step's results, until all steps in the plan are completed and the final answer is obtained.
