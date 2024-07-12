# UrQMD parser

Two small scripts to cram UrQMD f14 file into a pandas DataFrame and save into `.parquet` type.

First reduce f14 and f15 files for easier processing and then run processor.py

The `plots` branch contains modified script with some matplotlib plotting I need.

## Usage

```shell
$ python3 reducer.py f14.dat
$ python3 reducer.py f15.dat
$ python3 processor.py
```
