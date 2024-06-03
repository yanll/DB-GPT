import logging
import uuid
from datetime import datetime

from flask import Flask, jsonify

from dbgpt.extra.dag.buildin_awel.app.service import AppChatService
from dbgpt.extra.dag.buildin_awel.hanglv import hanglv_api_use
from dbgpt.extra.dag.buildin_awel.hanglv.airline_monitor_push import AirlineMonitorPush
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.extra.dag.buildin_awel.monitor import monitor, monitor1bypayer, monitor1bystat
from dbgpt.extra.dag.buildin_awel.monitor.monitor1bystat import Monitor1ByStat
from dbgpt.util.lark import lark_message_util


class AirlineMonitorPush1_1(AirlineMonitorPush):

    def __init__(self):
        self.monitor = Monitor1ByStat()
        super().__init__()

    def store_his_message(self, app_chat_service, sales, title, content, reason, display_type):
        current_date = datetime.now().strftime('%Y-%m-%d')
        rec = {
            "id": str(uuid.uuid1()),
            "agent_name": "SalesAssistant",
            "node_name": "final",
            # "conv_uid": sender_open_id,
            "message_type": "view",
            "content": content,
            "message_detail": "",
            "display_type": display_type,
            "biz_date": current_date,
            "sales": sales,
            "title": title,
            "scene": "",
            "chanel": "",
            "product": "",
            "merchant_no": "",
            "reason": reason,
            "type": "航旅波动检测归因1.1_交易笔数波动异常",
            "created_time": "",
            "modified_time": "",
        }
        print("rec的值是：", rec)
        try:
            app_chat_service.add_app_hanglv_msg(rec)
        except Exception as e:
            logging.error(f"Error storing message: {e}")

    def run_push(self):
        hv_data = self.monitor.run()
        print("数值的返回结果", hv_data)
        data = hv_data

        app_chat_service = AppChatService()  # Create the instance once

        # 逐条处理数据并传入 rec
        for item in data:
            # 合并 reason 字段
            reason = f"{item['reason1_text']}\n{item['reason2_text']}\n{item['reason3_text']}"

            # 构建内容字符串
            content = (
                f"Name: {item['name']}\n"
                f"Title: {item['title']}\n"
                f"Content: {item['content_text']}\n"
                f"Customer_name: {reason}\n"
            )

            # 调用存储消息的函数
            self.store_his_message(
                app_chat_service,
                # sender_open_id=sender_open_id,
                sales=item['name'],
                title=item['title'],
                content=content,
                reason=reason,
                display_type="hanglv_card",
            )

        name_to_data = {}
        conv_id_cache = {}
        for report in data:
            name = report['name']
            title = report['title']
            if name not in name_to_data:
                name_to_data[name] = []
            report_with_num = report.copy()
            report_with_num['num'] = len(name_to_data[name]) + 1
            name_to_data[name].append(report_with_num)

        for name, reports in name_to_data.items():
            if name not in conv_id_cache:
                # 只在第一次遇到该 name 时调用 API
                conv_id_cache[name] = hanglv_api_use.get_user_open_id(name)
            conv_id_map = conv_id_cache[name]
            print("cov_id的合集", conv_id_map)

            for email, conv_id in conv_id_map.items():
                content = card_templates.travel_report_content1(
                    template_variable={
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": "",
                            "event_data": {
                                "message": "航旅波动检测归因1.1_交易笔数波动异常"
                            }
                        },
                        "travel_report_list": reports,
                        "title": title,
                        "name": name
                    }
                )
                print("发送给:", name, "Conv ID:", conv_id)
                print("生成的内容:", content)
                resp = lark_message_util.send_card_message(
                    receive_id=conv_id,
                    content=content
                )
                print("发送的卡片信息:", resp)
                lark_message_id = resp.get("message_id", "")
                print("lark_message_id:", lark_message_id)

        return "Success"

# if __name__ == "__main__":
#     a = AirlineMonitorPush1_1()
#     b = a.run_push()
#     print(b)