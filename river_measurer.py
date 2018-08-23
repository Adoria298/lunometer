#River Measurer
import urllib.request, json, csv, os

#deal with JSON
def get_json_data(json_url):
    """
    Gets data in the JSON format from the government URL provided (json_url), 
    formats it to remove government extras ["@context",  "meta", "@id", 
    "measure"].
    """
    print("Getting data from the web... ")
    #download file and reads into program as variable data
    with urllib.request.urlopen(json_url) as url:
        data = json.loads(url.read().decode())

    print("Formating data... ")
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
    Converts government data to a csv file (headers = ['dateTime', 'value'].
    Attemps to prevent duplicates.
    """
    #used twice
    fieldnames = ["dateTime", "value"]

    # double checks and appends existing data
    if os.path.exists(output_file): 
        print("Comparing data to already existing data... ")
        with open(output_file, mode='r') as csv_file:
            existing_data = list(csv.DictReader(csv_file))
            #its a list of dicts, not a dict
            #check
            line_count = 0
            for erow in existing_data:
                if line_count == 0:
                    continue
                    #purge clones
                for drow in data["items"]:
                    if erow[fieldnames[0]] == drow[fieldnames[0]]:
                        existing_data.pop(line_count)                         
                #remaining data
                data["items"].append(erow)
                

    with open(output_file, mode="w") as csv_file:
        print(f"Saving data to {output_file}... ")
        #prep work
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        #hard work
        writer.writerows(data["items"])
      
    
def main(): 
    try:            
        data = get_json_data("https://environment.data.gov.uk/flood-monitoring/id"
        + "/measures/724629-level-stage-i-15_min-m/readings?_sorted&_limit=500")
        convert_to_csv("caton_readings.csv", data)
        print("Finished.")
    except Exception as e:
        print("An error occurred; it is described below.")
        print(e)
    finally: 
        input("Press enter to exit.")

if __name__ == "__main__":
    main()