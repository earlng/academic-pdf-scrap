# academic-pdf-scrap
Code that scrapes the contents of the PDF papers submitted for [NeurIPS 2020](https://proceedings.neurips.cc/paper/2020)

## Functions Available
This repository seeks to accomplish the following tasks:
* Download all the PDFs submitted for NeurIPS 2020
* Convert the PDFs to XML using [PDFx](http://pdfx.cs.man.ac.uk/)
* Scrap useful information from the XML files

## Background
The [Conference on Neural Information Processing Systems (NeurIPS)](https://nips.cc/Conferences/2020/PaperInformation/NeurIPS-FAQ) is one of the most preeminent machine learning conferences globally. With several thousand academic papers submitted each year. This year, NeurIPS has implemented a new requirement wherein submissions must now include a "Broader Impact Statement", which should describe the authors' assessment of how their research will impact society. A meta-analysis of this statement may help in informing, regulating, and/or monitoring the progress of artificial intelligence and machine learning research.

This repository aims to provide tools to quickly parse through the papers submitted to the conference, to faciliate analyzing these impact statements (in their various forms).
