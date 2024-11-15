import pandas as pd
import os
from urllib.request import urlretrieve
from pathlib import Path

def remove_http_from_url(url):
    # Remove http:// or https:// from the beginning of the URL
    if url.startswith('http://'):
        return url[7:]
    elif url.startswith('https://'):
        return url[8:]
    return url

def add_http_to_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'http://' + url
    return url

def generate_market_map():
    # Create necessary directories
    os.makedirs('output', exist_ok=True)

    # Read templates
    template_dir = Path('templates')
    with open(template_dir / 'template.html', 'r') as f:
        html_template = f.read()
    
    with open(template_dir / 'style.css', 'r') as f:
        css_content = f.read()

    # Generate categories HTML
    categories_html = ''
    for category, group in categories:
        companies_html = ''
        for _, row in group.iterrows():
            company_name = row['Company Name']
            company_url = remove_http_from_url(row['URL'])
            
            token = "pk_E47o-25SS6GVpDUMRcyD7Q" # logo.dev token
            logo_path = f"https://img.logo.dev/{company_url}?token={token}"
            logo_html = f"<img src='{logo_path}'>"

            companies_html += f'''
                <div class="company">
                    <div class="company-logo-container">
                        <a href="{add_http_to_url(company_url)}">
                            {logo_html}
                        </a>
                    </div>
                    <div class="company-name">{company_name}</div>
                </div>
            '''

        categories_html += f'''
            <div class="category">
                <div class="category-title">{category}</div>
                <div class="companies">
                    {companies_html}
                </div>
            </div>
        '''

    # Generate final HTML
    title = 'GenAI Prototyping Tools Market Map'
    final_html = html_template.replace('{{title}}', title)
    final_html = final_html.replace('{{categories}}', categories_html)

    # Save the files
    with open('output/market_map.html', 'w') as f:
        f.write(final_html)
    
    with open('output/style.css', 'w') as f:
        f.write(css_content)

# Read the CSV file
df = pd.read_csv('data.csv', sep=',', names=['Company Name', 'URL', 'Category'])

# Group by category
categories = df.groupby('Category')

# Generate the market map
generate_market_map()