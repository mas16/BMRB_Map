# BMRB_Map
by MAS 04/2019

## Introduction
This script is a stand-alone utility for generating SPARKY assignment peak list files ```.list``` from a BMRB NMR STAR file. NMR STAR files are very messy and contain a massive amount of information that is not relevant or required for generating peak lists. This script cleans the NMR STAR file, generating a simple, clean SPARKY peak list. 

## Set Up
* Save NMR STAR File > v. 3  as ```.txt``` (right click BMRB link, Save As)
* Put ```.txt``` file in current working directory

## Requirements
* Python 3.x
* pandas

## Test Data
A test NMR STAR file ```test.txt``` is provided with this repo as an example. 
