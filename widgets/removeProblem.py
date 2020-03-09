from PyQt5.QtWidgets import QMessageBox
import shutil
import os.path

def removeProblem(dir: str):
	"""Removes problem with all handlers inside.
	"""
	msg = QMessageBox(QMessageBox.Warning, "Are you sure you want to delete this problem?", "Are you sure you want to delete this problem? This cannot be undone!")
	msg.addButton(QMessageBox.No)
	yesButton = msg.addButton(QMessageBox.Yes)
	msg.exec()
	
	if msg.clickedButton() == yesButton:
		shutil.rmtree(dir, onerror=onDeleteError)
		return True
	return False

def onDeleteError(function, path, excinfo):
	if excinfo[0] != PermissionError:
		return

	msg = QMessageBox(QMessageBox.Critical, "Can't remove problem", excinfo[1].strerror + "\nPlease, delete the following directory manually:\n" + os.path.normpath(path))
	msg.exec()
