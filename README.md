# 🕷️ Web Scraping Premium (Python)

Scraper profissional para coleta robusta de dados: rotação de User-Agent, retry inteligente, paginação avançada, exportação limpa e logs detalhados.

---

## 📌 Visão Geral

Este projeto oferece um scraper de nível profissional, capaz de extrair dados de sites reais de modo:

- Estruturado
- Resiliente
- Escalável
- Seguro
- Confiável

Diferente de scrapers simples, este foi pensado para suportar:

- Alternância de headers
- Diversos erros HTTP (timeouts/5xx/429)
- Paginação automática
- HTML inconsistente
- Múltiplos formatos de saída
- Logs completos

É o tipo de solução entregue por freelancers em Upwork, Workana e 99Freelas, normalmente para áreas como BI, Pricing, Marketing, SEO, Auditoria, Financeiro ou Inteligência Competitiva.

---

## 🚀 Principais Recursos

### 1️⃣ Requisições HTTP realistas (User-Agent + Headers)

- Simulação de navegador real
- Headers completos e variados
- Rotação dinâmica de User-Agents
- Sleep aleatório para evitar bloqueios
- Reduz drasticamente códigos 429, 503 e banimentos

---

### 2️⃣ Retry com Backoff Exponencial

- Gerenciamento automático para erros como:
  - Timeout
  - Conexão perdida
  - 429 “Too Many Requests”
  - 5xx
- Tentativas automáticas com delays progressivos

---

### 3️⃣ Parsing Resiliente (BeautifulSoup)

- Extrações robustas (nome, preço, categoria, descrição, disponibilidade, rating)
- Limpeza e padronização integradas

---

### 4️⃣ Paginação Inteligente

- Detecta e percorre botão “próxima página” automaticamente
- Previne loops infinitos
- Registra páginas visitadas e coleta incremental
- Navega até o final sem intervenção manual

---

### 5️⃣ Vários formatos de saída

- CSV (padrão)
- Excel (.xlsx)
- JSON

Exemplo de arquivo de saída:

```
output/
└── scraped_YYYYMMDD_HHMMSS.csv
```

---

### 6️⃣ Logging Avançado

- Geração de logs detalhados em `output/scraper.log`:
  - Status das requisições
  - Tentativas e retries
  - Tempo total do scraping
  - Quantidade de páginas e registros coletados
- Facilita auditoria e debugging

---

### 7️⃣ CLI Completa

Principais comandos:

```bash
# Scraping padrão
python scraper.py

# Customizar URL target
python scraper.py --url https://books.toscrape.com/catalogue/page-1.html

# Limitar páginas
python scraper.py --max-pages 5

# Customizar diretório de saída
python scraper.py --output-dir ./dados

# Gerar JSON e Excel
python scraper.py --json --excel

# Ativar logs detalhados
python scraper.py -v
```

---

## 🧠 Estrutura do Projeto

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
    ├── fetcher.py      # Requisições HTTP
    ├── parser.py       # Parsing e extração
    ├── paginator.py    # Lógica de paginação
    ├── exporter.py     # CSV / Excel / JSON
    └── utils.py        # Funções auxiliares
```

---

## 📄 Site de Demonstração

O scraper utiliza o site Books to Scrape (usado para fins educacionais/demos), extraindo:

- Título do livro
- Preço
- Rating
- Disponibilidade
- Link direto
- Categoria

---

## 📁 Exemplo de Saída

Confira `sample_output.csv` com cerca de 60 registros extraídos automaticamente.

---

## 🔖 Tecnologias

- Python
- Requests
- BeautifulSoup
- Pandas
- Lxml
- OpenPyXL
- Logging avançado

---

## 📄 Licença

Livre para uso e adaptação comercial.