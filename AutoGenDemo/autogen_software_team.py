"""
AutoGen 软件开发团队协作案例
"""

import os
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 先测试一个版本，使用 OpenAI 客户端
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console


def create_openai_model_client():
    """创建 OpenAI 模型客户端用于测试"""
    return OpenAIChatCompletionClient(
        model=os.getenv("LLM_MODEL_ID", "gpt-4o"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
        model_info={
            "json_output": True,
            "function_calling": False,
            "vision": False,
            "family": "unknown",
            "structured_output": True,
        }
    )


def create_product_manager(model_client):
    """Create product manager agent"""
    system_message = """You are an experienced product manager specializing in requirement analysis and project planning for software products.

    Your core responsibilities include:
    1. **Requirement Analysis**: Deeply understand user needs, identify core functions and boundary conditions
    2. **Technical Planning**: Develop clear technical implementation paths based on requirements
    3. **Risk Assessment**: Identify potential technical risks and user experience issues
    4. **Coordination and Communication**: Communicate effectively with engineers and other team members

    When receiving a development task, please analyze it according to the following structure:
    1. Requirement understanding and analysis
    2. Functional module division
    3. Technology selection recommendations
    4. Implementation priority sorting
    5. Acceptance criteria definition

    Please respond concisely and clearly, and say "Please engineer start implementation" after completing the analysis."""

    return AssistantAgent(
        name="ProductManager",
        model_client=model_client,
        system_message=system_message,
    )


def create_engineer(model_client):
    """Create software engineer agent"""
    system_message = """You are a senior software engineer skilled in Python development and web application construction.

    Your technical expertise includes:
    1. **Python Programming**: Proficient in Python syntax and best practices
    2. **Web Development**: Expert in frameworks such as Streamlit, Flask, Django
    3. **API Integration**: Rich experience in third-party API integration
    4. **Error Handling**: Focus on code robustness and exception handling

    When receiving a development task, please:
    1. Carefully analyze technical requirements
    2. Choose appropriate technical solutions
    3. Write complete code implementation
    4. Add necessary comments and explanations
    5. Consider boundary cases and exception handling

    Please provide complete runnable code and say "Please code reviewer check" after completion."""

    return AssistantAgent(
        name="Engineer",
        model_client=model_client,
        system_message=system_message,
    )


def create_code_reviewer(model_client):
    """Create code reviewer agent"""
    system_message = """You are an experienced code review expert focusing on code quality and best practices.

    Your review focus includes:
    1. **Code Quality**: Check code readability, maintainability, and performance
    2. **Security**: Identify potential security vulnerabilities and risk points
    3. **Best Practices**: Ensure code follows industry standards and best practices
    4. **Error Handling**: Verify the completeness and rationality of exception handling

    Review process:
    1. Carefully read and understand code logic
    2. Check code standards and best practices
    3. Identify potential issues and improvement points
    4. Provide specific modification suggestions
    5. Evaluate overall code quality

    Please provide specific review comments and say "Code review completed, please user proxy test" after completion."""

    return AssistantAgent(
        name="CodeReviewer",
        model_client=model_client,
        system_message=system_message,
    )


def create_user_proxy():
    """Create user proxy agent"""
    return UserProxyAgent(
        name="UserProxy",
        description="""User proxy, responsible for the following duties:
1. Propose development requirements on behalf of users
2. Execute final code implementation
3. Verify whether functions meet expectations
4. Provide user feedback and suggestions

Please reply TERMINATE after completing the test.""",
    )


async def run_software_development_team():
    """运行软件开发团队协作"""

    print("🔧 正在初始化模型客户端...")

    # 先使用标准的 OpenAI 客户端测试
    model_client = create_openai_model_client()

    print("👥 正在创建智能体团队...")

    # 创建智能体团队
    product_manager = create_product_manager(model_client)
    engineer = create_engineer(model_client)
    code_reviewer = create_code_reviewer(model_client)
    user_proxy = create_user_proxy()

    # 添加终止条件
    termination = TextMentionTermination("TERMINATE")

    # 创建团队聊天
    team_chat = RoundRobinGroupChat(
        participants=[
            product_manager,
            engineer,
            code_reviewer,
            user_proxy
        ],
        termination_condition=termination,
        max_turns=2,  # 增加最大轮次
    )

    # 定义开发任务
    task = """We need to develop a Bitcoin price display application with the following specific requirements:
            Core functions:
            - Display Bitcoin current price in real-time (USD)
            - Display 24-hour price change trend (percentage and amount of increase/decrease)
            - Provide price refresh function

            Technical requirements:
            - Use Streamlit framework to create web application
            - Simple and beautiful interface, user-friendly
            - Add appropriate error handling and loading status

            Please team collaborate to complete this task, from requirement analysis to final implementation."""

    # 执行团队协作
    print("🚀 启动 AutoGen 软件开发团队协作...")
    print("=" * 60)

    # 使用 Console 来显示对话过程
    result = await Console(team_chat.run_stream(task=task))

    print("\n" + "=" * 60)
    print("✅ 团队协作完成！")

    return result


# 主程序入口
if __name__ == "__main__":
    try:
        # 运行异步协作流程
        result = asyncio.run(run_software_development_team())

        print(f"\n📋 协作结果摘要：")
        print(f"- 参与智能体数量：4个")
        print(f"- 任务完成状态：{'成功' if result else '需要进一步处理'}")

    except ValueError as e:
        print(f"❌ 配置错误：{e}")
        print("请检查 .env 文件中的配置是否正确")
    except Exception as e:
        print(f"❌ 运行错误：{e}")
        import traceback

        traceback.print_exc()


