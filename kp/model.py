"""Модель данных коммерческого предложения."""

from __future__ import annotations
from dataclasses import dataclass, field, asdict


@dataclass
class LineItem:
    name: str
    qty: float
    unit: str = "шт"
    price: float = 0.0          # цена за единицу, без НДС
    kind: str = "equipment"     # "equipment" (оборудование/материалы) | "work" (работы)

    @property
    def amount(self) -> float:
        return round(self.qty * self.price, 2)


@dataclass
class Proposal:
    # стороны
    company: str                 # наша компания
    company_tagline: str = ""    # короткий слоган/описание
    client: str = ""
    project: str = ""            # объект
    city: str = ""
    subject: str = ""            # предмет КП

    # контакты ответственного менеджера (отправителя КП)
    manager: str = ""            # ФИО
    manager_role: str = ""       # должность
    phone: str = ""
    email: str = ""

    # коммерция
    items: list[LineItem] = field(default_factory=list)
    discount_pct: float = 0.0
    vat_rate: float = 22.0
    advance_pct: float = 30.0
    lead_time_days: int = 30
    warranty_months: int = 24

    # тексты (генерируются ИИ или задаются вручную)
    offer: str = ""                                      # цепляющий оффер с выгодой
    pitch: str = ""                                      # о компании / почему мы
    advantages: list[str] = field(default_factory=list)  # выгоды/преимущества
    disclaimer: str = (
        "Спецификация является предварительной. Окончательный состав и количество "
        "оборудования утверждаются после выезда инженера на объект и технического расчёта."
    )

    @staticmethod
    def from_dict(data: dict) -> "Proposal":
        items = [LineItem(**it) for it in data.get("items", [])]
        known = {f for f in Proposal.__dataclass_fields__ if f != "items"}
        rest = {k: v for k, v in data.items() if k in known}
        return Proposal(items=items, **rest)

    def to_dict(self) -> dict:
        return asdict(self)
