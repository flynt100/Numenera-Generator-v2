"""
File handling utilities for the dungeon generator.

This module provides functions for loading and saving data files,
particularly the table files used for random generation.
"""

import json
import os
from pathlib import Path

def get_tables_path(custom=False):
    """
    Get the path to table files.
    
    Args:
        custom (bool, optional): Whether to get the path to custom tables.
            Defaults to False.
            
    Returns:
        Path: Path object pointing to the tables directory.
    """
    # Get the absolute path to the dungeon_generator directory
    base_dir = Path(__file__).resolve().parent.parent.parent.parent / "dungeon_generator"
    
    if custom:
        return base_dir / "data" / "custom_tables"
    return base_dir / "data" / "tables"

def load_table(table_name, custom=False):
    """
    Load a table from file.
    
    Args:
        table_name (str): The name of the table to load.
        custom (bool, optional): Whether to load from custom tables. 
            Defaults to False.
            
    Returns:
        dict or None: The loaded table, or None if the table doesn't exist.
    """
    tables_path = get_tables_path(custom)
    file_path = tables_path / f"{table_name}.json"
    
    if not file_path.exists():
        # Try without .json extension
        file_path = tables_path / table_name
        if not file_path.exists():
            return None
        
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading table {table_name}: {e}")
        return None

def save_table(table_name, data, custom=True):
    """
    Save a table to file.
    
    Args:
        table_name (str): The name of the table to save.
        data (dict): The table data to save.
        custom (bool, optional): Whether to save to custom tables. 
            Defaults to True.
            
    Returns:
        bool: True if successful, False otherwise.
    """
    tables_path = get_tables_path(custom)
    
    # Create directories if they don't exist
    tables_path.mkdir(parents=True, exist_ok=True)
    
    # Make sure table_name has .json extension
    if not table_name.endswith('.json'):
        table_name = f"{table_name}.json"
        
    file_path = tables_path / table_name
    
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving table {table_name}: {e}")
        return False

def list_available_tables(custom=False):
    """
    List all available tables.
    
    Args:
        custom (bool, optional): Whether to list custom tables. 
            Defaults to False.
            
    Returns:
        list: List of table names (without extension).
    """
    tables_path = get_tables_path(custom)
    
    if not tables_path.exists():
        return []
        
    return [f.stem for f in tables_path.glob("*.json")]
