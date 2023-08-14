"""
-------------------------------------------------------------------------------
A mean scriptoid for pulling all pertinent voting information directly off the Music League web page

IMPORTANT NOTES: Read through the scrip and check for anything you need to change, listed below with their line of code

Line  42: Change the xpath locator to the element you place in the actions list for your desired results page.
Line 122: Your Spotify Username
Line 123: Your Spotify Password
Line 126: The HTML Selector for whatever league you are trying to enter. The one I have input is unique to me as I am in several leagues.
Line 127: Change the xpath locator to the abs xpath for whatever results page you want, make sure the element you have selected is the one that highlights both the button and "Results" hyperlink.
Line 135: Make sure to change the user name list to whatever players were present that round
Line 141: Same as above but real names
Line 157: Change to path to temp text file needed to store text pulled from web page
Line 166: Change to path from above, this time file is reading line by line
line 215: Change to path of CSV you would like to store in

Will edit maybe to be a little bit more flexible and create voter lists from a master index
Could be improved on wait time if I could figure out explicit waits for Selenium instead of using time.sleep
Would like to also loop the driver to collect all rounds when the league is done for one big master list.
Also think there is a way to avoid needing the temporary text file but am too lazy to figure it out

-------------------------------------------------------------------------------
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import pandas as pd

# Function to click through music league page dependent on actions defined by HTML path
def perform_actions(driver, actions):
    try:
        for action_type, locator, value in actions:
            time.sleep(1.75)
            element = driver.find_element(*locator)
            if action_type == "click":
                if locator == (By.XPATH, "ABS XPATH HERE"): #CHANGE for different results page
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    time.sleep(1)
                ActionChains(driver).move_to_element(element).click().perform()
                #print(f"Clicked on element: {locator}")    #delete the '#' if you want to see what locator is being clicked
            elif action_type == "send_keys":
                element.send_keys(value)
                #print(f"Sent keys '{value}' to element: {locator}")   #same if you want to see what keys are being entered

    except Exception as e:
        print(f"Error during action: {e}")

# Function to search for voters not present in a submitted song, adds a 0 and no comment
def voter_fill(sublist):
    for conditional_string in voter_names:
        if conditional_string not in sublist:
            sublist.append(conditional_string)
            sublist.append('0')
            sublist.append('No Comment')
    return sublist

# Function to add no comment for submitter if they did not comment    
def SubmitCMT_fill(sublist):
    for conditional_string in voter_names:
        if conditional_string == sublist[6]:
            sublist.insert(6, 'No Comment')
    return sublist

# Function to add a 0 if someone left a comment but didn't vote
def NoVoteCMT_fill(sublist):
    for index, item in enumerate(sublist):
        if item in voter_names:
            if contains_number(sublist[index + 1]):
                continue
            else:
                sublist.insert(index + 1, '0')   
        else:
            continue
    return sublist

# Create the data frame, going through each row column by column. First 6 col are always song info, then next cols are sorted to their repective voter cols
def dfCreate(list, df):
    for rowidx, sublist in enumerate(list):
        for colidx, item in enumerate(sublist):
            if colidx <= 6:
                df.iloc[rowidx, colidx] = item  
                continue
            else:
                if item in voter_names:
                    df.iloc[rowidx, Columns.index(item)] = sublist[sublist.index(item) + 1]
                    continue
                else:
                    continue
    return df

#Needed to check for number in str in one of the other functions
def contains_number(input_string):
    for char in input_string:
        if char.isdigit():
            return True
    return False  
          
#Rename columns from usernames to real names
def rename_columns_from_index(df, start_index, new_column_names):
    if start_index >= 0 and start_index < len(df.columns):
        for i, new_name in enumerate(new_column_names):
            df.rename(columns={df.columns[start_index + i]: new_name}, inplace=True)
    else:
        print("Start index is out of range.")
    
    return df

#open web driver
driver = webdriver.Firefox()
url = "https://app.musicleague.com/"
driver.get(url)

# List of actions where each action is a tuple: (action_type, locator, value) You can change the locator depending on what selector works best for the element on the webpage. It varies
actions = [
    ("click", (By.CSS_SELECTOR, "div.row:nth-child(3) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)"), None), 
    ("send_keys", (By.ID, "login-username"), "USERNAME"), #CHANGE to your spotify username
    ("send_keys", (By.ID, "login-password"), "PASSWORD"), #CHANGE to your spotify password
    ("click", (By.CSS_SELECTOR, "#login-button"), None),
    ("click", (By.CSS_SELECTOR, ".Button-qlcn5g-0"), None),
    ("click", (By.XPATH, "XPATH OF SPECIFIED MUSIC LEAGUE"), None), #CHANGE This element is unique to your music league browser, Make sure to select xpath League desired
    ("click", (By.XPATH, "XPATH OF ROUND REULTS BUTTON"), None), #CHANGE This is the element for the round result button

    # Add more actions here if needed
]

SongInfo = ['Song', 'Artist', 'Album', 'Total Votes', 'Total Voters', 'Submitted By', 'Submitter comment']

#CHANGE Make sure this list is relevant to the round you are trying to collect data for    
voter_names = [
    'alictr', 'Allison', 'anastasia', 'mr.burnstein', 'TarkMemes', 'ari', 'Baileysheanichols', 'Beth', 'CJ Ryan', 'Con', 'Emma Weiss', 'Jacoby', 
    'Justin Lisonbee', 'Kat Shaw', 'Kristina Lisonbee', 'Lucía Soto', 'Luis Espinoza', 'Malachi', 'Maritza Medrano', 'michael', 'samlulloff', 'Spam', 
    '[ Competitor has left the league ]', 'Tan', 'zachlovvorn']

#CHANGE Same as above
names = [
    "Ali", "Allison", "Anastasia", "Andrew", "Andy", "Ari", "Bailey", 
    "Beth", "CJ", "Connor", "Emma", "Jacoby", "Justin", "Kat", 
    "Kristina", "Lucía", "Luis", "Malachi", "Maritza", "Michael", 
    "Sam L", "Sam T", "Shelby", "Tanner", "Zach"]

Columns = SongInfo + voter_names

if __name__ == "__main__":

    perform_actions(driver, actions)

    time.sleep(2)

    all_elements = driver.find_elements(By.XPATH, "//div[3]/div[1]/div[2]//*[normalize-space(text()) != '']")  # This selects all child elements within the main body of the results page that produce visible text
 
    with open('EXAMPLE.txt', "w", encoding="utf-8") as outp: #CHANGE to a text file you have stored to write all text to so it can be read back line by line
        for index, element in enumerate(all_elements):
            if index < 5:  # Delete header data
                continue
            outp.write(element.text + '\n')
    outp.close() 
        
    driver.quit() 
    
    with open('EXAMPLE.txt', 'r', encoding="utf-8") as inp:  #CHANGE to same text file as above but now reading for sublists
        lines = inp.readlines()
    
    lines_above = 5
    sublists = []
    current_sublist = []

    #Parse txt file into sublists by round, 
    for idx, line in enumerate(lines):
        if line.startswith('Submitted'): #Seaches for submutted in text
            if current_sublist:
                sublists.append(current_sublist[:-lines_above]) #returns rest of lines and appeanding 5 in front of detected string
            current_sublist = [lines[i] for i in range(max(0, idx - lines_above), idx + 1)] 
        else:
            current_sublist.append(line)

    # Append the last sublist if there are remaining items
    if current_sublist:
        sublists.append(current_sublist)  # Append the last sublist without duplicated lines

    if sublists and not sublists[0]:
        sublists.pop(0)



    CleanList = [[item[:-1] if item.endswith('\n') else item for item in sublist] for sublist in sublists] #clean new line chars


    # Apply the conditional_fill function to each sublist
    voter_filled = [voter_fill(sublist) for sublist in CleanList]
    SubmitCMT_filled = [SubmitCMT_fill(sublist) for sublist in voter_filled]
    NoVoteCMT_filled = [NoVoteCMT_fill(sublist) for sublist in SubmitCMT_filled]

    df = pd.DataFrame(columns=Columns)
    while len(NoVoteCMT_filled) >= len(df):
         df.loc[len(df)] = [None] * len(Columns)
    dfCreation = dfCreate(NoVoteCMT_filled, df)
    rename_columns_from_index(dfCreation, 7, names)

    #Block to clean up the data frame
    dfCreation = dfCreation.iloc[:-1]
    dfCreation['Submitted By'] = dfCreation['Submitted By'].str.replace('Submitted by ', '')
    replacement_dict = dict(zip(voter_names, names))
    dfCreation['Submitted By'] = dfCreation['Submitted By'].map(replacement_dict)
    sorted_df = dfCreation.sort_values(by='Submitted By')
    ColDropdf = sorted_df.drop(columns = ['Artist', 'Album', 'Total Votes', 'Total Voters', 'Submitter comment'])
    for col in ColDropdf.columns:
        ColDropdf[col] = ColDropdf[col].str.replace('+', '')

    ColDropdf.to_csv('OUTPUT.csv', index=False) #CHANGE To whatever CSV you want to write to then just import to sheets

    print('\n')
    print(ColDropdf)