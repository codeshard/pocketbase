from typing import Any

from httpx import Cookies

from pocketbase.models import Admin, Record
from pocketbase.stores import BaseAuthStore


class CookieAuthStore(BaseAuthStore):
    cookies: Cookies = None

    def __init__(
        self,
        base_token: str = "",
        base_model: Record | Admin | None = None,
    ) -> None:
        super().__init__(base_token, base_model)
        self.cookies = Cookies()

    @property
    def token(self) -> str:
        data = self._cookies_get("pocketbase.auth")
        if not data or "token" not in data:
            return None
        return data["token"]

    @property
    def model(self) -> Record | Admin | None:
        data = self._cookies_get("pocketbase.auth")
        if not data or "model" not in data:
            return None
        return data["model"]

    def save(
        self,
        token: str = "",
        model: Record | Admin | None = None,
    ) -> None:
        self._cookies_set(
            "pocketbase.auth",
            {"token": token, "model": model},
        )
        super().save(token, model)

    def clear(self) -> None:
        self._cookies_remove()
        super().clear()

    def _cookies_set(self, key: str, value: Any) -> None:
        self.cookies.set(name=key, value=value)

    def _cookies_get(self, key: str) -> Any:
        return self.cookies.get(name=key)

    def _cookies_remove(self) -> None:
        self.cookies.clear()
