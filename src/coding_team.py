import json
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, GroupChat, GroupChatManager

# This is actual coder who writes the python code.
pm = AssistantAgent(
        name = 'Program_Manager',
        llm_config = {'config_list': config_list_from_json('src/config_files/openai.json')},
        system_message = "You are a technical program manager. You can give create product ideas, review task, provide feedback and support the coder and tester."
        )


coder = AssistantAgent(
        name='coder',
        llm_config = {'config_list': config_list_from_json('src/config_files/openai.json')},
        system_message = "you are python coder with 20 years of experience. You write extremely well python code. Your code is always well commented and easy to read. You also always create a readme file for code base."
        )

tester = AssistantAgent(
        name='tester',
        llm_config = {'config_list': config_list_from_json('src/config_files/openai.json')},
        system_message = "whenever coder writes some code, can you please write pytest for same code base."
        )

# create a UserProxyAgent instance named "user_proxy"
user = UserProxyAgent(
        name="user",
        system_message = "A human admin who bring task and confirm the solution",
        human_input_mode="ALWAYS",
        max_consecutive_auto_reply=10,
        code_execution_config={
            "last_n_messages": 2,
            "work_dir": "myteam",
            "use_docker": False,
        },
    )

groupchat = GroupChat(agents=[coder, user, pm, tester], messages=[], max_round=20)
manager = GroupChatManager(groupchat=groupchat, llm_config = {'config_list': config_list_from_json('src/config_files/openai.json')})

user.initiate_chat(
    manager,
    message="create a flask based app for using a LLM model name askGITA which can be deployed on internet. It has a field to read in a question from a user and it provides a response. In backend to get responsee it calls a function name : ragchain()"
)