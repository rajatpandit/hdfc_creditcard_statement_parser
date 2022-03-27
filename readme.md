## HDFC Statement Parser

```
pip install -r requirements.txt
```

and running this for `statement.pdf`
```
python parser.py -s statement.pdf
```
this will generate an output.csv file

Original script credit to https://github.com/santosh1994/hdfc-creditcard-statement-parser

 ### Modifed from original
* Working with a single pdf file and control the output file name
* Fixed issues with date parsing - org script didn't work for date with timestamps
* Extended to add the credit/debit as transaction type
* WIP - categorisation of transactions