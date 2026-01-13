import os
import socket
import urllib.parse
from dotenv import load_dotenv
from utils.api_client import ApiClient
from faker import Faker
import pytest

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL")
API_TOKEN = os.getenv("API_TOKEN")


def _is_host_port_reachable(url: str, timeout: float = 2.0) -> bool:
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


@pytest.fixture(scope="session", autouse=True)
def require_integration_env():
    if not BASE_URL or not API_TOKEN:
        pytest.skip(
            "API_BASE_URL /API_TOKEN environment variables are not set"
        )

    if not _is_host_port_reachable(BASE_URL):
        pytest.skip(
            f"API not accessible {BASE_URL}"
        )


@pytest.fixture(scope="session")
def api_client():
    return ApiClient(
        base_url=BASE_URL,
        token=API_TOKEN
    )

fake = Faker()
@pytest.fixture
def sample_todo():
    return {
        "id": "",
        "title": fake.sentence(nb_words=4),
        "details": fake.text(max_nb_chars=50),
        "user": "victorbizzi"
    }
