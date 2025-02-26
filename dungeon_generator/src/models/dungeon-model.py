"""
Dungeon class for the dungeon generator.

This module defines the Dungeon class which represents a collection of connected rooms.
"""

import json
from datetime import datetime
from .room import Room

class Dungeon:
    """
    Represents a dungeon composed of multiple rooms.
    
    A dungeon has a name, creation date, and a collection of rooms.
    """
    
    def __init__(self, name="Random Dungeon"):
        """
        Initialize a new Dungeon.
        
        Args:
            name (str, optional): The name of the dungeon. Defaults to "Random Dungeon".
        """
        self.name = name
        self.rooms = []
        self.created_at = datetime.now().isoformat()
        self.notes = ""
        
    def add_room(self, room):
        """
        Add a room to the dungeon.
        
        Args:
            room (Room): The room to add.
            
        Returns:
            Room: The added room with its ID set.
        """
        # Set room ID based on its position in the dungeon
        room.id = len(self.rooms) + 1
        self.rooms.append(room)
        return room
        
    def get_room(self, room_id):
        """
        Get a room by its ID.
        
        Args:
            room_id (int): The ID of the room to retrieve.
            
        Returns:
            Room or None: The room with the given ID, or None if not found.
        """
        for room in self.rooms:
            if room.id == room_id:
                return room
        return None
        
    def to_dict(self):
        """
        Convert the dungeon to a dictionary for serialization.
        
        Returns:
            dict: Dictionary representation of the dungeon.
        """
        return {
            "name": self.name,
            "created_at": self.created_at,
            "notes": self.notes,
            "rooms": [room.to_dict() for room in self.rooms]
        }
        
    def to_json(self):
        """
        Convert the dungeon to a JSON string.
        
        Returns:
            str: JSON representation of the dungeon.
        """
        return json.dumps(self.to_dict(), indent=2)
        
    def save(self, filename):
        """
        Save the dungeon to a file.
        
        Args:
            filename (str): The name of the file to save to.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving dungeon: {e}")
            return False
            
    @classmethod
    def load(cls, filename):
        """
        Load a dungeon from a file.
        
        Args:
            filename (str): The name of the file to load from.
            
        Returns:
            Dungeon or None: The loaded dungeon, or None if loading failed.
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            dungeon = cls(name=data.get("name", "Loaded Dungeon"))
            dungeon.created_at = data.get("created_at", datetime.now().isoformat())
            dungeon.notes = data.get("notes", "")
            
            for room_data in data.get("rooms", []):
                room = Room.from_dict(room_data)
                # Don't use add_room so we preserve original IDs
                dungeon.rooms.append(room)
                
            return dungeon
        except Exception as e:
            print(f"Error loading dungeon: {e}")
            return None
            
    def __str__(self):
        """
        String representation of the dungeon.
        
        Returns:
            str: A formatted string describing the dungeon.
        """
        result = f"Dungeon: {self.name}\n"
        result += f"Created: {self.created_at}\n"
        result += f"Rooms: {len(self.rooms)}\n"
        
        if self.notes:
            result += f"Notes: {self.notes}\n"
            
        return result
