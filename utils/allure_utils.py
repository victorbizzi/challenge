import json
import allure


def attach_payload(name: str, payload: dict):
    allure.attach(
        json.dumps(payload, indent=2),
        name=name,
        attachment_type=allure.attachment_type.JSON
    )