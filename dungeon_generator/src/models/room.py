"""
Room class for the dungeon generator.

This module defines the Room class which represents a single room in a dungeon.
"""

class Room:
    """
    Represents a single room in a dungeon.
    
    A room has a main feature (such as corridor, chamber, etc.), details specific
    to that feature, and information about exits.
    """
    
    def __init__(self, main_feature=None, details=None, exits=None):
        """
        Initialize a new Room.
        
        Args:
            main_feature (str, optional): The room's main feature. Defaults to None.
            details (dict, optional): Details about the room. Defaults to {}.
            exits (list, optional): List of exits from the room. Defaults to [].
        """
        self.main_feature = main_feature
        self.details = details or {}
        self.exits = exits or []
        self.id = None  # Will be set when added to a dungeon
        
    @property
    def description(self):
        """
        Get a full description of the room.
        
        Returns:
            str: A formatted description of the room.
        """
        if not self.main_feature:
            return "Empty room"
            
        # Start with the main feature
        result = f"{self.main_feature}:\n"
        
        # Add details based on the feature type
        if "description" in self.details:
            result += f"{self.details['description']}\n"
            
        # Add specific details for different room types
        if self.main_feature == "Chamber":
            if "size" in self.details:
                result += f"Size: {self.details['size']}\n"
            if "shape" in self.details:
                result += f"Shape: {self.details['shape']}\n"
                
        # Add feature-specific details
        for key, value in self.details.items():
            if key not in ["description", "size", "shape"]:
                result += f"{key.capitalize()}: {value}\n"
                
        # Add exits
        if self.exits:
            exits_str = ", ".join(self.exits)
            result += f"Exits: {exits_str}"
        else:
            result += "No exits"
            
        return result
        
    def __str__(self):
        """
        String representation of the room.
        
        Returns:
            str: A formatted string describing the room.
        """
        return self.description
        
    def to_dict(self):
        """
        Convert the room to a dictionary for serialization.
        
        Returns:
            dict: Dictionary representation of the room.
        """
        return {
            "id": self.id,
            "main_feature": self.main_feature,
            "details": self.details,
            "exits": self.exits
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Create a Room from a dictionary.
        
        Args:
            data (dict): Dictionary containing room data.
            
        Returns:
            Room: New Room instance.
        """
        room = cls(
            main_feature=data.get("main_feature"),
            details=data.get("details", {}),
            exits=data.get("exits", [])
        )
        room.id = data.get("id")
        return room
