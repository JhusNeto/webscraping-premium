# -*- coding: utf-8 -*-
"""Módulo de exportação: CSV, Excel, JSON."""

import csv
import json
from datetime import datetime
from pathlib import Path

from .parser import Item


def _item_to_row(item: Item) -> dict[str, str | float | None]:
    """Converte Item para dicionário flat."""
    return {
        "nome": item.nome,
        "preco": item.preco,
        "categoria": item.categoria,
        "descricao": item.descricao,
        "disponibilidade": item.disponibilidade,
        "rating": item.rating,
        "link": item.link,
    }


def export_csv(items: list[Item], output_dir: Path) -> Path:
    """Exporta para CSV. Nome: scraped_YYYYMMDD_HHMMSS.csv"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"scraped_{timestamp}.csv"

    if not items:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nome", "preco", "categoria", "descricao", "disponibilidade", "rating", "link"])
        return path

    fieldnames = list(_item_to_row(items[0]).keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            row = _item_to_row(item)
            for k, v in row.items():
                if v is None:
                    row[k] = ""
            writer.writerow(row)

    return path


def export_json(items: list[Item], output_dir: Path) -> Path:
    """Exporta para JSON."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"scraped_{timestamp}.json"

    data = [_item_to_row(item) for item in items]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return path


def export_excel(items: list[Item], output_dir: Path) -> Path:
    """Exporta para Excel (requer openpyxl)."""
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("Para exportar Excel, instale: pip install pandas openpyxl")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"scraped_{timestamp}.xlsx"

    data = [_item_to_row(item) for item in items]
    df = pd.DataFrame(data)
    df.to_excel(path, index=False, engine="openpyxl")
    return path
