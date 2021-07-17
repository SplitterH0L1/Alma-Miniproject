from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from alma.auth import login_required
from alma.db import get_db

bp = Blueprint('alma', __name__)

@bp.route('/')
@login_required
def index():
    db, c = get_db()
    c.execute(
        'select t.id, t.description, u.username, t.completed, t.created_at from alma t JOIN user u on t.created_by = u.id order by created_at desc'
    )

    almas= c.fetchall()

    return render_template("alma/index.html", alma=almas)

@bp.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method == "POST":
        description = request.form['description']
        error=None

        if not description:
            error = "descripcion es requerida"
        
        if error is not None:
            flash(error)

        else:
            db, c = get_db()
            c.execute(
                'insert into alma (description, completed, created_by)'
                ' values (%s, %s, %s)',
                (description, False, g.user['id'])
            )
            db.commit()
            return redirect(url_for('alma.index'))

    return render_template('alma/create.html')

def get_alma(id):
    db, c = get_db()
    c.execute(
        'select t.id, t.description, t.completed, t.created_by, t.created_at, u.username'
        ' from alma t JOIN user u on t.created_by = u.id where t.id = %s',
        (id,)
    )
    alma = c.fetchone()

    if alma is None:
        abort(404, "el alma de id {0} no existe".format(id))

    return alma



@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):

    alma = get_alma(id)
    if request.method == "POST":
        description = request.form['description']
        completed= True if request.form.get('completed') == 'on' else False
        error = None

        if not description:
            error = "la description es requerida." 
        
        if error is not None:
            flash(error)
        
        else:
            db, c = get_db()
            c.execute(
                'update alma set description = %s, completed= %s'
                ' where id = %s and created_by = %s',
                (description, completed, id, g.user['id'])
                
            )


            db.commit()
            return redirect(url_for('alma.index'))


    return render_template('alma/update.html', alma=alma)

@bp.route('/<int:id>/delete', methods=['GET'])
@login_required
def delete(id):
    db, c = get_db()

    c.execute(
        'delete from alma where id = %s and created_by = %s', (id, g.user['id'] )
    )
    db.commit()

    
    return redirect(url_for('alma.index'))
