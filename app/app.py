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
    cursor.execute('SELECT * FROM scoresImport')
    result = cursor.fetchall()
    print(result[0])
    return render_template('index.html', title='Home', user=user, scores=result)


@app.route('/view/<int:sc_id>', methods=['GET'])
def record_view(sc_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM scoresImport WHERE id=%s', sc_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', score=result[0])


@app.route('/edit/<int:sc_id>', methods=['GET'])
def form_edit_get(sc_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM scoresImport WHERE id=%s', sc_id)
    result = cursor.fetchall()
    print(result[0])
    return render_template('edit.html', title='Edit Form', score=result[0])


@app.route('/edit/<int:sc_id>', methods=['POST'])
def form_update_post(sc_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldLName'), request.form.get('fldFName'), request.form.get('ssn'),
                 request.form.get('test1'), request.form.get('test2'), request.form.get('test3'), request.form.get('test4'), request.form.get('final'), request.form.get('grade'), sc_id)
    sql_update_query = """UPDATE scoresImport t SET t.fldLName = %s, t.fldFName = %s, t.ssn = %s, t.test1 = 
    %s, t.test2 = %s, t.test3 = %s, t.test4 = %s, t.final = %s, t.grade = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/scores/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New scores Form')


@app.route('/scores/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldLName'), request.form.get('fldFName'), request.form.get('ssn'),
                 request.form.get('test1'), request.form.get('test2'), request.form.get('test3'), request.form.get('test4'), request.form.get('final'),
                 request.form.get('grade'))
    sql_insert_query = """INSERT INTO scoresImport (fldLName,fldFName,ssn,test1,test2,test3,test4,final,grade) VALUES (%s, %s,%s, %s,%s, %s,%s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:sc_id>', methods=['POST'])
def form_delete_post(sc_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM scoresImport WHERE id = %s """
    cursor.execute(sql_delete_query, sc_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/scores', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM scoresImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/scores/<int:sc_id>', methods=['GET'])
def api_retrieve(sc_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM scoresImport WHERE id=%s', sc_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/scores/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/scores/<int:sc_id>', methods=['PUT'])
def api_edit(sc_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/scores/<int:sc_id>', methods=['DELETE'])
def api_delete(sc_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM scoresImport WHERE id = %s """
    cursor.execute(sql_delete_query, sc_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)