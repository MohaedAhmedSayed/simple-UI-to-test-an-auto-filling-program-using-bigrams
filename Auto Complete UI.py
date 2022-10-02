import tkinter as tk
import re
from tkinter import END

window = tk.Tk()
window.title("google")
window.geometry("1000x1000")
font=('Times',20,'bold')
inp=tk.StringVar()
inputbox=tk.Entry(window,font=font,textvariable=inp)
inputbox.place(x=500, y=500)
listsug=tk.Listbox(window,height=5,font=font, relief='flat',bg='white')
listsug.place(x=500, y=550)
import nltk
from nltk.corpus import gutenberg
book = list(gutenberg.words())
book = book[:200000]
text = []
signs = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@',
         '[', ']', '^', '_', '`', '{', '|', '}', '~', "''", "``", "--", "?."]
for word in book:
    if word not in signs:
        text.append(word)
# print(len(book))
# print(len(text))
#####################################################33
from nltk.probability import FreqDist
fdist = FreqDist()
for word in text:
    fdist[word.lower()] += 1
# print(len(fdist))
########################################################
bigram = nltk.bigrams(text)
bifdist = FreqDist()
for biword in bigram:
    bifdist[(biword[0].lower(), biword[1].lower())] += 1
def click(my_widget): # On selection of option
    my_w = my_widget.widget
    index = int(my_w.curselection()[0]) # position of selection
    value = my_w.get(index) # selected value
    inp.set(value) # set value for string variable of Entry
    listsug.delete(0,END)     # Delete all elements of Listbox
def enter(my_widget): # down arrow is clicked
    listsug.focus()  # move focus to Listbox
    listsug.selection_set(0) # select the first option

def complete(*args):

    ########################################
    searchWord = inputbox.get()
    words1 = [i[0] for i in list(bifdist.keys())]
    words2 = [i[1] for i in list(bifdist.keys())]
    # print(len(words1))
    wordi = []
    iw = 0
    while iw < len(words1):
        if searchWord in words1[iw:]:
            iw = words1.index(searchWord, iw)
            wordi.append(iw)
            iw += 1
        else:
            break
    found = dict()
    for i in wordi:
        found[(words1[i], words2[i])] = bifdist[(words1[i], words2[i])]
    f = FreqDist(found)
    for i in f.keys():
        f[i] /= fdist[searchWord]
    output = [i[0][1] for i in f.most_common(10)]
    listsug.delete(0, END)  # Delete all elements of Listbox
    for c in output:
        listsug.insert(END,c)
    # print(f.most_common(10))
inputbox.bind('<Down>', click) # down arrow key is pressed
listsug.bind('<Return>', enter)# return key is pressed





inp.trace('w',complete)
window.mainloop()