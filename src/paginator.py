# -*- coding: utf-8 -*-
"""Módulo de paginação: detecta próxima página, evita loop infinito."""

from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


def get_next_page_url(html: str, current_url: str, base_url: str | None = None) -> str | None:
    """
    Detecta URL do botão "Próxima página" ou link "next".
    Retorna None se não houver próxima página.
    """
    soup = BeautifulSoup(html, "html.parser")
    base = base_url or current_url

    # Seletores comuns para "próxima página" (Books to Scrape usa li.next a)
    next_el = (
        soup.select_one("li.next a[href]")
        or soup.select_one('[rel="next"]')
        or soup.select_one('a[aria-label="next"]')
        or soup.select_one(".pagination .next a")
    )

    if not next_el:
        # Fallback: procurar texto "next" em links
        for a in soup.select("a[href]"):
            if "next" in a.get_text().lower():
                href = a.get("href")
                if href:
                    return urljoin(base, href)
        return None

    href = next_el.get("href")
    if not href:
        return None

    return urljoin(base, href)


def is_same_page(url1: str, url2: str) -> bool:
    """Evita loop: verifica se duas URLs apontam para a mesma página."""
    p1 = urlparse(url1)
    p2 = urlparse(url2)
    return p1.path.rstrip("/") == p2.path.rstrip("/")


def paginate(
    start_url: str,
    fetch_fn,
    extract_fn,
    max_pages: int | None = None,
    seen_urls: set | None = None,
    logger=None,
):
    """
    Itera páginas, chama fetch_fn(url) -> html e extract_fn(html) -> items.
    Retorna lista de (url, html, items) por página.
    """
    seen = seen_urls or set()
    results: list[tuple[str, str, list]] = []
    current_url = start_url
    page_count = 0

    while current_url:
        if max_pages is not None and page_count >= max_pages:
            if logger:
                logger.info("Limite de %d páginas atingido", max_pages)
            break

        if current_url in seen:
            if logger:
                logger.warning("Loop detectado: %s já processada", current_url)
            break
        seen.add(current_url)

        html, status = fetch_fn(current_url)
        if not html or status != "ok":
            if logger:
                logger.warning("Falha ao obter página: %s (status=%s)", current_url, status)
            break

        items = extract_fn(html, current_url)
        results.append((current_url, html, items))
        page_count += 1

        if logger:
            logger.info("Página %d processada: %s (%d itens)", page_count, current_url, len(items))

        next_url = get_next_page_url(html, current_url, current_url)
        if not next_url or is_same_page(current_url, next_url):
            break
        current_url = next_url

    return results
