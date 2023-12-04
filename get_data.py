from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time
import numpy as np


def correct_price(str):
    """
    Extracts the numeric price from a string and converts it to an integer.
    Parameters:
        input_str (str): The input string containing the price.
    Returns:
        int: The extracted numeric price.
    """
    res=''
    for i in str :
        if i.isdigit(): res+=i
    return int(res)


def get_size_mac(st):
    """
    Extracts the number of users from a string describing a machine.
    Parameters:
        st (str): The input string describing the machine and its user capacity.
    Returns:
        str: The extracted number of users or a range of users (e.g., "1-5").
    """
    st = st.split()  # split the inpute
    st = [i[2:] if i[0:2] == 'ל-' else i for i in st]  # in casw that st have ל- drop that and take the other else is stay the same
    numbers = [st[i] for i in range(len(st)) if st[i].isdigit()] # if have a digit insert to the list numbers
    if len(numbers) == 0: numbers.append(1)  # check if contain word one I saw in the data that this is the only cash that dont have number

    if len(numbers) > 1:  # check if there is any dupliocate  #
        if numbers[0] == numbers[1] or numbers[0] > numbers[1]:  # check if have the same number twice - mayber gift
            numbers = numbers[0]
    return (numbers[0]) if len(numbers) == 1 else (str(numbers[0]) + '-' + str(numbers[1]))


def min_max(st):
    """
    Extracts the maximum number of users from a string that may contain a range.
    Parameters:
        st (str): The input string, which may contain a range of users (e.g., "1-5").
    Returns:
        str: The maximum number of users extracted from the input string.
    """
    return (st) if len(str(st)) == 1 else st[st.find('-') + 1:]  # find the max number of user


def adjust_number_of_user(st):
    """
       Extracts the minimum number of users from a string that may contain a range.
       Parameters:
           st (str): The input string, which may contain a range of users (e.g., "1-5").
       Returns:
           str: The minimum number of users extracted from the input string.
       """
    if str(st).find('-') != -1:   # split for 2 cases
        return (st[:str(st).find('-')])
    else:
        return (st)


"In this part, I retrieve the data from the web."
driver = webdriver.Chrome() # open driver
driver.get('https://ksp.co.il/web/cat/5183..3067')

first = int(driver.execute_script("return document.documentElement.scrollHeight"))
c = 0
"Scroll the page all the way down."

while (c < 3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    sec = int(driver.execute_script("return document.documentElement.scrollHeight"))
    c += 1 if first == sec else 0
    first = sec

data = driver.find_element(By.XPATH, '//*[@id="select-root"]/div[2]/div[3]').text  # extract all the relevant text
driver.close()

"Convert the data to a DataFrame."
df_data = pd.DataFrame(columns=['Barcode', 'description', 'price', 'Eilat-price'])
data = data.split('מק"ט')[1:] # Split the data starting from row one, because I observed that the first row is not relevant.
for i in range(1, len(data)):  # run on each row
    current_row = data[i].split('\n')
    barcode = current_row[0][6:] # extract barcode
    description = current_row[1] # ectract descriptiom
    try:
        eilat_index = [j for j in range(2, len(current_row)) if current_row[j].find('אילת') != -1][0]
        price = current_row[eilat_index - 2]
        if price == description: price = current_row[eilat_index - 1]
        price_eilat = current_row[eilat_index]
        start_take = price_eilat.find('₪')
        price_eilat = price_eilat[start_take + 1:]
    except:
        price = current_row[2][2:]
        price_eilat = int(int(price) * 0.8489)
    df_data.loc[len(df_data)] = [barcode, description, price, price_eilat]





"Apply the function to the data."

df_data['price']=df_data['price'].apply(correct_price)
df_data['price']=df_data['price'].astype(np.int32)

df_data['Barcode']=df_data['Barcode'].astype(np.int32)
df_data['Eilat-price']=df_data['Eilat-price'].astype(int)



df_data['min user'] = df_data['description'].apply(get_size_mac)

df_data['max user'] = df_data['min user'].apply(min_max)
df_data['min user'] = df_data['min user'].apply(adjust_number_of_user)
df_data['max user'] = df_data['max user'].astype(int)
df_data['min user'] = df_data['min user'].astype(int)

df_data.to_csv('df_price.csv',index=False,encoding = 'utf-8-sig')  # export the data to csv