import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import logging

# Start logging
logger = logging.getLogger('app')


def get_gsheet():
    """Function that uses the json credentials to get the gsheet from google

    Returns
    -------
        gsheet
    """

    logger.info("Starting to get the gsheet...")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "./settings/gsheet-on-updater-credentials.json", scope
    )  # json gfile from google developer website is used as credentials

    client = gspread.authorize(credentials)
    google_sheet = client.open("ONs en USD - Precio automatico")  # Name of the google sheet
    sheet = google_sheet.worksheet("Curva")  # Name of the sheet

    return sheet


def get_gsheet_as_df():
    """Transforms the gsheet to a pandas dataframe

    Parameters
    ----------
        on : str
            name of the ON that must be scrapped. The named is used in the url

    Returns
    -------
        price_float : float
            price of the ON as result of the webscrapping

    """

    logger.info("Starting to transform the gsheet to a DataFrame...")

    # Get the sheet using the function
    sheet = get_gsheet()

    # Get the data from gsheet
    data = sheet.get_all_records()

    # Import into a pandas df
    df = pd.DataFrame(data)

    return df


def update_gsheet_columns(df):
    """Updates the gsheet using the computed DataFrame

    Parameters
    ----------
        df : DataFrame
            DataFrame that is the result of the webscrapping operations
    """
    # Get the gsheet
    sheet = get_gsheet()

    # Get the prices as a list
    list_precios_usd = df["Precio USD"].to_list()
    list_precios_ars = df["Precio ARS"].to_list()

    # Calculate the last gsheet row with data
    last_row_index = str(len(list_precios_usd) + 1)

    # Get the cels to update in gsheet
    cell_list_usd = sheet.range("C2:C" + last_row_index)
    cell_list_ars = sheet.range("P2:P" + last_row_index)

    # Relate the prices with the corresponding cell
    for i, cell in enumerate(cell_list_usd):
        cell.value = list_precios_usd[i]

    for i, cell in enumerate(cell_list_ars):
        cell.value = list_precios_ars[i]

    # Update the prices in batch to avoid an excess in the use of the API
    sheet.update_cells(cell_list_usd)
    sheet.update_cells(cell_list_ars)
