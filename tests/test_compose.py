"""Тесты расчётного ядра КП."""

from kp.model import Proposal, LineItem
from kp import compose


def make(items, **kw):
    return Proposal(company="Тест", items=[LineItem(*it) for it in items], **kw)


def _digits(s: str) -> str:
    """Убирает любые пробелы (вкл. неразрывный) и символ рубля."""
    return s.replace(" ", "").replace(" ", "").replace("₽", "").strip()


def test_line_item_amount():
    assert LineItem("Товар", 3, "шт", 100).amount == 300


def test_subtotal():
    p = make([("A", 2, "шт", 100), ("B", 1, "компл", 500)])
    assert compose.subtotal(p) == 700


def test_discount_and_net():
    p = make([("A", 1, "шт", 1000)], discount_pct=10)
    assert compose.discount_amount(p) == 100
    assert compose.net(p) == 900


def test_vat_and_total():
    p = make([("A", 1, "шт", 1000)], vat_rate=22)
    assert compose.vat_amount(p) == 220
    assert compose.total(p) == 1220


def test_total_with_discount_and_vat():
    p = make([("A", 1, "шт", 1000)], discount_pct=10, vat_rate=22)
    assert compose.net(p) == 900
    assert compose.vat_amount(p) == 198
    assert compose.total(p) == 1098


def test_payment_schedule_sums_to_total():
    p = make([("A", 1, "шт", 1000)], vat_rate=20, advance_pct=30)
    sched = compose.payment_schedule(p)
    assert round(sum(s["amount"] for s in sched), 2) == compose.total(p)
    assert "30%" in sched[0]["name"]


def test_totals_keys():
    p = make([("A", 1, "шт", 1000)])
    t = compose.totals(p)
    assert set(t) >= {"subtotal", "discount", "net", "vat", "total"}


def test_format_money_ru():
    out = compose.format_money(1234567.5)
    assert out.endswith("₽")          # символ рубля
    assert _digits(out) == "1234567,50"
    assert _digits(compose.format_money(0)) == "0,00"
