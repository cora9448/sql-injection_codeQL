from flask import Flask, render_template, request
import uuid
import sqlite3
import threading
import time

flag = "FLAG\{I love bob!!!\}"

tokendb = []
admintoken = []

waf = [';', '/', 'char', 'alter', 'begin', 'cast', 'create', 'cursor',
'delete', 'drop', 'exec', 'fetch', '!', '"', '$', '%', '&', '+', '.', ':',
'<', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '|', '~', '*', '#', ' ', '\t',
'\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x09',
'\x0a', '\x0b', '\x0c', '\x0d', '\x0e', '\x0f', '\x10', 'sleep',
'table', 'delay', 'wait', 'and', 'or', 'collate', 'substr', 'like',
'union', 'case', 'when', 'between', 'end', 'as', 'group', 'schema',
'describe', 'show', 'all', 'database', 'column', 'declare', 'set', 'count',
'exists', 'benchmark', 'bin', 'ascii', 'ord', 'order', 'if', 'extract',
'update', 'xml', 'lpad', 'rpad', 'insert', 'limit', 'from','admin']

guest_token = None
admin_token = None

def adminbot():
    global guest_token
    print(tokendb)
    time.sleep(1)
    tokendb.clear()
    print(tokendb)
    guest_token = None

def adminbot2():
    global admin_token
    admintoken.append(admin_token)
    print(admintoken)
    time.sleep(1)
    admintoken.clear()
    print(admintoken)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()

    id = request.form.get('id')
    pw = request.form.get('pw')

    c.execute('SELECT * FROM list WHERE id = "{}" and pw = "{}"'.format(id, pw))
    message = (f"SELECT * FROM list WHERE id = '{id}' and pw ='{pw}'")
    result = c.fetchall()

    if result:
        try:
            for i in range(len(waf)):
                if id in waf[i] or pw in waf[i]:
                    message2 = 'nohack'
                    break
                else:
                    if result[0][0] == 'admin':
                        message2 = ('hi admin',flag)

                    elif result[0][0] == 'guest':
                        message2 = 'hi guest'
                        global guest_token
                        global admin_token
                        guest_token = str(uuid.uuid4())
                        admin_token = str(uuid.uuid4())
                        threading.Thread(target=tokendb.append(guest_token)).start()
                        threading.Thread(target=adminbot).start()
                        threading.Thread(target=adminbot2).start()  
                        return render_template('main2.html', message2=message2, token=guest_token)

                    else:
                        message2 = 'login plz'

        except:
            pass
    else:
        message2 = 'login plz'

    conn.close()
    return render_template('main.html', message=message, message2=message2)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1323)
