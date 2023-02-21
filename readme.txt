
# bloggly

To run this file, the following is needed

create virtual environement

pip3 install flask 
pip3 install psycopg2-binary
pip3 install flask-sqlalchemy

​
****************************************************
Hardcoded into the app.py is the database "blog_db"

to run file, run createdb blog_db on an active postgres server
 install ipython if you don't already have it, and use %run seed.py to populate 
 database with starter data
 or use psql < seed.py
 ****************************************************