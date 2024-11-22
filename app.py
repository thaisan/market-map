from flask import Flask, render_template, request
import pandas as pd
import market_mapper as mm

app = Flask(__name__)

def convert_sheet_url_to_csv(sheet_url):
    # Convert the Google Sheets URL to a CSV export URL
    # Example input: https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=0
    # Example output: https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/export?format=csv
    
    # Extract spreadsheet ID
    start = sheet_url.find('/d/') + 3
    end = sheet_url.find('/', start)
    if end == -1:
        end = sheet_url.find('?', start)
    if end == -1:
        end = sheet_url.find('#', start)
    if end == -1:
        end = len(sheet_url)
    
    spreadsheet_id = sheet_url[start:end]
    csv_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv'
    return csv_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sheet_url = request.form['sheet_url']
        try:
            csv_url = convert_sheet_url_to_csv(sheet_url)

            # Read the CSV file
            df = pd.read_csv(csv_url, sep=',', names=['Company Name', 'URL', 'Category'])
            mm.generate_market_map(df)
            with open('output/market_map.html', 'r') as f:
                return f.read()
        except Exception as e:
            return f'Error: {str(e)}'
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)