import functools
from flask import Blueprint, flash, render_template, request, url_for, session, redirect, g

from werkzeug.security import check_password_hash, generate_password_hash

from alma.db  import get_db


bp = Blueprint("auth", __name__, url_prefix='/auth')

@bp.route('/register', methods=["GET", "POST"])
def register():
   if request.method== "POST":
      username= request.form["username"]
      password= request.form["password"]
      db, c= get_db()
      error=None
      c.execute(
         'select id from user where username = %s', (username,)
      )

      if not username:
         error= 'Username es requerido'
      
      if not password:
         error= "password es requerido"

      elif c.fetchone () is not None:
         error = "usuario {} se encuentra registrado".format(username)

      if error is None:
         c.execute (
            'insert into user (username, password) values (%s, %s)',
            (username, generate_password_hash(password))
         )

         db.commit()

         return redirect(url_for('auth.login'))


      flash (error)

   return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login ():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form ['password']
      db, c = get_db()
      error = None
      c.execute(
         'select * from user where username = %s', (username,)
      )
      user = c.fetchone()
   
      if user is None:
         error='Usuario y/o contraseña invalida'
      elif not check_password_hash(user['password'], password):
         error = 'Usurios y/o contraseña invalida'

      if error is None:
         session.clear()
         session['user_id'] = user ['id']
         return redirect(url_for('alma.index'))

      flash(error)
   
   return render_template('auth/login.html')

@bp.before_app_request
def load_looged_in_user():
   user_id = session.get('user_id')

   if user_id is None:
      g.user = None
   else:
      db, c = get_db()
      c.execute(
         'select * from user where id = %s', (user_id,)
      )
      g.user=c.fetchone()


def login_required(view):
   @functools.wraps(view)
   def wrapped_view(**kwargs):
      if g.user is None:
         return redirect(url_for('auth.login'))

      return view(**kwargs)
      
   return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))