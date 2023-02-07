import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

def processData(file_content):
    logger = logging.getLogger("assignment2")
    lines = file_content.strip().split("\n")[1:]

    data = {}
    for linenum, line in enumerate(lines, start=2):
        id, name, birthday = line.split(",")
        id = int(id)
        try:    
            day, month, year = birthday.split("/")                  #split birthday - 17/09/1997 to 17 9 1997
            day, month, year = int(day), int(month), int(year)      #convert strings to numbers
            birthday = datetime.datetime(year, month, day)          #create datetime
        except:
            logger.error(f"Error processing line #{linenum} for ID #{id}")
        else:
            data[id] = (name, birthday)
    return data



def displayPerson(id, personData):
    if id in personData:
        print(f"Person #{id} is {personData[id][0]} with a birthday of {personData[id][1]:%Y-%m-%d}")
    else:
        print("No user found with that id")

def main(url):
    print(f"Running main with URL = {url}...")
    try:
        csvData = downloadData(url)
    except:
        print("Error downloading data, exiting.")
        return

    logging.basicConfig(filename="errors.log")
    logging.getLogger("assignment2")

    personData = processData(csvData)

    while True:
        id = int(input("Enter person ID (negative ID or 0 ends program): "))
        if id <= 0:
            break
        displayPerson(id, personData)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)