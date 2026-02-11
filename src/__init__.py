# -*- coding: utf-8 -*-
"""Web Scraping Premium - Módulos de coleta, parsing e exportação."""

from .exporter import export_csv, export_excel, export_json
from .fetcher import fetch_html, fetch_with_retry, get_random_headers, RequestBlocker
from .parser import Item, extract_items, extract_items_books_toscrape
from .paginator import get_next_page_url, paginate
from .utils import normalize_text, parse_price, parse_rating, setup_logging

__all__ = [
    "Item",
    "RequestBlocker",
    "extract_items",
    "extract_items_books_toscrape",
    "export_csv",
    "export_excel",
    "export_json",
    "fetch_html",
    "fetch_with_retry",
    "get_next_page_url",
    "get_random_headers",
    "normalize_text",
    "paginate",
    "parse_price",
    "parse_rating",
    "setup_logging",
]
