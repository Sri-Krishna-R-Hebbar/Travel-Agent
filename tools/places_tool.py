"""
Places/Attractions Tool using Model Context Protocol (MCP)
Mock implementation for places and attractions (can be replaced with real API)
"""
from typing import List, Dict, Any
import random


class PlacesTool:
    """Tool for finding places of interest and attractions"""
    
    def __init__(self):
        # Common attraction types
        self.attraction_types = {
            'historical': ['Monument', 'Palace', 'Fort', 'Archaeological Site', 'Heritage Site'],
            'cultural': ['Museum', 'Art Gallery', 'Theater', 'Cultural Center', 'Temple'],
            'natural': ['Park', 'Garden', 'Lake', 'Beach', 'Viewpoint'],
            'entertainment': ['Amusement Park', 'Zoo', 'Aquarium', 'Shopping Mall', 'Market'],
            'religious': ['Temple', 'Church', 'Mosque', 'Monastery', 'Shrine']
        }
        
        # Activity types
        self.activity_types = [
            'Sightseeing', 'Photography', 'Walking Tour', 'Food Tour',
            'Shopping', 'Cultural Experience', 'Adventure', 'Relaxation'
        ]
    
    def search_places(
        self,
        destination: str,
        categories: List[str] = None,
        limit: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Search for places of interest
        
        Args:
            destination: Destination city
            categories: List of categories to filter by
            limit: Maximum number of results
            
        Returns:
            List of places
        """
        if not categories:
            categories = list(self.attraction_types.keys())
        
        places = []
        places_per_category = max(limit // len(categories), 2)
        
        for category in categories:
            category_places = self._generate_places_for_category(
                destination, category, places_per_category
            )
            places.extend(category_places)
        
        # Shuffle and limit results
        random.shuffle(places)
        return places[:limit]
    
    def _generate_places_for_category(
        self,
        destination: str,
        category: str,
        count: int
    ) -> List[Dict[str, Any]]:
        """Generate mock places for a category"""
        places = []
        attraction_subtypes = self.attraction_types.get(category, ['Attraction'])
        
        # Some famous landmarks for common destinations
        famous_places = self._get_famous_places(destination, category)
        
        for i in range(count):
            if i < len(famous_places):
                # Use famous place
                place_data = famous_places[i]
            else:
                # Generate generic place
                subtype = random.choice(attraction_subtypes)
                place_data = {
                    'name': f"{destination} {subtype} {i+1}",
                    'description': f"A beautiful {category} {subtype.lower()} in {destination}."
                }
            
            place = {
                'name': place_data['name'],
                'category': category,
                'type': random.choice(attraction_subtypes),
                'rating': round(random.uniform(3.8, 4.9), 1),
                'num_reviews': random.randint(100, 5000),
                'description': place_data['description'],
                'address': f"{random.randint(1, 999)} {destination} Road, {destination}",
                'estimated_visit_duration': random.choice(['1-2 hours', '2-3 hours', '3-4 hours', 'Half day', 'Full day']),
                'entry_fee': self._generate_entry_fee(),
                'best_time_to_visit': random.choice(['Morning', 'Afternoon', 'Evening', 'Anytime']),
                'activities': random.sample(self.activity_types, random.randint(2, 4))
            }
            
            places.append(place)
        
        return places
    
    def _get_famous_places(self, destination: str, category: str) -> List[Dict[str, str]]:
        """Get famous places for well-known destinations"""
        # Database of famous places (expandable)
        famous_db = {
            'Paris': {
                'historical': [
                    {'name': 'Eiffel Tower', 'description': 'Iconic iron lattice tower and symbol of Paris'},
                    {'name': 'Arc de Triomphe', 'description': 'Monumental arch honoring French military victories'},
                ],
                'cultural': [
                    {'name': 'Louvre Museum', 'description': "World's largest art museum and historic monument"},
                    {'name': 'Musée d\'Orsay', 'description': 'Museum featuring Impressionist and Post-Impressionist masterpieces'},
                ]
            },
            'London': {
                'historical': [
                    {'name': 'Tower of London', 'description': 'Historic castle and UNESCO World Heritage Site'},
                    {'name': 'Buckingham Palace', 'description': 'Official residence of the British monarch'},
                ],
                'cultural': [
                    {'name': 'British Museum', 'description': 'World-famous museum of human history and culture'},
                ]
            },
            'Tokyo': {
                'historical': [
                    {'name': 'Senso-ji Temple', 'description': 'Ancient Buddhist temple in Asakusa'},
                    {'name': 'Imperial Palace', 'description': 'Primary residence of the Emperor of Japan'},
                ],
                'cultural': [
                    {'name': 'Tokyo National Museum', 'description': 'Japan\'s oldest and largest museum'},
                ]
            },
            'New York': {
                'historical': [
                    {'name': 'Statue of Liberty', 'description': 'Iconic symbol of freedom and democracy'},
                    {'name': 'Empire State Building', 'description': 'Art Deco skyscraper and American cultural icon'},
                ]
            }
        }
        
        # Check if destination has famous places
        dest_key = destination.title()
        if dest_key in famous_db and category in famous_db[dest_key]:
            return famous_db[dest_key][category]
        
        return []
    
    def _generate_entry_fee(self) -> Dict[str, Any]:
        """Generate entry fee information"""
        is_free = random.random() < 0.3  # 30% chance of being free
        
        if is_free:
            return {'is_free': True, 'price': 0, 'currency': 'USD'}
        else:
            return {
                'is_free': False,
                'price': random.randint(5, 50),
                'currency': 'USD'
            }
    
    def get_top_attractions(
        self,
        destination: str,
        num_results: int = 10
    ) -> List[Dict[str, Any]]:
        """Get top-rated attractions"""
        all_places = self.search_places(destination, limit=20)
        
        # Sort by rating
        all_places.sort(key=lambda x: x['rating'], reverse=True)
        
        return all_places[:num_results]
    
    def format_place_info(self, place: Dict[str, Any]) -> str:
        """Format place information as a readable string"""
        fee_text = "Free entry" if place['entry_fee']['is_free'] else f"${place['entry_fee']['price']} entry fee"
        
        info = f"**{place['name']}** ({place['type']})\n"
        info += f"  - Rating: {place['rating']}/5.0 ({place['num_reviews']} reviews)\n"
        info += f"  - {place['description']}\n"
        info += f"  - Visit Duration: {place['estimated_visit_duration']}\n"
        info += f"  - {fee_text}\n"
        info += f"  - Best Time: {place['best_time_to_visit']}\n"
        
        return info
    
    def create_itinerary_suggestions(
        self,
        destination: str,
        num_days: int
    ) -> List[Dict[str, Any]]:
        """
        Create day-wise itinerary suggestions
        
        Args:
            destination: Destination city
            num_days: Number of days
            
        Returns:
            List of daily itineraries
        """
        all_places = self.search_places(destination, limit=num_days * 4)
        itinerary = []
        
        places_per_day = max(len(all_places) // num_days, 2)
        
        for day in range(num_days):
            start_idx = day * places_per_day
            end_idx = start_idx + places_per_day
            day_places = all_places[start_idx:end_idx]
            
            itinerary.append({
                'day': day + 1,
                'theme': self._get_day_theme(day, num_days),
                'places': day_places,
                'activities': self._suggest_activities(day_places)
            })
        
        return itinerary
    
    def _get_day_theme(self, day: int, total_days: int) -> str:
        """Get a theme for the day"""
        themes = [
            'Historical Exploration',
            'Cultural Immersion',
            'Natural Beauty',
            'Local Experiences',
            'Adventure & Entertainment',
            'Relaxation & Leisure',
            'Shopping & Cuisine'
        ]
        
        if day == 0:
            return 'Arrival & City Orientation'
        elif day == total_days - 1:
            return 'Final Day Highlights'
        else:
            return themes[day % len(themes)]
    
    def _suggest_activities(self, places: List[Dict[str, Any]]) -> List[str]:
        """Suggest activities based on places"""
        all_activities = set()
        for place in places:
            all_activities.update(place.get('activities', []))
        
        return list(all_activities)[:4]
