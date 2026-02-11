# Web Scraping Premium

Scraper profissional com rotação de User-Agent, gestão de erros, paginação e exportação limpa (CSV/Excel/JSON).

## Funcionalidades

- Requisições HTTP com headers realistas e rotação de User-Agent
- Retry com backoff exponencial para 429/timeouts
- Parsing resiliente com BeautifulSoup
- Paginação inteligente (detecção de "próxima página")
- Exportação: CSV (default), Excel e JSON
- Logs rastreáveis em `output/scraper.log`
- CLI configurável

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
# Scraping padrão (Books to Scrape, CSV)
python scraper.py

# URL customizada
python scraper.py --url https://books.toscrape.com/catalogue/page-1.html

# Limitar páginas
python scraper.py --max-pages 5

# Pasta de saída
python scraper.py --output-dir ./meus_dados

# Exportar JSON e Excel
python scraper.py --json --excel

# Logs verbosos
python scraper.py -v
```

## Estrutura

```
webscraping-premium/
├── scraper.py
├── requirements.txt
├── output/
├── assets/
│   ├── screenshot-raw.png
│   ├── screenshot-clean.png
│   └── demo.gif
└── src/
    ├── fetcher.py
    ├── parser.py
    ├── paginator.py
    ├── exporter.py
    └── utils.py
```

## Site de Demonstração

O scraper usa [Books to Scrape](https://books.toscrape.com/) como site de demonstração — livros com nome, preço, rating e disponibilidade.

## Exemplo de Saída

O arquivo `sample_output.csv` contém 60 registros coletados como demonstração.
