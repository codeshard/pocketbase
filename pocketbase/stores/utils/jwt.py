import base64
import json
import time


def get_token_payload(token: str) -> dict:
    try:
        if token:
            encoded_payload = token.split(".")[1] + "=" * (
                -len(token.split(".")[1]) % 4
            )
            decoded_payload = base64.urlsafe_b64decode(encoded_payload).decode("utf-8")
            return json.loads(decoded_payload)
    except Exception as e:
        pass
    return {}


def is_token_expired(token: str, expiration_threshold: int = 0) -> bool:
    payload = get_token_payload(token)

    if payload and "exp" in payload:
        return payload["exp"] - expiration_threshold <= int(time.time())

    return True
