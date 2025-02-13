from flask import Flask,render_template,request
 
app=Flask(__name__)
 
@app.route("/")
def index():
    titulo="IDGS801"
    lista=["perdro","juan","luis"]
    return render_template("index.html",titulo=titulo,lista=lista)
 
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
    return f"<h1<!Hola,{usuario}</h1>"
 
@app.route("/numero/<int:n>")
def numero(n):
    return f"<h1>El numero es: {n}</h1>"
 
@app.route("/user/<int:id>/<string:username>")
def username(id,username):
    return f"<h1>Hola, {username} Tu ID es: {id}"
 
@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1,n2):
    return f"La suma es: {n1+n2}"
 
@app.route("/default/")
@app.route("/default/<string:param>")
def func(param="juan"):
    return f"<h1>Hola, {param}<h1>"
 
 
 
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
 

class Cine:
    precio_boleto = 12
    ventas = []

    def calcular_descuento(self, total, boletos):
        if boletos > 5:
            return total * 0.85
        elif 3 <= boletos <= 5:
            return total * 0.90
        else:
            return total

    def validar_boletos(self, personas, boletos):
        return boletos <= personas * 7

    def guardar_venta(self, nombre, total):
        self.ventas.append((nombre, total))

    def mostrar_resumen_ventas(self):
        if not self.ventas:
            return "No se realizaron ventas."
        else:
            resumen = ""
            total_general = 0
            for nombre, total in self.ventas:
                resumen += f"{nombre}: ${total:.2f}<br>"
                total_general += total
            resumen += f"Total General: ${total_general:.2f}"
            return resumen

cine = Cine()

@app.route("/cinepolis", methods=["GET", "POST"])
def cinepolis():
    resultado = None

    if request.method == "POST":
        nombre = request.form.get("nombre")
        personas = int(request.form.get("personas"))
        boletos = int(request.form.get("boletos"))
        metodo_pago = request.form.get("metodo_pago")

        if cine.validar_boletos(personas, boletos):
            total = cine.precio_boleto * boletos
            total_con_descuento = cine.calcular_descuento(total, boletos)

            # Aplicar descuento adicional si el método de pago es tarjeta
            if metodo_pago == "tarjeta":
                total_con_descuento *= 0.90

            cine.guardar_venta(nombre, total_con_descuento)
            resultado = f"Total a pagar: ${total_con_descuento:.2f}<br>"
        else:
            resultado = "Cantidad de boletos no válida (máximo 7 por persona)."

    return render_template("cinepolis.html", resultado=resultado)

@app.route("/goodbye")
def goodbye():
    return "Gracias por visitar Cinépolis. ¡Vuelve pronto!"

if __name__ == "__main__":
    app.run(debug=True, port=3000)