#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Scraping Premium - CLI principal.
Uso:
  python scraper.py --url https://books.toscrape.com/catalogue/page-1.html
  python scraper.py --output-dir ./meus_dados
  python scraper.py --max-pages 5
  python scraper.py --json
  python scraper.py --excel
"""

import argparse
import sys
import time
from pathlib import Path

from src.exporter import export_csv, export_excel, export_json
from src.fetcher import RequestBlocker, fetch_with_retry
from src.parser import extract_items
from src.utils import setup_logging

DEFAULT_URL = "https://books.toscrape.com/catalogue/page-1.html"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Web Scraping Premium - Coleta dados de sites com paginação, retry e exportação limpa."
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help="URL inicial para scraping (default: Books to Scrape)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Pasta de saída (default: ./output)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Máximo de páginas a processar (default: todas)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Exportar também em JSON",
    )
    parser.add_argument(
        "--excel",
        action="store_true",
        help="Exportar também em Excel",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Logs detalhados",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    log_file = output_dir / "scraper.log"

    logger = setup_logging(log_file=log_file, verbose=args.verbose)
    logger.info("=== Web Scraping Premium ===")
    logger.info("URL: %s", args.url)
    logger.info("Output: %s", output_dir.resolve())
    logger.info("Max páginas: %s", args.max_pages or "ilimitado")

    blocker = RequestBlocker(cooldown_seconds=1.5)

    def fetch(url: str):
        return fetch_with_retry(
            url,
            max_retries=3,
            base_delay=1.0,
            timeout=15,
            blocker=blocker,
            logger=logger,
        )

    def extract(html: str, base_url: str):
        return extract_items(html, base_url, site_type="books_toscrape")

    from src.paginator import paginate

    start = time.perf_counter()
    pages = paginate(
        args.url,
        fetch_fn=fetch,
        extract_fn=extract,
        max_pages=args.max_pages,
        logger=logger,
    )
    elapsed = time.perf_counter() - start

    all_items: list = []
    success_count = 0
    error_count = 0
    for _url, _html, items in pages:
        all_items.extend(items)
        success_count += len(items)

    total_items = len(all_items)
    logger.info("Total de itens extraídos: %d", total_items)
    logger.info("Tempo de execução: %.1f s", elapsed)
    logger.info("Log salvo em: %s", log_file.resolve())

    if not all_items:
        logger.warning("Nenhum item coletado. Verifique a URL e conectividade.")
        return 1

    # Exportar CSV (sempre)
    csv_path = export_csv(all_items, output_dir)
    logger.info("CSV salvo: %s", csv_path)

    if args.json:
        json_path = export_json(all_items, output_dir)
        logger.info("JSON salvo: %s", json_path)

    if args.excel:
        try:
            excel_path = export_excel(all_items, output_dir)
            logger.info("Excel salvo: %s", excel_path)
        except ImportError as e:
            logger.warning("Excel não exportado: %s", e)

    logger.info("=== Concluído ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
