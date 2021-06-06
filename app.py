from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'voda_br_bd'
#app.config['MYSQL_CURSORCLASS']

mysql = MySQL(app)



@app.route("/")
def main():
    return render_template('index.html')


#------------------Gestao Formulario----------------------------------------
@app.route('/nv_quest')
def nv_quest():
    return render_template('nv_quest.html')

@app.route('/at_quest')
def at_quest():
    return render_template('at_quest.html')

@app.route('/del_quest')
def del_quest():
    return render_template('del_quest.html')

@app.route('/consul_quest')
def consul_quest():
    return render_template('consul_quest.html')


#------------------Gestao Tipo de Questao----------------------------------------
@app.route('/consul_tipo_questao')
def consul_tipo_questao():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM tb_questions''')
    resultado = cur.fetchall()
    cur.close
    return render_template('consul_tipo_questao.html', data = resultado)

@app.route('/criar_tipo_questao')
def criar_tipo_questao():
    return render_template('criar_tipo_questao.html')


#------------------Gestao Resposta Padronizada----------------------------------------
@app.route('/consul_resp')
def consul_resp():
    return render_template('consul_resp.html')

@app.route('/criar_resp')
def criar_resp():
    return render_template('criar_resp.html')

@app.route('/inserir_resp')
def inserir_resp():
    return render_template('inserir_resp.html')

@app.route('/alterar_resp')
def alterar_resp():
    return render_template('alterar_resp.html')

#------------------Gestao Questao----------------------------------------
@app.route('/criar_questao')
def criar_questao():
    return render_template('criar_questao.html')

@app.route('/criar_questao', methods=['POST'])
def criar_questao_post():
    new_question_text = request.form['new_question_text']
    new_question_type = request.form['new_question_type']
    new_question_list_type = request.form['new_question_list_type']
    return new_question_text, new_question_type, new_question_list_type
#------
@app.route('/subord_questao')
def subord_questao():
    return render_template('subord_questao.html')

@app.route('/subord_questao', methods=['POST'])
def subord_questao_post():
    ID_questao_subordinada = request.form['ID_questao_subordinada']
    ID_questao_principal = request.form['ID_questao_principal']
    return ID_questao_subordinada, ID_questao_principal



if __name__ == "__main__":
    app.run()    