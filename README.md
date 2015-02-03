# portdis
A Command-line Utility written in Python to migrate Redis Keys from 1 instance or database to another instance or database given the appropriate arguments

###Requirements
- Python
- Redis python module https://pypi.python.org/pypi/redis/  

###Supported Data Types

Currently, v1 only supports `Hash`, `List`, `Set`, & `String`

###Sample Usage
`$ python portdis.py -d 127.0.0.1 -x 6388 -f 2 -o 127.0.0.1 -y 9998 -s 3 -k '*PREFIX:foo*'`

This code above will automatically migrate keys that are supported data types to the destination redis from your origin.

Please read Wiki for reference.
