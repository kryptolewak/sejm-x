from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def scrape_page(driver, i):
    page_id = str(i).zfill(3)
    url = f"https://sejm.gov.pl/Sejm10.nsf/posel.xsp?id={page_id}&type=A"
    driver.get(url)

    # Wait for the AJAX-triggered element to be clickable and click it
    wait = WebDriverWait(driver, 10)
    ajax_element = wait.until(EC.element_to_be_clickable((By.ID, 'osw')))
    ajax_element.click()

    # Wait for the AJAX request to complete and the new element to appear
    pdf_link_element = wait.until(EC.presence_of_element_located((By.ID, 'view:_id1:_id2:facetMain:_id190:_id257:0:_id262')))
    pdf_link = pdf_link_element.get_attribute('href')

    return {
        "id": i,
        "oswp": pdf_link
    }

# Function to save data to CSV
def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    driver = webdriver.Chrome()
    all_data = []
    for i in range(1, 461):
        print(f"Scraping page ID: {i}")
        try:
            osw_data = scrape_page(driver, i)
            if osw_data:
                all_data.append(osw_data)
        except Exception as e:
            print(f"Error scraping page {i}: {e}")

    driver.quit()
    save_to_csv(all_data, '../csv/sejm_x_oswiadczenia_majatkowe_p.csv')

if __name__ == "__main__":
    main()
