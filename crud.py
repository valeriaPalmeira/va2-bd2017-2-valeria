#coding: utf-8

from appJar import gui
import MySQLdb

def press(btn):

  global conexao
  global cursor

  
  host = app.getEntry("Host")
  usuario = app.getEntry("Usuario")
  senha = app.getEntry("Senha")
  conexao = MySQLdb.connect(host, usuario, senha,"va1base")
  cursor = conexao.cursor()

  app.stop()

  #print("Host:", host, "Usuario:", usuario, "Senha:", senha)

app = gui("Login", "400x200")
app.setBg("white")
app.setFont(12)

app.addLabel("title", "LOGIN")
app.setLabelFg("title", "black")
app.setLabelBg("title", "gray")

app.addLabelEntry("Host")
app.addLabelEntry("Usuario")
app.addLabelSecretEntry("Senha")

app.addButton("Entrar", press)


#conexao = MySQLdb.connect(host, usuario, senha,"va1base")
#cursor = conexao.cursor()

app.go()

app = gui("CRUD de MySQL", "600x400")

def pesquisar(btn):
  termo = app.getEntry("txtBusca")

  if termo == "" :
    app.errorBox("Erro", 'Informe um termo para pesquisar!')
  else:
    cursor.execute(
      "SELECT Cidade.nomeCidade, Estado.nomeEstado FROM Cidade INNER JOIN Estado ON Estado.idEstado = Cidade.EstadoCidade WHERE nomeCidade LIKE '%" + termo + "%'"
    )

    rs = cursor.fetchall()

    app.clearListBox("lBusca")

    for x in rs:
      app.addListItem("lBusca", x[0] + ' - ' + x[1])

def exibir(btn):
  cursor.execute(
    "SELECT Cidade.nomeCidade, Estado.nomeEstado, Pais.nomePais FROM Cidade INNER JOIN Estado ON Cidade.EstadoCidade = Estado.idEstado INNER JOIN Pais ON Estado.PaisEstado = idPais ORDER BY nomeCidade "
  )

  rs = cursor.fetchall()

  app.clearListBox("lBusca")

  for x in rs:
    app.addListItem("lBusca", x[0] + ' - ' + x[1] + ' - ' + x[2])

def inserir(btn):
  app.showSubWindow('janela_inserir')

def salvar_estado(btn):
  cidade = app.getEntry('txtcidade')
  idestado = app.getEntry('txtestado')
  cursor.execute("INSERT INTO Cidade (nomeCidade, EstadoCidade) VALUES('{}',{})".format(cidade,idestado))
  #cursor.execute("INSERT INTO Cidade (NomeCidade, Estado_idEstado) VALUES('%s',%s)" % (cidade,idestado))
  conexao.commit()

  app.clearListBox("lBusca")
  app.addListItem("lBusca", "A cidade " + cidade + " foi inserida com sucesso!")

  app.hideSubWindow('janela_inserir')

def deletar(btn):
  app.showSubWindow("delete_cidade")

def deletar_estado(btn):
  nome_cidade_delete = app.getEntry("cidade2")

  cursor.execute(
    "SELECT idCidade, nomeCidade FROM Cidade WHERE nomeCidade LIKE '%" + nome_cidade_delete + "%'"
  )

  rs = None
  rs = cursor.fetchone()

  app.clearListBox("lBusca")

  app.addListItem("lBusca", "A cidade " + rs[1] + " foi deletada!")

  cursor.execute(
    "DELETE FROM Cidade WHERE idCidade = %s" % (rs[0])
  )

  conexao.commit()

  app.hideSubWindow("delete_cidade")

def atualizar(btn):
  app.showSubWindow("atualizar_cidade")

def atualizar_estado(btn):
  nome_antigo = app.getEntry("nome_antigo")
  nome_novo = app.getEntry("nome_novo")
  id_novo = app.getEntry("id_novo")

  cursor.execute(
    "SELECT idCidade, nomeCidade FROM Cidade WHERE nomeCidade LIKE '%" + nome_antigo + "%'"
  )

  rs = cursor.fetchone()

  app.clearListBox("lBusca")

  app.addListItem("lBusca", "A cidade " + rs[1] + " foi atualizada para " + nome_novo + " com o ID " + id_novo + " !")

  cursor.execute(
    "UPDATE Cidade "+
    "SET idEstado = " + id_novo + ", nomeEstado = '" + nome_novo + "'"
    "WHERE idEstado = " + str(rs[0])
  )

  conexao.commit()

  app.hideSubWindow("atualizar_cidade")

#Janela Inserir ----------------
app.startSubWindow("janela_inserir", modal=True)
app.addLabel("l1", "Inserindo dados...")
app.addEntry('txtestado')
app.addEntry('txtcidade')
app.addButton('Salvar cidade',salvar_estado)
app.setEntryDefault("txtestado", "ID do Estado")
app.setEntryDefault("txtcidade", "Nome da cidade")
app.stopSubWindow()

# Janela Deletar ---------------
app.startSubWindow("delete_cidade", modal=True)

app.addLabel("lDelete", "Deletar cidade: ")

app.addEntry("cidade2")
app.addButton("Deletar Cidade", deletar_estado)
app.setEntryDefault("cidade2", "Nome Cidade")

app.stopSubWindow()

#Janela Atualizar ---------------
app.startSubWindow("atualizar_cidade", modal=True)

app.addLabel("lUpdate", "Atualizar cidade: ")

app.addEntry("nome_antigo")
app.addEntry("nome_novo")
app.addEntry("id_novo")

app.addButton("Atualizar Cidade", atualizar_estado)

app.setEntryDefault("nome_antigo", "Nome Antigo")
app.setEntryDefault("nome_novo", "Nome Novo")
app.setEntryDefault("id_novo", "Novo ID")

app.stopSubWindow()

# Menu principal ----------------
app.addLabel("lNome", '', 0, 0, 2)

app.addButton("Exibir dados", exibir, 1, 0)
app.addButton("Inserir dados", inserir, 1, 1)
app.addButton("Atualizar dados", atualizar, 2, 0)
app.addButton("Excluir dados", deletar, 2, 1)

app.addEntry("txtBusca", 3, 0, 2)
app.setEntryDefault("txtBusca", "Digite o termo...")

app.addButton("Pesquisar", pesquisar, 4, 0, 2)

app.addListBox("lBusca", [], 5, 0, 2)
app.setListBoxRows("lBusca", 5)

app.go()