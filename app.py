from flask import Flask, request, redirect, url_for, render_template
from redis import Redis

app = Flask(__name__)
cache = Redis(host='redis', port=6379, db=0,
              socket_connect_timeout=2, socket_timeout=2) # Añadimos timeouts

# --- RUTAS DE LA APLICACIÓN ---

@app.route('/')
def index():
    # --- Definimos las variables ANTES del try ---
    redis_status = ""
    status_class = ""
    tasks_list = []  # <--- IMPORTANTE: La lista de tareas se inicia vacía

    try:
        # --- REQUERIMIENTO 1: Comprobar conexión ---
        # El comando PING es la forma más rápida de saber si el servidor está vivo
        cache.ping()
        redis_status = "Conectado"
        status_class = "connected"

        # --- REQUERIMIENTO 2: Leer tareas (Read) ---
        # <--- MUDAMOS ESTA LÓGICA AQUÍ, DENTRO DEL TRY ---
        task_ids = cache.smembers('tasks:all')
        
        if task_ids:
            sorted_ids = sorted(task_ids, key=lambda x: int(x.decode('utf-8')))
            for task_id in sorted_ids:
                task_id_str = task_id.decode('utf-8')
                task_desc_bytes = cache.hget(f'task:{task_id_str}', 'description')
                task_desc = task_desc_bytes.decode('utf-8') if task_desc_bytes else "(Sin descripción)"
                
                tasks_list.append({
                    'id': task_id_str,
                    'description': task_desc
                })

    except Exception as e:
        # Si CUALQUIER cosa de arriba falla (el ping o el smembers/hget),
        # caemos aquí.
        redis_status = f"Desconectado"
        status_class = "disconnected"
        # No hacemos nada con tasks_list, se quedará como una lista vacía,
        # lo cual es correcto.

    # --- RENDERIZADO ---
    # La plantilla se renderiza en cualquier caso, ya sea con
    # la lista de tareas llena o vacía.
    return render_template(
        'index.html',
        redis_status=redis_status,
        status_class=status_class,
        tasks=tasks_list  
    )

# REQUERIMIENTO 2: CRUD (Create)
@app.route('/add', methods=['POST'])
def add_task():
    try:
        task_description = request.form['task']
        if task_description:
            new_id = cache.incr('next_task_id')
            cache.hset(f'task:{new_id}', 'description', task_description)
            cache.sadd('tasks:all', new_id)
    except Exception as e:
        # Opcional: manejar el error si Redis está caído al añadir
        print(f"Error al añadir tarea: {e}")
        pass # Simplemente no hace nada
        
    return redirect(url_for('index'))

# REQUERIMIENTO 2: CRUD (Delete)
@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    try:
        cache.srem('tasks:all', task_id)
        cache.delete(f'task:{task_id}')
    except Exception as e:
        print(f"Error al borrar tarea: {e}")
        pass
        
    return redirect(url_for('index'))

# REQUERIMIENTO 2: CRUD (Update)
@app.route('/update/<task_id>', methods=['POST'])
def update_task(task_id):
    try:
        new_description = request.form['new_task']
        if new_description:
            cache.hset(f'task:{task_id}', 'description', new_description)
    except Exception as e:
        print(f"Error al actualizar tarea: {e}")
        pass
        
    return redirect(url_for('index'))


# El 'if' de siempre para iniciar el servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)