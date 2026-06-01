"""Тесты модели и рендера."""

from kp.model import Proposal
from kp.render import render_html
from kp.compose import format_money


SAMPLE = {
    "company": "ООО «ПромТехСнаб»",
    "client": "ООО «Альфа»",
    "subject": "Поставка оборудования",
    "offer": "Снизим затраты на 30%",
    "pitch": "Мы надёжный поставщик.",
    "advantages": ["Гарантия 3 года", "Срок 45 дней"],
    "vat_rate": 22,
    "items": [{"name": "Светильник", "qty": 10, "unit": "шт", "price": 5000}],
}


def test_from_dict_roundtrip():
    p = Proposal.from_dict(SAMPLE)
    assert p.company == "ООО «ПромТехСнаб»"
    assert len(p.items) == 1
    assert p.items[0].amount == 50000
    assert p.advantages == ["Гарантия 3 года", "Срок 45 дней"]


def test_from_dict_ignores_unknown_keys():
    p = Proposal.from_dict({**SAMPLE, "unknown_field": 123})
    assert p.client == "ООО «Альфа»"


def test_render_html_contains_key_parts():
    p = Proposal.from_dict(SAMPLE)
    html = render_html(p, number="КП-042")
    assert "КП-042" in html
    assert "Снизим затраты на 30%" in html
    assert "Светильник" in html
    assert "Принять предложение" in html
    # итог с НДС: 50000 + 22% = 61000
    assert format_money(61000.0) in html


def test_render_escapes_html():
    p = Proposal.from_dict({**SAMPLE, "client": "<script>x</script>"})
    html = render_html(p)
    assert "<script>x</script>" not in html
    assert "&lt;script&gt;" in html
