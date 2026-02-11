# -*- coding: utf-8 -*-
"""Módulo de parsing e extração com BeautifulSoup e seletores resilientes."""

from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .utils import normalize_text, parse_price, parse_rating


@dataclass
class Item:
    """Item extraído (produto genérico para vitrine)."""

    nome: str
    preco: float | None
    categoria: str
    descricao: str
    disponibilidade: str
    rating: str | None
    link: str
    raw: dict[str, Any] | None = None


def extract_items_books_toscrape(html: str, base_url: str) -> list[Item]:
    """
    Extrai itens do Books to Scrape (livros).
    Campos: nome, preço, categoria, descrição, disponibilidade, rating, link.
    """
    soup = BeautifulSoup(html, "html.parser")
    items: list[Item] = []

    # Seletores resilientes: article.product_pod ou li.col-xs-6
    products = soup.select("article.product_pod") or soup.select("ol.row li.col-xs-6")

    for prod in products:
        raw: dict[str, Any] = {}

        # Nome e link
        title_el = prod.select_one("h3 a") or prod.select_one("a[title]")
        nome = ""
        link = ""
        if title_el:
            nome = normalize_text(title_el.get("title") or title_el.get_text())
            href = title_el.get("href", "")
            link = urljoin(base_url, href) if href else ""
        raw["nome"] = nome
        raw["link"] = link

        # Preço
        price_el = prod.select_one(".price_color") or prod.select_one("p.price_color")
        preco = None
        if price_el:
            preco = parse_price(price_el.get_text())
        raw["preco"] = preco

        # Rating
        rating_el = prod.select_one("p.star-rating")
        rating = None
        if rating_el:
            classes = rating_el.get("class", [])
            rating = parse_rating(classes)
        raw["rating"] = rating

        # Disponibilidade
        avail_el = prod.select_one(".instock.availability") or prod.select_one(
            "p.instock_availability"
        ) or prod.select_one(".availability")
        disponibilidade = ""
        if avail_el:
            disponibilidade = normalize_text(avail_el.get_text())
        raw["disponibilidade"] = disponibilidade

        # Categoria (na listagem geral não vem; usamos vazio ou "Livros")
        categoria = "Livros"
        raw["categoria"] = categoria

        # Descrição curta (na listagem não tem; usamos nome truncado)
        descricao = nome[:100] + "..." if len(nome) > 100 else nome
        raw["descricao"] = descricao

        items.append(
            Item(
                nome=nome,
                preco=preco,
                categoria=categoria,
                descricao=descricao,
                disponibilidade=disponibilidade,
                rating=rating,
                link=link,
                raw=raw,
            )
        )

    return items


def extract_items(html: str, base_url: str, site_type: str = "books_toscrape") -> list[Item]:
    """
    Extrai itens conforme o tipo de site.
    Permite extensão futura para outros sites.
    """
    if site_type == "books_toscrape":
        return extract_items_books_toscrape(html, base_url)
    raise ValueError(f"Tipo de site não suportado: {site_type}")
