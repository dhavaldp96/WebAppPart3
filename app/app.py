from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'scores'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'scores Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM Snakes_Ladders')
    result = cursor.fetchall()
    print(result[0])
    return render_template('index.html', title='Home', user=user, scores=result)


@app.route('/view/<int:GameNumber>', methods=['GET'])
def record_view(GameNumber):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM Snakes_Ladders WHERE id=%s', sc_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View', score=result[0])


@app.route('/edit/<int:GameNumber>', methods=['GET'])
def form_edit_get(GameNumber):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM Snakes_Ladders WHERE id=%s', GameNumber)
    result = cursor.fetchall()
    print(result[0])
    return render_template('edit.html', title='Edit', score=result[0])


@app.route('/edit/<int:GameNumber>', methods=['POST'])
def form_update_post(GameNumber):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('GameNumber'), request.form.get('GameLength'))
    sql_update_query = """UPDATE Snakes_Ladders t SET t.GameNumber = %s, t.GameLength = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/scores/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New')


@app.route('/scores/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('GameNumber'), request.form.get('GameLenght'))
    sql_insert_query = """INSERT INTO Snakes_Ladders (GameNumber,GameLength) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:GameNumber>', methods=['POST'])
def form_delete_post(sc_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM Snakes_Ladders WHERE GameNumber = %s """
    cursor.execute(sql_delete_query, GameNumber)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/scores', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM Snakes_Ladders')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/scores/<int:GameNumber>', methods=['GET'])
def api_retrieve(GameNumber) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM Snakes_Ladders WHERE id=%s', GameNumber)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/scores/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/scores/<int:GameNumber>', methods=['PUT'])
def api_edit(GameNumber) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/scores/<int:sc_id>', methods=['DELETE'])
def api_delete(GameNumber) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM Snakes_Ladders WHERE GameNumber = %s """
    cursor.execute(sql_delete_query, GameNumber)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)