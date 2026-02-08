"""
Hotel Search Tool using Model Context Protocol (MCP)
Mock implementation for hotel search (can be replaced with real API)
"""
from typing import List, Dict, Any
import random


class HotelTool:
    """Tool for searching hotel accommodations"""
    
    def __init__(self):
        # Mock hotel chains
        self.hotel_chains = [
            "Marriott", "Hilton", "Hyatt", "Radisson", "ITC Hotels",
            "Taj Hotels", "Oberoi Hotels", "Holiday Inn", "Sheraton",
            "The Leela", "AccorHotels", "Four Seasons"
        ]
        
        self.hotel_types = [
            "Hotel", "Resort", "Hotel & Spa", "Boutique Hotel", "Business Hotel"
        ]
        
        self.amenities_pool = [
            "Free WiFi", "Swimming Pool", "Fitness Center", "Spa",
            "Restaurant", "Bar", "Room Service", "Airport Shuttle",
            "Business Center", "Parking", "Laundry Service", "Concierge"
        ]
    
    def search_hotels(
        self,
        destination: str,
        check_in: str,
        check_out: str,
        guests: int = 2,
        min_rating: float = 3.0
    ) -> List[Dict[str, Any]]:
        """
        Search for hotel options
        
        Args:
            destination: Destination city
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)
            guests: Number of guests
            min_rating: Minimum hotel rating
            
        Returns:
            List of hotel options
        """
        num_hotels = random.randint(8, 15)
        hotels = []
        
        for i in range(num_hotels):
            rating = random.uniform(max(min_rating, 3.0), 5.0)
            
            # Generate hotel name
            chain = random.choice(self.hotel_chains)
            hotel_type = random.choice(self.hotel_types)
            hotel_name = f"{chain} {destination} {hotel_type}"
            
            # Base price varies by rating
            base_price_per_night = 50 + (rating * 40) + random.randint(-20, 50)
            
            # Room types
            room_types = self._generate_room_types(base_price_per_night)
            
            # Amenities (more for higher-rated hotels)
            num_amenities = int(rating * 2) + random.randint(3, 6)
            amenities = random.sample(self.amenities_pool, min(num_amenities, len(self.amenities_pool)))
            
            hotel = {
                'name': hotel_name,
                'rating': round(rating, 1),
                'address': f"{random.randint(1, 999)} {destination} Street, {destination}",
                'distance_from_center': round(random.uniform(0.5, 10), 1),
                'room_types': room_types,
                'amenities': amenities,
                'check_in': check_in,
                'check_out': check_out,
                'guest_rating': round(random.uniform(7.0, 9.8), 1),
                'num_reviews': random.randint(50, 2000)
            }
            
            hotels.append(hotel)
        
        # Sort by rating
        hotels.sort(key=lambda x: x['rating'], reverse=True)
        
        return hotels
    
    def _generate_room_types(self, base_price: float) -> List[Dict[str, Any]]:
        """Generate different room type options"""
        room_types = []
        
        # Standard Room
        room_types.append({
            'type': 'Standard Room',
            'price_per_night': round(base_price, 2),
            'max_guests': 2,
            'bed_type': 'Queen Bed',
            'size_sqm': random.randint(20, 30)
        })
        
        # Deluxe Room
        room_types.append({
            'type': 'Deluxe Room',
            'price_per_night': round(base_price * 1.3, 2),
            'max_guests': 2,
            'bed_type': 'King Bed',
            'size_sqm': random.randint(30, 40)
        })
        
        # Suite (not always available)
        if random.random() > 0.3:
            room_types.append({
                'type': 'Suite',
                'price_per_night': round(base_price * 2, 2),
                'max_guests': 4,
                'bed_type': 'King Bed + Sofa Bed',
                'size_sqm': random.randint(45, 70)
            })
        
        return room_types
    
    def get_best_hotels(
        self,
        destination: str,
        check_in: str,
        check_out: str,
        guests: int = 2,
        num_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get the best hotel options
        
        Args:
            destination: Destination city
            check_in: Check-in date
            check_out: Check-out date
            guests: Number of guests
            num_results: Number of results to return
            
        Returns:
            List of best hotels
        """
        all_hotels = self.search_hotels(destination, check_in, check_out, guests)
        return all_hotels[:num_results]
    
    def format_hotel_info(self, hotel: Dict[str, Any]) -> str:
        """Format hotel information as a readable string"""
        info = f"**{hotel['name']}** ({'⭐' * int(hotel['rating'])})\n"
        info += f"  - Rating: {hotel['rating']}/5.0 (Guest Rating: {hotel['guest_rating']}/10)\n"
        info += f"  - Location: {hotel['distance_from_center']} km from city center\n"
        info += f"  - Room Options:\n"
        
        for room in hotel['room_types']:
            info += f"    • {room['type']}: ${room['price_per_night']:.2f}/night ({room['max_guests']} guests)\n"
        
        info += f"  - Amenities: {', '.join(hotel['amenities'][:5])}\n"
        
        return info
    
    def calculate_total_cost(
        self,
        hotel: Dict[str, Any],
        room_type: str,
        num_nights: int
    ) -> float:
        """Calculate total cost for a hotel stay"""
        for room in hotel['room_types']:
            if room['type'] == room_type:
                return room['price_per_night'] * num_nights
        
        # Default to first room type
        return hotel['room_types'][0]['price_per_night'] * num_nights
