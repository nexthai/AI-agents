from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from hello_agents import HelloAgentsLLM
from hello_agents.agents import FunctionCallAgent
from hello_agents.context import ContextBuilder, ContextConfig, ContextPacket
from hello_agents.tools import MemoryTool, NoteTool, TerminalTool
from hello_agents.tools.registry import ToolRegistry
from hello_agents.core.message import Message


class CodebaseMaintainer:
    """Codebase Maintenance Assistant - Long-horizon agent example

    Integrates ContextBuilder + NoteTool + TerminalTool + MemoryTool
    Implements cross-session codebase maintenance task management
    """

    def __init__(
        self,
        project_name: str,
        codebase_path: str,
        llm: Optional[HelloAgentsLLM] = None
    ):
        self.project_name = project_name
        self.codebase_path = codebase_path
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Initialize LLM
        self.llm = llm or HelloAgentsLLM()

        # Initialize tools
        self.memory_tool = MemoryTool(user_id=project_name)
        self.note_tool = NoteTool(workspace=f"./{project_name}_notes")
        self.terminal_tool = TerminalTool(workspace=codebase_path, timeout=60)

        # Initialize context builder
        self.context_builder = ContextBuilder(
            memory_tool=self.memory_tool,
            rag_tool=None,  # This case does not use RAG
            config=ContextConfig(
                max_tokens=4000,
                reserve_ratio=0.15,
                min_relevance=0.2,
                enable_compression=True
            )
        )

        # Conversation history
        self.conversation_history: List[Message] = []

        # Statistics
        self.stats = {
            "session_start": datetime.now(),
            "commands_executed": 0,
            "notes_created": 0,
            "issues_found": 0
        }

        print(f"✅ Codebase maintenance assistant initialized: {project_name}")
        print(f"📁 Working directory: {codebase_path}")
        print(f"🆔 Session ID: {self.session_id}")

    def run(self, user_input: str, mode: str = "auto") -> str:
        """Run assistant

        Args:
            user_input: User input
            mode: Running mode
                - "auto": Automatically decide whether to use tools
                - "explore": Focus on code exploration
                - "analyze": Focus on problem analysis
                - "plan": Focus on task planning

        Returns:
            str: Assistant's answer
        """
        print(f"\n{'='*80}")
        print(f"👤 User: {user_input}")
        print(f"{'='*80}\n")

        # Step 1: Execute preprocessing based on mode
        pre_context = self._preprocess_by_mode(user_input, mode)

        # Step 2: Retrieve relevant notes
        relevant_notes = self._retrieve_relevant_notes(user_input)
        note_packets = self._notes_to_packets(relevant_notes)

        # Step 3: Build optimized context
        context = self.context_builder.build(
            user_query=user_input,
            conversation_history=self.conversation_history,
            system_instructions=self._build_system_instructions(mode),
            custom_packets=note_packets + pre_context
        )

        # Step 4: Call LLM
        print("🤖 Thinking...")
        response = self.llm.invoke(context)

        # Step 5: Post-processing
        self._postprocess_response(user_input, response)

        # Step 6: Update conversation history
        self._update_history(user_input, response)

        print(f"\n🤖 Assistant: {response}\n")
        print(f"{'='*80}\n")

        return response

    def _preprocess_by_mode(
        self,
        user_input: str,
        mode: str
    ) -> List[ContextPacket]:
        """Execute preprocessing based on mode, collect relevant information"""
        packets = []

        if mode == "explore" or mode == "auto":
            # Explore mode: Automatically view project structure
            print("🔍 Exploring codebase structure...")

            structure = self.terminal_tool.run({"command": "find . -type f -name '*.py' | head -n 20"})
            self.stats["commands_executed"] += 1

            packets.append(ContextPacket(
                content=f"[Codebase Structure]\n{structure}",
                timestamp=datetime.now(),
                token_count=len(structure) // 4,
                relevance_score=0.6,
                metadata={"type": "code_structure", "source": "terminal"}
            ))

        if mode == "analyze":
            # Analyze mode: Check code complexity and issues
            print("📊 Analyzing code quality...")

            # Count lines of code
            loc = self.terminal_tool.run({"command": "find . -name '*.py' -exec wc -l {} + | tail -n 1"})

            # Find TODO and FIXME
            todos = self.terminal_tool.run({"command": "grep -rn 'TODO\\|FIXME' --include='*.py' | head -n 10"})

            self.stats["commands_executed"] += 2

            packets.append(ContextPacket(
                content=f"[Code Statistics]\n{loc}\n\n[To-Do Items]\n{todos}",
                timestamp=datetime.now(),
                token_count=(len(loc) + len(todos)) // 4,
                relevance_score=0.7,
                metadata={"type": "code_analysis", "source": "terminal"}
            ))

        if mode == "plan":
            # Planning mode: Load recent notes
            print("📋 Loading task planning...")

            task_notes = self.note_tool.run({
                "action": "list",
                "note_type": "task_state",
                "limit": 3
            })

            if task_notes:
                content = "\n".join([f"- {note['title']}" for note in task_notes])
                packets.append(ContextPacket(
                    content=f"[Current Tasks]\n{content}",
                    timestamp=datetime.now(),
                    token_count=len(content) // 4,
                    relevance_score=0.8,
                    metadata={"type": "task_plan", "source": "notes"}
                ))

        return packets

    def _retrieve_relevant_notes(self, query: str, limit: int = 3) -> List[Dict]:
        """Retrieve relevant notes"""
        try:
            # Prioritize retrieving blockers
            blockers = self.note_tool.run({
                "action": "list",
                "note_type": "blocker",
                "limit": 2
            })

            # Search relevant notes
            search_results = self.note_tool.run({
                "action": "search",
                "query": query,
                "limit": limit
            })

            # Merge and deduplicate
            all_notes = {note.get('note_id') or note.get('id'): note for note in (blockers or []) + (search_results or [])}
            return list(all_notes.values())[:limit]

        except Exception as e:
            print(f"[WARNING] Note retrieval failed: {e}")
            return []

    def _notes_to_packets(self, notes: List[Dict]) -> List[ContextPacket]:
        """Convert notes to context packets"""
        packets = []

        for note in notes:
            # Set different relevance scores based on note type
            relevance_map = {
                "blocker": 0.9,
                "action": 0.8,
                "task_state": 0.75,
                "conclusion": 0.7
            }

            note_type = note.get('type', 'general')
            relevance = relevance_map.get(note_type, 0.6)

            content = f"[Note: {note.get('title', 'Untitled')}]\nType: {note_type}\n\n{note.get('content', '')}"

            packets.append(ContextPacket(
                content=content,
                timestamp=datetime.fromisoformat(note.get('updated_at', datetime.now().isoformat())),
                token_count=len(content) // 4,
                relevance_score=relevance,
                metadata={
                    "type": "note",
                    "note_type": note_type,
                    "note_id": note.get('note_id') or note.get('id')
                }
            ))

        return packets

    def _build_system_instructions(self, mode: str) -> str:
        """Build system instructions"""
        base_instructions = f"""You are the codebase maintenance assistant for the {self.project_name} project.

Your core capabilities:
1. Use TerminalTool to explore codebase (ls, cat, grep, find, etc.)
2. Use NoteTool to record discoveries and tasks
3. Provide coherent recommendations based on historical notes

Current session ID: {self.session_id}
"""

        mode_specific = {
            "explore": """
Current mode: Explore codebase

You should:
- Actively use terminal commands to understand code structure
- Identify key modules and files
- Record project architecture in notes
""",
            "analyze": """
Current mode: Analyze code quality

You should:
- Find code issues (duplication, complexity, TODOs, etc.)
- Evaluate code quality
- Record discovered issues as blocker or action notes
""",
            "plan": """
Current mode: Task planning

You should:
- Review historical notes and tasks
- Formulate next action plan
- Update task status notes
""",
            "auto": """
Current mode: Auto decision

You should:
- Flexibly choose strategies based on user needs
- Use tools when needed
- Maintain professionalism and practicality in responses
"""
        }

        return base_instructions + mode_specific.get(mode, mode_specific["auto"])

    def _postprocess_response(self, user_input: str, response: str):
        """Post-processing: Analyze response, automatically record important information"""

        # If issues found, automatically create blocker note
        if any(keyword in response.lower() for keyword in ["issue", "bug", "error", "blocker", "problem"]):
            try:
                self.note_tool.run({
                    "action": "create",
                    "title": f"Issue found: {user_input[:30]}...",
                    "content": f"## User Input\n{user_input}\n\n## Issue Analysis\n{response[:500]}...",
                    "note_type": "blocker",
                    "tags": [self.project_name, "auto_detected", self.session_id]
                })
                self.stats["notes_created"] += 1
                self.stats["issues_found"] += 1
                print("📝 Automatically created issue note")
            except Exception as e:
                print(f"[WARNING] Failed to create note: {e}")

        # If task planning, automatically create action note
        elif any(keyword in user_input.lower() for keyword in ["plan", "next", "task", "todo"]):
            try:
                self.note_tool.run({
                    "action": "create",
                    "title": f"Task planning: {user_input[:30]}...",
                    "content": f"## Discussion\n{user_input}\n\n## Action Plan\n{response[:500]}...",
                    "note_type": "action",
                    "tags": [self.project_name, "planning", self.session_id]
                })
                self.stats["notes_created"] += 1
                print("📝 Automatically created action plan note")
            except Exception as e:
                print(f"[WARNING] Failed to create note: {e}")

    def _update_history(self, user_input: str, response: str):
        """Update conversation history"""
        self.conversation_history.append(
            Message(content=user_input, role="user", timestamp=datetime.now())
        )
        self.conversation_history.append(
            Message(content=response, role="assistant", timestamp=datetime.now())
        )

        # Limit history length (keep recent 10 rounds of conversation)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

    # === Convenience methods ===

    def explore(self, target: str = ".") -> str:
        """Explore codebase"""
        return self.run(f"Please explore the code structure of {target}", mode="explore")

    def analyze(self, focus: str = "") -> str:
        """Analyze code quality"""
        query = f"Please analyze code quality" + (f", focusing on {focus}" if focus else "")
        return self.run(query, mode="analyze")

    def plan_next_steps(self) -> str:
        """Plan next steps"""
        return self.run("Based on current progress, plan next steps", mode="plan")

    def execute_command(self, command: str) -> str:
        """Execute terminal command"""
        result = self.terminal_tool.run({"command": command})
        self.stats["commands_executed"] += 1
        return result

    def create_note(
        self,
        title: str,
        content: str,
        note_type: str = "general",
        tags: List[str] = None
    ) -> str:
        """Create note"""
        result = self.note_tool.run({
            "action": "create",
            "title": title,
            "content": content,
            "note_type": note_type,
            "tags": tags or [self.project_name]
        })
        self.stats["notes_created"] += 1
        return result

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics"""
        duration = (datetime.now() - self.stats["session_start"]).total_seconds()

        # Get note summary
        try:
            note_summary = self.note_tool.run({"action": "summary"})
        except:
            note_summary = {}

        return {
            "session_info": {
                "session_id": self.session_id,
                "project": self.project_name,
                "duration_seconds": duration
            },
            "activity": {
                "commands_executed": self.stats["commands_executed"],
                "notes_created": self.stats["notes_created"],
                "issues_found": self.stats["issues_found"]
            },
            "notes": note_summary
        }

    def generate_report(self, save_to_file: bool = True) -> Dict[str, Any]:
        """Generate session report"""
        report = self.get_stats()

        if save_to_file:
            report_file = f"maintainer_report_{self.session_id}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2, default=str)
            report["report_file"] = report_file
            print(f"📄 Report saved: {report_file}")

        return report


def main():
    """主函数 - 演示 CodebaseMaintainer 的使用（Agentic 版本）

    在这个版本中：
    - Agent 自主决定使用哪些工具
    - 不预定义工作流
    - Agent 根据需求灵活探索代码库
    """
    print("=" * 80)
    print("CodebaseMaintainer 演示（Agentic 版本）")
    print("=" * 80 + "\n")

    # 初始化助手
    maintainer = CodebaseMaintainer(
        project_name="my_flask_app",
        codebase_path="./my_flask_app",
        llm=HelloAgentsLLM()
    )

    # 探索代码库（Agent 自主决定如何探索）
    print("\n### 探索代码库（Agent 自主探索）###")
    response = maintainer.explore()

    # 分析代码质量（Agent 自主决定分析方法）
    print("\n### 分析代码质量（Agent 自主分析）###")
    response = maintainer.analyze()

    # 规划下一步（Agent 基于历史信息规划）
    print("\n### 规划下一步任务（Agent 自主规划）###")
    response = maintainer.plan_next_steps()

    # 生成报告
    print("\n### 生成会话报告 ###")
    report = maintainer.generate_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))

    print("\n" + "=" * 80)
    print("演示完成!")
    print("=" * 80)


if __name__ == "__main__":
    main()