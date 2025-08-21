# Import modules that we will use. Please ensure all packages in requirements.txt are installed.
from bs4 import BeautifulSoup
import requests
import os
import csv

# Constants
STARTING_NUMBER = 422
LAST_NUMBER = 3782
BASE_PATH = os.getcwd()
DESCRIPTION_FOLDER = BASE_PATH + r"\Description"
KEYWORD_FILE = BASE_PATH + r"\keywords.txt"
CSV_FILE = BASE_PATH + r"\results.csv"
CSV_HEADERS = ["No.", "Link", "Upload Date", "Title", "Author", "Supervisor", "Pages", "Publish Date", "Subject", "Keywords"]

# Global variables
undergrad_only = True
keywords = []
file_count = 0


def create_description_folder(): # Should only need to run once, to create Description folder
    if not os.path.exists(DESCRIPTION_FOLDER):
        print("Creating Description Folder...")
        os.mkdir(DESCRIPTION_FOLDER)


def create_csv_file(): # Should only run once, to create results.csv file and its headers
    if not os.path.exists(CSV_FILE):
        print("Creating CSV File...")
        with open(CSV_FILE, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(CSV_HEADERS)


def create_keywords_file():  # Creates the keyword file, but the user needs to edit it
    if not os.path.exists(KEYWORD_FILE):
        with open(KEYWORD_FILE, 'w', newline='') as file:
            file.write("Please update this file in a text editor with a keyword on each new line.")
        return True
    return False


def get_keywords(): # To retrieve keyword list from keywords.txt
    try:
        print("Getting Keywords...")
        with open(KEYWORD_FILE, 'r') as f:
            for line in f:
                keywords.append(line.strip())
    except FileNotFoundError:
        print("Keywords file not found")


def search_keyword(cleaned_data):  # Searches for any keyword in all fields on the query
    for keyword in keywords:
        for data in cleaned_data:
            if keyword in data:
                if undergrad_only:
                    if cleaned_data[2] == "Undergraduate FYP":
                        return keyword
                else:
                    return keyword
    return None


def create_description_file(cleaned_data):  # Creates a description file to store the abstract of the query
    global file_count
    if len(cleaned_data) == 17:
        text = cleaned_data[5]
    else:
        text = "No Abstract/Description available for this file!"
    with open(DESCRIPTION_FOLDER + '/' + str(file_count) + ".txt", 'w', newline='', encoding="utf-8") as file:
        file.write(text)


def write_to_csv(cleaned_data, url):  # Writes the details of matching result to results.csv
    if len(cleaned_data) == 17:
        data_to_write = [file_count, url, cleaned_data[1], cleaned_data[3], cleaned_data[4],
                         cleaned_data[6], cleaned_data[9], cleaned_data[10], cleaned_data[15],
                         cleaned_data[16]]
    else:
        data_to_write = [file_count, url, cleaned_data[1], cleaned_data[3], cleaned_data[4], cleaned_data[5],
                         cleaned_data[8], cleaned_data[19], cleaned_data[14],
                         cleaned_data[15]]
    with open(CSV_FILE, 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_to_write)


def query_website(page_number):  # Retrieve the website and cleans data for other function
    global file_count
    url = f"https://library.apu.edu.my/apres/advanced-search/entry/{page_number}"
    website = requests.get(url)
    agent = BeautifulSoup(website.text, "html.parser")
    cleaned_data = []
    my_list = ""

    table = agent.find("table", attrs={"class": "gv-table-view-content"})
    datas = table.find_all('td')
    list_items = table.find_all('li')

    for list_item in list_items:
        if len(list_item.text) > 0:
            if len(my_list) > 0:
                my_list = my_list + ";" + list_item.text.strip('-\n')
            else:
                my_list = list_item.text.strip('-\n')

    for data in datas:
        if len(data.text) > 0:
            text = data.text.strip('\r\n\r')
            cleaned_data.append(text.strip('\r\n\r'))

    if len(cleaned_data) == 17:
        cleaned_data[15] = my_list
    else:
        cleaned_data[14] = my_list

    keyword = search_keyword(cleaned_data)

    if keyword is not None:
        print(f"Searching {page_number}... Keyword: \"{keyword}\" Found!")
        file_count += 1
        create_description_file(cleaned_data)
        write_to_csv(cleaned_data, url)
    else:
        print(f"Searching {page_number}... No Keyword Found!")


def main():  # Main function to select search parameter and error handling for rate-limits/timeouts
    global undergrad_only
    create_description_folder()
    create_csv_file()
    first_time = create_keywords_file()
    if first_time:
        print("Since this is your first time, edit the keywords.txt before you run this program again!")
        exit(0)
    else:
        get_keywords()

        print("Would you like to include all types of papers or only Undergraduate FYPs?")
        print("1) Only Undergraduate FYPs (Default)")
        print("2) Everything (Article, Book, Book Section, Monograph, Thesis, Diploma FYP, etc")
        print("")

        choice = int(input("Enter your choice: "))

        if choice == 2:
            undergrad_only = False
            print("Okay! Theses and other papers will be included in the search!")
        else:
            print("Okay! We will only search for undergraduate FYPs!")

        print("")

        print("Scanning through the library... Please wait for scan to finish before closing.")

        for i in range(STARTING_NUMBER, LAST_NUMBER):
            try:
                query_website(i)
            except AttributeError:
                print(f"Page {i} returned an error. Retrying to make sure...")
                try:
                    query_website(i)
                except AttributeError:
                    print(f"Page {i} most likely cannot be viewed by the public.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:  # Handles the program closing abruptly
        print("Closing...")