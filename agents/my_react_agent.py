from typing import List, Tuple, Union, Dict, Any
from langchain_core.tools import Tool
from langchain_core.tools.render import render_text_description
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents.output_parsers.react_single_input import (
    ReActSingleInputOutputParser,
)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool

    raise ValueError(f"Tool with name {tool_name} not found.")


def format_log_to_str(
    intermediate_steps: List[Tuple[AgentAction, str]],
    observation_prefix: str = "Observation: ",
    llm_prefix: str = "Thought: ",
) -> str:
    """Construct the scratchpad that lets the agent continue its thought process."""
    thoughts = ""
    for action, observation in intermediate_steps:
        thoughts += action.log
        thoughts += f"\n{observation_prefix}:{observation}\n{llm_prefix}"

    return thoughts


# agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)


def execute_react_agent(
    llm: BaseLanguageModel, tools: List[Tool], input: Dict[str, Any]
) -> Dict[str, Any]:
    react_prompt_template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """

    react_prompt = PromptTemplate.from_template(template=react_prompt_template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    intermediate_steps = []

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        }
        | react_prompt
        | llm
        | ReActSingleInputOutputParser()
    )

    agent_step = ""
    while not isinstance(agent_step, AgentFinish):
        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {"input": input, "agent_scratchpad": intermediate_steps}
        )
        print(agent_step)

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_to_use = find_tool_by_name(tools=tools, tool_name=tool_name)
            tool_input = agent_step.tool_input

            observation = tool_to_use.func(str(tool_input))
            print(f"{observation=}")

            intermediate_steps.append((agent_step, observation))

    return agent_step.return_values
