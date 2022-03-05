# GoodReadsWebScraper
Welcome to the book recommender!
A small tool that will start off from book link (off goodreads) and look in the recommended books and the recommended books of those books and so on and compile the data in a single place.It has the option to cross reference this to your own library

Intended use:
Whenever you read a great book and you don't know where to go next.
Whenever you are too sick of navigating Goodreads to see what they recommend, if you have read it, compare rating, ensure the number of raters is representative and other self imposed criteria
The tool brings everything in one place for you to better decide

Inputs necessary:
-The goodreads link to the initial book (do not use the link with search terms, the book link should be clean-https://goodreads/show/bookNo-/.Name)
-Output folder (a .csv file will be created with the name of the title of your original book)
-Depth (0 is the book itself, 1 is the 20 recommended books of your initial start point, 2 is the 20 recommended books of each of the 20 recommended books of your initial start and so on)
-(OPTIONAL) You can uplod your own Goodreads library. The program will search and mark what books from the compiled list you read or want to read (currently reading is overkill since you know what you are reading)
*To get your library from Goodreads, go to goodreads.com, sign in to your account, click on "My books" from the top bar, on your left there is a "Import and export" link. Once there, click on "Export Library" and that should generate a file that the tool can use.

Click on Start and away you go!!


Notes and observations:
This is a very basic algorithm, with some logging and error handling involved but nowhere near the levels required for a real tool.
*The tool has duplication removal baked in. If a book is visited twice, it will only appear once in the output
Whenever the tool encounters a field it cannot read for whatever reason (like the synopsys or series or others), it will gracefully throw away that book and carry on.
This could lead to some great gems getting missed but will guarantee that the other few hundreds (at depth 2 and beyond) get captured.
The current fields getting exported to the .csv are my own, very crude criteria. Other fields will be added in the future

Future developments:
-Ensuring all books belong to the same genre or an option to go across multiple genres
-Min number of reviewers/raters
-Other output fields to allow for other criteria

