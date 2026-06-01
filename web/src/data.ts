// Зашитый пример КП — результат реального прогона генератора.

export interface Item { name: string; qty: number; unit: string; price: number; kind?: "equipment" | "work"; }

export const disclaimer =
  "Спецификация является предварительной. Окончательный состав и количество оборудования утверждаются после выезда инженера на объект и технического расчёта.";

export const proposal = {
  number: "КП-042",
  date: "01.06.2026",
  company: "ООО «ПромТехСнаб»",
  client: "ООО «Альфа-Логистик»",
  project: "складской комплекс, 6 800 м²",
  city: "Екатеринбург",
  subject: "Поставка и монтаж системы освещения и вентиляции",
  manager: "Соколов Игорь Викторович",
  managerRole: "руководитель проектов",
  phone: "+7 343 200-15-40",
  email: "i.sokolov@promtehsnab.ru",
  offer:
    "Снизим энергозатраты складского комплекса до 35% и окупим проект примерно за 14 месяцев — за счёт промышленного LED-освещения с управлением и приточной вентиляции с рекуперацией тепла.",
  pitch:
    "ООО «ПромТехСнаб» 12 лет проектирует и монтирует инженерные системы под ключ. Работаем по договору с фиксированной сметой, держим сроки и даём гарантию на оборудование и работы. За плечами более 200 реализованных объектов в УрФО.",
  advantages: [
    "LED-освещение с датчиками присутствия снижает расход на свет до 60%",
    "Рекуперация тепла в вентиляции — экономия на отоплении до 25%",
    "Фиксированная смета: цена в договоре не растёт по ходу работ",
    "Один подрядчик на весь цикл: проект, поставка, монтаж и пусконаладка",
    "Гарантия 36 месяцев на оборудование и монтажные работы",
  ],
  items: [
    { name: "Светодиодные светильники промышленные, 150 Вт", qty: 220, unit: "шт", price: 4800 },
    { name: "Система управления освещением (датчики, контроллеры)", qty: 1, unit: "компл", price: 480000 },
    { name: "Приточно-вытяжная установка с рекуперацией", qty: 4, unit: "шт", price: 620000 },
    { name: "Монтажные и пусконаладочные работы", qty: 1, unit: "компл", price: 1150000, kind: "work" },
    { name: "Проектная и исполнительная документация", qty: 1, unit: "компл", price: 180000, kind: "work" },
  ] as Item[],
  discountPct: 5,
  vatRate: 22,
  advancePct: 30,
  leadTimeDays: 45,
  warrantyMonths: 36,
};

export const stages = [
  { id: "data", icon: "📋", title: "Данные объекта", tech: "клиент · объект · позиции", desc: "Что поставляем и кому" },
  { id: "ai", icon: "✍️", title: "AI-копирайтинг", tech: "LLM", desc: "Оффер, о компании, выгоды" },
  { id: "calc", icon: "🧮", title: "Расчёт", tech: "сумма · скидка · НДС", desc: "Смета и график оплаты" },
  { id: "doc", icon: "📄", title: "Готовое КП", tech: "веб + PDF", desc: "Интерактивная страница" },
];

export function money(v: number): string {
  return v.toLocaleString("ru-RU", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " ₽";
}

const subtotal = proposal.items.reduce((s, i) => s + i.qty * i.price, 0);
const discount = Math.round(subtotal * proposal.discountPct) / 100;
const net = subtotal - discount;
const vat = Math.round(net * proposal.vatRate) / 100;
export const totals = {
  subtotal,
  discount,
  net,
  vat,
  total: net + vat,
};

// Трёхэтапный график: закупка → поставка → монтаж (учитывает тип позиций)
const r2 = (v: number) => Math.round(v * 100) / 100;
const equipNet = proposal.items.filter((i) => i.kind !== "work").reduce((s, i) => s + i.qty * i.price, 0);
const equipGross = r2((totals.total * equipNet) / subtotal);
const advance = r2(equipGross * 0.5);
const delivery = r2(equipGross - advance);

export const payment = [
  { name: "Аванс на закупку оборудования (50%)", amount: advance, when: "при подписании договора" },
  { name: "Оплата оборудования по факту поставки", amount: delivery, when: "при поставке на объект" },
  { name: "Монтаж и пусконаладка", amount: r2(totals.total - advance - delivery), when: "после подписания актов КС-2 / КС-3" },
];

export const paymentStages = payment.length;
