# utils/safety.py
import re

BANNED_PHRASES = [
    "ignore previous",
    "simulate",
    "pretend",
    "execute",
    "admin",
    "sudo",
    "bypass",
    "reset",
    "shell",
    "os.system",
    "<script",
    "</script>",
    "hack",
    "injection",
    "prompt injection",
    "format c:",
    "delete all",
    "upload virus",
    ";"
]

MAX_TOKENS = 200  # or word count

def sanitize_input(user_input: str) -> str:
    input_lower = user_input.lower().strip()

    # Check length
    if len(input_lower.split()) > MAX_TOKENS:
        return "⚠️ Input too long. Please shorten your question."

    # Check for banned patterns
    for phrase in BANNED_PHRASES:
        if phrase in input_lower:
            return f"⚠️ Input violates system safety rules due to suspicious phrase: '{phrase}'"

    # Basic sanitization
    cleaned = re.sub(r"[`*<>\\]", "", input_lower)
    cleaned = cleaned.replace("\"", "")  # strip quotes
    return cleaned
