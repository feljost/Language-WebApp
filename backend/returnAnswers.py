from flask import Flask, request, jsonify
import pandas as pd
import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import create_engine
import requests
from flask import request
import json
import numpy as np

app = Flask(__name__)



# Create Connection to the SQL Database
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

create_connection(db_name='group1',
                 db_user='admin_group1',
                 db_password="pXysH3Qdhz7ZLhkRgz89mTQCQG",
                 db_host='35.228.244.65',
                 db_port='5432')

engine = create_engine('postgresql://admin_group1:pXysH3Qdhz7ZLhkRgz89mTQCQG@35.228.244.65:5432/group1')



# Get ML assigned exercise
@app.route('/returnanswer', methods=['GET', 'POST'])
def returnanswer():

    # get dataframe from the database.
    users = pd.read_sql('users2', engine)

    answers_returned = json.loads(request.data)
    #answers_returned = {'name': "Räto", 'surname': "Kessler", 'task_id': 130, 'duration': 110}

    # add user_id
    for row in range(len(users)):
        if users.loc[row, 'name'] == answers_returned['name'] and users.loc[row, 'surname'] == answers_returned['surname']:
             answers_returned['user_id'] = users.loc[row, 'user_id']

    # transform into df
    answers_returned = pd.DataFrame.from_dict(answers_returned, orient='index')
    answers_returned = answers_returned.transpose()

    # Load it back into the database.
    answers_returned.to_sql('answers2', engine, if_exists="append", method='multi', index=False)

    return jsonify({'message': 'answer returned'})


"""
#FRONTEND
import requests
import pandas as pd

json_file = {'name': "Räto", 'surname': "Kessler", 'task_id': 130, 'duration': 110}
response = requests.post('http://localhost:5000/returnanswer', json=json_file)
print(response.text)
"""






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

