import json
import unittest
from unittest.mock import patch

import update_payloads


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload.encode("utf-8")

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class ReleaseFallbackTests(unittest.TestCase):
    def test_get_latest_release_falls_back_to_http_when_gh_is_missing(self):
        def fake_urlopen(request):
            self.assertEqual(request.full_url, "https://api.github.com/repos/octo/repo/releases/latest")
            return FakeResponse(json.dumps({"tag_name": "v1.2.3"}))

        with patch("update_payloads.subprocess.run", side_effect=FileNotFoundError("gh not found")), patch(
            "update_payloads.urllib.request.urlopen", side_effect=fake_urlopen
        ):
            release = update_payloads.get_latest_release("github.com", "octo", "repo")

        self.assertEqual(release["tag_name"], "v1.2.3")


if __name__ == "__main__":
    unittest.main()
