import os
from flask import Flask, render_template, request, session
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
    global error

    error = {
        'title': '',
        'contents': ''
    }

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
    try:
        database()

        return render_template('sign-in.html')
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('sign-in.html', error=error)


@app.route('/sign-in', methods=['POST'])
def new_sign_in():
    try:
        username = request.form['inputUsername']
        password = request.form['inputPassword']

        cursor = mysql.get_db().cursor()

        cursor.execute(
            'SELECT user_id FROM tbl_user WHERE ' +
            'user_username = %s AND user_password = %s',
            (username, password)
        )

        result = cursor.fetchone()

        cursor.close()

        if result and len(result) == 1:
            session['user_id'] = result[0]

            if result[0] == 1:
                return list_exercise()
            else:
                return list_workout()
        else:
            error = {
                'title': 'Invalid user',
                'contents': 'Your request is invalid, ' +
                'check the information and try again!'
            }

            return render_template('sign-in.html', error=error)
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('sign-in.html', error=error)


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
            'INSERT INTO tbl_user ' +
            '(user_username, user_password) VALUES (%s, %s)',
            (username, password)
        )

        mysql.get_db().commit()

        cursor.close()

        return render_template('sign-in.html')
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('sign-up.html', error=error)


@app.route('/list-exercise')
def list_exercise(exercise_id=None):
    try:
        cursor = mysql.get_db().cursor()

        cursor.execute(
            'SELECT * FROM tbl_exercise'
        )

        exercises = cursor.fetchall()

        cursor.close()

        if exercise_id is None:
            return render_template('list-exercise.html', exercises=exercises)
        else:
            return render_template('list-exercise.html',
                                   exercise_id=exercise_id,
                                   exercises=exercises)
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('list-workout.html', error=error)


@app.route('/new-exercise')
def new_exercise():
    try:
        cursor = mysql.get_db().cursor()

        cursor.execute(
            'SELECT exercise_id, exercise_name FROM tbl_exercise'
        )

        datas = cursor.fetchall()

        return render_template('new-exercise.html', datas=datas)
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('new-exercise.html', error=error)


@app.route('/create-new-exercise', methods=['POST'])
def create_new_exercise():
    try:
        exercise_name = request.form['inputExercise']

        if exercise_name != 'default':
            cursor = mysql.get_db().cursor()

            cursor.execute(
                'INSERT INTO tbl_exercise ' +
                '(exercise_name) ' +
                'VALUES (%s)',
                (exercise_name)
            )

            mysql.get_db().commit()

            cursor.close()

            return list_exercise()
        else:
            error = {
                'title': 'Invalid fields',
                'contents': 'Check if the fields Exercise and ' +
                'Intensity are filled correctly and try again!'
            }

            return render_template('new-exercise.html', error=error)
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('new-exercise.html', error=error)


@app.route('/update-exercise/<exercise_id>')
def update_exercise(exercise_id=None):
    try:
        cursor = mysql.get_db().cursor()

        cursor.execute(
            'SELECT * FROM tbl_exercise WHERE exercise_id = %s',
            (exercise_id)
        )

        exercise = cursor.fetchall()

        return render_template('update-exercise.html',
                               exercise=exercise)
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('list-exercise.html', error=error)


@app.route('/make-update-exercise/<exercise_id>', methods=['POST'])
def make_update_exercise(exercise_id=None):
    try:
        exercise_name = request.form['inputExercise']

        cursor = mysql.get_db().cursor()

        cursor.execute(
            'UPDATE tbl_exercise SET ' +
            'exercise_name = %s ' +
            'WHERE exercise_id = %s',
            (exercise_name, exercise_id)
        )

        mysql.get_db().commit()

        cursor.close()

        return list_exercise()
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('list-exercise.html', error=error)


@app.route('/delete-confirmation-exercise/<exercise_id>')
def delete_confirmation_exercise(exercise_id):
    return list_exercise(exercise_id)


@app.route('/delete-exercise/<exercise_id>')
def delete_exercise(exercise_id=None):
    try:
        cursor = mysql.get_db().cursor()

        cursor.execute(
            'DELETE FROM tbl_exercise WHERE exercise_id = (%s)',
            (exercise_id)
        )

        mysql.get_db().commit()

        cursor.close()

        return list_exercise()
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('list-exercise.html', error=error)


@app.route('/list-workout')
def list_workout(workout_id=None):
    try:
        cursor = mysql.get_db().cursor()

        cursor.execute(
            'SELECT * FROM tbl_workout WHERE user_id = %s',
            (session['user_id'])
        )

        all = cursor.fetchall()

        datas = []

        for item in all:
            cursor.execute(
                'SELECT exercise_name FROM tbl_exercise ' +
                'WHERE exercise_id = %s',
                ({item[6]})
            )

            exercise_name = cursor.fetchone()

            datas.append({
                'workout_id': item[0],
                'workout_start': item[1].strftime("%d/%m/%Y %H:%M"),
                'workout_conclusion': item[2].strftime("%d/%m/%Y %H:%M"),
                'exercise_name': exercise_name[0],
                'intensity': item[4],
                'description': item[3],
            })

        cursor.close()

        if workout_id is None:
            return render_template('list-workout.html', datas=datas)
        else:
            return render_template('list-workout.html',
                                   datas=datas,
                                   workout_id=workout_id)
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('list-workout.html', error=error)


@app.route('/new-workout')
def new_workout():
    try:
        cursor = mysql.get_db().cursor()

        cursor.execute(
            'SELECT exercise_id, exercise_name FROM tbl_exercise'
        )

        datas = cursor.fetchall()

        return render_template('new-workout.html', datas=datas)
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('new-workout.html', error=error)


@app.route('/create-new-workout', methods=['POST'])
def create_new_workout():
    try:
        start = request.form['inputStart']
        conclusion = request.form['inputConclusion']
        exercise_id = request.form['inputExercise']
        intensity = request.form['inputIntensity']
        description = request.form['inputDescription']

        if exercise_id != 'default' and intensity != 'default':
            cursor = mysql.get_db().cursor()

            cursor.execute(
                'INSERT INTO tbl_workout ' +
                '(workout_start, workout_conclusion, description, ' +
                'intensity, user_id, exercise_id) ' +
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (start, conclusion, description, intensity,
                 session['user_id'], exercise_id)
            )

            mysql.get_db().commit()

            cursor.close()

            return list_workout()
        else:
            error = {
                'title': 'Invalid fields',
                'contents': 'Check if the fields Exercise and ' +
                'Intensity are filled correctly and try again!'
            }

            return render_template('new-workout.html', error=error)
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('new-workout.html', error=error)


@app.route('/update-workout/<workout_id>')
def update_workout(workout_id=None):
    try:
        datas = []

        cursor = mysql.get_db().cursor()

        cursor.execute(
            'SELECT * FROM tbl_workout WHERE workout_id = %s',
            (workout_id)
        )

        all = cursor.fetchone()

        cursor.execute(
            'SELECT exercise_name FROM tbl_exercise WHERE exercise_id = %s',
            (all[6])
        )

        exercise_name = cursor.fetchone()

        datas.append({
            'workout_id': all[0],
            'workout_start': all[1],
            'workout_conclusion': all[2],
            'exercise_id': all[6],
            'exercise_name': exercise_name[0],
            'intensity': all[4],
            'description': all[3],
        })

        cursor.execute(
            'SELECT exercise_id, exercise_name FROM tbl_exercise'
        )

        exercises = cursor.fetchall()

        return render_template('update-workout.html',
                               datas=datas, exercises=exercises)
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('list-workout.html', error=error)


@app.route('/make-update-workout/<workout_id>', methods=['POST'])
def make_update_workout(workout_id=None):
    try:
        start = request.form['inputStart']
        conclusion = request.form['inputConclusion']
        exercise_id = request.form['inputExercise']
        intensity = request.form['inputIntensity']
        description = request.form['inputDescription']

        cursor = mysql.get_db().cursor()

        cursor.execute(
            'UPDATE tbl_workout SET ' +
            'workout_start = %s, workout_conclusion = %s, ' +
            'description = %s, intensity = %s, ' +
            'exercise_id = %s WHERE workout_id = %s',
            (start, conclusion, description,
                intensity, exercise_id, workout_id)
        )

        mysql.get_db().commit()

        cursor.close()

        return list_workout()
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('list-workout.html', error=error)


@app.route('/delete-confirmation/<workout_id>')
def delete_confirmation(workout_id):
    return list_workout(workout_id)


@app.route('/delete-workout/<workout_id>')
def delete_workout(workout_id=None):
    try:
        cursor = mysql.get_db().cursor()

        cursor.execute(
            'DELETE FROM tbl_workout WHERE workout_id = (%s)',
            (workout_id)
        )

        mysql.get_db().commit()

        cursor.close()

        return list_workout()
    except Exception as e:
        error = {
            'title': 'Internal Server Error',
            'contents': str(e)
        }

        return render_template('list-workout.html', error=error)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
