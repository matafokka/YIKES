"""
YIKES 
Copyright (C) 2020 matafokka

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

"""

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QVBoxLayout, QScrollArea, QFrame, QPushButton
from PyQt5.QtGui import QIcon
from widgets import YikesPreview, removeProblem
from sys import argv, exit
import xml.etree.ElementTree as ET
import os.path


class MainWindow(QScrollArea):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("YIKES")
		logoIcon = QIcon("img/logo.ico")
		self.setWindowIcon(logoIcon)
		
		# Parse problems
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)

		problemsPath = os.path.dirname(os.path.abspath(__file__)) + "/problems/"
		for problem in os.listdir(problemsPath):
			pPath = problemsPath + "/" + problem
			questionFile = pPath + "/questions.xml"
			resultsFile = pPath + "/results.csv"
			try:
				f = open(resultsFile) # If there is no results file, pass this problem
				tree = ET.parse(questionFile)
			except FileNotFoundError:
				continue
			except ET.ParseError as e:
				msg = QMessageBox(QMessageBox.Critical,
					"Can't parse file",
					"Can't parse file: " + os.path.normpath(questionFile) + "\n\nFollowing error has occured:\n\t" + e.msg + "\n\nPlease try:\n\tContacting the author of the problem and hoping that they can solve it.\n\tCorrecting this error by manualy editing the XML file.\n\tDeleting directory (this will remove the problem): " + os.path.normpath(pPath)
					)
				deleteButton = QPushButton("Delete problem")
				deleteButton.clicked.connect(lambda: removeProblem(pPath))
				msg.addButton(deleteButton, QMessageBox.AcceptRole)
				msg.addButton(QMessageBox.Ignore)
				msg.setWindowIcon(logoIcon)
				msg.exec()
				continue
			finally:
				f.close()
			preview = YikesPreview(logoIcon, tree.getroot(), resultsFile)
			layout.addWidget(preview)
		layout.addStretch()

		widget = QWidget()
		widget.setLayout(layout)

		self.setFrameShape(QFrame.NoFrame)
		self.setWidgetResizable(True)
		self.setWidget(widget)
		self.resize(350, 350)

if __name__ == '__main__':
	app = QApplication(argv)
	window = MainWindow()
	window.show()
	exit(app.exec_())
