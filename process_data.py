import pandas  as pd
import os
from tqdm import tqdm
import argparse

def createDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def convert(args):
    
    col = [
        "matchDate","symbol","matchPri","matchQty","tolMatchQty","matchTime",
        "bidPri1","bidPri2","bidPri3","bidPri4","bidPri5",
        "bidQty1","bidQty2","bidQty3","bidQty4","bidQty5",
        "askPri1","askPri2","askPri3","askPri4","askPri5",
        "askQty1","askQty2","askQty3","askQty4","askQty5",
        "openPri","highPri","lowPri","refPri","upPri","dnPri"
    ]


    
    for e_date in os.listdir(args["file"]):
        
        createDir(os.path.join(args["save"],e_date))
        symbols = os.listdir(os.path.join(args["file"],e_date))
        loop = tqdm(symbols,total=len(symbols))
        loop.set_description(f"Date : {e_date}")
        for symbol in loop:
            
            filePath = os.path.join(args["file"],e_date,symbol)
            savePath = os.path.join(args["save"],e_date,os.path.splitext(symbol)[0]+".csv")
    
            if os.path.isfile(savePath):
                continue
            
            with open(filePath,"r") as f :
                
                preTime = -1
                preData = list()
                allData = list()

                for file in f:

                    if file == "":
                        break
                
                    file = file.split(",")
                    if file[5] =="":
                        continue
                    
                    if preTime == -1:
                        preTime = file[5]
                        preData = file[:32]
                        continue

                    if file[5] != preTime:
                        
                        allData.append(preData)
                        preTime = file[5]
                    
                    preData = file[:32]
                if len(preData) != 0 :
                    allData.append(preData)

                df = pd.DataFrame(allData,columns=col)
                df.sort_values(by="matchTime")
                df.to_csv(savePath,index=False)


def main(opt):

    args = vars(opt)
    
    createDir(args["save"])
    convert(args)



def parse_opt(known = False):

    ROOT = os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument("--save",type=str, default = r"./stock_process")
    parser.add_argument("--file",type= str ,required=True,default=r"./stock_raw")


    return parser.parse_known_args()[0] if known else parser.parse_args()


if __name__ == "__main__":

    opt = parse_opt()
    main(opt)