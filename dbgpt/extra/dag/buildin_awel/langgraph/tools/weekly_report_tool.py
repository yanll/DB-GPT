import logging
from typing import Optional, Type
from typing import List
from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil, lark_message_util


class PlanDetail(BaseModel):
    plan_content: str = Field(
        name="下周计划内容",
        description="下周计划内容",
        default=""
    )


class WeeklyReportCollectInput(BaseModel):
    """
    我要填写周报：
    周报内容：本周完成了一次客户回访，进展正常。
    填写日期：2024-04-22
    下周计划：1、继续跟进客户，2、完成3次回访，3、制定阅读计划
    """
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    weekly_report_content: str = Field(
        name="周报内容",
        description="周报内容",
        default=""
    )
    create_date: str = Field(
        name="创建日期",
        description="创建日期，格式：%Y-%m-%d",
        default=""
    )
    weekly_report_next_week_plans: List[PlanDetail] = Field(
        name="下周计划内容",
        description="下周计划内容",
        default=[]
    )

    senders_name: str = Field(
        name="抄送人员",
        description="抄送给谁",
        default=""
    )


class WeeklyReportCollectTool(BaseTool):
    name: str = "weekly_report_collect_tool"
    description: str = (
        "这是一个周报填写工具，帮助用户填写工作周报、填写每周工作总结。"
        "当需要填写周报/写周报/总结周报时非常有用。 "
        "能够尽可能全的收集周报信息。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        ""
    )
    args_schema: Type[BaseModel] = WeeklyReportCollectInput

    def _run(
            self,
            conv_id: str,
            weekly_report_content: str = "",
            create_date: str = "",
            senders_name: Optional[str] = "",
            weekly_report_next_week_plans: Optional[List[PlanDetail]] = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ):
        """Use the tool.77"""
        print("开始运行周报填写工具：", conv_id, weekly_report_content)
        try:

            reuqires = []
            if weekly_report_content == "":
                reuqires.append("weekly_report_content")
            if create_date == "":
                reuqires.append("create_date")
            if len(reuqires) > 0:
                return {"success": "false", "response_message": "the description of " + str(reuqires)}

            return handle(
                conv_id=conv_id,
                weekly_report_content=weekly_report_content,
                create_date=create_date,
                weekly_report_next_week_plans=weekly_report_next_week_plans
            )
        except Exception as e:
            logging.error("日报收集工具运行异常：" + conv_id + " " + weekly_report_content, e)
            return repr(e)


def handle(
        conv_id: str,
        weekly_report_content: str = "",
        create_date: str = "",
        weekly_report_next_week_plans: str = ""
):
    try:
        # 处理明日计划，如果为空则返回特定的消息
        if weekly_report_next_week_plans is None:
            plans_description = ""
        else:
            plans_description = ""
            # for index, weekly_report_next_week_plan in enumerate(weekly_report_next_week_plans):
            #     plans_description += str(index + 1) + '. ' + weekly_report_next_week_plan.plan_content + '; '

        return {
            "success": "true",
            "error_message": "",
            "action": {
                "action_name": "send_lark_form_card",
                "card_name": "weekly_report_collect"
            },
            "data": {
                "conv_id": conv_id,
                "weekly_report_next_week_plans": plans_description,
                "create_date": create_date,
                "weekly_report_content": weekly_report_content
            }
        }

    except Exception as e:
        raise Exception("周报数据组装失败：" + conv_id + " " + weekly_report_content, e)
