import numpy as np
import os
import pandas  as pd
from tqdm import tqdm
import argparse

def createDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

# dir_name="./stock_dataset/"

def create_symbol_list(file_path):
    symbols = list()
    with open(file_path ,"r") as f:
    
        return f.read().split("\n")
    


def convert(args):

    path = args["file"]
    symbols= create_symbol_list(args["symbol"])
    for stock in symbols:
        target_stock = stock
        target_stockFilePath = args["save"]+"/"+target_stock
        print(target_stockFilePath)
        createDir(target_stockFilePath)

        date = os.listdir(path)
        
        # 日期 , 時間, 成交價 , 成交量 , 成交總量 ,買五檔價、買五檔量 、賣五檔價 、賣五檔量
        col = [
            "matchDate","symbol","matchPri","matchQty","tolMatchQty","matchTime",
            "bidPri1","bidPri2","bidPri3","bidPri4","bidPri5",
            "bidQty1","bidQty2","bidQty3","bidQty4","bidQty5",
            "askPri1","askPri2","askPri3","askPri4","askPri5",
            "askQty1","askQty2","askQty3","askQty4","askQty5",
            "openPri","highPri","lowPri","refPri","upPri","dnPri","label"
        ]

        for e_date in date:
            
            filePath  = os.path.join(path,e_date,target_stock+".csv")
            target_filePath = os.path.join(target_stockFilePath,e_date+".csv")
            
            # don't have file
            if  not os.path.isfile(filePath):    
                continue

            # already have processed file

            if os.path.isfile(target_filePath):
                continue

            data = pd.read_csv(filePath)
        
            # file is empty
            if len(data) == 0:
                continue
            # remove tolMatchQty equal to -1  
            data = data[data["tolMatchQty"]!=-1]    
            # reset DataFrame's index 
            data =data.reset_index(drop=True)
        
            # create new col , "label"
            data.insert(32,"label",np.NaN)
            # set processing bar
            loop = tqdm(range(len(data)))
            loop.set_description(f"Stock :{stock} , Date : {e_date}")

            index = -1
            for idx in loop:
                
                try:
                    # when match price is down
                    if data["matchPri"][idx] > data["matchPri"][idx+1]:
                        data.loc[idx,"label"] = 0
                    # when match price is up
                    elif data["matchPri"][idx] < data["matchPri"][idx+1]:
                        data.loc[idx,"label"] = 1
                    # when match price is flatten
                    else :
                        data.loc[idx,"label"] = 2
                except:
                    index =idx
                    data = data.drop(index=index)
                    continue

            data = data[data["matchTime"]!=133000000]
            
            data.to_csv(target_filePath,index=False)


def main(opt):

    args = vars(opt)
    
    createDir(args["save"])
    convert(args)



def parse_opt(known = False):

    ROOT = os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument("--save",type=str , default = r"./stock_dataset")
    parser.add_argument("--file",type= str  ,default = r"./examples/use_using")
    parser.add_argument("--symbol",type= str ,default= r"./examples/symbols.txt")


    return parser.parse_known_args()[0] if known else parser.parse_args()


if __name__ == "__main__":

    opt = parse_opt()
    main(opt)