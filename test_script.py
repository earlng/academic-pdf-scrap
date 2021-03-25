import pandas as pd
import os
import re
import numpy as np
import xml.etree.ElementTree as ET

#The purpose of this file is for single tests

#XML files that are already generated via PDFx are assumed to be in a directory "xml"

directory="xml"
impact_dict={"title":[], "paper identifier":[], "paper link":[], "impact statement":[], "impact title":[], "impact statement word count":[], "impact statement sentence count":[], "citation count":[],
            "has positive":[], "has negative":[], "has opt out":[], "has NA":[], "has impact statement":[]}

#initialize citations_dict, which is a separate dictionary to be generated as a separate CSV file (citation.csv)
citation_dict={"paper title":[],"paper id":[],"citation":[]}

#filename is whatever file we want to test.
filename="4496bf24afe7fab6f046bf4923da8de6"
full_filename=filename+"-Paper.pdfx.xml"

full_path = os.path.join(directory, full_filename)
#i need to clear impact_statement_text for each file
impact_statement_text=""
tree = ET.parse(full_path)
root = tree.getroot()
#get article title
#initialize a list of citations for this document
citation_ref = []
#signals if impact statement exists
has_impact_statement = "False"

for section in root[1][0][0]:
    if section.tag=="article-title":
        title = section.text

for section in root[1][1]:
    citations = 0
    signal = 0
    for child in section:
        if signal == 1 :
            #print(section.text)
            #broader_dict[filename] = section.text
            #loop through any xrefs to count for citations
            for xref in child:
                #narrow down xref citations to bibliography references
                if xref.tag == "xref" and xref.attrib['ref-type'] == "bibr":
                    #use "rid" as the identifier, so we come out of this with a list of references
                    citation_ref.append(xref.attrib['rid'])
                    citations +=1
                    print("CITATIONS")
            #itertext will make sure that if there are any tags within the section, we still get the whole thing.
            #impact_statement_text will become whatever the current value of it is, plus whatever the for loop finds so long as it is true
            print(child.attrib)
            if child.itertext() != "" and (child.attrib["class"] == "DoCO:TextChunk" or child.attrib["class"] == "DoCO:TextBox" or child.attrib["class"] == "unknown"):
                #so it captures the text so long as there is text in the section
                print(''.join(child.itertext()))
                print("LOOP")
                impact_statement_text=impact_statement_text + " "+''.join(child.itertext())
            else:
                print(child.attrib["class"])
                print(''.join(child.itertext()), "[this is text]")
                if child.itertext() !="":
                    print(child.itertext())
                print("Broke 001")
                signal = 0
        #focus on heading
        if "impact" in str(child.text).lower() and child.tag == "h1":
            #print("It has a Broader Impact!")
            #log the title of the broader impact statement
            impact_statement_title = child.text
            signal=1
        elif str(child.text).lower() == "broader impact" and child.tag == "h1":
            impact_statement_title = child.text
            signal=1
        elif str(child.text).lower() == "broader impacts" and child.tag == "h1":
            impact_statement_title = child.text
            signal=1
        #insert a new for loop here to check for the "smaller" parts. The "h2" headers
        for smaller in child:
            if signal == 1 :
            #print(section.text)
            #broader_dict[filename] = section.text
            #loop through any xrefs to count for citations
                #print(''.join(smaller.itertext()), smaller.attrib["ref-type"])
                for xref in smaller:
                    #narrow down xref citations to bibliography references
                    if xref.tag == "xref" and xref.attrib['ref-type'] == "bibr":
                        #use "rid" as the identifier, so we come out of this with a list of references
                        citation_ref.append(xref.attrib['rid'])
                        citations +=1
                #itertext will make sure that if there are any tags within the section, we still get the whole thing.
                #if smaller.itertext() != "" and (smaller.attrib["class"] == "DoCO:TextChunk" or smaller.attrib["class"] == "DoCO:TextBox"):
                try:
                    if smaller.itertext() != "" and (smaller.attrib["class"] == "DoCO:TextChunk" or smaller.attrib["class"] == "DoCO:TextBox"):
                        impact_statement_text=impact_statement_text + " "+''.join(smaller.itertext())
                    elif smaller.attrib["ref-type"] == "bibr":
                        continue
                    else:
                        print("STOPPED BY SMALLER")
                        signal = 0
                except KeyError:
                    continue
            #focus on heading
            if "impact" in str(smaller.text).lower() and smaller.tag == "h2":
                #print("It has a Broader Impact!")
                #log the title of the broader impact statement
                impact_statement_title = smaller.text
                signal=1
            elif str(smaller.text).lower() == "broader impact" and smaller.tag == "h2":
                impact_statement_title = smaller.text
                signal=1
            elif str(smaller.text).lower() == "broader impacts" and smaller.tag == "h2":
                impact_statement_title = smaller.text
                signal=1