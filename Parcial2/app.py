from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
import hashlib


app = Flask(__name__, template_folder='templates')
app.secret_key = 'admin2023'

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_academica"
)


cursor = db.cursor()
app.secret_key = 'tu_clave_secreta_aqui'

## Administracion de productos............................................................................

     

## Administracion de ................................................................
@app.route('/usuarios')
def mostrar_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        clave = request.form['clave']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        # Inserta el nuevo usuario en la base de datos
        cursor.execute("INSERT INTO usuarios (nombre, usuario, clave, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, usuario, clave, direccion, telefono))
        db.commit()

        return redirect('/usuarios')


@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    try:
        if request.method == 'POST':
            id_usuario = request.form['id_usuario']
            cursor.execute("DELETE FROM usuarios WHERE idUsuario = %s", (id_usuario,))
            db.commit()
        return redirect('/usuarios')
    except Exception as e:
        print(f"Error: {str(e)}")
        return redirect('/usuarios')


@app.route('/modificar_usuario', methods=['GET'])
def modificar_usuario():
    if request.method == 'GET':
        id_usuario = request.args.get('id_usuario')

        # Obtiene la información del usuario de la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE idUsuario = %s", (id_usuario,))
        usuario = cursor.fetchone()

        return render_template('modificar_usuario.html', usuario=usuario)


@app.route('/guardar_modificacionU', methods=['POST'])
def guardar_modificacionU():
    try:
        if request.method == 'POST':
            id_usuario = request.form['id_usuario']
            nombre = request.form['nombre']
            usuario = request.form['usuario']
            clave = request.form['clave']
            direccion = request.form['direccion']
            telefono = request.form['telefono']

            # Actualiza la información del usuario en la base de datos
            cursor.execute("UPDATE usuarios SET nombre=%s, usuario=%s, clave=%s, direccion=%s, telefono=%s WHERE idUsuario=%s",
                           (nombre, usuario, clave, direccion, telefono, id_usuario))
            db.commit()

            return redirect('/usuarios')
    except Exception as e:
        print(f"Error: {str(e)}")
        return redirect('/usuarios')

## Extras...................................................................................
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Comprobación directa sin hash
    if username == 'user1' and password == '123456':
        session['username'] = username
        return redirect(url_for('Inicio'))
    else:
        error = "Usuario o contraseña incorrecta. Inténtalo de nuevo."
    
    return render_template('login.html', error=error)


@app.route('/Rlogin', methods=['POST'])
def Relogin():
    username = request.form['username']
    password = request.form['password']

    # Comprobación directa sin hash
    if username == 'user1' and password == '123456':
        return redirect(url_for('admin'))
    else:
        error = "Usuario o contraseña incorrecta. Inténtalo de nuevo."

    return render_template('login1.html', error=error)





@app.before_request
def before_request():
    if 'username' not in session and request.endpoint not in ['formulario', 'login']:
        return redirect(url_for('formulario'))


@app.route('/logout', methods=['POST'])
def logout():
    # Eliminar la sesión de usuario
    session.pop('username', None)
    # Redirigir al formulario de inicio de sesión
    return redirect(url_for('formulario'))

## Area Inicial........................................................

@app.route('/')
def formulario():
    if 'username' in session:
        return redirect(url_for('Inicio'))
    return render_template('login.html')
    


@app.route('/inicio')
def Inicio():
    return render_template('inicio.html')


@app.route('/seguridad')
def seguridad():
    return render_template('seguridad.html')

@app.route('/login1')
def login1():
    return render_template('login1.html')

@app.route('/admin')
def admin():
    return render_template('administracion.html')

## Area Administrativa.................................................



@app.route('/producto')
def producto():
    return render_template('productos.html')



@app.route('/proveedor')
def proveedore():
    return render_template('proveedores.html')

@app.route('/cliente')
def cliente():
    return render_template('clientes.html')

@app.route('/empleados')
def empleados():
    return render_template('empleados.html')

@app.route('/entradas')
def entradas():
    return render_template('entradas.html')

@app.route('/salidas')
def salidas():
    return render_template('salidas.html')

@app.route('/ventas')
def venta():
    return render_template('ventas.html')

@app.route('/reporte')
def reportes():
    return render_template('reportes.html')

@app.route('/actus')
def actus():
    return render_template('actus.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)