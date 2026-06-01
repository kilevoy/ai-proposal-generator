"""Рендер коммерческого предложения в интерактивную HTML-страницу."""

from __future__ import annotations
import html
from datetime import date

from kp.model import Proposal
from kp import compose

ACCENT = "#2f5fd0"


def _esc(s) -> str:
    return html.escape(str(s or ""))


def render_html(p: Proposal, number: str = "КП-001",
                day: str | None = None) -> str:
    day = day or date.today().strftime("%d.%m.%Y")
    t = compose.totals(p)
    fm = compose.format_money

    rows = "".join(
        f"<tr><td>{i+1}</td><td class='nm'>{_esc(it.name)}</td>"
        f"<td class='c'>{it.qty:g} {_esc(it.unit)}</td>"
        f"<td class='r'>{fm(it.price)}</td><td class='r'>{fm(it.amount)}</td></tr>"
        for i, it in enumerate(p.items)
    )

    advantages = "".join(f"<li>{_esc(a)}</li>" for a in p.advantages)
    pay = "".join(
        f"<div class='pay'><div><b>{_esc(s['name'])}</b><span>{_esc(s['when'])}</span></div>"
        f"<div class='pay-amt'>{fm(s['amount'])}</div></div>"
        for s in compose.payment_schedule(p)
    )
    discount_row = (
        f"<tr class='sub'><td colspan='4'>Скидка {t['discount_pct']:g}%</td>"
        f"<td class='r'>−{fm(t['discount'])}</td></tr>" if t["discount"] else ""
    )

    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Коммерческое предложение — {_esc(p.company)}</title>
<style>
:root{{--accent:{ACCENT};--ink:#1a1f2b;--muted:#6b7480;--line:#e4e8f0;--soft:#f4f6fa}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:var(--ink);background:#eef2f8;line-height:1.55}}
.doc{{max-width:880px;margin:28px auto;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 18px 55px rgba(27,54,93,.12)}}
.cover{{padding:44px 48px;background:linear-gradient(135deg,#1b2b4a,#2f5fd0);color:#fff}}
.cover .meta{{display:flex;justify-content:space-between;font-size:13px;opacity:.85;margin-bottom:26px}}
.cover h1{{margin:0;font-size:18px;font-weight:600;opacity:.9}}
.cover .offer{{margin:14px 0 0;font-size:30px;font-weight:800;letter-spacing:-.5px;line-height:1.15}}
.cover .for{{margin-top:22px;font-size:14px;opacity:.9}}
.sec{{padding:30px 48px;border-top:1px solid var(--line)}}
.sec h2{{font-size:13px;text-transform:uppercase;letter-spacing:.1em;color:var(--accent);margin:0 0 14px}}
.pitch{{font-size:16px;color:#3f4756;margin:0}}
.adv{{list-style:none;padding:0;margin:0;display:grid;gap:10px}}
.adv li{{padding-left:26px;position:relative;color:#3f4756}}
.adv li::before{{content:'✓';position:absolute;left:0;color:var(--accent);font-weight:800}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th{{text-align:left;color:var(--muted);font-weight:600;padding:8px 10px;border-bottom:2px solid var(--line);font-size:12px;text-transform:uppercase;letter-spacing:.04em}}
td{{padding:11px 10px;border-bottom:1px solid var(--line)}}
td.nm{{font-weight:500}} td.c{{text-align:center;white-space:nowrap}} td.r,th.r{{text-align:right;white-space:nowrap}}
.sub td{{color:var(--muted)}}
.totals{{margin-top:16px;margin-left:auto;width:320px;font-size:14px}}
.totals div{{display:flex;justify-content:space-between;padding:6px 0}}
.totals .net{{border-top:1px solid var(--line);margin-top:4px;padding-top:8px;font-weight:600;color:var(--ink)}}
.totals .grand{{border-top:2px solid var(--line);margin-top:6px;padding-top:12px;font-size:20px;font-weight:800;color:var(--accent)}}
.disc{{margin:14px 0 0;font-size:12.5px;color:var(--muted);font-style:italic}}
.terms{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.term{{background:var(--soft);border:1px solid var(--line);border-radius:12px;padding:16px}}
.term b{{display:block;font-size:22px;color:var(--accent)}}
.term span{{font-size:13px;color:var(--muted)}}
.pay{{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid var(--line)}}
.pay span{{display:block;font-size:13px;color:var(--muted)}}
.pay-amt{{font-weight:700}}
.mgr{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}}
.mgr b{{font-size:16px}} .mgr span{{display:block;font-size:13px;color:var(--muted)}}
.mgr-c{{display:flex;gap:18px;flex-wrap:wrap}}
.mgr-c a{{color:var(--accent);text-decoration:none;font-weight:600}}
.cta{{padding:32px 48px;text-align:center;background:var(--soft)}}
.cta button{{border:0;background:linear-gradient(90deg,#2f5fd0,#6d4ee0);color:#fff;font-size:16px;font-weight:700;padding:14px 32px;border-radius:12px;cursor:pointer;box-shadow:0 8px 24px rgba(47,95,208,.3)}}
.cta p{{color:var(--muted);font-size:13px;margin:12px 0 0}}
@media print{{@page{{size:A4;margin:12mm}}body{{background:#fff}}.doc{{box-shadow:none;margin:0;border-radius:0;max-width:100%}}.cta button{{display:none}}}}
</style></head><body>
<div class="doc">
  <div class="cover">
    <div class="meta"><span>{_esc(number)} от {day}</span><span>{_esc(p.company)}</span></div>
    <h1>Коммерческое предложение</h1>
    <div class="offer">{_esc(p.offer)}</div>
    <div class="for">Для: <b>{_esc(p.client) or '—'}</b>{(' · Объект: ' + _esc(p.project)) if p.project else ''}{(', ' + _esc(p.city)) if p.city else ''}</div>
  </div>

  <div class="sec"><h2>О компании</h2><p class="pitch">{_esc(p.pitch)}</p></div>

  {f'<div class="sec"><h2>Почему это выгодно</h2><ul class="adv">{advantages}</ul></div>' if advantages else ''}

  <div class="sec"><h2>{_esc(p.subject) or 'Предложение и расчёт'}</h2>
    <table>
      <thead><tr><th>№</th><th>Наименование</th><th class="c">Кол-во</th><th class="r">Цена</th><th class="r">Сумма</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <div class="totals">
      <div><span>Сумма без НДС</span><span>{fm(t['subtotal'])}</span></div>
      {f"<div><span>Скидка {t['discount_pct']:g}%</span><span>−{fm(t['discount'])}</span></div>" if t['discount'] else ''}
      {f"<div class='net'><span>Итого со скидкой (без НДС)</span><span>{fm(t['net'])}</span></div>" if t['discount'] else ''}
      <div><span>НДС {t['vat_rate']:g}% (на сумму со скидкой)</span><span>{fm(t['vat'])}</span></div>
      <div class="grand"><span>Итого с НДС</span><span>{fm(t['total'])}</span></div>
    </div>
    {f'<p class="disc">{_esc(p.disclaimer)}</p>' if p.disclaimer else ''}
  </div>

  <div class="sec"><h2>Условия</h2>
    <div class="terms">
      <div class="term"><b>{p.lead_time_days}</b><span>дней — срок поставки/работ</span></div>
      <div class="term"><b>{p.warranty_months}</b><span>мес. гарантии</span></div>
      <div class="term"><b>{len(compose.payment_schedule(p))}</b><span>этапа оплаты</span></div>
    </div>
    <div style="margin-top:18px">{pay}</div>
  </div>

  <div class="sec">
    <h2>Контакты</h2>
    <div class="mgr">
      <div><b>{_esc(p.manager) or _esc(p.company)}</b><span>{_esc(p.manager_role) or 'менеджер проекта'}</span></div>
      <div class="mgr-c">
        {f'<a href="tel:{_esc(p.phone)}">{_esc(p.phone)}</a>' if p.phone else ''}
        {f'<a href="mailto:{_esc(p.email)}">{_esc(p.email)}</a>' if p.email else ''}
      </div>
    </div>
  </div>

  <div class="cta">
    <button onclick="alert('Спасибо! Предложение принято. (демо)')">Принять предложение</button>
    <p>Предложение действительно 14 дней. Цены указаны с учётом НДС {t['vat_rate']:g}%.</p>
  </div>
</div>
</body></html>"""
