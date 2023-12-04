
import pandas as pd
from tkinter import *



click_count = 0

data=pd.read_csv('df_price.csv',encoding = 'utf-8-sig') # read the data
data=data[data['price']>40].reset_index(drop=True) # drop unrelevant rows
key_word=['Bialetti','Moka','Venus','Rainbow','Ibily','Bahia','Makaccina','G.A.T'] # key woed


def similarity(str_1, str_2):
    """
    A function that computes the differences between two strings using recursive approach.
    Parameters:
        str_1 (str): The first input string. str_2 (str): The second input string.
    Returns:
        int: The number of differences between the two strings.
    """
    faults = 0
    if min(len(str_1), len(str_2)) == 0:  # if the len is 0 so
        return (faults + max(len(str_1),
                             len(str_2)))  # if one of them is empty so the difference will be the length of the max

    for i in range(min(len(str_1), len(str_2))):
        if str_1[i] != str_2[i]:
            faults += 1
            return (min(similarity(str_1[i + 1:], str_2[i:]) + faults, similarity(str_1[i:], str_2[i + 1:]) + faults,
                        similarity(str_1[i + 1:], str_2[i + 1:]) + faults))
    return (0 + abs(len(str_2) - len(str_1)))


def define_input(key_word, inp, criteria=0.3):
    """
    A function that extracts keywords from an input string based on their similarity to the input words.
    Parameters:
        key_word (list): A list of keywords to compare against the input.
        inp (str): The input string to analyze.
        criteria (float): The similarity threshold. Keywords with similarity below this threshold are excluded. Default is 0.3.

    Returns:
        list: A list of relevant keywords extracted from the input.
    """
    inp = inp.split()  # split the input by space
    list_of_impor = []  # create a new list
    for j in range(len(inp)):  # run about all the differrent word in the input
        l = [round(similarity(key_word[i].lower(), inp[j].lower()) / max(len(key_word[i]), len(inp[j])), 2) for i in
             range(len(key_word))]  # run on all the key word and applay simalrity on each 2
        list_of_impor.append((l.index(min(l)), min(l)))  # append the min value and is index

    list_of_impor = [list_of_impor[i] for i in range(len(list_of_impor)) if
                     list_of_impor[i][1] < criteria]  # check how is less from the criteria
    w = [key_word[list_of_impor[i][0]] for i in range(len(list_of_impor))]  # get the relevant word
    return (list(set(w)))  # return only unique word

def filter_data(data,filters):
    """
        Filters a dataset based on specified criteria.
        This function applies a series of filters to a dataset to extract only the relevant parts.
        Parameters:
            data (DataFrame): The dataset to be filtered.
            filters (list of str): A list of strings representing the filtering criteria.
        Returns:
            DataFrame: A subset of the original dataset, filtered according to the specified criteria,
                       with the index reset.

        """
    if len(filters)==0: return(data) # basic case that I don't need any filter
    s=''
    for i in range(len(filters)):
        s=s+filters[i]+'|' if i+1<len(filters) else s+filters[i]

    return data[data['description'].str.contains(s)].reset_index(drop=True)


def find_price_c_limit(inp):
    """
    A function that extracts price and the number of people from an input string.
    Parameters:
        inp (str): The input string to analyze.
    Returns:
        list: A list containing either the price and the number of people or just the number of people.
    """
    inp = inp.split()
    numbers = [float(inp[i]) for i in range(len(inp)) if inp[i].isdigit()]
    # if max(numbers)>30: return(max(numbers))
    if len(numbers) > 1:
        if max(numbers) > 30:

            return ([max(numbers), min(numbers)])  # return price and N userse
        else:
            return ([min(numbers), max(numbers)])  # return number of pepole
    return (numbers)


def input_filters(data, input, key_word):
    """
        A function that filters a dataset based on user input and keyword criteria.
        Parameters:
            data (pandas.DataFrame): The dataset to filter.
            input (str): The user input string.
            key_word (list): A list of keywords for filtering.
        Returns:
            pandas.DataFrame: The filtered dataset.
    """
    word = define_input(key_word, input)  # get the key word
    data = filter_data(data, word)  # first filter relvant word
    price_coustmer = find_price_c_limit(input)

    if len(price_coustmer) > 0:
        if max(price_coustmer) > 30:  # check if its price or persons
            data = data[data['price'] <= max(price_coustmer)] # apply the filter
            if len(price_coustmer) > 1:  # if more than one so I also subject to number of person
                data = data[data['min user'] >= min(price_coustmer)]

        else: # I only get number of person
            data = data[data['min user'] >= min(price_coustmer)]

    return data.reset_index(drop=True)


"Begin coding the application itself."


def clear_chat_log():
    """
    A function to clear the chat log in a GUI application.
    """

    global chat_log
    global click_count
    chat_log.configure(state=NORMAL)  # Enable the widget to modify it
    chat_log.delete('1.0', END)
    click_count=0

def to():
    """
     A function that handles user interactions in a chatbot-like application.
     """
    global click_count
    global data_n

    chat_log.configure(state=NORMAL)
    chat_log.insert(END, "You: " + e1.get() + "\n")

    'first case this is the first input fron the user'
    if click_count==0:
        chat_log.configure(state=NORMAL)
        chat_log.insert(END, "Boot: " + f'This is the option that can fit' + "\n\n")
        relevant_data = input_filters(data, e1.get(), key_word)
        des = relevant_data['description'].to_list()
        c=0

        if len(des)>0:
            for i in range(len(des)):
                chat_log.configure(state=NORMAL)
                chat_log.insert(END, f"{c}\t" + f'{des[i]}' + "\n\n")
                c+=1

        chat_log.configure(state=NORMAL)
        chat_log.insert(END, 'If you want more details about item write his number' + "\n\n")
        data_n = relevant_data


    elif click_count==1: #'second case seconde input'

        d = e1.get()
        if d[0]=='n' or d[0]=='N':
            chat_log.configure(state=NORMAL)
            chat_log.insert(END, f"\n Bye Bye")

        elif d.find('min')!=-1 or d.find('Min')!=-1: # check if the user want the min price
            x = data_n[data_n['price'] == data_n['price'].min()][['description', 'price']]

            for i in range(len(x)):
                chat_log.configure(state=NORMAL)
                chat_log.insert(END, f"{x.iloc[i]['description']}\t" + f"the price for this product {x.iloc[i]['price']}" + "\n\n")

            chat_log.configure(state=NORMAL)
            chat_log.insert(END, f"did you want details about another item from the first list?\n")


        else:    # User want mor details
            d = int(e1.get())
            data_n.loc[d]

            chat_log.configure(state=NORMAL)
            chat_log.insert(END, f"\nBoot: {data_n['description'].loc[d]}\nthe price for this product {data_n['price'].loc[d]}\n\n")

            chat_log.configure(state=NORMAL)
            chat_log.insert(END, f"did you want details about another item from the first list?\n")


    else: # not the first or second input
        d = e1.get()
        if d[0]=='n' or d[0]=='N':
            chat_log.configure(state=NORMAL)
            chat_log.insert(END, f"\nBoot: Bye Bye")

        elif d.find('min') != -1 or d.find('Min') != -1:  # check if the user want the min price
            x = data_n[data_n['price'] == data_n['price'].min()][['description', 'price']]

            for i in range(len(x)):
                chat_log.configure(state=NORMAL)
                chat_log.insert(END, f"{x.iloc[i]['description']}\t" + f"{x.iloc[i]['price']}" + "\n\n")

            chat_log.configure(state=NORMAL)
            chat_log.insert(END, f"did you want details about another item from the first list?\n")

        else:
            d = int(e1.get())

            data_n.loc[d]

            chat_log.configure(state=NORMAL)
            chat_log.insert(END, f"{data_n['description'].loc[d]}\n the price for this product {data_n['price'].loc[d]}\n\n")

            chat_log.configure(state=NORMAL)
            chat_log.insert(END, f"\ndid you want details about another item from the first list?\n")



    click_count += 1



    e1.delete(0, END)






m=Tk()
c=0
m.geometry("1400x800")  # define the size of the window
m.configure(bg="lightblue")  # bg
'labels'
Label(m,text='',bg='lightblue').pack()
Label(m,text='Welcome to the Makineta chetbot',bg='white',font=16).pack()
'chat log'
chat_log = Text(m, state=DISABLED, height=30, width=100)
chat_log.pack(padx=10, pady=10)

'labels'
Label(m,text='',bg='lightblue').pack()
Label(m,text='',bg='lightblue').pack()

e1=Entry(m)# 'entry'
e1.pack()


Label(m,text='',bg='lightblue').pack()
Button(m,text='send message',command=to,bg='green').pack() #'buttons'

Label(m,text='',bg='lightblue').pack()
Button(m, text='Clear Chat', command=clear_chat_log,bg='red').pack()#'button'

m.mainloop()

