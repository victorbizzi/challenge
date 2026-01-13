import pytest
import allure
import logging
from utils.allure_utils import attach_payload
from faker import Faker

logger = logging.getLogger(__name__)

TODO_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "details", "user"],
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "details": {"type": "string"},
        "user": {"type": "string"},
        "timestamp": {"type": "string"}
    }
}

@allure.feature("Todos API")
@allure.story("GET /todos - Return list of Todos with valid structure")
@pytest.mark.api
def test_get_all_todos(api_client):
    resp = api_client.get("/todos", params={"user": "victorbizzi"})

    logger.info("Status code: ", resp.status_code)
    logger.info("RESPONSE BODY:\n", resp.text)

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"
    assert resp.headers["Content-Type"].startswith("application/json"), (
        f"Expected JSON response, got Content-Type: {resp.headers.get('Content-Type')}"
    )

    try:
        body = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Raw body: {resp.text}")

    assert isinstance(body, list), f"Expected response body to be a list, got {type(body)}"

    for item in body:
        assert item.get("id"), "Field 'id' must not be empty"
        assert item.get("title") and item["title"].strip(), "Field 'title' must not be empty"
        assert item.get("details") and item["details"].strip(), "Field 'details' must not be empty"

@allure.feature("Todos API")
@allure.story("POST /todos - Create Todo and return valid response")
@pytest.mark.api
def test_create_todo(api_client, sample_todo):
    resp = api_client.post("/todos", json_body=sample_todo)

    assert resp.status_code == 200, (
        f"Expected status code 200, got {resp.status_code}. Body: {resp.text}"
    )

    try:
        body = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Raw body: {resp.text}")

    assert isinstance(body, str), f"Expected response to be a string ID, got {type(body)}"
    assert body.strip(), "Returned Todo ID must not be empty"
    attach_payload("Create Todo Payload", sample_todo)


fake = Faker()
@allure.feature("Todos API")
@allure.story("POST /todos - Validation errors for invalid payloads")
@pytest.mark.api
@pytest.mark.parametrize(
    "payload, description",
    [
        (
            {
                "id": "",
                "user": "victorbizzi",
                "details": fake.text(max_nb_chars=50)
            },
            "Missing title"
        ),
        (
            {
                "id": "",
                "user": "victorbizzi",
                "title": fake.sentence(nb_words=4)
            },
            "Missing details"
        ),
        (
            {
                "id": "",
                "user": "victorbizzi",
                "title": "A" * 251,
                "details": fake.text(max_nb_chars=250)
            },
            "Title longer than 250 characters"
        ),
        (
                {
                    "id": "",
                    "user": "victorbizzi",
                    "title": fake.sentence(nb_words=4),
                    "details": fake.text(max_nb_chars=1200),
                },
                "Details longer than 1100 characters",
        ),
        (
            {
                "id": "",
                "user": "victorbizzi",
                "title": fake.sentence(nb_words=4),
                "details": ""
            },
            "Empty details"
        ),
        (
            {},
            "Empty payload"
        ),
    ]
)
@allure.title("POST /todos - {description}")
def test_create_todo_invalid_payload(api_client, payload, description):
    attach_payload(f"Invalid Payload - {description}", payload)

    resp = api_client.post("/todos", json_body=payload)

    assert resp.status_code in (400, 422), (
        f"Expected 400 or 422, got {resp.status_code}. Body: {resp.text}"
    )