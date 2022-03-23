"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""
import aiohttp
import pyshorteners

from typing import Tuple, List

from pyshorteners.exceptions import (
    BadAPIResponseException,
    BadURLException,
    ShorteningErrorException,
)

from config.ext.parser import config


from .logging import log


async def shorten_url(url: str) -> str:
    """Shorterns A URL Using Bit.ly API

    Parameters
    ----------
    url : str
        The URL to shorten

    Returns
    -------
    [str]
        URL Generated By Bit.ly
    """
    s = pyshorteners.Shortener(api_key=config["BITLY_API_TOKEN"])
    try:
        shortened_url = s.bitly.short(url)
    except (BadAPIResponseException, BadURLException, ShorteningErrorException):
        log.error("[red]ERROR WHEN TRYING TO SHORTEN URL.[/red]")

    return shortened_url


async def get_scam_links() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://raw.githubusercontent.com/DevSpen/scam-links/master/src/links.txt"
        ) as response:
            text = await response.text()
            return text


async def get_malicious_links() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://raw.githubusercontent.com/DevSpen/scam-links/master/src/malicious-terms.txt"
        ) as response:
            text = await response.text()
            return text


async def get_trailing_links() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://raw.githubusercontent.com/DevSpen/scam-links/master/src/trailing-slashes.txt"
        ) as response:
            text = await response.text()
            return text


async def is_scam_link(link: str) -> bool:
    async with aiohttp.ClientSession() as session:
        params = {"link": link}
        async with session.get(
            "https://spen.tk/api/v1/isScamLink", params=params
        ) as response:
            json = await response.json()

            if json["result"] == "true":
                return True
            else:
                return False


async def get_malicious_terms(text: str) -> Tuple[bool, List]:
    async with aiohttp.ClientSession() as session:
        params = {"text": text}
        async with session.get(
            "https://spen.tk/api/v1/isMaliciousTerm", params=params
        ) as response:
            json = await response.json()

            return json["hasMatch"], json["matches"]
