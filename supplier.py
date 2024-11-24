import requests

from hotel import Hotel, Location, ImageLink, Amenities

class BaseSupplier:
    def endpoint():
        '''URL to fetch supplier data'''

    def parse(obj: dict) -> Hotel:
        '''Parse supplier-provided data into Hotel object'''

    def fetch(self) -> list[Hotel]:
        url = self.endpoint()
        resp = requests.get(url)
        
        return [self.parse(dto) for dto in resp.json()]

class Acme(BaseSupplier):
    @staticmethod
    def endpoint():
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme'

    @staticmethod
    def parse(dto: dict) -> Hotel:
        return Hotel(
            id=dto.get('Id'),
            destination_id=dto.get('DestinationId'),
            name=dto.get('Name'),
            description=(dto.get('Description') or '').strip(),
            location=Location(
                lat=dto.get('Latitude'),
                lng=dto.get('Longitude'),
                address=(dto.get('Address') or '').strip(),
                city=dto.get('City'),
                country=dto.get('Country'),
                postcode=dto.get('PostalCode')
            ),
            amenities=Amenities(
                general=(dto.get('Facilities') or [])
            ),
        )

class Paperflies(BaseSupplier):
    @staticmethod
    def endpoint():
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies'

    @staticmethod
    def parse(dto: dict) -> Hotel: 
        return Hotel(
            id=dto.get('hotel_id'),
            destination_id=dto.get('destination_id'),
            name=dto.get('hotel_name'),
            description=(dto.get('details') or '').strip(),
            location=Location(
                lat=None,
                lng=None,
                address=(dto['location']['address'] or '').strip(),
                country=dto['location']['country'],
            ),
            amenities=Amenities(
                general=dto['amenities']['general'],
                room=dto['amenities']['room']
            ),
            images=dict({
                image: [
                    ImageLink(
                        link=link['link'],
                        description=link['caption']
                    ).to_dict() for link in links
                ]
                for image, links in (dto.get('images') or {}).items()
            }),
            booking_conditions=dto.get('booking_conditions'),
        )

class Patagonia(BaseSupplier):
    @staticmethod
    def endpoint():
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia'

    @staticmethod
    def parse(dto: dict) -> Hotel:
        return Hotel(
            id=dto.get('id'),
            destination_id=dto.get('destination'),
            name=dto.get('name'),
            description=(dto.get('info') or '').strip(),
            location=Location(
                lat=dto.get('lat'),
                lng=dto.get('lng'),
                address=(dto.get('address') or '').strip(),
            ),
            amenities=Amenities(
                general=(dto.get('amenities') or [])
            ),
            images=dict({
                image: [
                    ImageLink(
                        link=link['url'],
                        description=link['description']
                    ).to_dict() for link in links
                ]
                for image, links in (dto.get('images') or {}).items()
            }),
        )
