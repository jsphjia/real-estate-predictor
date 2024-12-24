import webScrape as ws
import dataProcessing as dp

def get_data(city, state):
    # create initial search link
    # sale_url = "https://www.zillow.com/"+city+"-"+state
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
    ws.scrape_town(0, sold_url, city, True) # for sold houses

    print("done scrapping homes in " + city + ", " + state + "...")
    print("start scrapping home details in " + city + ", " + state + "...")

    # scrape for house details
    # scrape_details(city, False) # for on sale houses
    ws.scrape_details(city, True) # for sold houses

    print("done scrapping home details in " + city + ", " + state + "...")
    # ws.to_spreadsheet(city)
    return

def main():
    # ask for location
    loc = input("Enter a city and state abreviation (city,state): ")
    sep = loc.find(',')
    city = loc[:sep]
    state = loc[sep+1:]

    # import the data
    get_data(city, state)
    dp.import_data(city)
    return

if __name__ == "__main__":
    main()