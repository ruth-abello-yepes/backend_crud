from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql 
import bcrypt
from flasgger import Swagger

app= Flask(__name__)
CORS(app) 
swagger = Swagger (app)

def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn

@app.route("/", methods=['GET'])
def consulta_general():
    """
    Consulta general del baúl de contraseñas
    ---
    responses:
      200:
        description: Lista de registros
    """
    try:
        conn = conectar('localhost', 'ruth', 'ruth', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul")
        datos = cur.fetchall()
        data = []
        for row in datos:
            dato = {'id_baul': row[0], 'plataforma': row[1], 'usuario': row[2], 'clave': row[3]}
            data.append(dato)
        cur.close()
        conn.close()
        return jsonify({'baul': data, 'mensaje': 'Baúl de contrasenas'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
    #ruta consulta individual
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    """
    Consulta individual por id
    ---
    parameters:
      - name: codigo 
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Registro encontrado
    """
    try:
        conn = conectar('localhost', 'ruth', 'ruth', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul WHERE id_baul = %s", (codigo,))
        dato = cur.fetchone()
        cur.close()
        conn.close()
        if dato:
            dato = {'id_baul': dato[0], 'plataforma': dato[1], 'usuario': dato[2], 'clave': dato[3]}
            return jsonify({'baul': dato, 'mensaje': 'Registro encontrado'})
        else:
            return jsonify({'mensaje': 'Registro no encontrado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

#ruta para registro 
@app.route("/registro", methods=['POST'])
def registro():
    """
    Registro de nueva contraseña
    ---
    parameters:
    - name: body
      in : body
      required: true
      shema:
        type: object
        properties:
          plataforma:
            type: string
          usuario:
            type: string
          clave:
            type: string
    responses:
      200:
        description: Registro agregado exitosamente
    """
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        clave = bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = conectar('localhost', 'ruth', 'ruth', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("INSERT INTO baul (plataforma, usuario, clave) VALUES (%s, %s, %s)",
                  (plataforma, usuario, clave))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro agregado exitosamente'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
    #ruta para eliminar registro
@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    """
    Eliminar un registro por id
    ---
    parameters:
      - name: codigo
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Registro eliminado exitosamente
    """
    try:
        conn = conectar('localhost', 'ruth', 'ruth', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("DELETE FROM baul WHERE id_baul = %s", (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro eliminado exitosamente'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
    #ruta para actualizar registro
@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    """
    Actualizar un registro por id
    ---
    parameters:
      - name: codigo
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            plataforma:
              type: string
            usuario:
              type: string
            clave:
              type: string
    responses:
      200:
        description: Registro actualizado exitosamente
    """
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        clave = bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = conectar('localhost', 'ruth', 'ruth', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("UPDATE baul SET plataforma = %s, usuario = %s, clave = %s WHERE id_baul = %s",
                  (plataforma, usuario, clave, codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro actualizado exitosamente'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
if __name__ == "__main__":
    app.run(debug=True)