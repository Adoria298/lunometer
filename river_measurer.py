#River Measurer
import urllib.request, json, csv, os

#deal with JSON
def get_json_data(json_url):
    """
    Gets data in the JSON format from the government URL provided (json_url), 
    formats it to remove government extras ["@context",  "meta", "@id", 
    "measure"].
    """
    #download file and reads into program as variable data
    with urllib.request.urlopen(json_url) as url:
        data = json.loads(url.read().decode())

    #deletes unnecessary info
    del data["@context"]
    del data["meta"]
    for item in data["items"]: #data["items"] is a list of dictionaries
        del item["@id"]
        del item["measure"]
    
    #returns the completely formatted JSON
    return data

#convert to csv
def convert_to_csv(output_file, data):
    """
    Converts government data to a csv file (headers = ['dateTime', 'value'], 
    assumes path doesn"t exist already.
    """
    with open(output_file, mode="w") as csv_file:
        #prep work
        fieldnames = ["dateTime", "value"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        #hard work
        writer.writerows(data["items"])

            
    
def main():              
    data = get_json_data("https://environment.data.gov.uk/flood-monitoring/id"
    + "/measures/724629-level-stage-i-15_min-m/readings?_sorted&_limit=500")
    convert_to_csv("caton_readings.csv", data)

if __name__ == "__main__":
    main()