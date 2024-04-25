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
    template_version_name = "1.0.31"

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def create_daily_report_card_content(template_variable: Dict):
    """需求提报表单"""
    template_id = ""
    template_version_name = ""

    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card
