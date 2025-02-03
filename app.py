import os.path
from webscraper import scrape_data
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Function for Google Sheets API Authentication
def authenticate_google_sheets():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

# Function to append data to the Google Sheet
def append_to_sheet(creds, sheet_id, data):
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Prepare the range (Append at the end of existing data)
        range_ = "Sheet1"
        body = {
            "values": data  # Data to be appended
        }

        # Append the data to the sheet
        result = (
            sheet.values()
            .append(spreadsheetId=sheet_id, range=range_, valueInputOption="RAW", body=body)
            .execute()
        )
        print(f"{result.get('updates').get('updatedCells')} cells appended.")
    except HttpError as err:
        print(f"An error occurred: {err}")

# Main function to authenticate and scrape, then append the data to the sheet
def main():
    creds = authenticate_google_sheets()
    sheet_id = "1RWHQLjdvOTtj62pF_rg0vIytzWzipZgGsavtFXEbuEg"
    
    # Scrape the data
    scraped_data = scrape_data(
        "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals",
        10,
        [0, 1, 2]  # Year, Winners, Score, Runners-up
    )
    
    # Append the scraped data to Google Sheets
    append_to_sheet(creds, sheet_id, scraped_data)

# Call the main function
if __name__ == "__main__":
    main()
