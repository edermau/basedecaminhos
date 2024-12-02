import pandas as pd
import hashlib

# Função para anonimizar o campo msisdn
def anonymize_msisdn(msisdn):
    return hashlib.sha256(msisdn.encode()).hexdigest()

# Função para carregar os dados e processar conforme solicitado
def process_data(file_path, output_file_path):
    # Carregar os dados da planilha 'Planilha1'  
    data = pd.read_excel(file_path, sheet_name='Planilha1')

    # Anonimizar o campo msisdn
    data['msisdn'] = data['msisdn'].astype(str).apply(anonymize_msisdn)

    # Converter 'dt_start_time (ano mes dia  hora minuto segundo)' para datetime
    data['dt_start_time'] = pd.to_datetime(data['dt_start_time (ano mes dia  hora minuto segundo)'], format='%Y%m%d%H%M%S', errors='coerce')

    # Ordenar os dados por 'dt_start_time'
    data = data.sort_values(by='dt_start_time')

    # Calcular a diferença de tempo entre a linha atual e a linha posterior
    data['next_dt_start_time'] = data['dt_start_time'].shift(-1)
    data['time_diff'] = data['next_dt_start_time'] - data['dt_start_time']

    # Filtrar para manter apenas resultados com diferença de tempo superior a x minutos se aplicavel
    filtered_data = data[data['time_diff'] > pd.Timedelta(minutes=-1)]

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
input_file_path = '/tmp/amostras2024Mesv3.xlsx'

# Caminho do arquivo de saída
output_file_path = '/tmp/base_de_caminhos9.xlsx'

# Processar os dados e salvar o resultado
process_data(input_file_path, output_file_path)

