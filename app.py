# Importa o Flask para criar a aplicação web, request para manipular requisições HTTP
# e render_template para renderizar arquivos HTML.
from flask import Flask, request, render_template

# Importa o pandas, uma biblioteca para manipulação e análise de dados, comumente usada para trabalhar com arquivos CSV.
import pandas as pd

# Cria uma instância da aplicação Flask.
app = Flask(__name__)

# Define uma rota para o endpoint raiz ('/') que será acionada quando o usuário acessar o site.
@app.route('/')
def index():
    # Renderiza o arquivo HTML 'index.html' como resposta para a requisição na rota raiz.
    return render_template('index.html')

# Define uma rota para o endpoint '/display', configurando-o para aceitar apenas requisições POST.
@app.route('/display', methods=['POST'])
def display_file():
    # Obtém o arquivo enviado na requisição através do campo 'file'.
    file = request.files['file']    
    # Verifica se nenhum arquivo foi enviado e retorna uma mensagem de erro.
    if not file:
        return "No file"
    # Tenta ler o arquivo CSV usando a codificação padrão do pandas e o delimitador ';'.
    try:
        df = pd.read_csv(file, delimiter=";")
    except UnicodeDecodeError:
        # Caso ocorra erro de codificação, o ponteiro do arquivo é resetado para o início.
        file.seek(0)  
        try:
            # Tenta ler o arquivo novamente, agora usando a codificação 'latin1'.
            df = pd.read_csv(file, encoding='latin1', delimiter=";")
        except UnicodeDecodeError:
            # Se ocorrer outro erro de codificação, o ponteiro do arquivo é resetado novamente.
            file.seek(0)
            # Tenta ler o arquivo usando a codificação 'ISO-8859-1'.
            df = pd.read_csv(file, encoding='ISO-8859-1', delimiter=";")
    
    # Renderiza o template 'display.html', passando o dataframe como uma tabela HTML.
    # O argumento 'tables' contém os dados do CSV convertidos em HTML.
    # O argumento 'titles' passa os nomes das colunas do dataframe como títulos da tabela.
    return render_template('display.html', tables=[df.to_html(classes='data')])
