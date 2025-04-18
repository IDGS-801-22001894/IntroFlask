from flask import Flask, render_template, request
from io import open
from datetime import datetime
import forms
from flask_wtf.csrf import CSRFProtect
from flask import flash
from flask import g
from forms import ZodiacoForm
from datetime import datetime 

from datetime import datetime

app = Flask(__name__)
app.secret_key="esta es una clave secreta"
csrf=CSRFProtect()
signos_zodiaco = {
    "Mono": "img/mono.png",
    "Gallo": "img/gallo.png",
    "Perro": "img/perro.png",
    "Cerdo": "img/cerdo.png",
    "Rata": "img/rata.png",
    "Buey": "img/buey.png",
    "Tigre": "img/tigre.png",
    "Conejo": "img/conejo.png",
    "Dragón": "img/dragon.png",
    "Serpiente": "img/serpiente.png",
    "Caballo": "img/caballo.png",
    "Cabra": "img/cabra.png"
}

@app.errorhandler(404)
def page_notfound(e):
    return render_template('404.html'), 404

@app.before_request
def before_requestr():
    g.user = "Mario"
    print("beforer1")

@app.after_request
def after_request(response):
    print("after1")
    return response

@app.route("/")
def index():
    nom='None'
    titulo = "IDGS801"
    lista = ["Pedro", "Juan", "Luis"]
    nom=g.user
    print("Index 2{}".format(g.user))
    return render_template("index.html", titulo=titulo,nom=nom,lista=lista)

@app.route("/ejemplo1")
def ejemplo1():
    return render_template("ejemplo1.html")

@app.route("/ejemplo2")
def ejemplo2():
    return render_template("ejemplo2.html")

@app.route("/hola")
def hola():
    return "<h1>Hola mundo hola</h1>"

@app.route("/user/<string:usuario>")
def user(usuario):
    return f"<h1>Hola, {usuario}</h1>"

@app.route("/numero/<int:n>")
def numero(n):
    return f"<h1>El número es: {n}</h1>"

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return f"<h1>Hola, {username}. Tu ID es: {id}</h1>"

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return f"La suma es: {n1 + n2}"

@app.route("/default/")
@app.route("/default/<string:param>")
def func(param="juan"):
    return f"<h1>Hola, {param}</h1>"

@app.route("/OperasBas", methods=["GET", "POST"])
def operas():
    resultado = None  # Inicializar la variable resultado

    if request.method == "POST":
        n1 = int(request.form.get("n1"))
        n2 = int(request.form.get("n2"))
        operacion = request.form.get("operacion")

        if operacion == "suma":
            resultado = f"{n1} + {n2} = {n1 + n2}"
        elif operacion == "resta":
            resultado = f"{n1} - {n2} = {n1 - n2}"
        elif operacion == "multiplicacion":
            resultado = f"{n1} * {n2} = {n1 * n2}"
        elif operacion == "division":
            if n2 != 0:
                resultado = f"{n1} / {n2} = {n1 / n2}"
            else:
                resultado = "Error: No se puede dividir por cero."

    return render_template("OperasBas.html", resultado=resultado)

@app.route("/Alumnos",methods=["GET","POST"])
def alumnos():
    mat=0
    nom=''
    ape=''
    email=''
    alumno_class=forms.UserForm(request.form)
    if request.method == 'POST' and alumno_class.validate():
        mat = alumno_class.matricula.data
        nom = alumno_class.nombre.data
        ape = alumno_class.apellido.data
        email = alumno_class.correo.data
 
        mensaje = 'Bienvenido {}'.format(nom)
        flash(mensaje)
 
    return render_template("Alumnos.html",form=alumno_class,mat=mat,nom=nom,ape=ape,email=email)



@app.route("/Zodiaco", methods=["GET", "POST"])
def zodiaco():
    zodiaco_class = forms.ZodiacoForm(request.form)
    resultado = None
    imagen_signo = None

    if request.method == "POST" and zodiaco_class.validate():
        
        nombreZ = zodiaco_class.nombreZ.data
        apellidoMaterno = zodiaco_class.apellidoMaterno.data
        apellidoPaterno = zodiaco_class.apellidoPaterno.data
        dia = zodiaco_class.dia.data
        mes = zodiaco_class.mes.data
        año = zodiaco_class.año.data
        sexo = zodiaco_class.sexo.data

        try:
            fecha_nacimiento = datetime(year=año, month=mes, day=dia)
            hoy = datetime.today()
            edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

            signos = ["Mono", "Gallo", "Perro", "Cerdo", "Rata", "Buey", "Tigre", "Conejo", "Dragón", "Serpiente", "Caballo", "Cabra"]
            signo_chino = signos[fecha_nacimiento.year % 12]

            imagen_signo = signos_zodiaco.get(signo_chino, "img/default.png")

            resultado = {
                "nombre": nombreZ,
                "apaterno": apellidoPaterno,
                "amaterno": apellidoMaterno,
                "edad": edad,
                "signo_chino": signo_chino,
                "imagen_signo": imagen_signo
            }

           
            mensaje = f'Bienvenido {nombreZ} {apellidoPaterno}, tienes {edad} años y tu signo chino es {signo_chino}.'
            flash(mensaje)

        except Exception as e:
            resultado = {"error": f"Error al procesar la fecha de nacimiento: {str(e)}"}

    return render_template("Zodiaco.html", form=zodiaco_class, resultado=resultado)


@app.route("/cine", methods=["GET", "POST"])
def cinepolis():
    resultado = None

    if request.method == "POST":
        nombre = request.form.get("nombre")
        personas = int(request.form.get("personas"))
        boletos = int(request.form.get("boletos"))
        metodo_pago = request.form.get("metodo_pago")

        if boletos <= personas * 7:
            total = 12 * boletos
            if boletos > 5:
                total *= 0.85
            elif 3 <= boletos <= 5:
                total *= 0.90
            if metodo_pago == "tarjeta":
                total *= 0.90
            resultado = f"Total a pagar: ${total:.2f}"
        else:
            resultado = "Cantidad de boletos no válida (máximo 7 por persona)."

    return render_template("cine.html", resultado=resultado)

@app.route("/goodbye")
def goodbye():
    return "Gracias por visitar Cinépolis. ¡Vuelve pronto!"

@app.route("/formulario", methods=["GET", "POST"])
def formulario():
    resultado = None
    imagen_signo = None

    if request.method == "POST":
        nombre = request.form.get("nombre")
        apaterno = request.form.get("apaterno")
        amaterno = request.form.get("amaterno")
        dia = request.form.get("dia")
        mes = request.form.get("mes")
        año = request.form.get("año")
        sexo = request.form.get("sexo")  

        
        
        try:
            fecha_nacimiento = datetime.strptime(f"{año}-{mes}-{dia}", "%Y-%m-%d")
            hoy = datetime.today()
            edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        
            signos = ["Mono", "Gallo", "Perro", "Cerdo", "Rata", "Buey", "Tigre", "Conejo", "Dragón", "Serpiente", "Caballo", "Cabra"]
            signo_chino = signos[(fecha_nacimiento.year) % 12]

           
            imagen_signo = signos_zodiaco.get(signo_chino, "img/default.png")

            resultado = {
                "nombre": nombre,
                "apaterno": apaterno,
                "amaterno": amaterno,
                "edad": edad,
                "signo_chino": signo_chino,
                "imagen_signo": imagen_signo
            }
        except ValueError:
            resultado = {"error": "Fecha de nacimiento no válida."}

    return render_template("formulario.html", resultado=resultado)

if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug=True, port=300)