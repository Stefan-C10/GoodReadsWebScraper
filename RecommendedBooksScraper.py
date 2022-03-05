# This is a sample Python script.
import csv
import pathlib
import os
import sys
import requests
import re
import tkinter as tk
from datetime import datetime
from _csv import reader
from itertools import chain
from bs4 import BeautifulSoup
from tkinter import filedialog
from tkinter import ttk
global window


def CleanText(text):
    text=text.replace('\n','')
    text=text.strip()
    return text

class Log():
    def __init__(self):
        self.FilePath = os.path.join(os.getcwd(), "Log.log")
        with open(self.FilePath, 'w',encoding="utf8") as file:
            file.close()

    def Log(self, message):
        with open(self.FilePath, 'a', newline='', encoding="utf8") as file:
            file.write(message+"\n")



class book():
    def __init__(self, url,depth, Log):
        self.Log=Log
        self.URL = ""
        self.Title = ""
        self.Series = ""
        self.NoInSeries = 0.0
        self.Author = []
        self.Rating = 0.0
        self.NoRaters = 0
        self.NoReviewers = 0
        self.Synopsys = ""
        self.Depth = 0
        self.RecommendedLinks=[]
        self.bookID = ""
        self.Status="Unread"
        self.Genres=[]
        page = requests.get(url)
        if (url.find("-")>url.rfind(".")):
            self.bookID = url[url.rfind("/") + 1:url.find("-")]
        else:
            self.bookID = url[url.rfind("/")+1:url.rfind(".")]
        self.soup = BeautifulSoup(page.content, 'html.parser')
        self.populate_all_book_fields()

    def __iter__(self):
        return iter([self.bookID, self.Depth,self.Title, self.NoInSeries,self.Series,self.Author,self.Status,self.Rating,self.NoRaters, self.NoReviewers, self.Genres, self.Synopsys])

    def __eq__(self, other):
        return self.bookID == other.bookID \
               and self.Title == other.Title

    def __hash__(self):
        return hash(('bookID', self.bookID,
                     'title', self.Title))

    def find_recommended(self):
        results = self.soup.find_all("li", {"class": "cover"})
        self.RecommendedLinks.extend([str(li.find('a')['href']) for li in results])

    def populate_all_book_fields(self):
        #Get book title
        try:
            divTitle=self.soup.find("div", {"id" :"metacol"})
            self.Title = CleanText(divTitle.find("h1",{"id" : "bookTitle"}).get_text())
        except:
            e = sys.exc_info()[0]
            self.Log.Log("Title could not be read. Error:" + str(e)+"\n")
        #Get book series
        try:
            FullSeries = CleanText(divTitle.find("h2",{"id" : "bookSeries"}).get_text())
            index=FullSeries.find('#')
            self.Series=FullSeries[1:index-1]
            self.NoInSeries = FullSeries[index:len(FullSeries) - 1]
        except:
            e = sys.exc_info()[0]
            self.Log.Log("BookSeries could not be read for book "+self.Title+". Error:" + str(e)+"\n")
        #Get book author
        try:
            [self.Author.append(CleanText(i.get_text())) for i in self.soup.find("div", {"id": "bookAuthors"}).find_all("span", itemprop="name")]
        except:
            e = sys.exc_info()[0]
            self.Log.Log("Author could not be read for book " + self.Title + ". Error:" + str(e)+"\n")
        #Get book rating and no. of raters and reviewers
        try:
            self.Rating = float(re.sub("[a-zA-Z]+","",CleanText(self.soup.find("span", itemprop="ratingValue").get_text())))
            self.NoRaters = int(re.sub("[a-zA-Z,]+","",CleanText(self.soup.find(itemprop="ratingCount").get_text())))
            self.NoReviewers = int(re.sub("[a-zA-Z,]+","",CleanText(self.soup.find(itemprop="reviewCount").get_text())))
        except:
            e = sys.exc_info()[0]
            self.Log.Log(" Book Rating and Rating and Reviewers could not be read for book " + self.Title + ". Error:" + str(e)+"\n")
        #Get book synopsis
        try:
            self.Synopsys=CleanText(self.soup.find("div", {"id": "descriptionContainer"}).find("div",{"id":"description"}).find("span", {"style" : "display:none"}).get_text())
        except:
            e = sys.exc_info()[0]
            self.Log.Log("Synopsis could not be read for book " + self.Title + ". Error:" + str(e)+"\n")

        #Get book recommended links
        try:
            self.find_recommended()
        except:
            e = sys.exc_info()[0]
            self.Log.Log("Recommended books could not be read for book " + self.Title + ". Error:" + str(e)+"\n")
        try:
            shelvesContainer = self.soup.find('div', class_='rightContainer').find_all('a', class_='actionLinkLite bookPageGenreLink')
            for cont in shelvesContainer:
                self.Genres.append(cont.text)


        except:
            e = sys.exc_info()[0]
            self.Log.Log("Genres could not be read for book " + self.Title + ". Error:" + str(e)+"\n")



class GUI:
    def __init__(self, window):
        self.Log=Log()
        self.CollectionFile=""
        self.CollectionRead=[]
        self.CollectionToRead=[]
        self.window=window
        self.window.title("Welcome to the Goodreads Recommended Books scraper")
        # BookURL
        L_BookURL = tk.Label(text="Please copy the book's URL from goodreads:")
        L_BookURL.grid(row=1, column=1)
        self.EntryURL = tk.Entry()
        self.EntryURL.grid(row=1, column=2, columnspan=2, sticky="W")
        # FolderPath
        L_FolderPath = tk.Label(text="Please select the folder where to generate the .csv file")
        L_FolderPath.grid(row=2, column=1)
        self.OutputFileBase = tk.StringVar()
        self.OutputFileBase.set("This field will populate when a folder is selected")
        button1 = tk.Button(text="Browse output folder", command=self.GetFolderLocation)
        button1.grid(row=2, column=2)
        O_FolderPath = tk.Label(textvariable=self.OutputFileBase)
        O_FolderPath.grid(row=2, column=3)
        #Depth
        L_Depth = tk.Label(text="Depth of book recommendation(0-The book,\n1-Recommended of initial book (30sec),\n 2-Recommended of Recommended of initial book(Approx 18 mins)\n 3-Rec of Rec of Initial(May the gods have mercy on your RAM time) etc)")
        L_Depth.grid(row=3, column=1)
        self.Depth = tk.Entry()
        self.Depth.grid(row=3, column=2)
        #Collection
        self.OwnCollection=tk.StringVar()
        L_OwnCollection = tk.Label(text="(OPTIONAL) Upload your Goodreads library to have books marked as read/to-read")
        L_OwnCollection .grid(row=4, column=1)
        I_OwnCollection = tk.Button(window,text="Browse Files",command=self.browseFiles)
        I_OwnCollection.grid(row=4,column=2)
        O_OwnCollection=tk.Label(textvariable=self.OwnCollection)
        O_OwnCollection.grid(row=4, column=3)
        self.OwnCollection.set("X")
        # Start button
        button2 = tk.Button(text="Start", command=self.GetRecommendedBooks,fg='green')
        button2.grid(row=3, column=3,columnspan=2)

        # Separator
        separator = ttk.Separator(window, orient='horizontal')
        separator.grid(row=5, columnspan=4, sticky="ew")
        # Updated during runtime
        L_BookTitle = tk.Label(text="Book title:")
        L_BookTitle.grid(row=6, column=1)
        # I_BookURL = tk.Label(textvariable=StartBook)
        self.StartBook = tk.StringVar()
        I_BookURL = tk.Label(textvariable=self.StartBook)
        self.StartBook.set("Title will populate when the algorithm starts")
        I_BookURL.grid(row=6, column=2, columnspan=2, sticky="W")
        self.FunctionalUpdates = tk.StringVar()
        L_Updates = tk.Label(textvariable=self.FunctionalUpdates)
        L_Updates.grid(row=7, columnspan=4, sticky="W")

    #Window resources
    def GetFolderLocation(self):
        file = filedialog.askdirectory()
        self.OutputFileBase.set(str(file))
    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir=self.OutputFileBase,
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.csv*"),
                                                         ("all files",
                                                          "*.*")))
        if (filename!=""):
            self.CollectionFile=filename
            self.StoreCollection()
            self.OwnCollection.set("✓")


    def StoreCollection(self):
        if (self.CollectionFile!=""):
            with open(self.CollectionFile,'r',encoding="utf8") as csv_source:
                csv_reader = reader(csv_source)
                header = next(csv_reader)
                try:
                    for line in csv_reader:
                        if line[18]=="read":
                            self.CollectionRead.append(line[0])
                        else:
                            self.CollectionToRead.append(line[0])
                except:
                    e = sys.exc_info()[0]
                    message="Own collection could not be read. Error:"+e
                    self.FunctionalUpdates.set(message)
                    self.Log.Log(message)

    def CheckIfRead(self, book):
        if (book.bookID in self.CollectionRead):
            book.Status="Read"
        else:
            if (book.bookID in self.CollectionToRead):
                book.Status = "Want to Read"

    def GetRecommendedBooks(self):
        self.FunctionalUpdates.set("The program started")
        self.Log.Log("The program started"+"\n")
        root = book('https://www.goodreads.com/en/book/show/37534869-zero-sum-game', 0,self.Log)
        #root = book(self.EntryURL.get(), 0, self.Log)
        List = []
        List.append(root)
        ToVisit = root.RecommendedLinks
        self.StartBook.set(str(root.Title))
        window.update()
        VisitedLinks = set()
        index = 0
        FinalString=""
        message=""
        #CreateOutputFile
        self.OutputFile = pathlib.Path(self.OutputFileBase.get(), self.StartBook.get()+".csv")
        try:
            with open(self.OutputFile, 'w', encoding="utf8") as csv_file:
                csv_file.close()
        except:
            self.FunctionalUpdates.set("ERROR:The file you are trying to write to is open in another program, please close that before clicking start again!")
            return False

        while (index < int(self.Depth.get())):
            NewList = []
            start = datetime.now()
            for enum, i in enumerate(ToVisit):
                if not i in VisitedLinks:
                    print("At depth " + str(index+1) + " current book " + str(enum) + " of " + str(len(ToVisit)))
                    try:
                        new = book(i, index, self.Log)
                        message="At depth " + str(index+1) + " current book is " + str(new.Title) + " number " + str(enum+1) + " of " + str(len(ToVisit)) + ". Continuing to next book...\n"
                        self.FunctionalUpdates.set(message)
                        self.Log.Log(message)
                        self.window.update()
                        self.CheckIfRead(new)
                        List.append(new)
                        VisitedLinks.add(i)
                        NewList.extend(new.RecommendedLinks)
                    except:
                        e = sys.exc_info()[0]
                        message ="At depth " + str(index) + " book number " + str(enum) + " of " + str(len(ToVisit))+ " abandoned due to problems with HTML. Error was "+str(e)+"\n"
                        self.FunctionalUpdates.set(message)
                        self.Log.Log(message)
            end = datetime.now()
            elapsedtime = str((end-start).total_seconds()/60)
            FinalString=FinalString+"Depth"+str(index+1)+" took " + elapsedtime +" minutes \n"
            index += 1
            ToVisit = NewList
        message=str(self.FunctionalUpdates.get()) + "\n" + "Finished processing\nEnd of runtime"
        self.FunctionalUpdates.set(message)
        self.Log.Log(message)
        self.write_to_file(sorted(List, key=lambda x: x.Rating, reverse=True))
        print(FinalString)


    def write_to_file(self,Booklist):
        try:
            with open(self.OutputFile, 'a', newline='', encoding="utf8") as csv_file:
                wr = csv.writer(csv_file, delimiter=',')
                heading = ["Index","BookID", "Depth", "Title", "Number in Series", "Series", "Authors", "Read","Rating",
                           "Number of Raters", "Number of Reviewers", 'Genres', "Synopsys"]
                wr.writerow(heading)
                for enum,cdr in enumerate(Booklist):
                    result=chain([str(enum)],list(cdr))
                    wr.writerow(list(result))
        except:
            self.FunctionalUpdates.set(
                "ERROR:The file you are trying to write to is open in another program, please close that before clicking start again!")


if __name__ == '__main__':
    #print_hi('PyCharm')
    window = tk.Tk()
    my_GUI=GUI(window)

    window.mainloop()


