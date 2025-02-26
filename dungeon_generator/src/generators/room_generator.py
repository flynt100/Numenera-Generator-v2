"""
Room generator for the dungeon generator.

This module defines the RoomGenerator class which generates individual rooms
based on the Numenera dungeon generation rules.
"""

from src.models.room import Room
from src.utils.dice import roll_d20, roll_d100, roll_on_table
from src.utils.file_handler import load_table

class RoomGenerator:
    """
    Generator for individual dungeon rooms.
    
    This class loads the necessary tables and provides methods to generate rooms
    with various features.
    """
    
    def __init__(self, use_custom_tables=True):
        """
        Initialize the RoomGenerator.
        
        Args:
            use_custom_tables (bool, optional): Whether to use custom tables. 
                Defaults to True.
        """
        self.use_custom_tables = use_custom_tables
        self.feature_generators = {
            "Corridor": self.generate_corridor,
            "Chamber": self.generate_chamber,
            "Creature": self.generate_creature,
            "Explorers": self.generate_explorers,
            "Interstitial cavity": self.generate_interstitial_cavity,
            "Accessway": self.generate_accessway,
            "Rupture": self.generate_rupture,
            "Shaft": self.generate_shaft,
            "Abhuman Colony": self.generate_abhuman_colony,
            "Integrated Machine": self.generate_integrated_machine,
            "Matter leak": self.generate_matter_leak,
            "Energy discharge": self.generate_energy_discharge,
            "Weird event": self.generate_weird_event,
            "Vault": self.generate_vault,
            "Relic Chamber": self.generate_relic_chamber
        }
        
    def generate_room(self):
        """
        Generate a complete random room.
        
        Returns:
            Room: A fully generated room.
        """
        # Generate the main feature
        main_feature_table = load_table("main_features")
        if not main_feature_table:
            raise ValueError("Could not load main_features table")
            
        main_feature_entry = roll_on_table(main_feature_table["entries"])
        if not main_feature_entry:
            raise ValueError("Failed to roll on main_features table")
            
        main_feature = main_feature_entry["name"]
        
        # Generate details based on the main feature
        if main_feature in self.feature_generators:
            details = self.feature_generators[main_feature]()
        else:
            details = {"description": "Empty room"}
            
        # Generate exits
        exits = self.generate_exits()
        
        # Create and return the room
        return Room(main_feature, details, exits)
        
    def generate_corridor(self):
        """
        Generate details for a corridor.
        
        Returns:
            dict: Dictionary of corridor details.
        """
        corridor_table = load_table("corridor_details")
        if not corridor_table:
            return {"description": "Simple corridor"}
            
        corridor_entry = roll_on_table(corridor_table["entries"])
        if not corridor_entry:
            return {"description": "Simple corridor"}
            
        details = {"description": corridor_entry["name"]}
        
        # Handle special cases like roll_again
        if "roll_again" in corridor_entry and corridor_entry["roll_again"]:
            # In a real implementation, you might want to handle this differently
            details["note"] = "Roll again on the main feature table"
            
        return details
        
    def generate_chamber(self):
        """
        Generate details for a chamber.
        
        Returns:
            dict: Dictionary of chamber details.
        """
        # Size
        size_table = [
            {"name": "Closet-sized", "min": 1, "max": 2},
            {"name": "15 feet (5 m) across", "min": 3, "max": 6},
            {"name": "30 feet (9 m) across", "min": 7, "max": 15},
            {"name": "50 feet (15 m) across", "min": 16, "max": 18},
            {"name": "60 feet (18 m) across", "min": 19, "max": 19},
            {"name": "90 feet (27 m) across", "min": 20, "max": 20}
        ]
        
        # Shape
        shape_table = [
            {"name": "Circle", "min": 1, "max": 2},
            {"name": "Square", "min": 3, "max": 4},
            {"name": "Rectangle", "min": 5, "max": 17},
            {"name": "Hexagon", "min": 18, "max": 18},
            {"name": "Half circle", "min": 19, "max": 19},
            {"name": "Triangle", "min": 20, "max": 20}
        ]
        
        # Roll for size and shape
        size_entry = roll_on_table(size_table)
        shape_entry = roll_on_table(shape_table)
        
        details = {
            "size": size_entry["name"] if size_entry else "Medium sized",
            "shape": shape_entry["name"] if shape_entry else "Rectangular"
        }
        
        # We would normally load and roll on a chamber features table here
        # For simplicity, we'll just add a placeholder
        details["features"] = "Various furnishings and decorations"
        
        return details
    
    def generate_creature(self):
        """
        Generate details for a creature encounter.
        
        Returns:
            dict: Dictionary of creature details.
        """
        # In a full implementation, this would load and roll on a creature table
        return {
            "description": "A creature lurks here",
            "creature_type": f"Level {roll_d20() % 10 + 1} hostile entity"
        }
        
    # For brevity, I'll include just placeholders for the remaining methods
    # In a real implementation, these would each have proper table lookups
    
    def generate_explorers(self):
        """Generate details for explorers."""
        return {"description": "A group of explorers is here"}
        
    def generate_interstitial_cavity(self):
        """Generate details for an interstitial cavity."""
        return {"description": "A vast interstitial cavity"}
        
    def generate_accessway(self):
        """Generate details for an accessway."""
        return {"description": "An accessway connecting areas"}
        
    def generate_rupture(self):
        """Generate details for a rupture."""
        return {"description": "A rupture in the structure"}
        
    def generate_shaft(self):
        """Generate details for a shaft."""
        return {"description": "A vertical shaft"}
        
    def generate_abhuman_colony(self):
        """Generate details for an abhuman colony."""
        return {"description": "An abhuman colony resides here"}
        
    def generate_integrated_machine(self):
        """Generate details for an integrated machine."""
        return {"description": "An integrated machine dominates this area"}
        
    def generate_matter_leak(self):
        """Generate details for a matter leak."""
        return {"description": "A strange matter leak is present"}
        
    def generate_energy_discharge(self):
        """Generate details for an energy discharge."""
        return {"description": "Energy discharges pulse through this area"}
        
    def generate_weird_event(self):
        """Generate details for a weird event."""
        return {"description": "A bizarre phenomenon occurs here"}
        
    def generate_vault(self):
        """Generate details for a vault."""
        return {"description": "A secure vault containing treasures"}
        
    def generate_relic_chamber(self):
        """Generate details for a relic chamber."""
        return {"description": "A chamber housing a powerful relic"}
        
    def generate_exits(self):
        """
        Generate exits for a room.
        
        Returns:
            list: List of exit descriptions.
        """
        exits_table = load_table("exits")
        if not exits_table:
            return ["1 exit"]
            
        exits_entry = roll_on_table(exits_table["entries"])
        if not exits_entry:
            return ["1 exit"]
            
        # Parse the exit description to determine how many exits to add
        exit_desc = exits_entry["name"]
        
        # Very simple parsing - in a real implementation this would be more robust
        exits = []
        
        if "No additional exits" in exit_desc:
            exits = ["Main entrance"]
        elif "1 additional exit" in exit_desc:
            exits = ["Main entrance", "Side passage"]
        elif "2 additional exits" in exit_desc:
            exits = ["Main entrance", "Side passage", "Back door"]
        elif "sealed exit" in exit_desc:
            exits = ["Main entrance", "Sealed door"]
        elif "trapped exit" in exit_desc:
            exits = ["Main entrance", "Trapped door"]
        elif "hidden exit" in exit_desc:
            exits = ["Main entrance", "Hidden passage"]
        else:
            exits = ["Main entrance"]
            
        return exits
