The ingenuity of ReAct lies in recognizing that thinking and acting are complementary. Thinking guides action, while action results in turn correct thinking. To this end, the ReAct paradigm uses a special prompt engineering to guide the model so that each step of its output follows a fixed trajectory:

- Thought (Thinking): This is the agent's "inner monologue." It analyzes the current situation, decomposes tasks, formulates the next plan, or reflects on the results of the previous step.
- Action (Acting): This is the specific action the agent decides to take, usually calling an external tool, such as Search['Huawei's latest phone'].
- Observation (Observing): This is the result returned from the external tool after executing the Action, such as a summary of search results or an API return value.
