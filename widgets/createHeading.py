from PyQt5.QtWidgets import QLabel

def createHeading(text: str):
	"""Creates QLabel heading with given text
	"""
	label = QLabel(text)
	label.setWordWrap(True)
	font = label.font()
	font.setBold(True)
	font.setPointSizeF(font.pointSize() * 1.3)
	label.setFont(font)
	return label
