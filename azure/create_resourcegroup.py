import sys
sys.path.append('../')
import os, logging, argparse
from config import init_log

#Azure SDK
from azure.identity import AzureCliCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.resource import ResourceManagementClient

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-s", "--subscription", required=True, help="subscription id")
    parser.add_argument("-n", "--rgname", required=True, help="resource group name")
    parser.add_argument("-l", "--location", required=True, help="location")
    args = parser.parse_args()
    return args

def main():
    #Read arguments and logging initialization
    args = parser()
    init_log(verbose=args.verbose)

    #Validate location
    logging.info("Validating Location... \'{0}\'".format(args.location))
    credential = AzureCliCredential()
    subscription_client = SubscriptionClient(credential)
    locations = subscription_client.subscriptions.list_locations(args.subscription)
    valid_location = False
    for location in locations:
        if location.name == args.location:
            logging.debug("Valid Location \'{0}\'".format(args.location))
            valid_location = True
            break
    if not valid_location:
        logging.error("Location \'{0}\' not found".format(args.location))
        exit(1)
    
    #Creation Resource Group
    logging.info("Creating Resource Group... \'{0}\'".format(args.rgname))
    resource_client = ResourceManagementClient(credential, subscription_id)
    rg_result = resource_client.resource_groups.create_or_update(args.rgname,{"location": args.location})
    logging.info("Resource Group Successfully Created ")

if __name__ == "__main__":
    main()
