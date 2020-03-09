from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QMessageBox
import xml.etree.ElementTree as ET
from .YikesWidget import YikesWidget
from .createHeading import createHeading
from .removeProblem import removeProblem
import os.path

class YikesPreview(QWidget):
	"""Widget containing preview of the problem.
	"""
	def __init__(self, icon, root: ET.Element, resultsCsv: str):
		super().__init__()

		name = root.find("name").text
		description = root.find("description").text
		if name == None:
			name = "Unnamed"
		if description == None:
			description = "No description available"

		self.yikesWidget = YikesWidget(root, resultsCsv)
		self.yikesWidget.setWindowTitle("YIKES - " + name)
		self.yikesWidget.setWindowIcon(icon)

		layout = QVBoxLayout()

		# Add name
		layout.addWidget(createHeading(name))

		# Add description
		label = QLabel(description)
		label.setWordWrap(True)
		layout.addWidget(label)

		# Add buttons
		self.startButton = QPushButton("Start")
		self.startButton.clicked.connect(self.yikesWidget.show)
		self.editButton = QPushButton("Edit")
		self.deleteButton = QPushButton("Delete")
		self.deleteButton.clicked.connect(lambda: self.removeProblem(os.path.normpath(resultsCsv + "/..")))

		buttonsLayout = QHBoxLayout()
		buttonsLayout.addWidget(self.startButton)
		#buttonsLayout.addWidget(self.editButton)
		buttonsLayout.addWidget(self.deleteButton)

		layout.addLayout(buttonsLayout)
		self.setLayout(layout)

	def removeProblem(self, dir):
		if removeProblem(dir):
			self.deleteLater()
