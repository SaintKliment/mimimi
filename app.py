from flask import Flask, render_template, request, redirect, url_for
from models import Database
from UserLogin import UserLogin
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
db = Database()
login_manager = LoginManager(app)

app.config['SECRET_KEY'] = '4aa58657559c70f9956627007f99e93a2daf4f32'


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, db)

@app.route("/register", methods=['POST', 'GET'])
def register(request=request):
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = db.add_user(request.form['name'], request.form['email'], hash)
            if res:
                print("Вы успешно авторизированы", "success")
                return redirect(url_for('login'))
            else:
                print("Ошибка при добавлении в БД", "error")
        else:
            print("Неверно заполнены поля", "error")

    return render_template("register.html", title="Регистрация")

@app.route('/login', methods=['POST', 'GET'])
def login(request=request):
    if request.method == 'POST':
        user = db.get_user_email(request.form['email'])
        if user and check_password_hash(user[3], request.form['psw']):
            login_user(UserLogin().create(user))
            return redirect('/')
        
        else:
            print("неверная пара логин/пароль")
    
    return render_template("login.html", title="Авторизация")

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Index Page')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return f"""<p><a href="{url_for('logout')}">Выйти из профиля</a>
        </p>user info: {current_user.get_id()}"""

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    print('выход из аккакунта')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)

