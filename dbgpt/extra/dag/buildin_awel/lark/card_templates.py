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
    template_version_name = "1.0.50"

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
    template_version_name = "1.0.12"

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
    template_version_name = "1.0.8"

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
    template_version_name = "1.0.17"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card



def create_merchant_list_card_content(template_variable: Dict):
    """需求提报表单"""
    template_id = "AAqkXYlYpaLEf"
    template_version_name = "1.0.5"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card