import os
import json
import requests
import allure


class ApiClient:

    def __init__(self, base_url: str, token: str = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        token = token or os.environ.get("API_TOKEN")
        self.auth_header = {"Authorization": f"Bearer {token}"} if token else {}

    def _attach(self, name: str, content: str, mime: str = 'application/json'):
        att_type = allure.attachment_type.JSON if 'json' in mime else allure.attachment_type.TEXT
        try:
            allure.attach(content, name=name, attachment_type=att_type)
        except Exception:
            allure.attach(content, name=name)

    def _full_url(self, path: str) -> str:
        if not path.startswith('/'):
            path = '/' + path
        return f"{self.base_url}{path}"

    def get(self, path: str, params: dict = None, headers: dict = None):
        url = self._full_url(path)
        merged_headers = {**self.auth_header, **(headers or {})}
        with allure.step(f"GET {url}"):
            resp = self.session.get(url, params=params, headers=merged_headers)
            self._attach("request_headers", json.dumps(merged_headers, indent=2), mime='application/json')
            self._attach("request_params", json.dumps(params or {}, indent=2), mime='application/json')
            self._attach("response_status", str(resp.status_code), mime='text/plain')
            self._attach("response_body", resp.text, mime='application/json')
            return resp

    def post(self, path: str, json_body: dict = None, headers: dict = None):
        url = self._full_url(path)
        merged_headers = {**self.auth_header, **(headers or {})}
        with allure.step(f"POST {url}"):
            resp = self.session.post(url, json=json_body, headers=merged_headers)
            self._attach("request_headers", json.dumps(merged_headers, indent=2), mime='application/json')
            self._attach("request_body", json.dumps(json_body or {}, indent=2), mime='application/json')
            self._attach("response_status", str(resp.status_code), mime='text/plain')
            self._attach("response_body", resp.text, mime='application/json')
            return resp