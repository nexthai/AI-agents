Files:

autogen_software_team.py - Main example code (based on the OpenAI client)

requirements.txt - List of dependency packages

README.md - This documentation

---
Multi-agent Collaboration: Demonstrates the complete collaboration process involving product managers, engineers, code reviewers, and user agents.

Real-world Development Scenario: The complete software development lifecycle from requirements analysis to code implementation.

Automated Process: Automatic task transfer between agents without manual intervention.

Code Generation and Review: Automatically generates runnable code and performs quality reviews.

- ProductManager (Product Manager): Responsible for transforming users' vague requirements into clear, executable development plans.
- Engineer: Based on the development plan, responsible for writing specific application code.
- CodeReviewer (Code Reviewer): Responsible for reviewing code submitted by engineers to ensure its quality, readability, and robustness.
- UserProxy (User Proxy): Represents the end user, initiates the initial task, and is responsible for executing and verifying the final delivered code.
