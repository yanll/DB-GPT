import asyncio
import json
import logging
from typing import Dict, List, Optional, Union, Tuple

from dbgpt.agent import AgentMessage, ActionOutput
from dbgpt.agent.expand.actions.demand_action import DemandAction
from dbgpt.agent.resource.resource_api import ResourceType
from dbgpt.agent.resource.resource_lark_api import ResourceLarkClient
from dbgpt.core import ModelMessageRoleType
from dbgpt.util.error_types import LLMChatError
from dbgpt.agent.core.base_agent import ConversableAgent
from dbgpt.serve.agent.db.gpts_conversations_db import GptsConversationsDao, GptsConversationsEntity

logger = logging.getLogger(__name__)


class ProductionAssistantAgent(ConversableAgent):
    name: str = "Listen"
    profile: str = "ProductionAssistant"
    goal: str = "提取我输入信息中的需求点并按字段要求拆解，最后将拆解后的信息按我要求的格式返回。"
    constraints: List[str] = [
        "必须按照我提供的格式返回。",
        "首先你具备通用AI助手的能力，不要作出奇怪的回答。",
        "如果我不想继续了，提醒我可以随时继续提问。",
        "如果类似的信息我多次输入，以最后输入的为准。",
        "注意你是一个需求内容专家，目标是提取信息，如果提取不到有用的信息，告诉我你能做什么。",
        "请仔细理解我的输入，客观真实的识别，按照：{fields} 将我输入的内容拆解出来。",
        "需求必须是有意义的内容，包含并不限于我的痛点、槽点、需求、期望、愿景等,不要改变我的需求内容。",
        "需求要明确客观，不随意编造内容。紧急程度根据我的输入的语义判断级别，按照【“非常紧急”，“比较紧急”，“不紧急”】处理。期望完成时间尽量提取准确的时间信息。",
        "如果我输入的信息太少或没有提取到有用信息，提醒我输入更详细的内容。",
        "如果没有提取到“需求内容”信息，按照“”处理并提醒我输入“需求内容”，不要胡乱编造需求。",
        "提取的“需求内容”至少10个字以上，否则按照“”处理并提醒我输入更详细的“需求内容”，不要胡乱处理。",
        "如果没有提取到“期望完成时间”信息，按照“”处理并提醒我输入“期望完成时间”，不要胡乱编造时间",
        "如果没有提取到“紧急程度”信息，按照“比较紧急”处理，不要胡乱处理。",
        "如果没有提取到“是否确认提交”信息，按照“”处理，不要胡乱处理，不用提醒我输入。",
        "“是否确认提交”要客观明确，根据上下文和我输入的语义判断，不要随意编造结果，只能按照【“是”，“否”】处理。",
        "如果无法理解我输入的信息，按照通用AI回复并告诉我你能做什么，引导我正确的输入。",
        "回复的内容不要包含情绪、主观思维信息。",

    ]
    desc: str = "提取输入中的 {fields} 信息”"
    max_retry_count: int = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([DemandAction])

    def _init_reply_message(self, received_message):
        reply_message = super()._init_reply_message(received_message)
        reply_message.context = {
            "fields": "[“需求内容”,“紧急程度”,“期望完成时间”,“是否确认提交”]"
        }
        print("需求收集代理回复消息模版内容：", reply_message)
        return reply_message

    async def correctness_check(self, message: AgentMessage):
        action_reply = message.action_report
        if action_reply is None:
            return (
                False,
                f"No executable analysis Demand is generated,{message['content']}.",
            )
        action_out = ActionOutput.from_dict(action_reply)
        if action_out.is_exe_success == False:
            return (
                False,
                f"Please check your answer, {action_out.content}.",
            )
        action_reply_obj = json.loads(action_out.content)
        demand = action_reply_obj.get("demand", None)
        if not demand:
            return (
                False,
                "请检查您的问题，生成的内容中没有找到需求信息！",
            )
        try:
            resource_lark_client: ResourceLarkClient = (
                self.not_null_resource_loader.get_resource_api(
                    ResourceType(action_out.resource_type)
                )
            )

            result = await resource_lark_client.a_lark_after_notify(
                receive_id="liangliang.yan@yeepay.com",
                text="\n已将需求内容提交到飞书，请查看结果！\n\n需求内容：" + demand
            )
            print('ProductionAssistantAgent处理结果：', result)
            if (result['code'] == 0):
                logger.info("代理任务执行成功！")
                delete_last = self.memory.my_conversation_memory.disable_con_by_conv_id(
                    conv_id=self.agent_context.conv_id
                )
                return (
                    True, None
                )
            else:
                logger.error("代理任务执行失败，请检查飞书接口调用日志！")
                return (
                    False,
                    "请检查飞书接口调用日志！",
                )
        except Exception as e:
            logger.exception(f"DataScientist check exception！{str(e)}")
            return (
                False,
                f"Lark execution error, please re-read the historical information to fix this API. The error message is as follows:{str(e)}",
            )

    async def thinking(
            self, messages: List[AgentMessage], prompt: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """Think and reason about the current task goal.

        Args:
            messages(List[AgentMessage]): the messages to be reasoned
            prompt(str): the prompt to be reasoned
        """
        last_model = None
        last_err = None
        retry_count = 0

        conv_uid = self.agent_context.conv_id.split("_")[0]
        convs = self.memory.my_conversation_memory.get_cons_by_conv_uid(
            conv_uid=conv_uid
        )
        # 替换原有消息，将历史记录传入GPT
        if True:
            messages = []
            for conv in convs:
                messages.append(AgentMessage(role="human", content=conv.user_goal))

        llm_messages = [message.to_llm_message() for message in messages]
        # LLM inference automatically retries 3 times to reduce interruption
        # probability caused by speed limit and network stability
        while retry_count < 3:
            llm_model = await self._a_select_llm_model(last_model)
            try:
                if prompt:
                    llm_messages = _new_system_message(prompt) + llm_messages
                else:
                    llm_messages = self.oai_system_message + llm_messages

                if not self.llm_client:
                    raise ValueError("LLM client is not initialized!")
                response = await self.llm_client.create(
                    context=llm_messages[-1].pop("context", None),
                    messages=llm_messages,
                    llm_model=llm_model,
                    max_new_tokens=self.not_null_agent_context.max_new_tokens,
                    temperature=self.not_null_agent_context.temperature,
                )
                return response, llm_model
            except LLMChatError as e:
                logger.error(f"model:{llm_model} generate Failed!{str(e)}")
                retry_count += 1
                last_model = llm_model
                last_err = str(e)
                await asyncio.sleep(10)

        if last_err:
            raise ValueError(last_err)
        else:
            raise ValueError("LLM model inference failed!")


def _new_system_message(content):
    """Return the system message."""
    return [{"content": content, "role": ModelMessageRoleType.SYSTEM}]
