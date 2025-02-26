"""
Main window for the dungeon generator application.

This module defines the MainWindow class which serves as the primary UI
for the application.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QSpinBox, QTextEdit, QLabel, QFileDialog,
    QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt

from src.generators.dungeon_generator import DungeonGenerator
from src.models.dungeon import Dungeon
from .table_editor import TableEditorDialog

class MainWindow(QMainWindow):
    """
    Main window of the dungeon generator application.
    
    This class provides the main user interface for generating, viewing,
    and saving dungeons.
    """
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self.dungeon = Dungeon()
        self.generator = DungeonGenerator()
        
        self.setWindowTitle("Numenera Dungeon Generator")
        self.setMinimumSize(1000, 700)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components."""
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Dungeon name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Dungeon Name:"))
        self.name_input = QLineEdit("Random Dungeon")
        name_layout.addWidget(self.name_input)
        left_layout.addLayout(name_layout)
        
        # Number of rooms control
        rooms_layout = QHBoxLayout()
        rooms_layout.addWidget(QLabel("Number of Rooms:"))
        self.room_count = QSpinBox()
        self.room_count.setMinimum(1)
        self.room_count.setMaximum(100)
        self.room_count.setValue(5)
        rooms_layout.addWidget(self.room_count)
        left_layout.addLayout(rooms_layout)
        
        # Generation button
        self.generate_btn = QPushButton("Generate Dungeon")
        self.generate_btn.clicked.connect(self.generate_dungeon)
        left_layout.addWidget(self.generate_btn)
        
        # Theme option
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme (optional):"))
        self.theme_input = QLineEdit()
        self.theme_input.setPlaceholderText("e.g., abandoned, infested")
        theme_layout.addWidget(self.theme_input)
        left_layout.addLayout(theme_layout)
        
        # Themed generation button
        self.generate_themed_btn = QPushButton("Generate Themed Dungeon")
        self.generate_themed_btn.clicked.connect(self.generate_themed_dungeon)
        left_layout.addWidget(self.generate_themed_btn)
        
        # Add separator
        left_layout.addWidget(QLabel(""))
        left_layout.addWidget(QLabel("Dungeon Management"))
        
        # Save/load buttons
        self.save_btn = QPushButton("Save Dungeon")
        self.save_btn.clicked.connect(self.save_dungeon)
        left_layout.addWidget(self.save_btn)
        
        self.load_btn = QPushButton("Load Dungeon")
        self.load_btn.clicked.connect(self.load_dungeon)
        left_layout.addWidget(self.load_btn)
        
        # Export button
        self.export_btn = QPushButton("Export to Text")
        self.export_btn.clicked.connect(self.export_dungeon)
        left_layout.addWidget(self.export_btn)
        
        # Add separator
        left_layout.addWidget(QLabel(""))
        left_layout.addWidget(QLabel("Customization"))
        
        # Custom table editor button
        self.edit_tables_btn = QPushButton("Edit Custom Tables")
        self.edit_tables_btn.clicked.connect(self.open_table_editor)
        left_layout.addWidget(self.edit_tables_btn)
        
        left_layout.addStretch()
        
        # Right panel - Output
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Header
        right_layout.addWidget(QLabel("Generated Dungeon"))
        
        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        right_layout.addWidget(self.output_text)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 3)
        
        self.setCentralWidget(central_widget)
        
    def generate_dungeon(self):
        """Generate a dungeon with the specified number of rooms."""
        room_count = self.room_count.value()
        name = self.name_input.text() or "Random Dungeon"
        
        try:
            self.dungeon = self.generator.generate_dungeon(room_count, name)
            self.display_dungeon()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate dungeon: {e}")
        
    def generate_themed_dungeon(self):
        """Generate a dungeon with the specified theme."""
        room_count = self.room_count.value()
        theme = self.theme_input.text()
        
        if not theme:
            QMessageBox.warning(self, "Warning", "Please enter a theme")
            return
            
        try:
            self.dungeon = self.generator.generate_themed_dungeon(theme, room_count)
            self.display_dungeon()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate themed dungeon: {e}")
        
    def display_dungeon(self):
        """Display the current dungeon in the output text area."""
        output = f"# {self.dungeon.name}\n\n"
        
        if self.dungeon.notes:
            output += f"{self.dungeon.notes}\n\n"
            
        output += f"Created: {self.dungeon.created_at}\n"
        output += f"Total Rooms: {len(self.dungeon.rooms)}\n\n"
        
        for i, room in enumerate(self.dungeon.rooms, 1):
            output += f"## Room {i}\n\n"
            output += str(room) + "\n\n"
            
        self.output_text.setText(output)
        
    def save_dungeon(self):
        """Save the current dungeon to a file."""
        if not self.dungeon or not self.dungeon.rooms:
            QMessageBox.warning(self, "Warning", "No dungeon to save")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Dungeon", "", "Dungeon Files (*.dungeon *.json);;All Files (*)"
        )
        
        if not file_path:
            return
            
        # Ensure the file has an extension
        if not file_path.endswith(('.dungeon', '.json')):
            file_path += '.dungeon'
            
        if self.dungeon.save(file_path):
            QMessageBox.information(self, "Success", "Dungeon saved successfully")
        else:
            QMessageBox.critical(self, "Error", "Failed to save dungeon")
        
    def load_dungeon(self):
        """Load a dungeon from a file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Dungeon", "", "Dungeon Files (*.dungeon *.json);;All Files (*)"
        )
        
        if not file_path:
            return
            
        loaded_dungeon = Dungeon.load(file_path)
        if loaded_dungeon:
            self.dungeon = loaded_dungeon
            self.display_dungeon()
            self.name_input.setText(self.dungeon.name)
        else:
            QMessageBox.critical(self, "Error", "Failed to load dungeon")
        
    def export_dungeon(self):
        """Export the dungeon to a text file."""
        if not self.dungeon or not self.dungeon.rooms:
            QMessageBox.warning(self, "Warning", "No dungeon to export")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Dungeon", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if not file_path:
            return
            
        # Ensure the file has an extension
        if not file_path.endswith('.txt'):
            file_path += '.txt'
            
        try:
            with open(file_path, 'w') as f:
                f.write(self.output_text.toPlainText())
            QMessageBox.information(self, "Success", "Dungeon exported successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export dungeon: {e}")
        
    def open_table_editor(self):
        """Open the custom table editor."""
        editor = TableEditorDialog(self)
        editor.exec()
"""
Main window implementation for the dungeon generator GUI.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QSpinBox, QPushButton, QTextEdit,
    QMessageBox, QFileDialog
)
from src.models.dungeon import Dungeon
from src.generators.dungeon_generator import DungeonGenerator

class MainWindow(QMainWindow):
    """Main window of the dungeon generator application."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self.dungeon = Dungeon()
        self.generator = DungeonGenerator()
        
        self.setWindowTitle("Dungeon Generator")
        self.setMinimumSize(800, 600)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components."""
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Dungeon name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Dungeon Name:"))
        self.name_input = QLineEdit("Random Dungeon")
        name_layout.addWidget(self.name_input)
        left_layout.addLayout(name_layout)
        
        # Room count input
        rooms_layout = QHBoxLayout()
        rooms_layout.addWidget(QLabel("Number of Rooms:"))
        self.room_count = QSpinBox()
        self.room_count.setMinimum(1)
        self.room_count.setMaximum(100)
        self.room_count.setValue(5)
        rooms_layout.addWidget(self.room_count)
        left_layout.addLayout(rooms_layout)
        
        # Generate button
        self.generate_btn = QPushButton("Generate Dungeon")
        self.generate_btn.clicked.connect(self.generate_dungeon)
        left_layout.addWidget(self.generate_btn)
        
        # Save/Load buttons
        self.save_btn = QPushButton("Save Dungeon")
        self.save_btn.clicked.connect(self.save_dungeon)
        left_layout.addWidget(self.save_btn)
        
        self.load_btn = QPushButton("Load Dungeon")
        self.load_btn.clicked.connect(self.load_dungeon)
        left_layout.addWidget(self.load_btn)
        
        main_layout.addWidget(left_panel)
        
        # Right panel - Output
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)
        
        self.setCentralWidget(central_widget)
        
    def generate_dungeon(self):
        """Generate a new dungeon based on current settings."""
        try:
            name = self.name_input.text()
            room_count = self.room_count.value()
            
            self.dungeon = self.generator.generate_dungeon(room_count, name)
            self.display_dungeon()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate dungeon: {e}")
            
    def display_dungeon(self):
        """Display the current dungeon in the output text area."""
        output = f"# {self.dungeon.name}\n\n"
        output += f"Created: {self.dungeon.created_at}\n"
        output += f"Total Rooms: {len(self.dungeon.rooms)}\n\n"
        
        for i, room in enumerate(self.dungeon.rooms, 1):
            output += f"## Room {i}\n\n"
            output += str(room) + "\n\n"
            
        self.output_text.setText(output)
        
    def save_dungeon(self):
        """Save the current dungeon to a file."""
        if not self.dungeon or not self.dungeon.rooms:
            QMessageBox.warning(self, "Warning", "No dungeon to save")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Dungeon", "", "Dungeon Files (*.dungeon);;All Files (*)"
        )
        
        if file_path:
            if self.dungeon.save(file_path):
                QMessageBox.information(self, "Success", "Dungeon saved successfully")
            else:
                QMessageBox.critical(self, "Error", "Failed to save dungeon")
                
    def load_dungeon(self):
        """Load a dungeon from a file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Dungeon", "", "Dungeon Files (*.dungeon);;All Files (*)"
        )
        
        if file_path:
            loaded_dungeon = Dungeon.load(file_path)
            if loaded_dungeon:
                self.dungeon = loaded_dungeon
                self.display_dungeon()
                self.name_input.setText(self.dungeon.name)
            else:
                QMessageBox.critical(self, "Error", "Failed to load dungeon")
