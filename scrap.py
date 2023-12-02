from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

options = Options()
options.add_experimental_option("detach", True)

def scrape_website(url):
    # Set up the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Open the website
        driver.get(url)
        for r in range(0,1000):
            scroll_to_bottom(driver)
        items = [
                'Furnace','Sleeping Bag','Semi-Automatic Rifle'
            "Sheet Metal Door", "Metal Chest Plate", "Metal Facemask", "Burlap Trousers",
            "Burlap Shirt", "Road Sign Kilt", "Road Sign Jacket", "Coffee Can Helmet",
            "Hoodie", "Pants", "Garage Door", "Hatchet", "Pickaxe", "LR-300 Assault Rifle",
            "Pump Shotgun", "Crossbow", "Double Barrel Shotgun", "Bolt Action Rifle",
            "MP5A4", "Revolver", "Large Wood Box", "Boots", "Roadsign Gloves", "Thompson",
            "Hunting Bow", "Hide Poncho", "Bandana Mask", "Wood Storage Box", "L96 Rifle",
            "Armored Door", "Concrete Barricade", "Wooden Door", "Rug", "Fridge",
            "Python Revolver", "Salvaged Sword", "Locker", "Wood Double Door", "Custom SMG",
            "Satchel Charge", "Sheet Metal Double Door", "Rock", "Wide Weapon Rack",
            "Jacket", "M39 Rifle", "Jackhammer", "Bone Club", "M249", "Semi-Automatic Pistol",
            "Vending Machine", "Hazmat Suit", "Rocket Launcher", "Boonie Hat", "Eoka Pistol",
            "Baseball Cap", "Hammer", "Hide Boots", "Riot Helmet", "Hide Vest", "Hide Pants",
            "Improvised Balaclava", "Stone Hatchet", "Stone Pickaxe", "Armored Double Door",
            "Burlap Headwrap", "Burlap Shoes", "Bone Helmet", "Rug Bear Skin", "T-Shirt",
            "Bucket Helmet", "Waterpipe Shotgun", "Bone Knife", "Snowman Helmet",
            "Water Purifier", "Shorts", "Salvaged Icepick", "Longsword", "Combat Knife",
            "Snow Jacket", "Bunny Hat", "Leather Gloves", "Table", "Miners Hat", "Shirt",
            "Beenie Hat", "Tank Top","Acoustic Guitar","Chair"
        ]
        wrappah_div = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]")

        # Find all the a tags under the wrappah div
        a_tags = wrappah_div.find_elements(By.TAG_NAME, 'a')
        
        # Extract and print the data-item and data-group attributes of each a tag
        for each in items:
            data_list = []
            for a in a_tags:
                # Extract data-item from the current 'a' tag
                data_item = a.get_attribute('data-item')
                item_name = a.text
                # Click on the current 'a' tag to navigate inside
                if data_item==each:
                    a.click()

                    try:
                        # Wait for the element to be present inside the 'a' tag
                        data_group_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="right-column"]/div[1]/table/tbody/tr[4]/td[2]/a'))
                        )

                        item_name_element = driver.find_element(By.XPATH, '//*[@id="left-column"]/div[1]/div[1]/h1')
                        item_name = item_name_element.text

                        # Inside the 'a' tag, get data-group from the specified XPath
                        data_group = data_group_element.text

                        data_list.append((item_name, f'{data_group},'))
                    
                    except Exception as e:
                        print(f"Error for {each}: {str(e)}")
                        print(f"Data group element not found for {each}. Skipping...")

                    # Go back to the main page
                    driver.back()
                    #scroll_to_bottom(driver)

            # Save the data to a CSV file
            save_to_csv(data_list,each)

    finally:
        # Close the browser window
        driver.quit()

def scroll_to_bottom(driver):
    # Scroll to the bottom of the page using JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
def save_to_csv(data_list, file_name):
    # Specify the CSV file path
    csv_file_path = f'./skins/{file_name}.csv'

    # Write data to CSV file with utf-8 encoding
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        csv_writer.writerow(['data-item', 'data-group'])  # Write header
        csv_writer.writerows(data_list)

if __name__ == "__main__":
    # Replace 'your_website_url' with the actual URL of the website you want to scrape
    website_url = 'https://rustlabs.com/skins'
    scrape_website(website_url)

