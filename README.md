# Base de caminhos
Script para gerar uma Base de Caminhos utilizando CDR 

# Processamento e Anonimização de Dados de Conexão

Este projeto visa processar dados de conexão de uma planilha Excel, calcular a duração da conexão entre diferentes sites e anonimizar os números de telefone (`msisdn`) usando a função de hash SHA-256.

## Requisitos

- Python 3.x
- Pandas
- Openpyxl

## Instalação

1. Instale o Python 3.x se ainda não estiver instalado.
2. Instale as bibliotecas necessárias usando `pip`:

```sh
pip install pandas openpyxl


Uso
Salve o código abaixo em um arquivo Python, por exemplo, process_data_anonimized.py.
Certifique-se de que o arquivo Excel (base.xlsx) está localizado no caminho especificado (/tmp/base.xlsx).
Execute o script:

python process_data_anonimized.py



import pandas as pd
import hashlib

# Função para anonimizar o campo msisdn
def anonymize_msisdn(msisdn):
    return hashlib.sha256(msisdn.encode()).hexdigest()

# Função para carregar os dados e processar conforme solicitado
def process_data(file_path, output_file_path):
    # Carregar os dados da planilha 'amostra202406'
    data = pd.read_excel(file_path, sheet_name='amostra202406')

    # Anonimizar o campo msisdn
    data['msisdn'] = data['msisdn'].astype(str).apply(anonymize_msisdn)

    # Converter 'dt_start_time (ano mes dia  hora minuto segundo)' para datetime
    data['dt_start_time'] = pd.to_datetime(data['dt_start_time (ano mes dia  hora minuto segundo)'], format='%Y%m%d%H%M%S', errors='coerce')

    # Ordenar os dados por 'dt_start_time'
    data = data.sort_values(by='dt_start_time')

    # Calcular a diferença de tempo entre a linha atual e a linha posterior
    data['next_dt_start_time'] = data['dt_start_time'].shift(-1)
    data['time_diff'] = data['next_dt_start_time'] - data['dt_start_time']

    # Filtrar para manter apenas resultados com diferença de tempo superior a 5 minutos
    filtered_data = data[data['time_diff'] > pd.Timedelta(minutes=5)]

    # Criar base de caminhos com origem e destino
    filtered_data['next_ds_site'] = filtered_data['ds_site'].shift(-1)

    # Remover linhas onde 'ds_site' é igual ao 'next_ds_site' (mantendo apenas trocas de site)
    filtered_data = filtered_data[filtered_data['ds_site'] != filtered_data['next_ds_site']]

    # Exibir o resultado com todos os campos
    final_data_result = filtered_data[['msisdn', 'mbou', 'dt_dia', 'cgi', 'hora_start', 
                                       'dt_start_time', 'next_dt_start_time', 'time_diff', 
                                       'ds_site', 'next_ds_site', 'nome_site', 'long', 'lat']]
    final_data_result.reset_index(drop=True, inplace=True)

    # Salvar o resultado em um novo arquivo Excel
    final_data_result.to_excel(output_file_path, index=False)
    print(f"Resultado salvo em: {output_file_path}")

# Caminho do arquivo de entrada
input_file_path = '/tmp/base.xlsx'

# Caminho do arquivo de saída
output_file_path = '/tmp/basedecaminhos.xlsx'

# Processar os dados e salvar o resultado
process_data(input_file_path, output_file_path)



Explicação do Código
Função de Anonimização:

A função anonymize_msisdn(msisdn) utiliza SHA-256 para gerar um hash do valor msisdn, garantindo anonimização consistente.
Carregar os Dados:

O arquivo Excel é carregado utilizando pandas, especificando a planilha amostra202406.
Anonimizar msisdn:

Aplica a função de anonimização ao campo msisdn da planilha amostra202406.
Converter a Coluna de Tempo:

Converte a coluna dt_start_time (ano mes dia hora minuto segundo) para o tipo datetime.
Ordenar os Dados por dt_start_time:

Ordena os dados pela coluna dt_start_time para garantir que as operações de diferença de tempo sejam precisas.
Calcular a Diferença de Tempo Entre Linhas:

Calcula a diferença de tempo entre a linha atual e a linha posterior e armazena o resultado na coluna time_diff.

Filtrar Resultados com Diferença de Tempo Superior a 5 Minutos:

Filtra o DataFrame para manter apenas as linhas onde time_diff é superior a 5 minutos.

Criar Base de Caminhos com Origem e Destino:

Cria uma nova coluna next_ds_site que contém o valor de ds_site da próxima linha.
Remove as linhas onde ds_site é igual ao next_ds_site, mantendo apenas as trocas de site.
Selecionar e Reorganizar as Colunas:

Seleciona as colunas necessárias e reorganiza o DataFrame.
Salvar o Resultado em um Novo Arquivo Excel:

Salva o DataFrame resultante em um novo arquivo Excel especificado por output_file_path.

# Contribuição
Sinta-se à vontade para contribuir com este projeto através de pull requests. Qualquer sugestão ou melhoria é bem-vinda!


Este arquivo `README.md` fornece uma visão geral completa do código, incluindo requisitos, instruções de instalação, uso e uma explicação detalhada do que o código faz. Salve o conteúdo acima em um arquivo chamado `README.md` no mesmo diretório do seu script Python.
