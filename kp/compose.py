"""Расчёт коммерческого предложения: суммы, скидка, НДС, график оплаты."""

from __future__ import annotations

from kp.model import Proposal


def subtotal(proposal: Proposal) -> float:
    """Сумма по позициям без скидки и НДС."""
    return round(sum(item.amount for item in proposal.items), 2)


def discount_amount(proposal: Proposal) -> float:
    return round(subtotal(proposal) * proposal.discount_pct / 100, 2)


def net(proposal: Proposal) -> float:
    """Сумма после скидки, без НДС."""
    return round(subtotal(proposal) - discount_amount(proposal), 2)


def vat_amount(proposal: Proposal) -> float:
    return round(net(proposal) * proposal.vat_rate / 100, 2)


def total(proposal: Proposal) -> float:
    """Итого с НДС."""
    return round(net(proposal) + vat_amount(proposal), 2)


def payment_schedule(proposal: Proposal) -> list[dict]:
    """Простой график оплаты: аванс + остаток по факту."""
    grand = total(proposal)
    advance = round(grand * proposal.advance_pct / 100, 2)
    balance = round(grand - advance, 2)
    return [
        {"name": f"Аванс ({proposal.advance_pct:.0f}%)", "amount": advance,
         "when": "при подписании договора"},
        {"name": f"Остаток ({100 - proposal.advance_pct:.0f}%)", "amount": balance,
         "when": "по факту поставки/выполнения работ"},
    ]


def totals(proposal: Proposal) -> dict:
    """Полная сводка расчёта."""
    return {
        "subtotal": subtotal(proposal),
        "discount": discount_amount(proposal),
        "net": net(proposal),
        "vat": vat_amount(proposal),
        "total": total(proposal),
        "vat_rate": proposal.vat_rate,
        "discount_pct": proposal.discount_pct,
    }


def format_money(value: float) -> str:
    """1234567.5 → '1 234 567,50 ₽' (русский формат)."""
    s = f"{value:,.2f}".replace(",", " ").replace(".", ",")
    return f"{s} ₽"
