"""
Dice rolling utilities for the dungeon generator.

This module provides functions for simulating dice rolls,
which are used throughout the generator for random determinations.
"""

import random

def roll_dice(num_dice, sides, modifier=0):
    """
    Roll a number of dice with the given number of sides.
    
    Args:
        num_dice (int): Number of dice to roll.
        sides (int): Number of sides on each die.
        modifier (int, optional): Modifier to add to the result. Defaults to 0.
        
    Returns:
        int: The sum of the dice rolls plus the modifier.
    """
    if num_dice <= 0 or sides <= 0:
        return modifier
        
    total = sum(random.randint(1, sides) for _ in range(num_dice))
    return total + modifier

def roll_d20():
    """
    Roll a 20-sided die.
    
    Returns:
        int: A random number between 1 and 20.
    """
    return random.randint(1, 20)

def roll_d100():
    """
    Roll a 100-sided die (d%).
    
    Returns:
        int: A random number between 1 and 100.
    """
    return random.randint(1, 100)

def roll_on_table(table_entries):
    """
    Roll on a table and return the corresponding entry.
    
    Args:
        table_entries (list): A list of table entries, each with min and max values.
        
    Returns:
        dict or None: The selected table entry, or None if the table is empty.
    """
    if not table_entries:
        return None
        
    roll = roll_d100()
    
    for entry in table_entries:
        if entry["min"] <= roll <= entry["max"]:
            return entry
    
    # Fallback to the last entry if none matched
    return table_entries[-1] if table_entries else None
