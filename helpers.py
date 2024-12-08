import re

def validate_address(address):
    regex = r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::(\d{1,5}))?$"
    match = re.match(regex, address)
    if not match:
        return None
    ip = match.group(1)
    port = match.group(2) or "8765"
    return f"ws://{ip}:{port}"
