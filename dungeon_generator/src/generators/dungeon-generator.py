"""
Dungeon generator for the dungeon generator application.

This module defines the DungeonGenerator class which generates complete
dungeons composed of multiple rooms.
"""

from src.models.dungeon import Dungeon
from .room_generator import RoomGenerator

class DungeonGenerator:
    """
    Generator for complete dungeons.
    
    This class uses a RoomGenerator to create individual rooms and
    combines them into a complete dungeon structure.
    """
    
    def __init__(self, use_custom_tables=True):
        """
        Initialize the DungeonGenerator.
        
        Args:
            use_custom_tables (bool, optional): Whether to use custom tables. 
                Defaults to True.
        """
        self.room_generator = RoomGenerator(use_custom_tables)
        
    def generate_dungeon(self, num_rooms=5, name="Random Dungeon"):
        """
        Generate a complete dungeon with the specified number of rooms.
        
        Args:
            num_rooms (int, optional): Number of rooms to generate. Defaults to 5.
            name (str, optional): Name of the dungeon. Defaults to "Random Dungeon".
            
        Returns:
            Dungeon: A generated dungeon with rooms.
        """
        dungeon = Dungeon(name)
        
        # Generate the specified number of rooms
        for _ in range(num_rooms):
            room = self.room_generator.generate_room()
            dungeon.add_room(room)
            
        # In a more advanced implementation, we might want to:
        # - Connect rooms logically
        # - Generate a dungeon layout
        # - Ensure all rooms are accessible
        # - Add special features to the dungeon as a whole
        
        return dungeon
        
    def generate_themed_dungeon(self, theme, num_rooms=5):
        """
        Generate a dungeon with a specific theme.
        
        Args:
            theme (str): The theme of the dungeon (e.g., "abandoned", "infested").
            num_rooms (int, optional): Number of rooms to generate. Defaults to 5.
            
        Returns:
            Dungeon: A generated dungeon with the specified theme.
        """
        # This is a placeholder for a more advanced feature
        # In a full implementation, this would adjust probabilities or
        # select specific tables based on the theme
        
        name = f"{theme.capitalize()} Dungeon"
        dungeon = self.generate_dungeon(num_rooms, name)
        dungeon.notes = f"This dungeon has a {theme} theme."
        
        return dungeon
        
    def regenerate_room(self, dungeon, room_id):
        """
        Regenerate a specific room in a dungeon.
        
        Args:
            dungeon (Dungeon): The dungeon containing the room.
            room_id (int): The ID of the room to regenerate.
            
        Returns:
            Room or None: The regenerated room, or None if the room wasn't found.
        """
        room = dungeon.get_room(room_id)
        if not room:
            return None
            
        # Generate a new room with the same ID
        new_room = self.room_generator.generate_room()
        new_room.id = room_id
        
        # Replace the old room in the dungeon
        for i, r in enumerate(dungeon.rooms):
            if r.id == room_id:
                dungeon.rooms[i] = new_room
                break
                
        return new_room
