from hotel import Hotel

class HotelsService:
    def __init__(self, hotels: dict[(int, int), Hotel] = {}):
        self.hotels = hotels # (hotel_id, destination_id) -> merged_hotel: Hotel
    
    def merge_and_save(self, hotels: dict[(int, int), list[Hotel]]) -> dict[(int, int), Hotel]:
        '''convert dict((hotel_id, destination_id) -> [Hotel]) to dict((hotel_id, destination_id) -> merged_hotel)'''      
        for id_pair, hotel_list in hotels.items():
            hotel = hotel_list[0]
            for i in range(1, len(hotel_list)):
                hotel.merge(hotel_list[i])

            # save
            self.hotels[id_pair] = hotel
        
        return self.hotels

    def find(self, hotel_ids: set | list, destination_ids: set | list) -> list[Hotel]:
        '''find hotels by hotel_ids and/or destination_ids
        if hotel_ids or destination_ids is None, return all hotels'''
        res = []
        for (hotel_id, destination_id), hotel in self.hotels.items():            
            if hotel_ids and hotel_id not in hotel_ids:
                continue
            elif destination_ids and destination_id not in destination_ids:
                continue
            
            res.append(hotel.to_dict())
        
        return res
    