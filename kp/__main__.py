"""
CLI: python -m kp sample/example.json [--number КП-042] [--no-ai]

Загружает данные КП из JSON, при необходимости генерирует продающие тексты
через ИИ, считает суммы/НДС и сохраняет интерактивную HTML-страницу КП.
"""

import sys
import json
import logging
import argparse
from pathlib import Path

from kp import config
from kp.model import Proposal
from kp.compose import totals, format_money
from kp.render import render_html

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)-7s  %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("kp")


def main(argv=None):
    parser = argparse.ArgumentParser(description="AI-генератор коммерческих предложений")
    parser.add_argument("file", help="JSON с данными КП")
    parser.add_argument("--number", default="КП-001", help="Номер КП")
    parser.add_argument("--no-ai", action="store_true", help="Не вызывать ИИ (тексты из JSON)")
    args = parser.parse_args(argv)

    data = json.loads(Path(args.file).read_text(encoding="utf-8"))
    proposal = Proposal.from_dict(data)

    if not args.no_ai:
        config.validate()
        log.info("Генерирую продающие тексты через ИИ...")
        from kp.ai import fill_texts
        proposal = fill_texts(proposal)

    t = totals(proposal)
    html = render_html(proposal, number=args.number)

    out_dir = Path(config.OUTPUT_DIR)
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / (Path(args.file).stem + ".html")
    out_path.write_text(html, encoding="utf-8")

    print("\n" + "=" * 60)
    print(f"  Компания:  {proposal.company}")
    print(f"  Клиент:    {proposal.client}")
    print(f"  Оффер:     {proposal.offer}")
    print(f"  Позиций:   {len(proposal.items)}")
    print(f"  Итого:     {format_money(t['total'])} (НДС {t['vat_rate']:g}%)")
    print("=" * 60)
    log.info(f"📄 КП сохранено: {out_path}  (откройте в браузере → Печать в PDF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
