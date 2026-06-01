"""Единый клиент LLM (Ollama Cloud / OpenRouter, OpenAI-совместимый API)."""

import json
import logging
import re

import httpx

from kp import config

log = logging.getLogger(__name__)


def call_llm(messages: list, *, json_mode: bool = False,
             max_tokens: int = 2000, temperature: float | None = None) -> str:
    temperature = config.LLM_TEMPERATURE if temperature is None else temperature

    if config.LLM_BACKEND == "ollama":
        url = f"{config.OLLAMA_BASE_URL}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {config.OLLAMA_API_KEY}"}
        model = config.OLLAMA_MODEL
    else:
        url = f"{config.OPENROUTER_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://github.com/kilevoy/ai-proposal-generator",
            "X-Title": "AI Proposal Generator",
        }
        model = config.OPENROUTER_MODEL

    payload = {"model": model, "messages": messages,
               "max_tokens": max_tokens, "temperature": temperature}
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    log.info(f"  LLM: {config.LLM_BACKEND}/{model} (json={json_mode})")
    with httpx.Client(timeout=300, follow_redirects=True) as client:
        resp = client.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(f"LLM вернул {resp.status_code}: {resp.text[:500]}")
    return resp.json()["choices"][0]["message"]["content"].strip()


def parse_json(raw: str) -> dict:
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    raise ValueError("Модель вернула невалидный JSON")
