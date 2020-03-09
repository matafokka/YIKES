from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QRadioButton, QButtonGroup, QVBoxLayout, QHBoxLayout, QSpacerItem, QScrollArea
import xml.etree.ElementTree as ET
import csv
from .createHeading import createHeading


class YikesWidget(QWidget):
	"""Widget that actually solves the problem
	"""
	def __init__(self, root: ET.Element, resultsCsv: str):
		super().__init__()
		self.resultsCsv = resultsCsv

		# Flatten questions
		# I know about O(2n) in total, but eeeh, I wanna make parsing easier
		self.questions = []
		for child in root:
			if child.tag == "question-group":
				try: childIncludeIf = child.attrib["includeIf"]
				except KeyError: childIncludeIf = ""
				try: childExcludeIf = child.attrib["excludeIf"]
				except KeyError: childExcludeIf = ""
				
				for question in child:
					try: questionIncludeIf = question.attrib["includeIf"]
					except KeyError: questionIncludeIf = ""
					includes = childIncludeIf + " " + questionIncludeIf
					if includes != " ": question.set("includeIf", includes)

					try: questionExcludeIf = question.attrib["excludeIf"]
					except KeyError: questionExcludeIf = ""
					excludes = childExcludeIf + " " + questionExcludeIf
					if excludes != " ": question.set("excludeIf", excludes)

					self.questions.append(question)
			elif child.tag == "question": self.questions.append(child)

		# Compose UI
		widget = QWidget()
		self.sLayout = QVBoxLayout()
		widget.setLayout(self.sLayout)

		self.nameLabel = createHeading("")

		self.scrollArea = QScrollArea()
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setWidget(widget)
		
		self.nextButton = QPushButton("Next >>")
		self.nextButton.clicked.connect(self.readData)

		layout2 = QVBoxLayout()
		layout2.addWidget(self.nameLabel)
		layout2.addWidget(self.scrollArea)
		layout2.addWidget(self.nextButton)
		self.setLayout(layout2)
	
	def show(self):
		self.tags = {}
		self.iterator = iter(self.questions)
		self.nameLabel.show()
		self.nextButton.show()
		self.createPage()
		super().show()
		
	def createPage(self):
		# Clear previous widgets
		self.clearLayout()

		# Get question
		try: element = next(self.iterator)
		except StopIteration:
			self.showResults()
			return
		
		# Check if we should exclude this question

		doExclude = True
		includeIf = element.get("includeIf")
		if includeIf != None:
			for tag in includeIf.split():
				try:
					self.tags[tag]
					doExclude = False
					break
				except KeyError: pass
		else: doExclude = False
		
		excludeIf = element.get("excludeIf")
		if excludeIf != None and not doExclude:
			for tag in excludeIf.split():
				try:
					self.tags[tag]
					doExclude = True
					break
				except KeyError: pass

		if doExclude: return self.createPage()

		# Create page
		self.nameLabel.setText(element.find("title").text)
		
		# Create answers
		self.buttonGroup = QButtonGroup()
		for answer in element.findall("answer"):
			isBreaking = True
			if answer.get("breaking") == None:
				isBreaking = False

			radio = QRadioButton(answer.find("title").text)
			tags = {}
			for tag in answer.findall("tag"):
				tags.update({tag.text: None})
			radio.setProperty("tags", tags)
			radio.setProperty("isBreaking", isBreaking)
			self.buttonGroup.addButton(radio)
			self.sLayout.addWidget(radio)
		self.sLayout.itemAt(0).widget().setChecked(True)
		self.sLayout.addStretch()

	def readData(self):
		button = self.buttonGroup.checkedButton()
		self.tags.update(button.property("tags"))
		if button.property("isBreaking"): self.showResults()
		else: self.createPage()

	def showResults(self):
		self.clearLayout()
		self.nameLabel.setText("Here are your results:")
		self.nextButton.hide()
		
		results = csv.reader(open(self.resultsCsv))
		for result in results:
			res = dict.fromkeys(result) # For O(1) for get, resulting in O(n) istead of O(mn) when checking
			containsTag = True
			for tag in self.tags:
				if tag[0] == "_": continue
				try: res[tag]
				except KeyError:
					containsTag = False
					break
			if not containsTag: continue
			nameLabel = createHeading(result[0])
			nameLabel.setWordWrap(True)
			textLabel = QLabel(result[1])
			textLabel.setWordWrap(True)

			self.sLayout.addWidget(nameLabel)
			self.sLayout.addWidget(textLabel)

		if self.sLayout.count() == 0:
			failLabel = QLabel("No results have been found. Please, try again with different answers or report this incident to the problem's author.")
			failLabel.setWordWrap(True)
			self.sLayout.addWidget(failLabel)
		
		self.sLayout.addStretch()

	def clearLayout(self):
		while True:
			item = self.sLayout.takeAt(0)
			if item == None: break
			if not isinstance(item, QSpacerItem): item.widget().deleteLater()

