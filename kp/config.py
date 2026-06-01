"""
Конфигурация AI-генератора коммерческих предложений.
LLM-бэкенд: Ollama Cloud (по умолчанию) или OpenRouter.
"""

import os
from dotenv import load_dotenv

load_dotenv()

LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")  # "ollama" | "openrouter"

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "https://ollama.com")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-v4-pro")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-3.5-flash")

# Чуть выше температура — текст оффера живее, но без лишних фантазий
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.4"))

# Ставка НДС по умолчанию (РФ, 2026)
DEFAULT_VAT_RATE = float(os.getenv("VAT_RATE", "22"))

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "out")


def validate():
    errors = []
    if LLM_BACKEND == "ollama" and not OLLAMA_API_KEY:
        errors.append("OLLAMA_API_KEY не задан (LLM_BACKEND=ollama)")
    if LLM_BACKEND == "openrouter" and not OPENROUTER_API_KEY:
        errors.append("OPENROUTER_API_KEY не задан (LLM_BACKEND=openrouter)")
    if LLM_BACKEND not in ("ollama", "openrouter"):
        errors.append(f"LLM_BACKEND='{LLM_BACKEND}' — допустимо 'ollama' или 'openrouter'")
    if errors:
        raise RuntimeError("Ошибки конфигурации:\n  - " + "\n  - ".join(errors))
