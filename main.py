from concurrent.futures import process
import csv, json, zipfile
from unicodedata import numeric
from fileinput import filename
from tika import parser
import pip._vendor.requests as requests
import os, glob
import re
import fitz
from datetime import date

current_year = str(date.today().year)
zip_file_url = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/'+current_year+'FD.ZIP'
pdf_file_url = 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/'+current_year+'/'
regex1 = "\s(SP|S|P)\s(.*\s?.*?)\s?\((\S+)\)\s+(\[\S+\])\s+(P|E|S|S \(partial\))\s+(\d+\/\d+\/\d+)\s+(\d+\/\d+\/\d+)\s+(\$\S+)\s+\-\s+(\$\S+).*\s+.*\s+D\S+\:\s+(.*)\."
regex2 = "\s(SP|S|P)\s(.*\s?.*?)\s?\((\S+)\)\s+(\[\S+\])\s+(P|E|S|S \(partial\))\s+(\d+\/\d+\/\d+)\s+(\d+\/\d+\/\d+)\s+(\$\S+)\s+\-\s+(\$\S+)\s+\S+\s+.*\nD\S+\:\s+(.*\.)"
regex3 = ""

#this needs to be redone with REGEX
def printTradeReport():
    
    return

def pullTrades():
    
    printTradeReport()
    return

def retrieveInformation():
    r = requests.get(zip_file_url)
    zipfile_name = current_year+'.zip'

    with open(''+zipfile_name, 'wb') as f:
        f.write(r.content)

    with zipfile.ZipFile(zipfile_name) as z:
        z.extractall('.')

    with open(current_year+'FD.txt') as f:
        for line in csv.reader(f, delimiter='\t'):
            if line[1] == 'Pelosi':
                doc_id = line[8]
                r = requests.get(pdf_file_url + doc_id + '.pdf')
                filename = doc_id + '.pdf'
                with open(''+filename, 'wb') as pdf_file:
                    pdf_file.write(r.content)
    
    file_to_delete = open("tradesRegex.txt",'w')
    file_to_delete.close()

    for pdffiles in glob.glob('*.pdf'):
        raw = parser.from_file(pdffiles)
        raw['content'] = re.sub(r'(https.*|Dig.*|Fil.*|I CE.*|gfedc.*|\*.*|Perio.*|Clerk.*|name:.*|Name:.*|Status:.*|State\/.*|Date.*|filer.*|tranS.*|type.*|Type.*|certif.*|best of.*|gains.*|Gains.*|iD.*|ID O.*|init.*|nml.*|amount.*|Amount.*|Yes.*|yes.*|No.*|my.*|\$\d+\?)', '', raw['content'])
        raw['content'] = re.sub(r'(\s\s\s)', '', raw['content'])
        raw['content'] = raw['content'].replace("�", "X")
        #raw['content'] = raw['content'].replace("\n", " ")
        raw['content'] = raw['content'].replace("XS", "\nS")
        with open('tradesRegex.txt', 'a', encoding="utf-8") as text:
            text.write("\n---------------------------------------------\n")
            text.write(raw['content'])                  
    pullTrades()
    return



retrieveInformation()

#input("Enter anything to close application...")




#Current Regexs for the text file
#(SP|P)\s+(.*)\s+(\(\S+\)| )\s+\[\S+\]\s+(P|S|S \(partial\))\s+(\d+\/\d+\/\d+)\s+(\d+\/\d+\/\d+)\s+(\$\S+\s+-\s+\$\S+)
#(SP|P)\s+((.|\s+).*)\s+(\[\S+\])\s+(P|E|S|S \(partial\))\s+(\d+\/\d+\/\d+)\s+(\d+\/\d+\/\d+)\s+(\$\S+\s+-\s+\$\S+)\s+F.*\sD.*:\s((.|\n).*)