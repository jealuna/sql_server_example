# This Python file uses the following encoding: utf-8
import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from db import connection

class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        self.load_ui()
        self.centralwidget = self.findChild(QWidget, "centralwidget")
        self.tableWidget = self.findChild(QTableWidget, "tableWidget")

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

if __name__ == "__main__":
    app = QApplication([])
    widget = main()
    widget.setCentralWidget(widget.centralwidget)
    tableWidget = widget.tableWidget
    connection_obj = connection.SqlConnection()
    conn = connection_obj.get_connection()
    result = []
    with conn.cursor() as cursor:
        # sql = 'exec [dbo].[SP_PRODUCT_IMAGES] (@IdProductImage=?, @Option=?))'
        sql = """\
                DECLARE @out VARCHAR(max);
                EXEC [dbo].[SP_PRODUCT_IMAGES] @IdProductImage=?, @Option=?, @Result=@out OUTPUT;
                SELECT @out AS the_output;
                """
        # sql = "{call SP_PRODUCT_IMAGES (@IdProductImage=?, @Option=?, @Result=?)}"
        values = (1, 0)
        try:
            cursor.execute(sql, (values))
            result = cursor.fetchall()
        except Exception as ex:
            print(ex)
    numrows = len(result)
    numcols = len(result[0])
    tableWidget.setColumnCount(numcols)
    tableWidget.setRowCount(numrows)
    for row in range(numrows):
        for column in range(3): #Exclude the image blob
            tableWidget.setItem(row, column, QTableWidgetItem((str(result[row][column]))))
    widget.show()
    sys.exit(app.exec_())
