import argparse
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# URLs
URLS = {
    'characters': 'https://brotato.wiki.spellsandguns.com/Characters',
    'weapons': 'https://brotato.wiki.spellsandguns.com/Weapons',
    'items': 'https://brotato.wiki.spellsandguns.com/Items',
}

# Index ranges for each section
INDEXES = {
    'characters': [3, 66],
    'weapons': [-1, 76],
    'items': [-1, 224]
}

# Prefixes for filenames
PREFIXES = {
    'characters': 'c',
    'weapons': 'w',
    'items': 'i'
}

# Create Selenium driver
def create_driver():
    """ Creates and configures Selenium WebDriver. """
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run without GUI
    chrome_options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=chrome_options)

# Function to parse a section and take screenshots
def parse_section(driver, section, url, output_dir):
    """ Parses a given section (Characters, Weapons, Items) and saves row screenshots. """
    print(f'Parsing: {url}')
    driver.get(url)
    time.sleep(3)  # Wait for page to load

    os.makedirs(output_dir, exist_ok=True)

    elements = driver.find_elements(By.XPATH, "//table[contains(@class, 'wikitable')]/tbody/tr")

    progress = len(elements)
    min_i, max_i = INDEXES[section]
    prefix = PREFIXES[section]

    for index, element in enumerate(elements):
        if min_i < index < max_i:  # Filtering range
            filepath = f'{output_dir}/{prefix}_{index-min_i-1}.png'
            element.screenshot(filepath)
            print(f'Saved: {filepath} ({index}/{progress})')

# Main function to handle arguments
def main():
    parser = argparse.ArgumentParser(description='Parse Brotato wiki pages and take screenshots.')
    parser.add_argument('--section', choices=['characters', 'weapons', 'items', 'all'], default='all',
                        help='Choose section to parse or "all" for everything (default: all)')

    args = parser.parse_args()

    driver = create_driver()

    if args.section == 'all':
        for section, url in URLS.items():
            output_dir = f'screenshots/{section}'
            parse_section(driver, section, url, output_dir)
    else:
        output_dir = f'screenshots/{args.section}'
        parse_section(driver, args.section, URLS[args.section], output_dir)

    driver.quit()

if __name__ == '__main__':
    main()
