"""AI-генерация продающих текстов КП: оффер, о компании, преимущества."""

import logging

from kp.llm import call_llm, parse_json
from kp.model import Proposal

log = logging.getLogger(__name__)

_SYSTEM = (
    "Ты — эксперт по B2B-продажам и копирайтер коммерческих предложений в РФ. "
    "Пишешь по-деловому, конкретно, с акцентом на выгоду клиента. Без воды и клише. "
    "Возвращаешь только валидный JSON без markdown."
)


def _prompt(p: Proposal) -> str:
    items = "; ".join(f"{i.name} ({i.qty} {i.unit})" for i in p.items) or "не указаны"
    return f"""Составь продающие блоки коммерческого предложения.

Наша компания: {p.company}{(' — ' + p.company_tagline) if p.company_tagline else ''}
Клиент: {p.client or 'потенциальный клиент'}
Объект: {p.project or 'не указан'}{(', ' + p.city) if p.city else ''}
Предмет: {p.subject or 'поставка и работы'}
Позиции: {items}

Верни JSON строго в формате:
{{
  "offer": "1-2 предложения: цепляющий оффер с конкретной выгодой клиента (экономия, срок, окупаемость). Без преувеличений, правдоподобно.",
  "pitch": "2-3 предложения о нашей компании: почему нам можно доверять (опыт, подход, гарантии). По-деловому, без штампов.",
  "advantages": ["4-5 коротких преимуществ-выгод для клиента, по пункту в строке"]
}}

Правила:
1. Пиши на русском, по-деловому.
2. Выгоды — конкретные и измеримые, где уместно (сроки, %, гарантия).
3. Не выдумывай цифры, которых нет; формулируй обтекаемо, если данных мало.
4. Оффер должен обещать решение задачи клиента, а не просто «продать»."""


def generate_texts(proposal: Proposal) -> dict:
    """Возвращает dict с ключами offer, pitch, advantages."""
    messages = [
        {"role": "system", "content": _SYSTEM},
        {"role": "user", "content": _prompt(proposal)},
    ]
    raw = call_llm(messages, json_mode=True, max_tokens=1500)
    data = parse_json(raw)
    return {
        "offer": str(data.get("offer", "")).strip(),
        "pitch": str(data.get("pitch", "")).strip(),
        "advantages": [str(a).strip() for a in data.get("advantages", []) if str(a).strip()],
    }


def fill_texts(proposal: Proposal) -> Proposal:
    """Заполняет пустые текстовые поля КП через ИИ."""
    if proposal.offer and proposal.pitch and proposal.advantages:
        return proposal
    texts = generate_texts(proposal)
    proposal.offer = proposal.offer or texts["offer"]
    proposal.pitch = proposal.pitch or texts["pitch"]
    proposal.advantages = proposal.advantages or texts["advantages"]
    return proposal
