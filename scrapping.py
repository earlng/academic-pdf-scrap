import pandas as pd
import os
import re
import numpy as np
import xml.etree.ElementTree as ET

#The purpose of this file is to take XML files found in the `/xml` directory, and produce a csv output (`output.csv`)

#XML files that are already generated via PDFx are assumed to be in a directory "xml"

directory="xml"
impact_dict={"title":[], "paper identifier":[], "paper link":[], "impact statement":[], "impact title":[], "impact statement word count":[], "impact statement sentence count":[], "citation count":[],
            "has positive":[], "has negative":[], "has opt out":[], "has NA":[], "has impact statement":[]}

#initialize citations_dict, which is a separate dictionary to be generated as a separate CSV file (citation.csv)
citation_dict={"paper title":[],"paper id":[],"citation":[]}

#loops through the directory, and appends the relevant information to impact_dict, which will be appended to the dataframe later
for filename in os.listdir(directory):
    #to exclude "sample.xml"
    if filename.endswith(".pdfx.xml"):
        full_path = os.path.join(directory, filename)
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
                    #itertext will make sure that if there are any tags within the section, we still get the whole thing.
                    impact_statement_text=''.join(child.itertext())
                    impact_statement_number_of_words=len(impact_statement_text.split())
                    #add count for setences using delimeters of ".", "?", and "!"
                    impact_statement_number_of_sentences=len(re.split("\.|\?|!", impact_statement_text))-1
                    #will identify the hash based off of this pattern "86d7c8a08b4aaa1bc7c599473f5dddda-Paper.pdfx.xml"
                    paper_identifier = re.search("(\w*)(-Paper)", filename)
                    #check if "positive" is in the statement
                    has_positive = "True" if "positive" in impact_statement_text.lower() else "False"
                    #check if "negative" is in the statement
                    has_negative = "True" if "negative" in impact_statement_text.lower() else "False"
                    #check if it has the NeurIPS opt-out phrase
                    has_opt_out = "True" if "this work does not present any foreseeable societal consequence" in impact_statement_text.lower() else "False"
                    #check if it has "Not Applicable"
                    has_NA = "True" if "not applicable" in impact_statement_text.lower() else "False"
                    has_impact_statement = "True"
                    #add everything to the dictionary
                    impact_dict["impact title"].append(impact_statement_title)
                    impact_dict["impact statement"].append(impact_statement_text)
                    impact_dict["impact statement word count"].append(impact_statement_number_of_words)
                    impact_dict["impact statement sentence count"].append(impact_statement_number_of_sentences)
                    impact_dict["citation count"].append(citations)
                    impact_dict["title"].append(title)
                    impact_dict["paper identifier"].append(paper_identifier[1])
                    impact_dict["paper link"].append("https://proceedings.neurips.cc/paper/2020/file/" + paper_identifier[1] + "-Paper.pdf")
                    impact_dict["has positive"].append(has_positive)
                    impact_dict["has negative"].append(has_negative)
                    impact_dict["has opt out"].append(has_opt_out)
                    impact_dict["has NA"].append(has_NA)
                    impact_dict["has impact statement"].append(has_impact_statement)
                    signal = 0
                    #print(citation_ref)
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
                        for xref in smaller:
                            #narrow down xref citations to bibliography references
                            if xref.tag == "xref" and xref.attrib['ref-type'] == "bibr":
                                #use "rid" as the identifier, so we come out of this with a list of references
                                citation_ref.append(xref.attrib['rid'])
                                citations +=1
                        #itertext will make sure that if there are any tags within the section, we still get the whole thing.
                        impact_statement_text=''.join(smaller.itertext())
                        impact_statement_number_of_words=len(impact_statement_text.split())
                        #add count for setences using delimeters of ".", "?", and "!"
                        impact_statement_number_of_sentences=len(re.split("\.|\?|!", impact_statement_text))-1
                        #will identify the hash based off of this pattern "86d7c8a08b4aaa1bc7c599473f5dddda-Paper.pdfx.xml"
                        paper_identifier = re.search("(\w*)(-Paper)", filename)
                        #check if "positive" is in the statement
                        has_positive = "True" if "positive" in impact_statement_text.lower() else "False"
                        #check if "negative" is in the statement
                        has_negative = "True" if "negative" in impact_statement_text.lower() else "False"
                        #check if it has the NeurIPS opt-out phrase
                        has_opt_out = "True" if "this work does not present any foreseeable societal consequence" in impact_statement_text.lower() else "False"
                        #check if it has "Not Applicable"
                        has_NA = "True" if "not applicable" in impact_statement_text.lower() else "False"
                        has_impact_statement = "True"
                        #add everything to the dictionary
                        impact_dict["impact title"].append(impact_statement_title)
                        impact_dict["impact statement"].append(impact_statement_text)
                        impact_dict["impact statement word count"].append(impact_statement_number_of_words)
                        impact_dict["impact statement sentence count"].append(impact_statement_number_of_sentences)
                        impact_dict["citation count"].append(citations)
                        impact_dict["title"].append(title)
                        impact_dict["paper identifier"].append(paper_identifier[1])
                        impact_dict["paper link"].append("https://proceedings.neurips.cc/paper/2020/file/" + paper_identifier[1] + "-Paper.pdf")
                        impact_dict["has positive"].append(has_positive)
                        impact_dict["has negative"].append(has_negative)
                        impact_dict["has opt out"].append(has_opt_out)
                        impact_dict["has NA"].append(has_NA)
                        impact_dict["has impact statement"].append(has_impact_statement)
                        signal = 0
                        #print(citation_ref)
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
            #identify the bibliography
            if section.attrib["class"] == "DoCO:Bibliography":
                #loop through the bibliography section, but we really only want one part
                for references in section:
                    if references.attrib["class"] == "DoCO:BiblioGraphicReferenceList":
                        #loop through all the entries in the reference list
                        for citation in references:
                            #the try statement is because if the bibliography is across multiple pages, there will be entries with no "rid", so we account for that with a keyerror.
                            try:
                                #check if the citation is in the citation_ref we established earlier
                                if citation.attrib["rid"] in citation_ref:
                                    citation_dict["paper title"].append(title)
                                    citation_dict["paper id"].append(paper_identifier[1])
                                    citation_dict["citation"].append(citation.text)
                            except KeyError:
                                continue
        if has_impact_statement == "False":
            #no impact statement was found at all
            #set variables
            impact_statement_title = ""
            impact_statement_text = ""
            impact_statement_number_of_words = 0
            impact_statement_number_of_sentences = 0
            citations = 0
            paper_identifier = re.search("(\w*)(-Paper)", filename)
            has_positive = "False"
            has_negative = "False"
            has_opt_out = "False"
            has_NA = "False"
            #append to dictionary
            impact_dict["impact title"].append(impact_statement_title)
            impact_dict["impact statement"].append(impact_statement_text)
            impact_dict["impact statement word count"].append(impact_statement_number_of_words)
            impact_dict["impact statement sentence count"].append(impact_statement_number_of_sentences)
            impact_dict["citation count"].append(citations)
            impact_dict["title"].append(title)
            impact_dict["paper identifier"].append(paper_identifier[1])
            impact_dict["paper link"].append("https://proceedings.neurips.cc/paper/2020/file/" + paper_identifier[1] + "-Paper.pdf")
            impact_dict["has positive"].append(has_positive)
            impact_dict["has negative"].append(has_negative)
            impact_dict["has opt out"].append(has_opt_out)
            impact_dict["has NA"].append(has_NA)
            impact_dict["has impact statement"].append(has_impact_statement)

#create the dataframe for the output from the dictionary
impact_statements =pd.DataFrame.from_dict(impact_dict)

#create the dataframe for the citations from the dictionary
total_citations =pd.DataFrame.from_dict(citation_dict)

#generate the CSV file from the dataframe

impact_statements.to_csv("output.csv",index=False)

#generate the CSV file for the citations
total_citations.to_csv("citations.csv",index=False)