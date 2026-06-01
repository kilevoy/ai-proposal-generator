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


def category_totals(proposal: Proposal) -> dict:
    """Валовые суммы (с учётом скидки и НДС, пропорционально) по типам позиций."""
    sub = subtotal(proposal)
    grand = total(proposal)
    equip = round(sum(it.amount for it in proposal.items if it.kind != "work"), 2)
    if sub <= 0:
        return {"equipment": 0.0, "work": 0.0}
    equip_gross = round(grand * equip / sub, 2)
    return {"equipment": equip_gross, "work": round(grand - equip_gross, 2)}


def payment_schedule(proposal: Proposal) -> list[dict]:
    """График оплаты.

    Если есть и оборудование, и работы — трёхэтапный (закупка → поставка → монтаж),
    что снимает риски обеих сторон. Иначе — классический аванс + остаток.
    """
    grand = total(proposal)
    cats = category_totals(proposal)
    equip, work = cats["equipment"], cats["work"]

    if equip > 0 and work > 0:
        advance = round(equip * 0.5, 2)        # аванс на закупку = 50% стоимости оборудования
        delivery = round(equip - advance, 2)   # остаток за оборудование — по факту поставки
        install = round(grand - advance - delivery, 2)  # работы — после актов
        return [
            {"name": "Аванс на закупку оборудования (50%)", "amount": advance,
             "when": "при подписании договора"},
            {"name": "Оплата оборудования по факту поставки", "amount": delivery,
             "when": "при поставке на объект"},
            {"name": "Монтаж и пусконаладка", "amount": install,
             "when": "после подписания актов КС-2 / КС-3"},
        ]

    advance = round(grand * proposal.advance_pct / 100, 2)
    return [
        {"name": f"Аванс ({proposal.advance_pct:.0f}%)", "amount": advance,
         "when": "при подписании договора"},
        {"name": f"Остаток ({100 - proposal.advance_pct:.0f}%)", "amount": round(grand - advance, 2),
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
