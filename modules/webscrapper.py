import aiohttp
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import cchardet as chardet
import re
import logging

# Enable logging
logger = logging.getLogger('app')


async def webscrapper(on):
    """Async Function that does the webscrapping using aiohttp to have multiple requests in parallel

    Parameters
    ----------
        on : str
            name of the ON that must be scrapped. The named is used in the url

    Returns
    -------
        price_float : float
            price of the ON as result of the webscrapping

    """

    logger.info(f"Starting the webscrapping of {on}...")

    # Create a timeout to avoid a TimeoutError
    timeout = aiohttp.ClientTimeout(total=600)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        url = "https://www.allaria.com.ar/Bono/Especie/" + on
        async with session.get(url) as response:
            try:
                page = await response.text()

                # Strainer is used to only parse the wanted id
                strainer = SoupStrainer(id="datos")

                # Parse with Beautiful Soup
                soup = BeautifulSoup(page, "lxml", parse_only=strainer)

                # Get the last_price h2 and transform to text
                div = soup.find(id="datos")
                last_price = div.find("h2", class_="float-left").get_text()

                # Find the number
                price_str = re.findall(r"(?:\d+\.)?\d+,\d+", last_price)[0]
                price_float = float(price_str.replace(".", "").replace(",", "."))
                
                # print(last_price.prettify())
                return price_float
            
            except:
                logger.error(f"Error in the webscrapping of {on}")
           
            
