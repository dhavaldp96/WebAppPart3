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
app.config['MYSQL_DATABASE_DB'] = 'Snakes_Ladders'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Snakes and Ladders Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblsnldImport')
    result = cursor.fetchall()
    print(result[0])
    return render_template('index.html', title='Home', user=user, results=result)


@app.route('/view/<int:res_GameNumber>', methods=['GET'])
def record_view(res_GameNumber):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblsnldImport WHERE GameNumber=%s', res_GameNumber)
    result = cursor.fetchall()
    print(result[0])
    return render_template('view.html', title='View Form', res=result[0])


@app.route('/edit/<int:res_GameNumber>', methods=['GET'])
def form_edit_get(res_GameNumber):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblsnldImport WHERE GameNumber=%s', res_GameNumber)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', res=result[0])


@app.route('/edit/<int:res_GameNumber>', methods=['POST'])
def form_update_post(res_GameNumber):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('GameNumber'), request.form.get('GameLength'), res_GameNumber)
    sql_update_query = """UPDATE tblsnldImport t SET t.GameNumber = %s, t.GameLength = %s WHERE t.GameNumber = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/results/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New')


@app.route('/results/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('GameNumber'), request.form.get('GameLength'))
    sql_insert_query = """INSERT INTO tblsnldImport (GameNumber, GameLength) VALUES (%s, %s)"""
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:res_GameNumber>', methods=['POST'])
def form_delete_post(res_GameNumber):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblsnldImport WHERE GameNumber = %s """
    cursor.execute(sql_delete_query, res_GameNumber)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/results', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblsnldImport')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/results/<int:res_GameNumber>', methods=['GET'])
def api_retrieve(res_GameNumber) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblsnldImport WHERE GameNumber=%s',res_GameNumber)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/results/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/results/<int:res_GameNumber>', methods=['PUT'])
def api_edit(res_GameNumber) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/results/<int:res_GameNumber>', methods=['DELETE'])
def api_delete(res_GameNumber) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblsnldImport WHERE GameNumber = %s """
    cursor.execute(sql_delete_query,res_GameNumber)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
