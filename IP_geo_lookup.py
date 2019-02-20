import sys
import os
import requests
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from openpyxl import load_workbook
import xlrd

def file_path():
    '''
    #global df
    global file_path
    root = tk.Tk()
    root.title('Choose the file')
    root.withdraw()
    root.update()
    file_path = filedialog.askopenfilename()'''
    file_path = read_csv()
    df = pd.read_excel(file_path, index_col ='respID')
    return file_path, df
    
def writer(filepath, df):
    ws_dict = pd.read_excel(filepath, sheetname=None)
    sheets= list(ws_dict.keys())
    ws_dict[sheets[0]]= df
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        for ws_name, df_sheet in ws_dict.items():
            df_sheet.to_excel(writer, sheet_name=ws_name, index=False)

def read_from_static_data(path):
    #bug testing feature that will read dicts created by the commented code in create_ip_dicts
    file_list=[]
    file= open(path)
    for line in file:
        file_list.append(line.replace('\n',''))
    file_list[0]=str(file_list[0]).replace('{',' ')
    file_list[-1]=str(file_list[-1]).replace('}','')
    dictvalues={}
    for entry in file_list:
        line=entry.split(':')
        dictvalues[line[0].lstrip()]=(line[1].replace('\'','')).lstrip()
    return dictvalues
    '''keys_from_dict=[x for x in whatever.keys()]
    values_from_dict=[x for x in whatever.values()]
    for i in range(10):
        print('%s %s \n' % (keys_from_dict[i], values_from_dict[i])) '''
    '''
        Bug testing feature that prints the first 10 keys (or whatever the range value is ) to console
        Note: the '' syntax which denotes a string is lost because it's been printed to a console. All the keys and
        values are strings. Printing the entire dictionary is ineffective.
    '''

def read_csv():
    #reads from desktop directory and pandas database
    user_path=os.getcwd()
    csv_files=[]
    for file in os.listdir(user_path):
        if file.endswith(".xlsx"):
            csv_files.append(os.path.join(user_path, file))

    for counter, file in enumerate(csv_files):
        print(file[(file.rfind('/')+1):] + ' [%d]' % (counter))
        counter+=1
    user_input=input("Which file do you want to use?")
    return csv_files[int(user_input)]    

def test_funct():
    #global df
    global file_path
    file_path= "/foo/bar/directory/filename.xlsx"
    df = pd.read_excel(file_path, index_col ='respID')
    return df

def ip_lookup(ip):
    ip = ip
    url = 'http://freegeoip.net/json/'+ip
    r= requests.get(url)
    js = r.json()
    return js['region_name'], js['city']

def create_ip_dicts(df):
    ips = dict(df.ipAddr)
    state_names= {}
    city_names = {}
    key_index = ips.keys()
    for ip in key_index:
        state_names[ip], city_names[ip]= ip_lookup(ips[ip])
    return state_names, city_names
    '''
    with open('state_names.txt', 'w+') as x:
        x.write("\n".join(str(state_names).split(",")))
    with open('city_names.txt', 'w+') as x:
        x.write("\n".join(str(city_names).split(",")))'''
    #testing by writing dicts to .txt
    #dicts can be read w/ read_from_static_data(path)
        
def update_columns(first_dict,second_dict, df):
    first_series = pd.Series(first_dict, name='State Names')
    second_series = pd.Series(second_dict, name='City Names')
    column_loc=list(df.columns.values).index("ipAddr")
    df.insert(column_loc+1, 'State Names', first_series.values)
    df.insert(column_loc+2, 'City Names', second_series.values)
    return df

def bug_testing():
    #df = test_funct()
    pd.set_option('display.max_rows', 4)
    pd.set_option('display.max_columns', 32)
    #print(df.head)
    

def main ():
    try:
        path, df = file_path()
    except FileNotFoundError:
        print('No File Selected')
        sys.exit()
    state_names, city_names = create_ip_dicts(df)
    df =update_columns(state_names, city_names, df)
    writer(path, df)
    print('Complete')

if __name__ == "__main__":
    main()
