#!/usr/bin/env python3
"""
Main entry point for the Dungeon Generator application.
"""

import sys
from pathlib import Path

# Ensure proper paths for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Ensure GUI mode
UI_ENABLED = True

try:
    from PyQt6.QtWidgets import QApplication
    from src.ui.main_window import MainWindow
except ImportError:
    UI_ENABLED = False
    print("PyQt6 not found. Please run: pip install PyQt6")
    print("Falling back to console mode.")

from src.models.dungeon import Dungeon
from src.generators.dungeon_generator import DungeonGenerator

def ensure_data_dirs():
    """Ensure the data directories exist."""
    data_dir = Path(__file__).resolve().parent / "data"
    tables_dir = data_dir / "tables"
    custom_dir = data_dir / "custom_tables"

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
    print("Dungeon Generator - Console Mode")
    print("===============================")

    generator = DungeonGenerator()

    while True:
        try:
            room_count = input("\nHow many rooms? (q to quit): ")
            if room_count.lower() == 'q':
                break

            room_count = int(room_count)
            if room_count <= 0:
                print("Please enter a positive number.")
                continue

            name = input("Dungeon name (Enter for default): ")
            if not name:
                name = "Random Dungeon"

            dungeon = generator.generate_dungeon(room_count, name)

            print(f"\n{dungeon.name}")
            print(f"Created: {dungeon.created_at}")
            print(f"Rooms: {len(dungeon.rooms)}\n")

            for i, room in enumerate(dungeon.rooms, 1):
                print(f"Room {i}:")
                print(str(room))
                print()

        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point."""
    ensure_data_dirs()

    if len(sys.argv) > 1 and sys.argv[1] == '--console':
        run_console()
    elif UI_ENABLED:
        run_gui()
    else:
        run_console()

if __name__ == "__main__":
    main()