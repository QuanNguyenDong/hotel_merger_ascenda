import re
from dataclasses import dataclass, asdict, field

from utils import merge_str, merge_dict, merge_list

@dataclass
class ImageLink:
    link: str = ""
    description: str = ""
    
    def to_dict(self):
        return {
            key: val for key, val in asdict(self).items() if val
        }

class Amenities:
    def __init__(self, general: list[str] = [], room: list[str] = []):
        def process_str(words: str) -> str:
            '''lowercase, strip and split by capital letter/ space'''
            words.strip()
            words = re.findall(r'[A-Z][^A-Z\s]*|[^A-Z\s]+', words)
            word = " ".join(words)
            
            return word.lower()
        
        self.general = [process_str(word) for word in general]
        self.room    = [process_str(word) for word in room]

    def merge(self, amenities: 'Amenities'):
        self.general = merge_list(self.general, amenities.general)
        self.room    = merge_list(self.room, amenities.room)

    def to_dict(self):
        return {
            key: val for key, val in self.__dict__.items() if val
        }


@dataclass
class Location:
    lat: float
    lng: float
    address: str
    city: str = ""
    country: str = ""
    
    def merge(self, location: 'Location'):
        self.address = merge_str(self.address, location.address)
        self.city    = merge_str(self.city, location.city)
        self.country = merge_str(self.country, location.country)
    
    def to_dict(self):
        return {
            key: val for key, val in asdict(self).items() if val
        }
        
@dataclass
class Hotel:
    id: str
    destination_id: str
    name: str
    description: str
    location: Location
    amenities: Amenities
    images: dict[str, list] = field(default_factory=dict)
    booking_conditions: list[str] = field(default_factory=list)
    
    def merge(self, hotel: 'Hotel'):
        self.name = merge_str(self.name, hotel.name)
        self.description = merge_str(self.description, hotel.description)
        self.location.merge(hotel.location)
        self.amenities.merge(hotel.amenities)
        self.images = merge_dict(self.images, hotel.images)
        self.booking_conditions = merge_list(self.booking_conditions, hotel.booking_conditions)
        
    def to_dict(self):
        res = {
            key: val for key, val in asdict(self).items() if val
        }
        res["location"] = self.location.to_dict() # remove null values
        res["amenities"] = self.amenities.to_dict()
        
        return res
