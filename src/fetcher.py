# -*- coding: utf-8 -*-
"""Módulo de requisições HTTP: headers, retry, fallback, rotação de User-Agent."""

import random
import time

import requests
from requests.exceptions import Timeout, ConnectionError as ReqConnectionError
from requests.exceptions import HTTPError

from .utils import DEFAULT_HEADERS, USER_AGENTS, might_be_captcha


class RequestBlocker:
    """Evita requisições duplicadas para a mesma URL em curto período."""

    def __init__(self, cooldown_seconds: float = 2.0):
        self._last: dict[str, float] = {}
        self.cooldown = cooldown_seconds

    def is_blocked(self, url: str) -> bool:
        now = time.time()
        if url in self._last and (now - self._last[url]) < self.cooldown:
            return True
        return False

    def register(self, url: str) -> None:
        self._last[url] = time.time()


def get_random_headers() -> dict[str, str]:
    """Retorna headers com User-Agent aleatório."""
    h = DEFAULT_HEADERS.copy()
    h["User-Agent"] = random.choice(USER_AGENTS)
    return h


def fetch_html(
    url: str,
    timeout: int = 15,
    session: requests.Session | None = None,
    logger=None,
) -> tuple[str | None, str]:
    """
    Faz requisição GET e retorna (html, status).
    status: 'ok', 'erro', 'timeout', 'connection_error', 'http_error', 'captcha'.
    """
    sess = session or requests.Session()
    headers = get_random_headers()
    try:
        r = sess.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        html = r.text
        if might_be_captcha(html) and logger:
            logger.warning("Possível CAPTCHA detectado na página: %s", url)
            return html, "captcha"
        return html, "ok"
    except Timeout:
        if logger:
            logger.warning("Timeout em %s", url)
        return None, "timeout"
    except ReqConnectionError:
        if logger:
            logger.warning("Erro de conexão em %s", url)
        return None, "connection_error"
    except HTTPError as e:
        if logger:
            logger.warning("HTTP %s em %s", e.response.status_code if e.response else "?", url)
        return None, "http_error"
    except Exception as e:
        if logger:
            logger.exception("Erro inesperado em %s", url)
        return None, "erro"


def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
    timeout: int = 15,
    blocker: RequestBlocker | None = None,
    logger=None,
) -> tuple[str | None, str]:
    """
    Requisição com retry e backoff exponencial.
    Retorna (html, status). Status: 'ok', 'erro', 'retry'.
    """
    blocker = blocker or RequestBlocker()
    if blocker.is_blocked(url):
        if logger:
            logger.debug("URL bloqueada (duplicada): %s", url)
        time.sleep(blocker.cooldown)

    sess = requests.Session()
    last_status = "erro"

    for attempt in range(max_retries):
        html, status = fetch_html(url, timeout=timeout, session=sess, logger=logger)

        if status == "ok" and html:
            blocker.register(url)
            # Sleep aleatório entre requisições (0.5 a 2.0 segundos)
            time.sleep(random.uniform(0.5, 2.0))
            return html, "ok"

        last_status = status

        # 429 ou timeout: aplicar backoff
        if status in ("timeout", "http_error") and attempt < max_retries - 1:
            delay = base_delay * (2**attempt) + random.uniform(0, 1)
            if logger:
                logger.info("Retry %d/%d em %.1fs para %s", attempt + 1, max_retries, delay, url)
            time.sleep(delay)
        else:
            break

    return None, last_status if last_status != "ok" else "retry"
