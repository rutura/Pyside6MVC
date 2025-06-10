from PySide6.QtWidgets import QWidget, QListWidgetItem 
from ui_widget import Ui_Widget
from person import Person

class Widget(QWidget): 
    def __init__(self, parent = None):
        super().__init__(parent)

        # Connect to the ui form
        self.ui = Ui_Widget()
        self.ui.setupUi(self)


        # Print the tree structure
        self.print_tree()


    def print_tree(self):

        # Initialize the root person
        root_person = Person(["John Doe", "CEO"])

