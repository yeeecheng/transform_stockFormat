# Process the raw data from yuanta API
# Delete the same raw data
# Add the date in front of the raw data
# Change the time format which is HH:MM:SS.MS to HHMMSSMS in the raw data

import pandas  as pd
import os
from tqdm import tqdm
import argparse

def createDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def convert(args):

    path = args["file"]

    for e_date in os.listdir(path):
        
        # change format from HH:MM:SS.MS to HHMMSSMS
        try:
            y,m,d = e_date.split("-")
            date = y+m+d
        except:
            pass
        
        # if it's already created the file , continue it.
        if  os.path.isdir(os.path.join(args["save"],date)):
            continue
        createDir(os.path.join(args["save"],date))

        for file in os.listdir(os.path.join(path,e_date)):
            filePath = os.path.join(path,e_date,file)

            count = len(open(filePath,"r").readlines())
            cur_data = -1
            allData = ""
            
            with open(filePath,"r") as f :
                loop = tqdm(f,total=count)
                loop.set_description(f"{date}/{file}")
                
                for idx , data  in enumerate(loop):
                    
                    if (cur_data == -1 or cur_data == data) and idx != count-1:
                        cur_data = data
                        continue 
                    
                    new_data = str(date)+","+data
                    new_data = new_data.split(",")
                    # avoid raw data is incomplete , otherwise , skip it.
                    try:
                        if(new_data[5]==""):
                            cur_data  = data
                            new_data  = ",".join(new_data)
                            allData += new_data
                            continue
                        time = new_data[5].split(":")
                        s , ms = time[2].split(".")
                        time = str(time[0]+time[1]+s+ms)
                        new_data[5]=time
                        new_data  = ",".join(new_data)
                        allData += new_data
                    except:
                        continue

            savePath =  os.path.join(args["save"],date,file)
            with open(savePath,"a") as f :
                f.write(allData)

def main(opt):

    args = vars(opt)
    
    createDir(args["save"])
    convert(args)



def parse_opt(known = False):

    ROOT = os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument("--save",type=str, default = r"./stock_raw")
    parser.add_argument("--file",type= str ,require =True , default=r"")


    return parser.parse_known_args()[0] if known else parser.parse_args()


if __name__ == "__main__":

    opt = parse_opt()
    main(opt)