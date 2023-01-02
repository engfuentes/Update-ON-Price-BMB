import asyncio
import pandas as pd
import platform
import logging
from modules.gsheet_operations import get_gsheet_as_df, update_gsheet_columns
from modules.webscrapper import webscrapper

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting the script...")


async def main():
    """Async main module.
    1. Gets the gsheet as a DataFrame
    2. Webscrap the prices of the ONs
    3. Update the prices into the gsheet"""

    logger.info("Starting the async main module...")

    # Load the gsheet as pandas dataframe
    df = get_gsheet_as_df()

    # Get the prices in USD and ARS
    df["Precio USD"] = await asyncio.gather(*(webscrapper(on) for on in df["Especie en USD"]))
    df["Precio ARS"] = await asyncio.gather(*(webscrapper(on) for on in df["Especie en Pesos"]))

    # Update the values to gsheet
    update_gsheet_columns(df)


# Set this if the code is run in Windows to avoid a loop error
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
