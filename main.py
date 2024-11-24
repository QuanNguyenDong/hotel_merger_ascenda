import json
import argparse
from collections import defaultdict

from supplier import Acme, Paperflies, Patagonia
from hotel_service import HotelsService

def get_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    
    parser.add_argument("hotel_ids", type=str, help="Hotel IDs")
    parser.add_argument("destination_ids", type=str, help="Destination IDs")
    
    return parser

def fetch_hotels(hotel_ids: str, destination_ids: str) -> json:
    hotel_ids       = set() if hotel_ids == 'none' else set(hotel_ids.split(","))
    destination_ids = set() if destination_ids == 'none' else set({
        int(id) for id in destination_ids.split(",")
    })
    
    suppliers = [
        Acme(),
        Paperflies(),
        Patagonia(),
    ]

    # Fetch data from all suppliers
    all_supplier_data = defaultdict(list) # (hotel_id, destination_id) -> [Hotel]
    for supp in suppliers:
        for hotel in supp.fetch(): 
            all_supplier_data[(hotel.id, hotel.destination_id)].append(hotel)

    # Merge all the data and save it in-memory somewhere
    svc = HotelsService()
    svc.merge_and_save(all_supplier_data)
    
    merged_hotels = svc.find(hotel_ids, destination_ids)

    return json.dumps(merged_hotels, indent=4)
    
def main():
    args = get_args_parser().parse_args()
    
    hotel_ids       = args.hotel_ids
    destination_ids = args.destination_ids
    
    result = fetch_hotels(hotel_ids, destination_ids)
    print(result)
        
if __name__ == "__main__":
    main()