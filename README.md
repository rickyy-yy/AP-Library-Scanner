# 📖 APU Library Scanner

This program automatically scans the [APU library](https://library.apu.edu.my/apres/advanced-search) for papers that contain at least one keyword that you specify. Then it saves details of each paper into a .csv and .txt file. Will be useful for 2nd year students who are currently researching for their FYP. 

## ⤵️ Installation

Either download the repository as a .zip file and unzip it, or run the following command in command prompt:

```
git clone https://github.com/rickyy-yy/AP-Library-Scanner.git
cd AP-Library-Scanner
```

Then, use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements. Navigate to the directory containing requirements.txt and run the following. 

```bash
pip install -r requirements.txt
```

Alternatively, make sure the BeautifulSoup4 (bs4) and requests modules are installed in your environment. 

You can check if you have pip install by running the following in command prompt. It should return a version number.

```
pip --version
```

## ✅ Usage

Navigate to the directory containing the main.py file and run the following:

```python
python main.py
```

You will see this message appear:

```
Would you like to include all types of papers or only Undergraduate FYPs?
1) Only Undergraduate FYPs (Default)
2) Everything (Article, Book, Book Section, Monograph, Thesis, Diploma FYP, etc

Enter your choice:
```

Typing '2' and pressing Enter will include everything in the program's search. This includes:

- Articles
- Book
- Book Sections
- Monographs
- Conference or Workshop Items
- Diploma FYPs
- Theses
- Patents
- Compositions
- Undergraduate FYPs.

Typing any other character will default to only including Undergraduate FYPs in the search scope. 

## 📁 Results

You will be able to seeing the status of each page the program scans, as well as the keyword for any hits. As shown below:

```
Searching 425... No Keyword Found!
Searching 426... Keyword: "security" Found!
Searching 427... Keyword: "security" Found!
Searching 428... No Keyword Found!
```

The program will then save the following details to results.csv:

- Link to the library page
- Upload Date
- Title
- Author & TP Number
- Supervisor
- Number of Pages
- Publish Date
- Subject
- Keywords

Additionally, if the paper/item has an abstract/description, it will be saved to the Descriptions folder with its corresponding name to avoid taking up too much space in the .csv file. 

Both the Descriptions folder and results.csv will be created in the same directory as the main.py file.

## ⛔️ Errors

Some pages in between the set starting and ending numbers are not available. Therefore they won't return anything. When this happens, the program will output this message:

```
Page 550 returned an error. Retrying to make sure...
Page 550 most likely cannot be viewed by the public.
```

Sometimes the error message occurs because the website failed to load or we are being rate-limited. Therefore, the program will always try again once, to double-check. An error message like this may be shown:

```
Page 438 returned an error. Retrying to make sure...
Searching 438... Keyword: "security" Found!
```

Basically, all the errors should already be handled by the program. There is no need for you to re-run the program. 

## 🔍 Search Scope

The program current searches for items numbered 422 to 3782. If you discover a new upper or lower limit, please let me know by raising it as an issue through GitHub.
