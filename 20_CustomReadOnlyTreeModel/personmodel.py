import os
from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt
from person import Person

class PersonModel(QAbstractItemModel):
    def __init__(self, parent = None):
        super().__init__(parent)

        # Initialize the root person
        self.root_person = Person(["John Doe", "CEO"])

        # Create the managers
        manager1 = Person(["Jane Smith", "Manager"], self.root_person)
        manager2 = Person(["Bob Johnson", "Manager"], self.root_person)

        # Add managers to root
        self.root_person.append_child(manager1)
        self.root_person.append_child(manager2)

        # Add employees under manager1
        employee1 = Person(["Alice Brown", "Developer"], manager1)
        employee2 = Person(["Tom Wilson", "Designer"], manager1)
        manager1.append_child(employee1)
        manager1.append_child(employee2)

        # Add employees under manager2
        employee3 = Person(["Charlie Davis", "Developer"], manager2)
        employee4 = Person(["Eve Anderson", "Tester"], manager2)
        manager2.append_child(employee3)
        manager2.append_child(employee4)


    def rowCount(self, parent = QModelIndex()):
        if parent.column() > 0:
            return 0
        parent_person = parent.internalPointer() if parent.isValid() else self.root_person
        return parent_person.child_count()


    def columnCount(self, parent = QModelIndex()):
        return 2
    
    def data(self, index, role = Qt.DisplayRole):

        if not index.isValid():
            return None
        
        if role != Qt.DisplayRole:
            return None
        
        person = index.internalPointer()
        return person.data(index.column())
    

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return "Name" if section == 0 else "Profession"
        return None
    
    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return super().flags(index)
    

    # Implement index and parent to make this a proper tree model.
    def index(self, row, column, parent = QModelIndex()):

        if not self.hasIndex(row,column,parent):
            return QModelIndex()
        
        if parent.isValid():
            parent_person = parent.internalPointer()
        else:
            parent_person = self.root_person

        child_person = parent_person.child(row)

        if child_person:
            return self.createIndex(row,column, child_person)
        else:
            return QModelIndex()


    def parent(self,childIndex):
        if not childIndex.isValid():
            return QModelIndex()
        
        child_person = childIndex.internalPointer()
        parent_person = child_person.parent_person()

        if parent_person == self.root_person:
            return QModelIndex()
        return self.createIndex(parent_person.row(), 0, parent_person)
        

        
