import { useState, useEffect, useRef } from "react";
import { proposal, stages, totals, payment, paymentStages, disclaimer, money } from "./data";

type Phase = "idle" | "running" | "done";

function ThemeToggle() {
  const [theme, setTheme] = useState<"light" | "dark">(() =>
    localStorage.getItem("theme") === "dark" ? "dark" : "light"
  );
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);
  return (
    <button className="theme-toggle" onClick={() => setTheme(theme === "light" ? "dark" : "light")}
      aria-label="Переключить тему" title={theme === "light" ? "Тёмная тема" : "Светлая тема"}>
      {theme === "light" ? "🌙" : "☀️"}
    </button>
  );
}

function BackLink() {
  return <a className="backlink" href="https://kilevoy.github.io/" title="Вернуться в портфолио">← Портфолио</a>;
}

export default function App() {
  return (
    <div className="page">
      <BackLink />
      <ThemeToggle />
      <Hero />
      <Demo />
      <HowItWorks />
      <Stack />
      <Footer />
    </div>
  );
}

function Hero() {
  const toDemo = () => document.getElementById("demo")?.scrollIntoView({ behavior: "smooth" });
  return (
    <header className="hero">
      <div className="badge">AI-автоматизация · продажи</div>
      <h1>Коммерческое предложение <span className="grad">за минуту</span></h1>
      <p className="lead">
        Менеджер тратит часы на сборку КП в Word. Здесь: вводишь объект и позиции —
        получаешь готовое предложение с <b>продающим оффером</b>, расчётом с НДС и условиями,
        в современном интерактивном формате и PDF.
      </p>
      <div className="hero-cta">
        <button className="btn primary" onClick={toDemo}>▶ Сгенерировать на примере</button>
        <a className="btn ghost" href="https://github.com/kilevoy/ai-proposal-generator" target="_blank" rel="noreferrer">Исходный код</a>
      </div>
      <div className="flow">
        <span>📋 Данные</span><i>→</i><span>✍️ AI-текст</span><i>→</i><span>🧮 Расчёт</span><i>→</i><span>📄 КП + PDF</span>
      </div>
    </header>
  );
}

function Demo() {
  const [phase, setPhase] = useState<Phase>("idle");
  const [active, setActive] = useState(-1);
  const timers = useRef<number[]>([]);
  useEffect(() => () => timers.current.forEach(clearTimeout), []);

  const run = () => {
    timers.current.forEach(clearTimeout); timers.current = [];
    setPhase("running"); setActive(0);
    const step = 950;
    stages.forEach((_, i) => timers.current.push(window.setTimeout(() => setActive(i), step * i)));
    timers.current.push(window.setTimeout(() => { setActive(stages.length); setPhase("done"); }, step * stages.length));
  };
  const reset = () => { timers.current.forEach(clearTimeout); setPhase("idle"); setActive(-1); };

  return (
    <section id="demo" className="demo">
      <h2>Демонстрация</h2>
      <p className="section-sub">Пример: поставка инженерных систем для склада. Нажмите «Сгенерировать».</p>
      <div className="demo-controls">
        {phase === "idle" && <button className="btn primary" onClick={run}>▶ Сгенерировать КП</button>}
        {phase === "running" && <button className="btn" disabled>⏳ Генерация…</button>}
        {phase === "done" && <button className="btn ghost" onClick={reset}>↺ Заново</button>}
      </div>
      <div className="pipeline">
        {stages.map((s, i) => {
          const state = active > i ? "done" : active === i ? "active" : "wait";
          return (
            <div key={s.id} className={`stage ${state}`}>
              <div className="stage-icon">{s.icon}</div>
              <div className="stage-body">
                <div className="stage-title">{s.title}</div>
                <div className="stage-tech">{s.tech}</div>
                <div className="stage-desc">{s.desc}</div>
              </div>
              <div className="stage-status">{state === "done" ? "✓" : state === "active" ? "…" : ""}</div>
            </div>
          );
        })}
      </div>
      {phase === "done" && <ProposalView />}
    </section>
  );
}

function ProposalView() {
  const download = () => window.open("proposal-example.pdf", "_blank");
  return (
    <div className="result show">
      <div className="result-bar">
        <span className="viewed">● Клиент открыл КП · 2 мин назад</span>
        <button className="btn primary sm" onClick={download}>↓ Скачать PDF</button>
      </div>

      <div className="kp">
        <div className="kp-cover">
          <div className="kp-meta"><span>{proposal.number} от {proposal.date}</span><span>{proposal.company}</span></div>
          <div className="kp-h1">Коммерческое предложение</div>
          <div className="kp-offer">{proposal.offer}</div>
          <div className="kp-for">Для: <b>{proposal.client}</b> · Объект: {proposal.project}, {proposal.city}</div>
        </div>

        <div className="kp-sec"><h3>О компании</h3><p>{proposal.pitch}</p></div>

        <div className="kp-sec">
          <h3>Почему это выгодно</h3>
          <ul className="kp-adv">{proposal.advantages.map((a, i) => <li key={i}>{a}</li>)}</ul>
        </div>

        <div className="kp-sec">
          <h3>{proposal.subject}</h3>
          <table className="kp-table">
            <thead><tr><th>№</th><th>Наименование</th><th className="c">Кол-во</th><th className="r">Цена</th><th className="r">Сумма</th></tr></thead>
            <tbody>
              {proposal.items.map((it, i) => (
                <tr key={i}><td>{i + 1}</td><td>{it.name}</td><td className="c">{it.qty} {it.unit}</td>
                  <td className="r">{money(it.price)}</td><td className="r">{money(it.qty * it.price)}</td></tr>
              ))}
            </tbody>
          </table>
          <div className="kp-totals">
            <div><span>Сумма без НДС</span><span>{money(totals.subtotal)}</span></div>
            <div><span>Скидка {proposal.discountPct}%</span><span>−{money(totals.discount)}</span></div>
            <div className="net"><span>Итого со скидкой (без НДС)</span><span>{money(totals.net)}</span></div>
            <div><span>НДС {proposal.vatRate}% (на сумму со скидкой)</span><span>{money(totals.vat)}</span></div>
            <div className="grand"><span>Итого с НДС</span><span>{money(totals.total)}</span></div>
          </div>
          <p className="kp-disc">{disclaimer}</p>
        </div>

        <div className="kp-sec">
          <h3>Условия</h3>
          <div className="kp-terms">
            <div><b>{proposal.leadTimeDays}</b><span>дней — срок</span></div>
            <div><b>{proposal.warrantyMonths}</b><span>мес. гарантии</span></div>
            <div><b>{paymentStages}</b><span>этапа оплаты</span></div>
          </div>
          <div className="kp-pay">
            {payment.map((p, i) => (
              <div key={i}><div><b>{p.name}</b><span>{p.when}</span></div><div className="amt">{money(p.amount)}</div></div>
            ))}
          </div>
        </div>

        <div className="kp-sec">
          <h3>Контакты</h3>
          <div className="kp-mgr">
            <div><b>{proposal.manager}</b><span>{proposal.managerRole}</span></div>
            <div className="kp-mgr-c">
              <a href={`tel:${proposal.phone}`}>{proposal.phone}</a>
              <a href={`mailto:${proposal.email}`}>{proposal.email}</a>
            </div>
          </div>
        </div>

        <div className="kp-cta">
          <button onClick={() => alert("Спасибо! Предложение принято. (демо)")}>Принять предложение</button>
          <p>Действительно 14 дней. Цены с учётом НДС {proposal.vatRate}%.</p>
        </div>
      </div>
    </div>
  );
}

function HowItWorks() {
  const steps = [
    { n: "1", t: "Данные объекта", d: "Клиент, объект, позиции с ценами — вручную или импортом из таблицы/CRM." },
    { n: "2", t: "AI-копирайтинг", d: "LLM пишет продающий оффер с выгодой, блок «о компании» и преимущества под конкретного клиента." },
    { n: "3", t: "Расчёт", d: "Сумма, скидка, НДС (2026 — 22%), график оплаты «аванс + остаток». Чистые функции, покрыты тестами." },
    { n: "4", t: "Готовое КП", d: "Интерактивная веб-страница (как Qwilr/PandaDoc) с кнопкой «Принять» + экспорт в PDF. Концепт аналитики просмотра." },
  ];
  return (
    <section className="how">
      <h2>Как устроено</h2>
      <div className="steps">
        {steps.map((s) => (
          <div key={s.n} className="step"><div className="step-n">{s.n}</div><div><h4>{s.t}</h4><p>{s.d}</p></div></div>
        ))}
      </div>
    </section>
  );
}

function Stack() {
  const tech = ["Python", "LLM (Ollama / OpenRouter)", "HTML/CSS-рендер", "pytest", "React + TypeScript"];
  return (
    <section className="stack">
      <h2>Технологии</h2>
      <div className="chips">{tech.map((t) => <span key={t} className="chip">{t}</span>)}</div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="footer">
      <p>Кейс из портфолио по AI-автоматизации.{" "}
        <a href="https://github.com/kilevoy/ai-proposal-generator" target="_blank" rel="noreferrer">ai-proposal-generator</a></p>
      <p className="muted">Демо-режим: показан результат реального прогона генератора. Тренды учтены: AI-копирайтинг, интерактивный веб-формат, аналитика просмотра, расчёт с НДС.</p>
    </footer>
  );
}
