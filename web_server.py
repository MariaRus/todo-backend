from flask import Flask, request
from resources import EntryManager
from resources import Entry

FOLDER = 'C:/Users/m_rusinovich/Desktop/to-do-list/'
app = Flask(__name__)

@app.route("/api/entries/")
def get_entries():
    entry_manager = EntryManager(FOLDER)
    entry_manager.load()
    entries_list = []
    for entry in entry_manager.entries:
        entries_list.append(entry.json())
    return entries_list

@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    data = request.get_json()
    print(data)
    for entry_data in data:
        entry = Entry.from_json(entry_data)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)