import tkinter as tk
from tkinter import EW, NS, NSEW, VERTICAL, W, ttk
import re
import mysql.connector
from numpy import record

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        
        self.title("App Base de Dados")

        self.varResultado= tk.StringVar(self)
        self.lblResultado= ttk.Label(
            self, textvariable= self.varResultado,
            font=("Arial", 18),
            background="#DDDDDD"
        )
        self.lblResultado.grid(row=0, column=0, columnspan=3, padx=20, pady=10, sticky=NSEW)

        # Nome
        self.lblNome= ttk.Label(
            self, text="Nome",
            font=("Arial", 18, "bold")
        )
        self.lblNome.grid(row=1, column=0, sticky=W, padx=20, pady=5)

        self.varNome= tk.StringVar(self)
        self.txtNome = ttk.Entry(
            self, textvariable=self.varNome,
            font=("Arial", 18)
        )
        self.txtNome.grid(row=1, column=1, sticky=EW, padx=20, pady=5)
        self.txtNome.focus()

        # E-mail
        self.lblEmail= ttk.Label(
            self, text="E-mail",
            font=("Arial", 18, "bold")
        )
        self.lblEmail.grid(row=2, column=0, sticky=W, padx=20, pady=5)

        self.varEmail= tk.StringVar(self)
        self.txtEmail= ttk.Entry(
            self, textvariable=self.varEmail,
            font=("Arial", 18)
        )
        self.txtEmail.grid(row=2, column=1, sticky=EW, padx=20, pady=5)
        
        #Lista de Resultados
        self.frameLista= ttk.Frame(self)
        self.frameLista.grid(row=3, column=0, columnspan=2, rowspan=4, sticky=NSEW, padx=20, pady=10)

        self.txtLista= ttk.Treeview(
            self.frameLista, columns=('nome', 'email'),
            show="headings", height=7
        )
        self.txtLista.heading('nome', text="Nome")
        self.txtLista.heading('email', text="Email")

        def item_selected(event):
            for selected_item in self.txtLista.selection():
                item= self.txtLista.item(selected_item)
                record= item['values']
                self.varNome.set(record[0])
                self.varEmail.set(record[1])

        self.txtLista.bind('<<TreeviewSelect>>', item_selected)

        self.txtLista.grid(row=0, column=0, sticky=NSEW)

        scrollbar= ttk.Scrollbar(
            self.frameLista, orient=VERTICAL,
            command=self.txtLista.yview)
        self.txtLista.configure(yscroll= scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=NS)

        # Botôes
        self.btnConectar = ttk.Button(
            self, text="Conectar",
            command=self.btnConectar_Click
        )
        self.btnConectar.grid(row=1, column=2, sticky=NSEW, padx=20, ipadx=20, pady=5)

        self.btnCriarTabela= ttk.Button(
            self, text="Criar Tabela",
            command=self.btnCriarTabela_Click
        )
        self.btnCriarTabela.grid(row=2, column=2, sticky=NSEW, padx=20, ipadx=20, pady=5)

        self.btnInserir= ttk.Button(
            self, text="Inserir",
            command=self.btnInserir_click
        )
        self.btnInserir.grid(row=3, column=2, sticky=NSEW, padx=20, ipadx=20, pady=5)

        self.btnProcurar= ttk.Button(
            self, text="Procurar"
        )
        self.btnProcurar.grid(row=4, column=2, sticky=NSEW, padx=20, ipadx=20, pady=5)

        self.btnExcluir=ttk.Button(
            self, text="Excluir"
        )
        self.btnExcluir.grid(row=5, column=2, sticky=NSEW, padx=20, ipadx=20, pady=5)

        self.btnEditar=ttk.Button(
            self, text="Editar"
        )
        self.btnEditar.grid(row=6, column=2, sticky=NSEW, padx=20, ipadx=20, pady=5)

    def btnConectar_Click(self):
        try:
            conexao= mysql.connector.connect(
                host= "localhost",
                user= "root",
                password=""
            )
            mycursor= conexao.cursor()
            sql= "CREATE DATABASE IF NOT EXISTS curso_db"
            mycursor.execute(sql)
            self.varResultado.set("Base de dados conectada com sucesso!")
            self.lblResultado.configure(background="#99ff99")
            
        except:
            self.varResultado.set("Erro ao conectar com a base de dados!")
            self.lblResultado.configure(background="#FF9999")

    def btnCriarTabela_Click(self):
        try:
            conexao= mysql.connector.connect(
                host= "localhost",
                user= "root",
                password="",
                database="curso_db"
            )
            mycursor= conexao.cursor()
            sql= """
                CREATE TABLE IF NOT EXISTS pessoas (
                    nome VARCHAR(50),
                    email VARCHAR (50),
                    PRIMARY KEY(email))
            """
            mycursor.execute(sql)
            self.varResultado.set("Tabela criada com sucesso!")
            self.lblResultado.configure(background="#99ff99")
        except:
            self.varResultado.set("Erro ao criar a tabela!")
            self.lblResultado.configure(background="#ff9999")

    def btnInserir_click(self):
        nome = self.varNome.get().strip()
        email= self.varEmail.get().strip()

        reNome = re.fullmatch(r"\b[A-Za-z ]+\b", nome)
        reEmail= re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",email)

        if reNome is None:
            self.varResultado.set("O campo nome é obrigatório!")
            self.lblResultado.configure(background="#ff9999")
            self.txtNome.focus()

        elif reEmail is None:
            self.varResultado.set("Insira um email válido!")
            self.lblResultado.configure(background="#ff9999")
            self.txtEmail.focus()
        else:
            try:
                conexao= mysql.connector.connect(
                    host= "localhost",
                    user= "root",
                    password="",
                    database="curso_db"
                )
                mycursor= conexao.cursor()
                sql= "INSERT INTO pessoas (nome, email) VALUES (%s, %s)"
                val=(nome, email)
                mycursor.execute(sql, val)
                conexao.commit()

                self.varResultado.set(str(mycursor.rowcount)+"Registro(s) inserido(s)")
                self.lblResultado.configure(background="#99FF99")
                self.varNome.set("")
                self.varEmail.set("")
                self.txtNome.focus()
            except:
                self.varResultado.set("Erro ao Inserir novo registro!")
                self.lblResultado.configure(background="#FF9999")

if __name__ == "__main__":
    app= App()
    app.mainloop()