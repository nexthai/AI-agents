The inspiration for the Reflection mechanism comes from the human learning process: we proofread after completing a first draft and verify after solving a math problem. This idea is embodied in multiple studies, such as the Reflexion framework proposed by Shinn, Noah in 2023[3]. Its core workflow can be summarized as a concise three-step loop: Execute -> Reflect -> Refine.

- Execution: First, the agent attempts to complete the task using familiar methods (such as ReAct or Plan-and-Solve), generating a preliminary solution or action trajectory. This can be seen as a "first draft."
- Reflection: Next, the agent enters the reflection phase. It calls an independent large language model instance, or one with special prompts, to play the role of a "reviewer." This "reviewer" examines the "first draft" generated in the first step and evaluates it from multiple dimensions, such as:
  -Factual Errors: Is there content that contradicts common sense or known facts?
  - Logical Flaws: Are there inconsistencies or contradictions in the reasoning process?
  - Efficiency Issues: Is there a more direct, more concise path to complete the task?
  - Missing Information: Are some key constraints or aspects of the problem overlooked? Based on the evaluation, it generates structured Feedback, pointing out specific problems and improvement suggestions.
- Refinement: Finally, the agent uses the "first draft" and "feedback" as new context, calls the large language model again, and asks it to revise the first draft based on the feedback content, generating a more complete "revised draft."

