from PySide6.QtCore import (
    QAbstractListModel, QModelIndex, Qt, QMimeData
)

class PersonModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._persons = [
            "Donald Bush", 
            "Xi Jing Tao", 
            "Vladmir Golbathev", 
            "Emmanuel Mitterand", 
            "Jacob Mandela"
        ]

    def rowCount(self, parent=QModelIndex()):
        """Return the number of rows in the model."""
        return len(self._persons)
    
    def data(self, index, role=Qt.DisplayRole):
        """Provide data for the given index and role."""
        if not index.isValid():
            return None

        if index.row() < 0 or index.row() >= len(self._persons):
            return None

        if role in (Qt.DisplayRole, Qt.EditRole):
            return self._persons[index.row()]

        return None
    

    def setData(self, index, value, role=Qt.EditRole):
        """Update data for a given index."""
        if role == Qt.EditRole and index.isValid():
            self._persons[index.row()] = str(value)
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Provide header data."""
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return "Names" if section == 0 else None
        return None
    
    def insertRows(self, row, count=1, parent=QModelIndex()):
        """Insert rows into the model."""
        self.beginInsertRows(parent, row, row + count - 1)
        for _ in range(count):
            self._persons.insert(row, "")
        self.endInsertRows()
        return True

    def removeRows(self, row, count=1, parent=QModelIndex()):
        """Remove rows from the model."""
        self.beginRemoveRows(parent, row, row + count - 1)
        del self._persons[row:row+count]
        self.endRemoveRows()
        return True
    
    def flags(self, index):
        return super().flags(index) | Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled
    
    # Drag and drop methods: list the types we support for drag and drop
    def mimeTypes(self):
        return super().mimeTypes() + ["text/plain"]

    # Drag and drop methods:  Package the data when a drag is initiated
    def mimeData(self, indexes):
        mime_data = super().mimeData(indexes)
        text_data = ",".join(str(index.data()) for index in indexes)
        mime_data.setText(text_data)
        return mime_data

    # Drag and drop methods:  Unpack dropped data and do what needs to be done.
    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasText():
            return False
        
        if parent.isValid():
            self.setData(parent,data.text())
        else:
            # Add new item at the end
            self.insertRows(self.rowCount())
            self.setData(self.index(self.rowCount() - 1), data.text())

        return True