import json

def serializer(message) -> bytes:
    """Serialize a message to JSON format."""
    return json.dumps(message).encode('utf-8')
