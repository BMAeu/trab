from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
host="localhost",
user="root",
passwd="",
database="vodan_br_bd"
)












@app.route("/")
def main():
    return render_template('index.html')


#------------------Gestao Formulario-------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/nv_quest') #CRIA UM NOVO QUESTIONARIO
def nv_quest():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tb_questionnaire;")
    resultado = cur.fetchall()
    cur.close()
    return render_template('nv_quest.html', data = resultado)

@app.route('/nv_quest2')
def nv_quest2():
    cur = mydb.cursor()
    description = request.args.get('description', '')
    cur.execute("SELECT max(questionnaireID) FROM tb_questionnaire")
    nv_ID = cur.fetchall()[0][0] + 1
    cur.execute("INSERT INTO tb_questionnaire (questionnaireID, description) VALUES ({0}, '{1}');".format(nv_ID, description))
    mydb.commit()
    cur.close()
    return render_template('nv_quest2.html', data = description)

@app.route('/crfform')
def crfform():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tb_questionnaire;")
    resultado = cur.fetchall()
    cur.close()
    return render_template('crfform.html', data = resultado)

@app.route('/crfform2')
def crfform2():
    cur = mydb.cursor()
    description_mod = request.args.get('description_mod', '')
    nv_ID = request.args.get('nv_ID', '')
    cur.execute("SELECT max(crfFormsID) FROM tb_crfforms")
    nv_ID_crrform = cur.fetchall()[0][0] + 1
    cur.execute("INSERT INTO tb_crfforms (crfFormsID, questionnaireID, description) VALUES ({0}, {1}, '{2}');".format(nv_ID_crrform, nv_ID, description_mod))
    mydb.commit()
    cur.close()
    return render_template('crfform2.html', data = description_mod)
    
@app.route('/questionGroupForm')
def questionGroupForm():
    cur = mydb.cursor()
    cur.execute("SELECT questionID, description FROM tb_questions;")
    resultado = cur.fetchall() 
    cur.close()
    return render_template('questionGroupForm.html', data = resultado)

@app.route('/questionGroupForm2')
def questionGroupForm2():
    cur = mydb.cursor()
    question_id = request.args.get('question_id','')
    question_order = request.args.get('question_order','')
    cur.execute("SELECT max(crfFormsID) FROM tb_crfforms")
    nv_ID_crrform = cur.fetchall()[0][0] + 1
    cur.execute("INSERT INTO tb_questiongroupform (crfFormsID, questionID, questionOrder) VALUES ({0}, {1}, {2});".format(nv_ID_crrform, question_id, question_order))
    mydb.commit()
    cur.close()
    return render_template('questionGroupForm2.html')
    
@app.route('/question')
def question():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tb_listtype;")
    tabela1 = cur.fetchall()
    cur.execute("SELECT * FROM tb_questiontype;")
    tabela = cur.fetchall()    
    cur.execute("SELECT * FROM tb_questiongroup;")
    tabela2 = cur.fetchall()  
    cur.close()
    return render_template('question.html', data = (tabela, tabela1, tabela2))
    
@app.route('/question2')
def question2():
    cur = mydb.cursor()
    new_question_text = request.args.get('new_question_text', '')
    new_question_typeID = request.args.get('new_question_typeID', '')
    new_question_list_typeID = request.args.get('new_question_list_typeID', '')
    new_question_groupID = request.args.get('new_question_groupID', '')
    cur.execute("SELECT max(questionID) FROM tb_questions;")
    nv_ID = cur.fetchall()[0][0] + 1
    query = "INSERT INTO tb_questions (questionID,  description, questionTypeID, listTypeID, questionGroupID) VALUES ({0},  '{1}',  {2},  {3}, {4});".format(nv_ID, new_question_text, new_question_typeID, new_question_list_typeID, new_question_groupID)
    cur.execute(query)
    mydb.commit()
    questao_criada = (nv_ID, new_question_text, new_question_typeID, new_question_list_typeID)        
    cur.close()
    return render_template('question2.html', data = new_question_text)
    
@app.route('/questGroup')
def questGroup():
    return render_template('questGroup.html')
    
@app.route('/questGroup2')
def questGroup2():
    cur = mydb.cursor()
    new_group_text = request.args.get('new_group_text', '')
    new_group_comment = request.args.get('new_group_comment', '')
    cur.execute("SELECT max(questionGroupID) FROM tb_questiongroup;")
    nv_ID_agrupamento = cur.fetchall()[0][0] + 1
    query = "INSERT INTO tb_questiongroup (questionGroupID,  description, comment) VALUES ({0},  '{1}',  '{2}');".format(nv_ID_agrupamento, new_group_text, new_group_comment)
    cur.execute(query)
    mydb.commit()     
    cur.close()
    return render_template('questGroup2.html', data = new_group_text)
#------------------------------------------------------------------------
@app.route('/at_quest') #ALTERAR QUESTIONARIO 
def at_quest():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tb_questionnaire;")
    resultado = cur.fetchall()
    cur.close()
    return render_template('at_quest.html', data = resultado)	
#------------------------------------------------------------------------
@app.route('/del_quest') #DELETA UM QUESTIONARIO EXISTENTE
def del_quest():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tb_questionnaire;")
    resultado = cur.fetchall()
    cur.close()
    return render_template('del_quest.html', data = resultado)
    
@app.route('/del_quest2')
def del_quest2():
    cur = mydb.cursor()
    d_questionnaireID = request.args.get('d_questionnaireID', '')
    cur.execute("SELECT count(questionnaireID) FROM tb_assessmentquestionnaire WHERE questionnaireID = {0}".format(d_questionnaireID))
    vezes = cur.fetchall()[0][0]
    if vezes != 0:
    	cur.close()
    	return "Nao pode deletar questionario com pesquisa associada"
    else:
    	cur.execute("DELETE FROM tb_questionnaire WHERE questionnaireID = {0};".format(d_questionnaireID))
    	mydb.commit()
    	cur.execute("DELETE FROM tb_questiongroupform WHERE crfFormsID = (SELECT crfFormsID FROM tb_crfforms WHERE questionnaireID = {0});".format(d_questionnaireID))
    	mydb.commit()
    	cur.execute("DELETE FROM tb_crfforms WHERE questionnaireID = {0};".format(d_questionnaireID))
    	mydb.commit()
    	cur.close()
    	return render_template('del_quest_final.html')
#------------------------------------------------------------------------
@app.route('/consul_quest') #CONSULTA QUESTIONARIO 
def consul_quest():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tb_questionnaire;")
    resultado = cur.fetchall()
    cur.close()
    return render_template('consul_quest.html', data = resultado)

@app.route('/consul_quest2')
def consul_quest2():
    cur = mydb.cursor()
    id_consulta = request.args.get('id_consulta', '')
    query = "SELECT tb_crfforms.description AS modulo, questao, agrupamento, tipo_questao, nome_lista, lista_respostas FROM tb_questionnaire LEFT JOIN (tb_crfforms LEFT JOIN (tb_questiongroupform LEFT JOIN ((SELECT tb_questions.description AS questao, tb_questions.questionID, tb_questiongroup.description AS agrupamento, tb_questiontype.description AS tipo_questao, tb_questions.listTypeID FROM tb_questiongroup RIGHT JOIN (tb_questions LEFT JOIN tb_questiontype ON tb_questions.questionTypeID = tb_questiontype.questionTypeID) ON tb_questions.questionGroupID = tb_questiongroup.questionGroupID) AS tabelaquestao LEFT JOIN (SELECT tb_listtype.listTypeID, tb_listtype.description AS nome_lista,tb_listofvalues.description AS lista_respostas FROM tb_listofvalues LEFT JOIN tb_listtype ON tb_listofvalues.listTypeID = tb_listtype.listTypeID) AS tabelatipo ON tabelatipo.listTypeID = tabelaquestao.listTypeID) ON tb_questiongroupform.questionID = tabelaquestao.questionID) ON tb_crfforms.crfFormsID = tb_questiongroupform.crfFormsID) ON tb_questionnaire.questionnaireID = tb_crfforms.questionnaireID WHERE tb_questionnaire.questionnaireID = {0}".format(id_consulta)
    cur.execute(query)
    resultado = cur.fetchall()
    cur.close()
    return render_template('consul_quest_final.html', data = resultado)


#------------------Gestao Tipo de Questao--------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/consul_tipo_questao') # CONSULTAR TIPOS DE QUESTOES
def consul_tipo_questao():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tb_questiontype;")
    resultado = cur.fetchall()
    cur.close()
    return render_template('consul_tipo_questao.html', data = resultado)
#------------------------------------------------------------------------
@app.route('/criar_tipo_questao') #CRIAR UM TIPO DE QUESTAO
def criar_tipo_questao():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tb_questiontype;")
    resultado = cur.fetchall()
    cur.close()
    return render_template('criar_tipo_questao.html', data = resultado)

@app.route('/criar_tipo_questao2')
def criar_tipo_questao2():
    cur = mydb.cursor()
    new_question_type = request.args.get('new_question_type', '')
    cur.execute("SELECT max(questionTypeID) FROM tb_questiontype;")
    nv_ID = cur.fetchall()[0][0] + 1
    cur.execute("INSERT INTO tb_questiontype (questionTypeID, description) VALUES ({0}, '{1}');".format(nv_ID, new_question_type))
    mydb.commit()
    tipo_nv = (nv_ID, new_question_type)
    cur.close()
    return render_template('criar_tipo_questao_final.html', data = tipo_nv)


#------------------Gestao Resposta Padronizada---------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/consul_resp') #CONSULTAR AS RESPOSTAS PADRONIZADAS E SUAS LISTAS CORRESPONDENTES
def consul_resp():
    cur = mydb.cursor()
    cur.execute("SELECT tb_listtype.description AS Listas, tb_listofvalues.description AS Respostas FROM tb_listofvalues RIGHT JOIN tb_listtype ON tb_listtype.listTypeID = tb_listofvalues.listTypeID ORDER BY Listas;")
    resultado = cur.fetchall()
    cur.close()
    return render_template('consul_resp.html', data = resultado)
#------------------------------------------------------------------------
@app.route('/criar_resp') #CRIAR LISTA DE RESPOSTAS PADRONIZADA
def criar_resp():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tb_listtype;")
    resultado = cur.fetchall()
    cur.close()
    return render_template('criar_resp.html', data = resultado)
    
@app.route('/criar_resp2')     
def criar_resp2():
    cur = mydb.cursor()
    new_list_type_description = request.args.get('new_list_type_description', '')
    cur.execute("SELECT max(listTypeID) FROM tb_listtype;")
    nv_ID = cur.fetchall()[0][0] + 1
    cur.execute("INSERT INTO tb_listtype (listTypeID, description) VALUES ({0}, '{1}');".format(nv_ID, new_list_type_description))
    mydb.commit()
    lista_nv = (nv_ID, new_list_type_description)
    cur.close()
    return render_template('criar_resp_final.html', data = lista_nv)
#------------------------------------------------------------------------
@app.route('/inserir_resp') # EM UMA LISTA EXISTENTE INSERIR NOVOS ITENS
def inserir_resp():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tb_listtype;")
    resultado = cur.fetchall()    
    cur.close()    
    return render_template('inserir_resp.html', data = resultado)
    
@app.route('/inserir_resp2') 
def inserir_resp2():
    cur = mydb.cursor()
    list_type_id = request.args.get('list_type_id', '')
    new_list_value_description = request.args.get('new_list_value_description', '')
    cur.execute("SELECT max(listOfValuesID) FROM tb_listofvalues;")
    nv_ID = cur.fetchall()[0][0] + 1
    cur.execute("INSERT INTO tb_listofvalues (listOfValuesID, listTypeID, description) VALUES ({0}, {1}, '{2}');".format(nv_ID, list_type_id, new_list_value_description))
    mydb.commit()
    cur.execute("SELECT description FROM tb_listtype WHERE listTypeID = {0};".format(list_type_id))
    lista_aumentada = cur.fetchall()[0][0]
    resposta_nv = (new_list_value_description, lista_aumentada)
    cur.close()    
    return render_template('inserir_resp_final.html', data = resposta_nv)
#------------------------------------------------------------------------
@app.route('/alterar_resp') # ALTERAR ITENS DE UMA LISTA EXISTENTE
def alterar_resp():
    cur = mydb.cursor()
    cur.execute("SELECT tb_listtype.listTypeID, listOfValuesID, tb_listtype.description AS Listas, tb_listofvalues.description AS Respostas FROM tb_listofvalues RIGHT JOIN tb_listtype ON tb_listtype.listTypeID = tb_listofvalues.listTypeID ORDER BY tb_listtype.listTypeID;")
    resultado = cur.fetchall()    
    cur.close()    
    return render_template('alterar_resp.html', data = resultado)

@app.route('/alterar_resp2')
def alterar_resp2():
    cur = mydb.cursor()
    list_type_id = request.args.get('list_type_id', '')
    list_values_id = request.args.get('list_values_id', '')
    new_list_value_description = request.args.get('new_list_value_description', '')
    cur.execute("SELECT count(listOfValuesID) FROM tb_questiongroupformrecord WHERE listOfValuesID = {0}".format(list_values_id))
    vezes = cur.fetchall()[0][0]
    if vezes != 0:
    	cur.close()
    	return "Nao pode alterar lista em uso, crie uma nova"
    else:
    	cur.execute("UPDATE  tb_listofvalues SET tb_listofvalues.description = '{0}' WHERE listOfValuesID={1} AND listTypeID={2};".format(new_list_value_description, list_values_id, list_type_id))
    	mydb.commit()
    	cur.close()
    	return render_template('alterar_resp_final.html', data = new_list_value_description)

#------------------Gestao Questao----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/criar_questao') # CRIAR QUESTAO
def criar_questao():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tb_listtype;")
    tabela1 = cur.fetchall()
    cur.execute("SELECT * FROM tb_questiontype;")
    tabela = cur.fetchall()
    cur.execute("SELECT questionID, description FROM tb_questions;")
    tabela2 = cur.fetchall()
    cur.close()
    return render_template('criar_questao.html', data = (tabela, tabela1, tabela2))

@app.route('/criar_questao2')
def criar_questao2():
    cur = mydb.cursor()
    new_question_text = request.args.get('new_question_text', '')
    new_question_typeID = request.args.get('new_question_typeID', '')
    new_question_list_typeID = request.args.get('new_question_list_typeID', '')
    cur.execute("SELECT max(questionID) FROM tb_questions;")
    nv_ID = cur.fetchall()[0][0] + 1
    query = "INSERT INTO tb_questions (questionID,  description, questionTypeID, listTypeID) VALUES ({0},  '{1}',  {2},  {3});".format(nv_ID, new_question_text, new_question_typeID, new_question_list_typeID)
    cur.execute(query)
    mydb.commit()
    questao_criada = (nv_ID, new_question_text, new_question_typeID, new_question_list_typeID)
    cur.close()
    return render_template('criar_questao_final.html', data = questao_criada)
#------------------------------------------------------------------------
@app.route('/subord_questao') #SUBORDINAR QUESTAO
def subord_questao():
    cur = mydb.cursor()
    cur.execute("SELECT questionID, description, subordinateTo FROM tb_questions;")
    resultado = cur.fetchall()        
    cur.close()
    return render_template('subord_questao.html', data = resultado)
    
@app.route('/subord_questao2')
def subord_questao2():
    cur = mydb.cursor()
    ID_questao_subordinada = request.args.get('ID_questao_subordinada', '')
    ID_questao_principal = request.args.get('ID_questao_principal', '')  
    query = "UPDATE tb_questions SET subordinateTo = {0} WHERE questionID = {1};".format(ID_questao_principal, ID_questao_subordinada)
    cur.execute(query)
    mydb.commit()
    cur.execute("SELECT description FROM tb_questions WHERE questionID = {0} OR questionID = {1}".format(ID_questao_subordinada, ID_questao_principal))
    resultado = cur.fetchall()
    cur.close()
    return render_template('subord_questao_final.html', data = resultado)


if __name__ == "__main__":
    app.run()
