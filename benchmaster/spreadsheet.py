#!/usr/bin/python3

import gspread
from google.oauth2.service_account import Credentials



def connect(credentials_file):
    """ Connect to the google API using the credentials in the file specified.
        We return a connection on which operations can be performed. """

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(credentials_file, scopes=scope)
    return gspread.authorize(credentials)
    


def create(gconn, sheet_name, accounts):
    """ Creates a spreadsheet on the google connection with the given name, and then shares it with 
        the accounts specified (so that you can access it with your normal google docs account: something
        like ['harry@softiron.com']). 
        We return the spreadsheet. """
    
    sheet = gconn.create(sheet_name)

    for a in accounts:
        sheet.share(a, perm_type='user', role='writer')

    return sheet;


 
def open(gconn, sheet_name):
    """ Open an existing sheet on the google connection. """

    try:
        return gconn.open(sheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        return None



def set_columns(sheet, columns):
    """ Sets the column titles """
    ws = sheet.get_worksheet(0)
    ws.update('A1', [columns], value_input_option="RAW")



def append_row(sheet, values):
    """ Appends a row of values (one for each of the columns we provided to set_columns. """
    ws = sheet.get_worksheet(0)

    # The 'USER_ENTERED' flag means that things like dates and times will be picked up as such by the spreadsheet.
    # If we used the default value (or 'RAW') it would treat dates as strings.
    ws.append_row(values, value_input_option='USER_ENTERED')
    
