import requests
import csv

# Function to get data from the API
def get_mp_data(id):
    url = f"https://api.sejm.gov.pl/sejm/term10/MP/{id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to save data to CSV
def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Main script to query the API and save the data
def main():
    all_data = []
    for id in range(1, 461):  # IDs range from 1 to 460
        mp_data = get_mp_data(id)
        if mp_data:
            all_data.append(mp_data)
    
    # Save to CSV file
    save_to_csv(all_data, '../csv/sejm_x_mps.csv')

# Run the script
main()
