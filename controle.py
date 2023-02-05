from PyQt5 import uic, QtWidgets
from reportlab.pdfgen import canvas
import mysql.connector

nova_conexao = mysql.connector.connect  (
    host='localhost',
    port='3306',
    user='root',
    passwd='',
    database=' cadastro_produtos'
)        

def gerar_pdf():
    cursor = nova_conexao.cursor()
    sql = """SELECT * FROM produtos"""
    cursor.execute(sql)
    dados_lidos= cursor.fetchall()
    y=0
    pdf=canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos Cadastrados: ")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "CÓDIGO")
    pdf.drawString(210, 750, "PRODUTO")
    pdf.drawString(380, 750, "PREÇO")
    pdf.drawString(480, 750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y+= 50 
        pdf.drawString(10 , 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(380, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(480, 750 - y, str(dados_lidos[i][4]))
    
    pdf.save()
    print("PDF FOI SALVO COM SUCESSO!")


def editar():
    linha= segunda_tela.tableWidget.currentRow()

    cursor=  nova_conexao.cursor() 
    sql=  '''SELECT id FROM produtos'''
    cursor.execute(sql)
    dados_lidos= cursor.fetchall()
    valor_id= dados_lidos[linha][0]

    banco= '''SELECT * FROM produtos WHERE id= '''+ str(valor_id)
    cursor.execute(banco)
    produto= cursor.fetchall()
    tela_editar.show()

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))

    print(produto[0][0])
    print(produto[0][4])


def excluir_produto():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    sql =  '''SELECT id FROM produtos'''
    cursor= nova_conexao.cursor() 
    cursor.execute(sql)
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    banco = '''DELETE FROM produtos WHERE id= '''+ str(valor_id)
    cursor.execute(banco)
    nova_conexao.commit()

def salvar_editado():
    print("TESTE")



def sair_janela():
    janela.close()  

def funcao_princial():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

    if linha1 == '':
        janela.show()
    elif linha2 == '':
        janela.show()
    elif linha3 == '':
        janela.show()
    else:
        categoria = ''
        if formulario.radioButton.isChecked():
            print("Categoria Informática foi selecionada")
            categoria = 'Informatica'
        elif formulario.radioButton_2.isChecked():
            print("Catergoria Alimentos foi selecionada")
            categoria = 'Alimentos'
        else: 
            formulario.radioButton_3.isChecked()
            print("Categoria Eletronicos foi selecionada ")
            categoria = 'Eletronicos'

            
        print("Codigo", linha1)
        print("Descricao", linha2)
        print("Preco", linha3)

        cursor = nova_conexao.cursor()
        comando_sql = 'INSERT INTO produtos(codigo, descricao, preco, categoria) VALUES(%s,%s,%s,%s)'
        dados = (str(linha1), str(linha2), str(linha3), categoria)
        cursor.execute(comando_sql, dados)
        nova_conexao.commit()
        formulario.lineEdit.setText("")
        formulario.lineEdit_2.setText("")
        formulario.lineEdit_3.setText("")

def chama_segunda_tela():
    segunda_tela.show()
 
    cursor = nova_conexao.cursor()
    comand_sql = "SELECT * FROM produtos"
    cursor.execute(comand_sql)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)
    for i in range(len(dados_lidos)):
        for j in range(0, 5):
            segunda_tela.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app=QtWidgets.QApplication([])
formulario=uic.loadUi("Projeto_Cadastro_de_Produtos.ui")
segunda_tela=uic.loadUi("listar_dados.ui")
janela=uic.loadUi("janela_atencao.ui")
tela_editar=uic.loadUi("menu.ui")
formulario.pushButton.clicked.connect( funcao_princial)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
janela.pushButton.clicked.connect(sair_janela)
segunda_tela.pushButton_2.clicked.connect(excluir_produto)
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_3.clicked.connect(editar)
tela_editar.pushButton.clicked.connect(salvar_editado)

formulario.show()
app.exec()