# transform_stockFormat

### raw_data.py
* Process the raw data from yuanta API
>python raw_data.py --save <save_filepath> --file <stock_filepath>


### process_data.py
* Pick the same raw data from raw data 
>python process_data.py --save <save_filepath> --file <stock_filepath>


### use_data.py
* Generate the stock data between 9:00 and 13:25 
>python use_data.py --save <save_filepath> --file <stock_filepath> --symbol <symbol_data>

* symbol_data create as symbol.txt
* classification -> down : 0 , up : 1 ,flatten : 2
