# -*- coding: utf-8 -*-
"""Utilitários compartilhados: logging, normalização de texto, constantes."""

import logging
import re
from pathlib import Path

# User-Agents realistas para rotação
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
]

# Headers base para requisições (sem br - requests não decodifica Brotli nativamente)
DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# Padrões de CAPTCHA (detecção básica)
CAPTCHA_PATTERNS = [
    r"captcha",
    r"recaptcha",
    r"hcaptcha",
    r"cloudflare.*challenge",
    r"please verify you are human",
    r"unusual traffic",
]


def setup_logging(
    log_file: Path | None = None,
    verbose: bool = False,
) -> logging.Logger:
    """Configura logging para o scraper."""
    logger = logging.getLogger("scraper")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    if log_file:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


def normalize_text(text: str | None) -> str:
    """Remove espaços múltiplos, strip e caracteres especiais problemáticos."""
    if text is None or not isinstance(text, str):
        return ""
    t = text.strip()
    t = re.sub(r"\s+", " ", t)
    return t


def parse_price(text: str | None) -> float | None:
    """Extrai valor numérico de string de preço."""
    if text is None or not isinstance(text, str):
        return None
    # Remove símbolos de moeda e espaços, mantém apenas números e ponto/vírgula
    cleaned = re.sub(r"[^\d,.]", "", text.strip())
    cleaned = cleaned.replace(",", ".")
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def parse_rating(classes: list[str] | str) -> str | None:
    """Extrai rating de classes como 'star-rating Three' -> '3'."""
    if isinstance(classes, str):
        classes = classes.split()
    for c in classes:
        lower = c.lower()
        if lower in ("one", "two", "three", "four", "five"):
            return {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5"}.get(
                lower
            )
    return None


def might_be_captcha(html: str) -> bool:
    """Verifica se a página pode conter desafio CAPTCHA."""
    html_lower = html.lower()
    for pattern in CAPTCHA_PATTERNS:
        if re.search(pattern, html_lower):
            return True
    return False
