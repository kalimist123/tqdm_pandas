import pandas as pd
import numpy as np
from tqdm import tqdm
import hashlib
import pem
import pandas as pd
import os
import sys
import random


def start_setup():
    prompt = '> '

    print("Hi, welcome to Simple.Pseudonymizer")
    here = os.path.dirname(os.path.abspath(sys.argv[0]))
    print("Please enter cert file name")

    while True:
        try:
            certfilename = input(prompt)
            certfilename = os.path.join(here, certfilename)

            while not os.path.exists(certfilename):
                print('cannot find cert file. please enter valid cert file name')
                certfilename = input(prompt)
                certfilename = os.path.join(here, certfilename)


            certs = pem.parse_file(certfilename)
            salt = certs[0].sha1_hexdigest
            break
        except:
            print('cannot hash cert. please enter valid cert')
            continue



    print(salt)
    print("Please enter the name of an xlsx file to process")

    pseudofile = input(prompt)
    pseudofile = os.path.join(here, pseudofile)
    while True:
        while not os.path.exists(pseudofile) or not pseudofile.endswith(".xlsx"):
                print("Cannot process file. Please enter the name of an xlsx file to process")
                pseudofile = input(prompt)
                pseudofile = os.path.join(here, pseudofile)

        temp_name = pseudofile.replace(".xlsx", "_psuedo.xlsx")
        temp_name = os.path.join(here, temp_name)

        if os.path.exists(temp_name):
                os.remove(temp_name)
        print('opening file....')
        df = pd.read_excel(pseudofile, dtype='str', encoding='utf-8')
        if 'identifier' in df.columns:
            break
        else:
            print("No 'identifier' column exists in file!")
            pseudofile = ""
            continue

    tqdm.pandas()
    print('started pseudonymising....')
    df['DIGEST'] = df.identifier.progress_apply(pseudo)
    print('finished pseudonymising....')
    print('saving file....')
    df.to_excel(temp_name, index=False)
    print('saving file done')

def pseudo(x):
    sentence = str(x) + salt
    return str(hashlib.blake2s(sentence.encode('utf-8')).hexdigest())


salt = ""
start_setup()