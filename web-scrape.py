import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_town(total_homes, url, city_name, isSold):
    # user agents
    header = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

    # scrape initial url for links to listed homes
    sale_page = requests.get(url, headers=header)
    # print(sale_page) # confirm status 200

    # parse the scraped result
    parsed = BeautifulSoup(sale_page.text, 'html.parser')

    # NOT NEEDED IN FINAL RESULT
    # storing in a txt file to check
    # f = open("results.txt", "w")
    # f.write(parsed.prettify())

    # finding the one line with all houses
    sale_homes = parsed.find('script', id='__NEXT_DATA__')
    homes_listed = sale_homes.string
    homes_this_page = homes_listed.count("detailUrl")
    total_homes += homes_this_page
    # print(total_homes)

    # NOT NEEDED FOR FINAL RESULT
    # storing that one line in a txt file
    if not isSold:
        file_name = city_name + ".txt"
    else:
        file_name = city_name + "-sold.txt"
    h = open(file_name, "a")
    for x in range(homes_this_page):
        start = homes_listed.find("detailUrl")
        end = homes_listed.find("statusType")
        h.write(homes_listed[start+12:end-4])
        h.write("\n")
        homes_listed = homes_listed[end+1:]
    h.close()

    # check to see if there are more pages of results
    # find the right arrow button and see if it is disabled
    # need to check if there are arrow buttons (if only 1 page, there is no arrow buttons)
    arrow_buttons = parsed.find_all('a', href=True, title=True)
    next_page = [button['href'] for button in arrow_buttons if (button['title'] == "Next page" and button['aria-disabled'] == "false")]
    if len(next_page) == 0:
        return
    next_url = "https://www.zillow.com" + next_page[0]
    # print(next_url)
    scrape_town(total_homes, next_url, city_name, isSold)
    return

def scrape_details(city, isSold):
    # get the correct file name
    if not isSold:
        details_file_name = city + ".txt"
    else: 
        details_file_name = city + "-sold.txt"
    details_file = open(details_file_name, "r")

    # user agents
    header = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

    # open new file to store info
    details_csv_name = city + "-details.csv"
    details_csv = open(details_csv_name, "a")

    # iterate through each detailUrl link
    for line in details_file:
        # send http request
        current_details = requests.get(line, headers=header)
        parsed_details = BeautifulSoup(current_details.text, 'html.parser')
        # print(current_details) # confirm status 200

        if isSold:
            # filter to the relevant line of code
            info = parsed_details.find('script', id='__NEXT_DATA__')
            info_string = info.string
            
            # add bedroom and bathroom counts
            bd_start = info_string.find("bedrooms")
            br_start = info_string.find("bathrooms")
            bd_end = br_start
            br_end = info_string.find("price")
            # details_csv.write(info_string[bd_start+11:bd_end-3] + "," + info_string[br_start+12:br_end-3] + ",")

            # add square footage and land area
            sf_start = info_string.find("livingAreaValue")
            sf_end = info_string.find("livingAreaUnits")
            area_start = info_string.find("lotSize")
            area_end = info_string.find("lotArea")
            # details_csv.write(info_string[sf_start+18:sf_end-3] + "," + info_string[area_start+10:area_end-3] + ",")

            # if sold, get most recent sold price, its original listing price, days in between
            # if on sale, get current listing price and last sold price and date
            all_pr_start = info_string.find('"priceHistory')
            tmp_info_string = info_string[all_pr_start+15:]
            sold_date_start = tmp_info_string.find("date")
            sold_date_end = tmp_info_string.find("time")
            sold_pr_start = tmp_info_string.find("price")
            sold_pr_end = tmp_info_string.find("pricePer")

            # enter all info to the csv file
            curr_home_info = info_string[bd_start+11:bd_end-3] + "," + info_string[br_start+12:br_end-3] + "," + info_string[sf_start+18:sf_end-3] + "," + info_string[area_start+10:area_end-3] + "," + tmp_info_string[sold_date_start+9:sold_date_end-5] + "," + tmp_info_string[sold_pr_start+8:sold_pr_end-3] + "\n"
            if len(curr_home_info) <= 75:
                details_csv.write(curr_home_info)
            # details_csv.write(tmp_info_string[sold_date_start+9:sold_date_end-5] + "," + tmp_info_string[sold_pr_start+8:sold_pr_end-3] + "\n")

        else:
            continue

    return

def to_spreadsheet(city):
    input_file_name = city + "-details.csv"
    file = pd.read_csv(input_file_name)
    output_file_name = city + "-details.xlsx"
    with pd.ExcelWriter('/Users/josephjia/Downloads/test_data.xlsx') as writer:
        file.to_excel(writer, sheet_name = 'Sheet1')
    return

def main():
    # ask for location
    loc = input("Enter a city and state abreviation (city,state): ")
    sep = loc.find(',')
    city = loc[:sep]
    state = loc[sep+1:]

    # create initial search link
    sale_url = "https://www.zillow.com/"+city+"-"+state
    sold_url = "https://www.zillow.com/"+city+"-"+state+"/sold"

    # clear text files if they exist
    sold_file_name = city + "-sold.txt"
    details_file_name = city + "-details.csv"
    sold_file = open(sold_file_name, "w")
    details_file = open(details_file_name, "w")
    sold_file.close()
    details_file.close()

    print("start scrapping homes in " + city + ", " + state + "...")

    # scrape for all houses
    # scrape_town(sale_url, city, False) # for on sale houses
    scrape_town(0, sold_url, city, True) # for sold houses

    print("done scrapping homes in " + city + ", " + state + "...")
    print("start scrapping home details in " + city + ", " + state + "...")

    # scrape for house details
    # scrape_details(city, False) # for on sale houses
    scrape_details(city, True) # for sold houses

    print("done scrapping home details in " + city + ", " + state + "...")
    to_spreadsheet(city)
    return

if __name__ == "__main__":
    main()