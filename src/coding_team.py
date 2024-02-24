import json
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# This is actual coder who writes the python code.
program_manager = AssistantAgent(
        name = 'TechnicalProjectManager',
        llm_config = {'config_list': config_list_from_json('src/config_files/openai.json')},
        system_message = "You are a technical project manager. You break complex task into simple doable steps for coder and also reviews his code."
        )

user = UserProxyAgent(
        name = 'user',
        max_consecutive_auto_reply=0,
        human_input_mode='NEVER',
        code_execution_config={"work_dir": "coding", "use_docker": False},
        )

def ask_program_manager(message):
    user.initiate_chat(program_manager, message=message)
    return user.last_message()['content']

assistant = AssistantAgent(
        name = 'assistant',
        llm_config={
            "temperature": 0,
            "timeout": 600,
            "cache_seed": 42,
            "config_list": config_list_from_json('src/config_files/openai.json'),
            "functions": [
                {
                    "name": "ask_program_manager",
                    "description": "ask program manager to: 1. get a plan for finishing a task, 2. verify the execution result of the plan and potentially suggest new task.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "question to ask program manager. Make sure the question include enough context, such as the code and the execution result. The program manager does not know the conversation between you and the user, unless you share the conversation with the program manager.",
                                },
                        },
                    "required": ["message"],
                    },
                }
            ]
            }
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="TERMINATE",
        max_consecutive_auto_reply=10,
    # is_termination_msg=lambda x: "content" in x and x["content"] is not None and x["content"].rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "planning",
            "use_docker": False,
        },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
        function_map={"ask_project_manager": ask_program_manager},
)

user_proxy.initiate_chat(
    assistant,
    message="""Create a flask based web app for asking question and getting responses. Both questions and answers will be in str. Code should be written in python.""",
)