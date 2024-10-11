import customtkinter
from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import tkinter as tk
from PIL import Image
import datetime
from datetime import date, timedelta, datetime
import sqlite3



def Datas_all():
    global data
    global dval
    data = Calendario.get_date()
    datainfostr = txtVal.get()
    dataint = int(datainfostr)
    dinfo = timedelta(dataint)
    dval = data + dinfo
    pass


def limpar_Cadastro():
    txtTAG.delete(0, END)
    txtDesc.delete(0, END)
    txtOrgão.delete(0, END)
    txtNum.delete(0, END)
    txtVal.delete(0, END)
    pass


def conectardb():
    global conecta
    global cursor
    conecta = sqlite3.connect("Padrões.db")
    cursor = conecta.cursor()
    print("conectado")
    pass


def desconectadb():
    conecta.close()
    print("desconectado")
    pass


def criartabela():
    conectardb()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS padroes(
        Tag TEXT NOT NULL,
        Orgao TEXT NOT NULL,
        Certificado TEXT NOT NULL,
        Descrição TEXT NOT NULL,
        DataCal TEXT NOT NULL,
        DataVal TEXT NOT NULL,
        Estatus TEXT NOT NULL
        );
    """)
    conecta.commit()
    print("Tabela Criada com Sucesso")
    desconectadb()
    pass


def receber_entradas_Cadastro():
    global CertfN
    tag = txtTAG.get()
    orgao = txtOrgão.get()
    CertfN = txtNum.get()
    Desc = txtDesc.get()
    Dcal = data
    Dval = dval
    try:
        conectardb()
        cursor.execute("""
            INSERT INTO padroes (Tag,Orgao,Certificado,Descrição,DataCal,DataVal,Estatus)
            VALUES(?,?,?,?,?,?,'')
        """, (tag, orgao, CertfN, Desc, Dcal, Dval))

    
        if (tag == "" or orgao == "" or CertfN == "" or Desc == ""):
            messagebox.showerror(title="Sistema de Cadastro",
                                 message="Por favor, preencha todos os campos!!!")
        else:
            conecta.commit()
            messagebox.showinfo(title="Sistema de Cadastro",
                                message="Padrão Cadastrado com Sucesso!")
            desconectadb()
    except:
        messagebox.showerror(title="Sistema de Cadastro",
                             message="Error NotFound 404")
    pass


def Status():
    conectardb()
    cursor.execute(
        "SELECT DataVal FROM padroes WHERE Certificado = ?", (CertfN,))
    resultados = cursor.fetchall()
    dr = resultados[0]
    drd = datetime.strptime(dr[0], "%Y-%m-%d")
    dabd = drd.strftime("%Y-%m-%d")
    daf = datetime.strptime(dabd, "%Y-%m-%d")
    datahj = date.today()
    if datetime.date(daf) < datahj:
        status = 'OBSOLETO'
    else:
        status = 'VÁLIDO'
    cursor.execute(
        "UPDATE padroes SET Estatus = ? WHERE Certificado = ?", (status, CertfN,))

    conecta.commit()
    desconectadb()
    pass


def Rodar_programa():
    Datas_all()
   
    receber_entradas_Cadastro()
    limpar_Cadastro()
    Status()
    pass

def popular():
    tree.delete(*tree.get_children())
    conectardb()
    cursor.execute("SELECT * FROM padroes")
    dados = cursor.fetchall()
    cursor.close()
    desconectadb()
    for i in dados:
        tree.insert("","end", values=i)
    pass
def consulta():
    global NtxtNPC
    tree.delete(*tree.get_children())
    conectardb()
    NtxtNPC = txtNPC.get()
    cursor.execute ("SELECT * FROM padroes WHERE Certificado = ?", (NtxtNPC,))
    dadosc = cursor.fetchall()
    cursor.close()
    desconectadb()
    for i in dadosc:
        tree.insert("","end", values=i)
    conectardb()    
    cursor.execute ("SELECT Estatus FROM padroes WHERE Certificado = ?", (NtxtNPC,))
    status = cursor.fetchall()[0]
    statusF = status[0]
    cursor.close()
    desconectadb()
    if statusF == "VÁLIDO":
        messagebox.showinfo(title="Sistema de Cadastro",message="Certificado Críticamente Analisado e Válido!!")
    else:
        messagebox.showinfo(title="Sistema de Cadastro",message="Certificado Críticamente Analisado e Obsoleto, Enviar para Calibração!!")   
    pass
def Deletar_Padrão():
    NtxtNPC = txtNPC.get()
    conectardb()
    cursor.execute("DELETE FROM padroes WHERE Certificado = ?", (NtxtNPC,))
    conecta.commit()
    cursor.close()
    desconectadb()
    txtNPC.delete(0, END)
    messagebox.showinfo(title="Sistema de Cadastro",message="Certificado Deletado com sucesso!")
    pass
def Atualizar():
    conectardb()
    cursor.execute("""UPDATE padroes SET Estatus = CASE WHEN DataVal>date("now") THEN "VÁLIDO" ELSE "OBSOLETO" END;""")
    conecta.commit()
    cursor.close()
    desconectadb()
    print ("Estatus Atualizado")
    pass
def Notificar():
    Em = txtEmail.get()
    diasE = txtDtEmail.get()
    conectardb()
    cursor.execute("""
            UPDATE Email SET Email = ?, Dias = ?
        """, (Em, diasE))
    conecta.commit()
    desconectadb()
    txtEmail.delete(0, END)
    txtDtEmail.delete(0, END)
    messagebox.showinfo(title="Sistema de Cadastro",message="Email, e dias Atualizados!")
    pass
def Criartabela_Cad_Email():
    conectardb()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Email(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Email TEXT NOT NULL,
            Dias TEXT NOT NULL
        );
    """)
    conecta.commit()
    print("Tabela Email Criada com Sucesso")
    desconectadb()
    pass
janela = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
janela.geometry("600x350")
# criando Abas
dias = 30
tabview = customtkinter.CTkTabview(janela, width=550, height=300)
tabview.pack()
tabview.add("Cadastrar Padrão")
tabview.tab("Cadastrar Padrão").grid_columnconfigure(0, weight=1)
tabview.add("Consultar")
tabview.tab("Consultar").grid_columnconfigure(0, weight=1)
tabview.add("Configurações")
tabview.tab("Configurações").grid_columnconfigure(0, weight=1)
# campos da primeira ABA
lbltitulo = customtkinter.CTkLabel(tabview.tab(
    "Cadastrar Padrão"), width=10, height=10, text="Cadastrar Padrão", font=("Arial bold", 20))
lbltitulo.pack()
lblTAG = customtkinter.CTkLabel(tabview.tab(
    "Cadastrar Padrão"), text="Identificação TAG:").place(x=40, y=30)
txtTAG = customtkinter.CTkEntry(tabview.tab(
    "Cadastrar Padrão"), placeholder_text="         Digite o TAG", width=160)
txtTAG.place(x=145, y=30)
lblOrgão = customtkinter.CTkLabel(tabview.tab("Cadastrar Padrão"), text="Órgão Calibrador:").place(x=40, y=60)
txtOrgão = customtkinter.CTkEntry(tabview.tab("Cadastrar Padrão"), placeholder_text="Digite o Órgão Calibrador ", width=160)
txtOrgão.place(x=145, y=60)
lblNum = customtkinter.CTkLabel(tabview.tab(
    "Cadastrar Padrão"), text="N° Certificado:").place(x=40, y=90)
txtNum = customtkinter.CTkEntry(tabview.tab(
    "Cadastrar Padrão"), placeholder_text="Digite o N° do Certificado", width=160)
txtNum.place(x=145, y=90)
lblNum = customtkinter.CTkLabel(tabview.tab(
    "Cadastrar Padrão"), text="N° Certificado:").place(x=40, y=90)
txtDesc = customtkinter.CTkEntry(tabview.tab(
    "Cadastrar Padrão"), placeholder_text="     Digite a Descrição", width=160)
txtDesc.place(x=145, y=120)
lblDesc = customtkinter.CTkLabel(tabview.tab(
    "Cadastrar Padrão"), text="Descrição Padrão:").place(x=40, y=120)
lblCali = customtkinter.CTkLabel(tabview.tab(
    "Cadastrar Padrão"), text="Data de Calibração:").place(x=40, y=150)
Calendario = DateEntry(tabview.tab("Cadastrar Padrão"),
                       format="%d/%m/%y", locale="pt_BR", width=14, font=("Arial", 15))
Calendario.place(x=200, y=190)
lblVal = customtkinter.CTkLabel(tabview.tab(
    "Cadastrar Padrão"), text="Digite a Periodicidade em dias:").place(x=40, y=180)
txtVal = customtkinter.CTkEntry(tabview.tab(
    "Cadastrar Padrão"), placeholder_text="Digite os dias", width=90)
txtVal.place(x=215, y=180)

# definindo imagem ao Lado
img1 = customtkinter.CTkImage(light_image=Image.open(
    './inmetro2.jpg'), dark_image=Image.open('./inmetro2.jpg'), size=(150, 150))
lblimage = customtkinter.CTkLabel(tabview.tab(
    "Cadastrar Padrão"), text=None, image=img1, corner_radius=20).place(x=350, y=30)

# alocando Botão de Registrar Padrão
customtkinter.CTkButton(tabview.tab("Cadastrar Padrão"),
                        width=30, text="Cadastrar", command=Rodar_programa).place(x=30, y=220)
#criando Banco ao abrir
criartabela()
# campos da Tab de Consulta
lblNPC = customtkinter.CTkLabel(tabview.tab(
    "Consultar"), width=10, height=10, text="Certificado Número:")
lblNPC.place(x=10, y=15)
txtNPC = customtkinter.CTkEntry(tabview.tab(
    "Consultar"), placeholder_text="Digite o N° de certificado do padrão", width=220)
txtNPC.place(x=125, y=10)
# Botões da Tab de Consulta
# Botão consultar
customtkinter.CTkButton(tabview.tab("Consultar"), width=30,
                        text="Consultar", command=consulta).place(x=350, y=10)
# Botão Deletar
customtkinter.CTkButton(tabview.tab("Consultar"), width=50, text="Deletar Padrão",
                        fg_color="#FF0000", hover_color="#800000", command= Deletar_Padrão).place(x=425, y=10)
customtkinter.CTkButton(tabview.tab("Consultar"), width=50, text="Exibir Todos", command=popular).place(x=390, y=43)
#Barra de Rolagem
scroll = ttk.Scrollbar(tabview.tab("Consultar"))
scroll.place(x=648,y=90, height=225)
# treeview da consulta na tab consulta
tree = ttk.Treeview(tabview.tab("Consultar"), yscrollcommand=scroll.set)
tree.place(x=10, y=90, relwidth=0.95)
tree['columns'] = ('coluna1', 'coluna2', 'coluna3',
                   'coluna4', 'coluna5', 'coluna6', 'coluna7')
tree.heading('#0', text='')
tree.heading('coluna1', text='TAG')
tree.heading('coluna2', text='Órgão')
tree.heading('coluna3', text='N° Certificado')
tree.heading('coluna4', text='Descrição')
tree.heading('coluna5', text='Data Calibração')
tree.heading('coluna6', text='Data Validade')
tree.heading('coluna7', text='Estatus')
#definindo tamanho das colunas
tree.column('#0', width=0)
tree.column('coluna1', width=45)
tree.column('coluna2', width=60)
tree.column('coluna3', width=120)
tree.column('coluna4', width=110)
tree.column('coluna5', width=80)
tree.column('coluna6', width=70)
tree.column('coluna7', width=70)
Atualizar()
popular()
Criartabela_Cad_Email()
#Tab de Configurações
lbltitulo = customtkinter.CTkLabel(tabview.tab(
    "Configurações"), width=10, height=10, text="Configurar Alerta", font=("Arial bold", 20))
lbltitulo.pack()
lblTemail = customtkinter.CTkLabel(tabview.tab(
    "Configurações"), text="Informe um Email para receber o aviso de vencimento.").place(x=70, y=25)
lblEmail = customtkinter.CTkLabel(tabview.tab(
    "Configurações"), text="Email:").place(x=70, y=55)
txtEmail = customtkinter.CTkEntry(tabview.tab(
    "Configurações"), placeholder_text="       Informe o Email a ser Notificado", width=250,)
txtEmail.place(x=110, y=55)
lblTDtEmail = customtkinter.CTkLabel(tabview.tab(
    "Configurações"), text="Digite os dias:").place(x=70, y=115)
lblDtEmail = customtkinter.CTkLabel(tabview.tab(
    "Configurações"), text="Com quantos dias de antecedência gostaria de ser notificado?").place(x=70, y=85)
txtDtEmail = customtkinter.CTkEntry(tabview.tab(
    "Configurações"), placeholder_text="Dias", width=50)
txtDtEmail.place(x=150, y=115)
#Botão de Aplicar Configurações
customtkinter.CTkButton(tabview.tab("Configurações"), width=70, text="Aplicar", command=Notificar).place(x=345, y=160)

janela.mainloop()
