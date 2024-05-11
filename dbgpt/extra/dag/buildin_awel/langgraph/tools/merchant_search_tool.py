import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_customer_search


class MerchantSearchToolInput(BaseModel):
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    customer_number: str = Field(name="商户编号", description="商户编号", default="")
    customer_name: str = Field(name="商户名称", description="商户名称", default="")


class MerchantSearchTool(BaseTool):
    name: str = "merchant_search_tool"
    description: str = (
        "你是一个全面优化的商户信息查询工具，结果准确、可信。 "
        "当你需要通过调用工具查询商户信息时非常有用。 "
        "输入参数应该是工具需要的全部参数。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        "请将查询结果数据整理并美化后输出。"
        ""
    )
    max_results: int = 20
    args_schema: Type[BaseModel] = MerchantSearchToolInput

    def _run(
            self,
            conv_id: str = "",
            customer_number: str = "",
            customer_name: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始执行商户信息查询工具：", conv_id, customer_number, customer_name, self.max_results)
        try:
            resp_data = {}
            if customer_number == "" and customer_name == "":
                return {"success": "false", "response_message": "the description of customer_number and customer_name"}
            data = crem_customer_search.customer_list_search(
                open_id=conv_id,
                customer_name=customer_name,
                customer_number=customer_number
            )
            resp_data = data
            query_str = (customer_name + "" + customer_number).strip()
            print("商户查询结果：", query_str, resp_data)
            list = []
            if resp_data and len(resp_data) == 0:
                return {"success": "true", "data": []}

            for m in resp_data:
                customerName = m.get("customerName", "")
                customerIntroduction = m.get("customerIntroduction", "")
                industryLine = m.get("industryLine", "")
                saleName = m.get("saleName", "")
                customerNo = m.get("customerNo", "")
                list.append({
                    "customerName": customerName if customerName is not None else "",
                    "customerIntroduction": customerIntroduction if customerIntroduction is not None else "",
                    "industryLine": industryLine if industryLine is not None else "",
                    "saleName": saleName if saleName is not None else "",
                    "customerNo": customerNo if customerNo is not None else ""
                })

            return {
                "success": "true",
                "error_message": "",
                "action": {
                    "action_name": "send_lark_form_card",
                    "card_name": "merchant_list_card"
                },
                "data": {
                    "list": list,
                    "query_str": query_str
                }
            }
        except Exception as e:
            logging.error("商户查询工具运行异常：", e)
            return repr(e)