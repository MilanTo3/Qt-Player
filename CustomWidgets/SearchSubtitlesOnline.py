from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QTableWidget, QTableWidgetItem, QLineEdit, QFileDialog
from bs4 import BeautifulSoup, PageElement
import requests, re, os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from CustomWidgets.StyledButton import StyledButton

class SearchSubtitlesOnline(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def startSearching(self):

        if self.edit.text() == "":
            self.statusLabel.setText("Please specify a search term.")
            return

        self.mediaName : str = self.edit.text().replace(" ", "%")
        self.baseSearchUrl = "https://www.podnapisi.net/sr/subtitles/search/?keywords=" + self.mediaName
        self.sourcehtmlpage = requests.get(self.baseSearchUrl, verify=False)
        self.plaintext = self.sourcehtmlpage.text
        if self.plaintext == "":
            self.close()
        self.soup = BeautifulSoup(self.plaintext)
        try:
            self.numOfPages = len(self.soup.find("ul", { "class": "pagination pagination-right" }).find_all("li")) - 2
        except:
            self.statusLabel.setText("No subtitles found.")
            return

        self.colheaders = []
        self.rowEntries = []
        self.processedEntries : [EntryClass] = []

        if self.numOfPages < 2:
            self.subTitlesTable = self.soup.find("table", { "class": "table table-striped table-hover" })
            self.rowEntries = self.subTitlesTable.find("tbody").find_all("tr")
        else:
            i : int = 1
            while i != self.numOfPages:
                self.baseSearchUrl = "https://www.podnapisi.net/sr/subtitles/search/?keywords=" + self.mediaName + "&page=" + str(i)
                self.sourcehtmlpage = requests.get(self.baseSearchUrl, verify=False)
                self.plaintext = self.sourcehtmlpage.text
                if self.plaintext == "":
                    self.close()
                self.soup = BeautifulSoup(self.plaintext)
                self.subTitlesTable = self.soup.find("table", {"class": "table table-striped table-hover"})
                self.rowEntries.extend(self.subTitlesTable.find("tbody").find_all("tr"))
                i = i + 1

        self.processEntries(self.rowEntries)

    def processEntries(self, listOfEntries):

        for pageElement in listOfEntries:
            temp = EntryClass()
            try:
                resultCells = pageElement.find_all("td")
                temp.title = resultCells[0].find("span", {'class', 'release'}).text
                temp.link = resultCells[0].find_next("a").attrs.get("href")
                temp.framesPerSeconds = resultCells[1].find_next("a").text
                temp.language = resultCells[3].find("span").text
                try:
                    temp.author = resultCells[4].find("a").text
                except:
                    temp.author = "Unknown"
                temp.numOfTimesDownloaded = resultCells[5].text
                temp.grade = resultCells[7].find("div", {"class": "progress rating"}).attrs.get("data-title")
                temp.madeOn = resultCells[8].find("span").text
                self.processedEntries.append(temp)
            except: pass
            self.drawProcessedEntries()

    def initUI(self):

        p = QPalette()
        p.setColor(QPalette.Window, QColor("#FF69B4"))
        p.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(p)
        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.edit = QLineEdit()
        self.titleLabel = QLabel("This dialog enables you to search for subtitles online. They will be downloaded in this apps folder, if you dont provide a path to save the subs.")
        self.statusLabel = QLabel("Status: ")
        self.urlPath = QLabel("Url path:")
        self.url = ""
        self.searchBtn = StyledButton("Search")
        self.downloadSelectionBtn = StyledButton("Download checked subs")
        self.downloaddIRPATH = StyledButton("Set download path.")
        self.cancelBtn = StyledButton("Cancel")
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["", "Title", "Frames per Seconds", "Language", "Author", "Num of Times Downloaded", "Grade", "Made on", "Select for download"])
        self.hbox1.addWidget(self.edit)
        self.hbox1.addWidget(self.searchBtn)
        self.hbox2.addWidget(self.downloadSelectionBtn)
        self.hbox2.addWidget(self.cancelBtn)
        self.hbox3.addWidget(self.downloaddIRPATH)
        self.hbox3.addWidget(self.urlPath)
        self.table.hideColumn(0)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(8, 140)
        self.vbox.addWidget(self.titleLabel)
        self.vbox.addWidget(self.statusLabel)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addWidget(self.table)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox2)
        self.setGeometry(0, 0, 1000, 400)
        self.searchBtn.clicked.connect(self.startSearching)
        self.cancelBtn.clicked.connect(self.cancelDialog)
        self.downloadSelectionBtn.clicked.connect(self.startDownload)
        self.downloaddIRPATH.clicked.connect(self.setDirectoryPath)
        self.setLayout(self.vbox)
        self.setStyleSheet("QLabel{ font-weight: bold; color: white; }")
        self.table.setStyleSheet("QTableWidget{ font-weight: bold; }")

    def drawProcessedEntries(self):

        self.statusLabel.setText("Drawing entries...")
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.processedEntries) + 1)
        processedEntri = self.processedEntries
        entry : EntryClass
        i = 0
        for entry in processedEntri:
            self.table.setItem(i, 0, QTableWidgetItem("https://www.podnapisi.net" + entry.link))
            self.table.setItem(i, 1, QTableWidgetItem(entry.title))
            self.table.setItem(i, 2, QTableWidgetItem(entry.framesPerSeconds.replace(" ", "").replace("\n", "")))
            self.table.setItem(i, 3, QTableWidgetItem(entry.language))
            self.table.setItem(i, 4, QTableWidgetItem(entry.author.replace(" ", "").replace("\n", "")))
            self.table.setItem(i, 5, QTableWidgetItem(entry.numOfTimesDownloaded.replace(" ", "").replace("\n", "")))
            self.table.setItem(i, 6, QTableWidgetItem(entry.grade))
            self.table.setItem(i, 7, QTableWidgetItem(entry.madeOn.replace(" ", "").replace("\n", "")))
            checkBoxItem = QTableWidgetItem()
            checkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkBoxItem.setCheckState(Qt.Unchecked)
            self.table.setItem(i, 8, checkBoxItem)
            i = i + 1
        self.statusLabel.setText("Found " + str(len(self.processedEntries)) + " subtitles")

    def startDownload(self):

        self.statusLabel.setText("Download started...")
        column = 8
        linkList = []
        for row in range(self.table.rowCount()):
            # item(row, 0) Returns the item for the given row and column if one has been set; otherwise returns nullptr.
            _item = self.table.item(row, column)
            if _item:
                item = self.table.item(row, column).checkState()
                if item == 2:
                    linkList.append(self.table.item(row, 0).text())

        for link in linkList:
            result = requests.get(link, verify=False)

            fname = "Subtitle"
            if "Content-Disposition" in result.headers.keys():
                fname = re.findall("filename=(.+)", result.headers["Content-Disposition"])[0]

            with open(self.url + "/" + fname.replace('"', ''), "wb") as f:
                f.write(result.content)

        self.statusLabel.setText("Files downloaded.")

    def setDirectoryPath(self):

        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file != "":
            self.url = file
            self.urlPath.setText(file)

    def cancelDialog(self):
        self.accept()

class EntryClass():

    def __init__(self):

        self.link = ""
        self.title = ""
        self.framesPerSeconds = 0
        self.language = ""
        self.author = ""
        self.numOfTimesDownloaded = 0
        self.grade = 0
        self.madeOn = ""