# Numenera Dungeon Generator

A Python application for generating rooms and complete dungeons for the Numenera tabletop RPG.

## Features

- Generate random dungeon rooms based on Numenera rules
- Create complete dungeons with multiple connected rooms
- Customize generation with themes
- Save and load dungeon designs
- Export dungeons to text files
- Customize generation tables with the built-in editor

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/dungeon-generator.git
   cd dungeon-generator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### GUI Mode (Default)

Run the application with the graphical user interface:

```
python main.py
```

This opens a window where you can:
- Set the dungeon name and number of rooms
- Generate random or themed dungeons
- Save/load dungeons to/from files
- Export dungeons to text files
- Edit custom tables for generation

### Console Mode

Run the application in console mode:

```
python main.py --console
```

In console mode, you'll be prompted to enter:
- The number of rooms to generate
- A name for your dungeon
- Whether to save the generated dungeon

## Customization

### Custom Tables

The application uses JSON files for table-based generation. These tables can be customized through the UI or by directly editing the JSON files in the `data/custom_tables` directory.

Each table follows this structure:

```json
{
  "table_info": {
    "name": "Table Name",
    "description": "Description of this table"
  },
  "entries": [
    {
      "name": "Entry name",
      "min": 1,
      "max": 20
    },
    {
      "name": "Another entry",
      "min": 21,
      "max": 40
    }
  ]
}
```

## Project Structure

```
dungeon_generator/
├── data/
│   ├── tables/           # Standard tables
│   └── custom_tables/    # User-created tables
├── src/
│   ├── models/           # Data models
│   ├── generators/       # Generation logic
│   ├── utils/            # Utility functions
│   └── ui/               # User interface
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

## Extending the Generator

To add new room types or features:

1. Create a new table JSON file
2. Add appropriate methods to the RoomGenerator class
3. Update the feature_generators dictionary in RoomGenerator

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on the original code by flynt100
- Uses the Numenera dungeon generation rules
