"""
Table editor dialog for the dungeon generator application.

This module defines the TableEditorDialog class which allows users
to view and edit the tables used for random generation.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QComboBox, QLabel,
    QMessageBox, QLineEdit, QSpinBox, QHeaderView
)
from PyQt6.QtCore import Qt

from src.utils.file_handler import load_table, save_table, list_available_tables

class TableEditorDialog(QDialog):
    """
    Dialog for editing custom tables.
    
    This class provides a UI for viewing and editing the tables used
    for random generation.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the table editor dialog.
        
        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        
        self.setWindowTitle("Custom Table Editor")
        self.setMinimumSize(800, 600)
        
        self.current_table = None
        self.current_table_name = ""
        
        self.init_ui()
        self.load_available_tables()
        
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # Table management
        mgmt_layout = QHBoxLayout()
        
        # Table selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Select Table:"))
        self.table_selector = QComboBox()
        self.table_selector.setMinimumWidth(200)
        self.table_selector.currentIndexChanged.connect(self.on_table_selected)
        selector_layout.addWidget(self.table_selector)
        mgmt_layout.addLayout(selector_layout)
        
        # Create new table
        new_layout = QHBoxLayout()
        new_layout.addWidget(QLabel("New Table:"))
        self.new_table_input = QLineEdit()
        self.new_table_input.setPlaceholderText("table_name")
        new_layout.addWidget(self.new_table_input)
        self.create_btn = QPushButton("Create")
        self.create_btn.clicked.connect(self.create_new_table)
        new_layout.addWidget(self.create_btn)
        mgmt_layout.addLayout(new_layout)
        
        layout.addLayout(mgmt_layout)
        
        # Table info
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel("Table Description:"))
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description of this table")
        info_layout.addWidget(self.description_input)
        layout.addLayout(info_layout)
        
        # Table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Chance Min", "Chance Max"])
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add Row")
        self.add_btn.clicked.connect(self.add_row)
        button_layout.addWidget(self.add_btn)
        
        self.delete_btn = QPushButton("Delete Row")
        self.delete_btn.clicked.connect(self.delete_row)
        button_layout.addWidget(self.delete_btn)
        
        self.save_btn = QPushButton("Save Table")
        self.save_btn.clicked.connect(self.save_table)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        
    def load_available_tables(self):
        """Load available tables into the selector."""
        self.table_selector.clear()
        
        # Add standard tables (read-only reference)
        standard_tables = list_available_tables(custom=False)
        if standard_tables:
            self.table_selector.addItem("-- Standard Tables (Read-Only) --", None)
            for table_name in sorted(standard_tables):
                self.table_selector.addItem(f"(Std) {table_name}", 
                                           {"name": table_name, "custom": False})
        
        # Add custom tables
        custom_tables = list_available_tables(custom=True)
        if custom_tables:
            self.table_selector.addItem("-- Custom Tables --", None)
            for table_name in sorted(custom_tables):
                self.table_selector.addItem(f"(Custom) {table_name}", 
                                           {"name": table_name, "custom": True})
        
        # Add option to create new table
        self.table_selector.addItem("-- Create New Table --", None)
        
    def on_table_selected(self, index):
        """
        Handle table selection.
        
        Args:
            index (int): Index of the selected item.
        """
        data = self.table_selector.currentData()
        if not data:
            # Divider or "Create New" option
            self.clear_table()
            return
            
        table_name = data["name"]
        is_custom = data["custom"]
        
        self.current_table_name = table_name
        self.current_table = load_table(table_name, custom=is_custom)
        
        if not self.current_table:
            QMessageBox.critical(self, "Error", f"Failed to load table {table_name}")
            self.clear_table()
            return
            
        self.load_table_data()
        
        # Disable editing for standard tables
        is_editable = is_custom
        self.table_widget.setEnabled(is_editable)
        self.add_btn.setEnabled(is_editable)
        self.delete_btn.setEnabled(is_editable)
        self.save_btn.setEnabled(is_editable)
        self.description_input.setEnabled(is_editable)
        
    def load_table_data(self):
        """Load data for the selected table."""
        if not self.current_table:
            self.clear_table()
            return
            
        # Set description
        table_info = self.current_table.get("table_info", {})
        self.description_input.setText(table_info.get("description", ""))
        
        # Clear table
        self.table_widget.setRowCount(0)
        
        # Add entries
        entries = self.current_table.get("entries", [])
        for entry in entries:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            
            # Set name
            name_item = QTableWidgetItem(entry.get("name", ""))
            self.table_widget.setItem(row_position, 0, name_item)
            
            # Set min chance
            min_chance = entry.get("min", 0)
            min_item = QTableWidgetItem(str(min_chance))
            self.table_widget.setItem(row_position, 1, min_item)
            
            # Set max chance
            max_chance = entry.get("max", 0)
            max_item = QTableWidgetItem(str(max_chance))
            self.table_widget.setItem(row_position, 2, max_item)
        
    def clear_table(self):
        """Clear the table widget."""
        self.table_widget.setRowCount(0)
        self.description_input.clear()
        self.current_table = None
        self.current_table_name = ""
        
    def add_row(self):
        """Add a new row to the table."""
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        
        # Set default values
        name_item = QTableWidgetItem("")
        self.table_widget.setItem(row_position, 0, name_item)
        
        min_item = QTableWidgetItem("0")
        self.table_widget.setItem(row_position, 1, min_item)
        
        max_item = QTableWidgetItem("0")
        self.table_widget.setItem(row_position, 2, max_item)
        
    def delete_row(self):
        """Delete the selected row from the table."""
        selected_rows = self.table_widget.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "No row selected")
            return
            
        # Get unique row indexes
        row_indexes = set(index.row() for index in selected_rows)
        
        # Remove rows in reverse order (to avoid index shifting)
        for row in sorted(row_indexes, reverse=True):
            self.table_widget.removeRow(row)
        
    def create_new_table(self):
        """Create a new custom table."""
        table_name = self.new_table_input.text().strip()
        if not table_name:
            QMessageBox.warning(self, "Warning", "Please enter a table name")
            return
            
        # Ensure valid table name (alphanumeric and underscores only)
        if not table_name.replace('_', '').isalnum():
            QMessageBox.warning(self, "Warning", 
                               "Table name should contain only letters, numbers, and underscores")
            return
            
        # Create new table structure
        self.current_table_name = table_name
        self.current_table = {
            "table_info": {
                "name": table_name,
                "description": ""
            },
            "entries": []
        }
        
        # Clear and enable widgets
        self.clear_table()
        self.description_input.clear()
        self.table_widget.setEnabled(True)
        self.add_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.description_input.setEnabled(True)
        
        # Add first row
        self.add_row()
        
        # Save the new table
        if save_table(table_name, self.current_table):
            QMessageBox.information(self, "Success", f"Created new table {table_name}")
            self.load_available_tables()
            
            # Select the new table
            for i in range(self.table_selector.count()):
                data = self.table_selector.itemData(i)
                if data and data.get("name") == table_name and data.get("custom"):
                    self.table_selector.setCurrentIndex(i)
                    break
        else:
            QMessageBox.critical(self, "Error", f"Failed to create table {table_name}")
        
    def save_table(self):
        """Save the current table data."""
        if not self.current_table_name:
            QMessageBox.warning(self, "Warning", "No table selected")
            return
            
        # Update description
        description = self.description_input.text()
        if "table_info" not in self.current_table:
            self.current_table["table_info"] = {}
        self.current_table["table_info"]["description"] = description
        
        # Update entries
        entries = []
        for row in range(self.table_widget.rowCount()):
            name = self.table_widget.item(row, 0).text()
            
            # Skip empty rows
            if not name.strip():
                continue
                
            try:
                min_chance = int(self.table_widget.item(row, 1).text())
                max_chance = int(self.table_widget.item(row, 2).text())
            except (ValueError, AttributeError):
                QMessageBox.warning(self, "Warning", 
                                   f"Invalid chance values in row {row+1}. Using 0.")
                min_chance = 0
                max_chance = 0
                
            entries.append({
                "name": name,
                "min": min_chance,
                "max": max_chance
            })
            
        self.current_table["entries"] = entries
        
        # Save to file
        if save_table(self.current_table_name, self.current_table):
            QMessageBox.information(self, "Success", f"Saved table {self.current_table_name}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to save table {self.current_table_name}")
