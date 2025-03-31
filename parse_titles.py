import argparse
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

# Prefixes for images
PREFIXES = {
    'characters': 'c',
    'weapons': 'w',
    'items': 'i'
}

# Starting Steam image ID
STEAM_ID_START = 40214553

# Problematic names that appear twice, causing shifts in Steam ID sequence
EXCEPTION_NAMES = {'Pacifist', 'Cryptid', 'Masochist', 'Hatchet', 'SMG', 'Compass', 'Coral(DLC)', 'Greek Fire',
                   'Little Muscley Dude', 'Lost Duck', 'Lucky Coin', 'Lure', 'Mastery', 'Medical Turret',
                   'Metal Detector', 'Nail'}


# Create Selenium driver
def create_driver():
    '''Creates and configures Selenium WebDriver.'''
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run without GUI
    chrome_options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=chrome_options)


# Function to parse names from a section, excluding header row
def parse_titles(driver, section, url):
    '''Extracts names from all relevant tables on the page in correct order.'''
    print(f'Parsing: {url}')
    driver.get(url)
    time.sleep(3)  # Wait for page to load

    names = []

    if section == 'characters':
        table_xpaths = ["(//table[contains(@class, 'wikitable')])[2]"]
    elif section == 'weapons':
        table_xpaths = ["(//table[contains(@class, 'wikitable')])[1]", "(//table[contains(@class, 'wikitable')])[2]"]
    else:
        table_xpaths = ["(//table[contains(@class, 'wikitable')])[1]"]

    for table_xpath in table_xpaths:
        rows = driver.find_elements(By.XPATH, f'{table_xpath}//tbody/tr[td]')
        for row in rows:
            try:
                cell = row.find_element(By.XPATH, './td[1]')
                name = cell.text.strip()
                if name:
                    names.append(name)
            except Exception:
                continue
    return names


# Function to generate guide text with image references
def generate_guide_text(section, names):
    '''Formats extracted names with corresponding image references for the Steam guide.'''
    prefix = PREFIXES[section]
    lines = []
    steam_id = STEAM_ID_START
    steam_id_map = {}  # To store correct mapping of names to IDs

    for i, name in enumerate(names):
        img_filename = f'{prefix}_{i}.png'

        steam_id_map[name] = steam_id

        img_tag = f'[previewimg={steam_id};sizeFull,floatLeft;{img_filename}][/previewimg]'
        lines.append(f'[h1] {name} [/h1]')
        lines.append(img_tag)

        if name in EXCEPTION_NAMES:
            steam_id += 2
        else:
            steam_id += 1

    return '\n'.join(lines)


# Main function
def main():
    parser = argparse.ArgumentParser(description='Parse Brotato wiki pages and extract names.')
    parser.add_argument('--section', choices=['characters', 'weapons', 'items', 'all'], default='items',
                        help='Choose section to parse or "all" for everything (default: all)')
    args = parser.parse_args()

    driver = create_driver()
    results = []

    if args.section == 'all':
        for section, url in URLS.items():
            names = parse_titles(driver, section, url)
            results.append(generate_guide_text(section, names))
    else:
        names = parse_titles(driver, args.section, URLS[args.section])
        results.append(generate_guide_text(args.section, names))

    driver.quit()
    print('\n\n'.join(results))


if __name__ == '__main__':
    main()
