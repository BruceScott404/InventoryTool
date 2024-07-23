# Author: Bruce Scott
# Date: 7/23/2024
# Description: Tool to help with inventory

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QMessageBox, \
    QLabel, QListWidgetItem, QDialog, QLineEdit, QComboBox, QCheckBox


class Part(QWidget):
    def __init__(self, part_number, qty):
        super().__init__()

        self.qty = str(qty)
        self.part_number = str(part_number)

        layout = QHBoxLayout()
        self.part_number_label = QLabel(self.part_number)
        self.qty_label = QLabel(self.qty)

        layout.addWidget(self.part_number_label)
        layout.addWidget(self.qty_label)

        self.setLayout(layout)

class ManualDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("new Item")

        layout = QVBoxLayout()

        self.done_button = QPushButton("Add or Edit Item")
        self.done_button.clicked.connect(self.done_clicked)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_clicked)

        self.part_num_label = QLabel("Part #:")
        self.qty_label = QLabel("Qty #:")

        self.part_num_edit = QLineEdit()
        self.part_num_edit.setPlaceholderText("Ex. 295100330")
        self.part_num_edit.textChanged.connect(self.onTextChanged)

        self.qty_edit = QLineEdit()
        self.qty_edit.setPlaceholderText("Ex. 1")
        self.qty_edit.textChanged.connect(self.onTextChanged)
        
        layout.addWidget(self.part_num_label)
        layout.addWidget(self.part_num_edit)
        layout.addWidget(self.qty_label)
        layout.addWidget(self.qty_edit)
        layout.addWidget(self.done_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)
        self.setFixedWidth(600)
        self.onTextChanged()

        self.result = ''

    # Event that is raised when the user completes the form
    def done_clicked(self):
        self.accept()
        self.part_num = self.part_num_edit.text()
        self.qty = self.qty_edit.text()


    # Cancels the form when cancel is pressed
    def cancel_clicked(self):
        self.reject()
        self.result = ''
        
    # Runs checks on input data any time they are changed
    def onTextChanged(self):
        # Enable or disable Remove and Edit buttons based on item selection
        if self.part_num_edit.text() == '' or self.qty_edit.text() == '':
            self.done_button.setEnabled(False)
        else:
            self.done_button.setEnabled(True)

class NewBinDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("New Bin")

        layout = QVBoxLayout()

        self.done_button = QPushButton("Add Bin")
        self.done_button.clicked.connect(self.done_clicked)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_clicked)

        self.bin_num_label = QLabel("Bin #:")

        self.bin_num_edit = QLineEdit()
        self.bin_num_edit.setPlaceholderText("Ex. C27")
        self.bin_num_edit.textChanged.connect(self.onTextChanged)
        
        layout.addWidget(self.bin_num_label)
        layout.addWidget(self.bin_num_edit)
        layout.addWidget(self.done_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)
        self.setFixedWidth(600)
        self.onTextChanged()

        self.result = ''

    def done_clicked(self):
        bin_num_value = self.bin_num_edit.text()
        self.accept()
        self.result = bin_num_value

    def cancel_clicked(self):
        self.reject()
        self.result = ''

    def onTextChanged(self):
        if self.bin_num_edit.text() == '':
            self.done_button.setEnabled(False)
        else:
            self.done_button.setEnabled(True)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.save_bin_button = QPushButton("Save Bin")
        self.save_bin_button.clicked.connect(self.save_bin)
        self.save_bin_button.setEnabled(False)

        self.new_bin_button = QPushButton("New Bin")
        self.new_bin_button.clicked.connect(self.new_bin)
        self.new_bin_button.setEnabled(True)

        self.manual_input_button = QPushButton("Manual Input")
        self.manual_input_button.clicked.connect(self.manual_input)
        self.manual_input_button.setEnabled(False)

        self.bin_number_label = QLabel("Bin #: ")
        self.part_number_label = QLabel("Part #")
        self.qty_label = QLabel("QTY")

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.itemSelectionChanged.connect(self.on_item_selection_changed)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.new_bin_button)
        button_layout.addWidget(self.save_bin_button)
        button_layout.addWidget(self.manual_input_button)

        label_layout = QHBoxLayout()
        label_layout.addWidget(self.bin_number_label)

        listLabelsLayout = QHBoxLayout()
        listLabelsLayout.addWidget(self.part_number_label)
        listLabelsLayout.addWidget(self.qty_label)

        layout.addLayout(button_layout)
        layout.addLayout(label_layout)
        layout.addLayout(listLabelsLayout)
        layout.addWidget(self.list_widget)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Scan a barcode here...")
        self.input_field.returnPressed.connect(self.handle_return_pressed)
        layout.addWidget(self.input_field)

        self.input_field.setFocus()
        self.input_field.setEnabled(False)

        self.setLayout(layout)
        self.show()

    def handle_return_pressed(self):
        scanned_text = self.input_field.text()
        self.process_barcode(scanned_text)
        self.input_field.clear()

    def process_barcode(self, text):
        if text == '':
            return
        self.add_item(text)
    
    def add_item(self, num, count=0):
        for index in range(self.list_widget.count()):
            list_item = self.list_widget.item(index)
            part_widget = self.list_widget.itemWidget(list_item)
            
            if part_widget.part_number == num:
                if count != 0:
                    part_widget.qty = str(count)
                    part_widget.qty_label.setText(str(count))
                    return
                part_widget.qty = str(int(part_widget.qty) + 1)
                part_widget.qty_label.setText(part_widget.qty)
                return
        if count == 0:
            count = 1
        part = Part(num, count)
        list_item = QListWidgetItem()
        list_item.setSizeHint(part.sizeHint())
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, part)


    def save_bin(self):
        bin_num_str = self.bin_number_label.text().lstrip("Bin #: ")
        if bin_num_str == '':
            return
        with open(bin_num_str + ".csv", 'w') as f:
            f.write("bin,part,qty\n")
            for index in range(self.list_widget.count()):
                list_item = self.list_widget.item(index)
                part_widget = self.list_widget.itemWidget(list_item)
                f.write(bin_num_str + "," + part_widget.part_number + "," + part_widget.qty + "\n")

    def new_bin(self):
        self.save_bin()

        dialog = NewBinDialog()
        dialog.exec_()
        result = dialog.result
        if result == '':
            return
        self.bin_number_label.setText("Bin #: " + str(result))
        self.save_bin_button.setEnabled(True)
        self.manual_input_button.setEnabled(True)
        self.input_field.setEnabled(True)
        self.input_field.setFocus()
        self.list_widget.clear()
    
    def manual_input(self):
        dialog = ManualDialog()
        dialog.exec_()
        num = dialog.part_num
        qty = dialog.qty
        self.add_item(num, qty)

    def on_item_selection_changed(self):
        selected_items = self.list_widget.selectedItems()
        if len(selected_items) > 0:
            selected_item = selected_items[0]
        else:
            pass

        self.input_field.setFocus()


# If this is the main execution, run the main window
if __name__ == '__main__':
    # Creates window on connection
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    
