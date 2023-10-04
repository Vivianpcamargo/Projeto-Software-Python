import os
from flask import Flask, render_template, json, request, session
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'workoutDay'
app.config['MYSQL_DATABASE_HOST'] = '172.18.0.2'

app.secret_key = 'veRYdPHOqig2WqQZLzZxoGvxVy0Un6cV'

mysql.init_app(app)


def database():
    cursor = mysql.get_db().cursor()

    cursor.execute(
        'SHOW tables'
    )

    result = cursor.fetchall()

    if len(result) != 3:
        with open('./schemas/createDatabase.sql', 'r') as source_creation:
            arq_creation = source_creation.read()
            tuple_arq_creation = tuple(arq_creation.split(';\n'))
            for i in tuple_arq_creation:
                cursor.execute(i)

        with open('./schemas/insertData.sql', 'r') as source_insertion:
            arq_insertion = source_insertion.read()
            tuple_arq_insertion = tuple(arq_insertion.split(';\n'))
            for i in tuple_arq_insertion:
                cursor.execute(i)

        mysql.get_db().commit()

    cursor.close()


@app.route('/')
def sign_in():
    database()

    return render_template('sign-in.html')


@app.route('/sign-in', methods=['POST'])
def new_sign_in():
    try:
        username = request.form['inputUsername']
        password = request.form['inputPassword']

        cursor = mysql.get_db().cursor()

        cursor.execute(
            'SELECT user_id FROM tbl_user WHERE user_username = %s AND user_password = %s',
            (username, password)
        )

        result = cursor.fetchone()

        cursor.close()

        if len(result) == 1:
            session['user_id'] = result[0]

            return list_workout()
        else:
            return json.dumps({'html': '<span>Invalid user!</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/logout')
def logout():
    session['user_id'] = 0

    return render_template('sign-in.html')


@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')


@app.route('/new-sign-up', methods=['POST'])
def new_sign_up():
    try:
        username = request.form['inputUsername']
        password = request.form['inputPassword']

        cursor = mysql.get_db().cursor()

        cursor.execute(
            'INSERT INTO tbl_user (user_username, user_password) VALUES (%s, %s)',
            (username, password)
        )

        mysql.get_db().commit()

        cursor.close()

        return render_template('sign-in.html')
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/list-workout')
def list_workout():
    cursor = mysql.get_db().cursor()

    cursor.execute(
        'SELECT * FROM tbl_workout WHERE user_id = %s',
        (session['user_id'])
    )

    all = cursor.fetchall()

    datas = []

    for item in all:
        cursor.execute(
            'SELECT exercise_name FROM tbl_exercise WHERE exercise_id = %s',
            ({item[6]})
        )

        exercise_name = cursor.fetchone()

        datas.append({
            'workout_id': item[0],
            'workout_start': item[1].strftime("%d/%m/%Y %H:%M"),
            'workout_conclusion': item[2].strftime("%d/%m/%Y %H:%M"),
            'exercise_name': exercise_name[0],
            'instensity': item[4],
            'description': item[3],
        })

    cursor.close()

    return render_template('list-workout.html', datas=datas)


@app.route('/new-workout')
def new_workout():
    cursor = mysql.get_db().cursor()

    cursor.execute(
        'SELECT exercise_name FROM tbl_exercise'
    )

    datas = cursor.fetchall()

    return render_template('new-workout.html', datas=datas)


@app.route('/create-new-workout', methods=['POST'])
def create_new_workout():
    try:
        start = request.form['inputStart']
        conclusion = request.form['inputConclusion']
        exercise_name = request.form['inputExercise']
        instensity = request.form['inputIntensity']
        description = request.form['inputDescription']

        if exercise_name != 'default' and instensity != 'default':
            cursor = mysql.get_db().cursor()

            cursor.execute(
                'SELECT exercise_id FROM tbl_exercise WHERE exercise_name = %s',
                (exercise_name)
            )

            result = cursor.fetchone()

            exercise_id = result[0]

            cursor.execute(
                'INSERT INTO tbl_workout (workout_start, workout_conclusion, description, instensity, user_id, exercise_id) VALUES (%s, %s, %s, %s, %s, %s)',
                (start, conclusion, description, instensity,
                 session['user_id'], exercise_id)
            )

            mysql.get_db().commit()

            cursor.close()

            return list_workout()
        else:
            return json.dumps({'html': '<span>Fill in all fields!</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
