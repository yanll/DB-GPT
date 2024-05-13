from typing import Dict


def create_card_content_by_template(template_id: str, template_version_name: str, template_variable: Dict):
    """"""
    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_requirement_card_content(template_variable: Dict):
    """需求提报表单"""
    template_id = "AAqkjMFhiuVwF"
    template_version_name = "1.0.59"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_daily_report_card_content(template_variable: Dict):
    """日报表单"""
    template_id = "AAqkjM4Ffisl2"
    template_version_name = "1.0.18"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id,
            "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


class create_crm_bus_customer_card_content:
    """报单客户信息表单"""

    @staticmethod
    def Web3_or_ForeignComprehensiveService(template_variable: Dict):
        template_id = "AAqkEJ9hph8Ij"
        template_version_name = "1.0.24"
        card = {
            "type": "template",
            "data": {
                "template_id": template_id,
                "template_version_name": template_version_name,
                "template_variable": template_variable
            }
        }
        return card

    @staticmethod
    def Finance_or_CrossBorder(template_variable: Dict):
        template_id = "AAqkooGVViOUK"
        template_version_name = "1.0.4"
        card = {
            "type": "template",
            "data": {
                "template_id": template_id,
                "template_version_name": template_version_name,
                "template_variable": template_variable
            }
        }
        return card

    @staticmethod
    def Retail(template_variable: Dict):
        template_id = "AAqklNZ65v58c"
        template_version_name = "1.0.3"
        card = {
            "type": "template",
            "data": {
                "template_id": template_id,
                "template_version_name": template_version_name,
                "template_variable": template_variable
            }
        }
        return card

    @staticmethod
    def Government(template_variable: Dict):
        template_id = "AAq3O0CfLPZJu"
        template_version_name = "1.0.0"
        card = {
            "type": "template",
            "data": {
                "template_id": template_id,
                "template_version_name": template_version_name,
                "template_variable": template_variable
            }
        }
        return card

    class AirTravel:
        @staticmethod
        def Category_I(template_variable: Dict):
            template_id = "AAq3OtM7vxU1e"
            template_version_name = "1.0.2"
            card = {
                "type": "template",
                "data": {
                    "template_id": template_id,
                    "template_version_name": template_version_name,
                    "template_variable": template_variable
                }
            }
            return card

        @staticmethod
        def Category_II(template_variable: Dict):
            template_id = "AAq3Ob7zQPV6t"
            template_version_name = "1.0.1"
            card = {
                "type": "template",
                "data": {
                    "template_id": template_id,
                    "template_version_name": template_version_name,
                    "template_variable": template_variable
                }
            }
            return card


def create_interactive_update_daily_report_card_content(template_variable: Dict):
    """交互更新日报表单"""
    template_id = "AAqkIQ23gTztS"
    template_version_name = "1.0.1"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id,
            "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_weekly_report_card_content(template_variable: Dict):
    """周报表单  """
    template_id = "AAqkjMz1cWwRB"
    template_version_name = "1.0.13"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_customer_visit_record_card_content(template_variable: Dict):
    """拜访表单"""
    template_id = "AAqkjMxmwdE8s"
    template_version_name = "1.0.21"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_merchant_list_card_content(template_variable: Dict):
    """商户查询"""
    template_id = "AAqkXYlYpaLEf"
    template_version_name = "1.0.21"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_search_daily_report_card_content(template_variable: Dict):
    """日报查询"""
    template_id = "AAqkZz4JvpXQR"
    template_version_name = "1.0.8"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_search_daily_report_id_card_content(template_variable: Dict):
    """日报详情查询"""
    template_id = "AAqkart7DnGFW"
    template_version_name = "1.0.5"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_requirement_search_card_content(template_variable: Dict):
    """需求查询"""
    template_id = "AAqk5wmyPFr8z"
    template_version_name = "1.0.2"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_requirement_search_list_card_content(template_variable: Dict):
    """需求查询列表展示"""
    template_id = "AAqklS3kyRc0R"
    template_version_name = "1.0.9"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_feedback_card_content(template_variable: Dict):
    """需求查询列表展示"""
    template_id = "AAqkEvmXj7MSH"
    template_version_name = "1.0.7"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_tool_tips_content(template_variable: Dict):
    """需求查询列表展示"""
    template_id = "AAq3fRz6x3j5O"
    template_version_name = "1.0.0"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card
