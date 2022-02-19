import sys
sys.path.append('../')
import os, logging, argparse
import json
from config import init_log

#Azure SDK
from azure.identity import AzureCliCredential
from azure.mgmt.subscription import SubscriptionClient

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-s", "--subscription", required=True, help="subscription id")
    args = parser.parse_args()
    return args

def main():
    #Read arguments and logging initialization
    args = parser()
    init_log(verbose=args.verbose)

    #Get Locations
    logging.info("Getting Locations from Azure")
    credential = AzureCliCredential()
    subscription_client = SubscriptionClient(credential)
    locations = subscription_client.subscriptions.list_locations(args.subscription)
    locations_json = []
    for location in locations:
        locations_json.append({'name':location.display_name,'value':location.name})
    locations_json = json.dumps(locations_json, sort_keys=True, indent=4)

    #Print in file
    logging.info("Saving to file data/locations.json")
    f = open("data/locations.json", "w")
    f.write(str(locations_json))
    f.close()
    logging.info("Successfully saved")

if __name__ == "__main__":
    main()
