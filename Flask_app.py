# app.py
from flask import Flask, render_template, request, redirect, send_file
from datetime import datetime
import pandas as pd

app = Flask(__name__)

guestbook_entries = []

@app.route('/')
def index():
    return render_template('index.html', entries=guestbook_entries)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    name = request.form.get('name')
    rut = request.form.get('rut')
    age = request.form.get('age')
    phone = request.form.get('phone')
    message = request.form.get('message')

    if name and rut and age and phone:
        entry = {
            'name': name,
            'rut': rut,
            'age': age,
            'phone': phone,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        guestbook_entries.append(entry)

    return redirect('/')

@app.route('/delete_entry/<int:index>')
def delete_entry(index):
    if 0 <= index < len(guestbook_entries):
        del guestbook_entries[index]

    return redirect('/')

@app.route('/export_excel')
def export_excel():
    if guestbook_entries:
        # Crear un DataFrame con todos los campos
        df = pd.DataFrame(guestbook_entries, columns=['name', 'rut', 'age', 'phone', 'message', 'timestamp'])

        # Guardar el DataFrame en un archivo Excel
        filename = 'guestbook_entries.xlsx'
        df.to_excel(filename, index=False)

        # Enviar el archivo Excel como una descarga
        return send_file(filename, as_attachment=True)
    else:
        return "No entries to export."
    
@app.route('/edit_entry/<int:index>', methods=['GET', 'POST'])
def edit_entry(index):
    if 0 <= index < len(guestbook_entries):
        entry = guestbook_entries[index]

        if request.method == 'POST':
            # Procesar el formulario de edición
            entry['name'] = request.form.get('name')
            entry['rut'] = request.form.get('rut')
            entry['age'] = request.form.get('age')
            entry['phone'] = request.form.get('phone')
            entry['message'] = request.form.get('message')
            entry['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            return redirect('/')
        else:
            # Mostrar el formulario de edición
            return render_template('edit_entry.html', index=index, entry=entry)
    else:
        return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)
