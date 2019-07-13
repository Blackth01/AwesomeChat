# ChatRoomming
A simple chat room site built with Flask.


## Starting application
1. pip install -r requirements.txt
2. create a mysql database and configure the uri on config.py
3. flask db init
4. flask db migrate -m "creating database"
5. flask db upgrade
6. python chat.py
