import os
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql

class BlobDelegate(QtWidgets.QStyledItemDelegate):
    def displayText(self, value, locale):
        if isinstance(value, QtCore.QByteArray):
            value = value.data().decode()
        return super(BlobDelegate, self).displayText(value, locale)

def createConnection():
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "CurrentVoltage.db")
    db.setDatabaseName(file)
    if not db.open():
        QtWidgets.QMessageBox.critical(
            None,
            QtWidgets.qApp.tr("Cannot open database"),
            QtWidgets.qApp.tr(
                "Unable to establish a database connection.\n"
            ),
            QtWidgets.QMessageBox.Cancel,
        )
        return False
    return True

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if not createConnection():
        sys.exit(-1)

    w = QtWidgets.QTableView()
    w.horizontalHeader().setStretchLastSection(True)
    w.setWordWrap(True)
    w.setTextElideMode(QtCore.Qt.ElideLeft)
    delegate = BlobDelegate(w)
    w.setItemDelegateForColumn(4, delegate)
    model = QtSql.QSqlQueryModel()
    model.setQuery("SELECT * FROM DataTable")
    w.setModel(model)
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())

