# main.py

import ply.lex as plex
from my_utils import slurp
from tabulate import tabulate
import pandas as pd


class Converter:
    tokens = ("WORD", "NEWLINE", "QUOTES", "COMMENT")

    t_ANY_ignore = ""
    t_ignore = ","

    def t_ANY_error(self, t):
        print(f"Unexpected token {t.value[:11]}")
        exit(1)

    def t_COMMENT(self, t):
        r"\#.*\n"
        pass

    def t_QUOTES(self, t):
        r'"[^"]+"'
        t = t.value.strip()
        self.list_lines.insert(self.count_words, t)  # Inserting each word read into the lines list
        self.count_words += 1
        pass

    def t_WORD(self, t):
        r"[^,\n]+"
        t = t.value.strip()
        self.list_lines.insert(self.count_words, t)  # Inserting each word read into the lines list
        self.count_words += 1
        pass

    def t_NEWLINE(self, t):
        r"\n"
        num = self.counts
        final_list = self.list_lines.copy()  # Copying the lines list
        self.list_col.insert(num, final_list)  # Insert lines list in the main list
        self.counts = self.counts + 1
        self.list_lines.clear()
        self.count_words = 0
        pass

    def t_eof(self, t):
        num = self.counts
        final_list = self.list_lines.copy()
        self.list_col.insert(num, final_list)
        self.counts = self.counts + 1

    def __init__(self, filename):
        self.lexer = None
        self.filename = filename
        self.list_lines = []  # List that holds the file lines
        self.list_col = []  # List that holds all the line lists
        self.counts = 0
        self.count_words = 0

    def toc(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)
        self.lexer.input(slurp(self.filename))

        for token in iter(self.lexer.token, None):
            pass

        f1 = open("list1.html", "w")  # Creating files to output results
        f2 = open("list1.tex", "w")

        pos = 0
        new_list = []  # Temporarily holds one of the columns selected
        final_list = []  # Holds all of the columns selected
        table = []  # Copy of the last list, to convert into HTML LATEX

        print("MENU")
        print("1-Choose columns to include in output;")
        print("2-Output the entire file;")
        print("0-Exit.")

        choice = input()

        if int(choice) == 1:
            num = int(input("How many columns to show?: "))
            j = 0
            while j < num:
                column = input("Which column to show?: ")
                i = 0
                for x in self.list_col[0]:  # Search for columns index
                    if x == column:
                        print(x)
                        pos = i
                    i += 1
                for x in self.list_col:  # Save every item in the index given before
                    new_list.append(x[pos])
                    final_list.append(new_list)
                final_list = new_list.copy()
                new_list.clear()
                table.append(final_list)
                j += 1
            chosen = pd.DataFrame(table).T.values.tolist()  # Transposing the Matrix
            f1.write(tabulate(chosen, tablefmt='html'))
            f2.write(tabulate(chosen, tablefmt='tex'))
        if int(choice) == 2:
            f1.write(tabulate(self.list_col, tablefmt='html'))
            f2.write(tabulate(self.list_col, tablefmt='tex'))

        print("Processing finished!")


main = Converter("list1.csv")
main.toc()

