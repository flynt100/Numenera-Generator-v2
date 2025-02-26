#!/usr/bin/env python3
"""
Main entry point for the Numenera Dungeon Generator application.

This script initializes and runs the dungeon generator application.
"""

import sys
import os
from pathlib import Path

# Ensure proper paths for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Run in console mode only
UI_ENABLED = False

from src.models.dungeon import Dungeon
from src.generators.dungeon_generator import DungeonGenerator

def ensure_data_dirs():
    """Ensure the data directories exist."""
    data_dir = Path(__file__).resolve().parent / "data"
    tables_dir = data_dir / "tables"
    custom_dir = data_dir / "custom_tables"
    
    # Create directories if they don't exist
    tables_dir.mkdir(parents=True, exist_ok=True)
    custom_dir.mkdir(parents=True, exist_ok=True)

def run_gui():
    """Run the application in GUI mode."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

def run_console():
    """Run the application in console mode."""
    print("Numenera Dungeon Generator - Console Mode")
    print("=========================================")
    
    generator = DungeonGenerator()
    
    while True:
        try:
            room_count = input("How many rooms would you like to generate? (type q to quit): ")
            
            if room_count.lower() == 'q':
                print("Goodbye!")
                break
                
            room_count = int(room_count)
            if room_count <= 0:
                print("Please enter a positive number.")
                continue
                
            dungeon_name = input("Enter a name for your dungeon (or press Enter for default): ")
            if not dungeon_name:
                dungeon_name = "Random Dungeon"
                
            print(f"\nGenerating {room_count} rooms for '{dungeon_name}'...\n")
            
            dungeon = generator.generate_dungeon(room_count, dungeon_name)
            
            print(f"Dungeon: {dungeon.name}")
            print(f"Created: {dungeon.created_at}")
            print(f"Rooms: {len(dungeon.rooms)}\n")
            
            for i, room in enumerate(dungeon.rooms, 1):
                print(f"Room {i}:")
                print(str(room))
                print()
                
            save_option = input("Would you like to save this dungeon? (y/n): ")
            if save_option.lower() == 'y':
                filename = input("Enter filename (or press Enter for default): ")
                if not filename:
                    filename = f"{dungeon.name.replace(' ', '_').lower()}.dungeon"
                elif not (filename.endswith('.dungeon') or filename.endswith('.json')):
                    filename += '.dungeon'
                    
                if dungeon.save(filename):
                    print(f"Dungeon saved to {filename}")
                else:
                    print("Failed to save dungeon")
                    
            print()
            
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    """Main entry point for the application."""
    # Ensure data directories exist
    ensure_data_dirs()
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--console':
        run_console()
    elif UI_ENABLED:
        run_gui()
    else:
        run_console()

if __name__ == "__main__":
    main()
