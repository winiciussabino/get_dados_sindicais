import requests
import pandas as pd
import os
from itertools import chain
from datetime import datetime


def get_dados(resposta):

    texto = resposta.text 
    df = pd.read_html(texto)
    
    if len(df) == 22:
        #----------------------------------------
        # Criando lista a partir dos data frames
        #----------------------------------------
        lista = []
        for d in df:
            lista.append(d.values.tolist())

        #----------------------------------------
        # Desaninhando listas 
        #----------------------------------------
        ll = list(chain(*lista[2:15]))

        ll2 = list(chain(*ll))

        #---------------------------------
        # Tratando situacoes especiais 
        # situacao, razao_social,
        # data inicio mandato e data termino
        # mandato
        #---------------------------------
        ll2[0] = 'situacao: ' + ' ' + ll2[0]
        ll2[5] = ll2[4] + '  ' + ll2[5]
        t_lista = len(ll2)
        ll2[t_lista-3] = ll2[t_lista-4] + '  ' + ll2[t_lista-3]
        ll2[t_lista-1] = ll2[t_lista-2] + '  ' + ll2[t_lista-1]
        ll2.remove('Razão Social:')
        ll2.remove('Data início mandato:')
        ll2.remove('Data término mandato:')

        #------------------------------------------------------
        # Criando Data Frame a partir da lista 
        #------------------------------------------------------
        frame = pd.DataFrame({'coluna':ll2})
        frame.dropna(inplace=True)
        frame[['variaveis','descricoes']] = frame['coluna'].str.split(':', 1,expand=True)
        frame.drop(columns=['coluna'],inplace=True)

        #------------------------------------------------------
        # remove espaços em branco no inicio e fim da string
        #------------------------------------------------------
        frame['variaveis'] = frame['variaveis'].str.strip()
        frame['descricoes'] = frame['descricoes'].str.strip()

        #------------------------------------------------------
        # Transpõe Data Frame 
        #------------------------------------------------------
        frame = frame.set_index('variaveis') 

        frame_final = frame.T

        frame_final['data_leitura_mte'] = datetime.today().strftime('%d/%m/%Y') 

        frame_final.columns = list(frame_final.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower().str.replace(" ","_"))
        
        return frame_final
    else:
        print('Padrão diferente dos 22 data frames')
        df = pd.DataFrame({'situacao':['erro no formato de lista de 22 dataframes']}) 
        return df

    
    
def acessa(cnpj):

    url = 'http://www3.mte.gov.br/sistemas/CNES/usogeral/HistoricoEntidadeDetalhes.asp'
    parametros = {'NRCNPJ':cnpj} 
    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

    try:
        res = requests.get(url, verify=False, headers = headers, params = parametros) 
        status = res.status_code
        if status == 200:
            return res
        else:
            print('erro ao acessar CNPJ')
            return 'erro'
    except: 
        pass 
    

#---------------------------------------------------
# INICIO
#---------------------------------------------------

sindicatos = pd.read_excel('sindicatos_cnpj.xlsx')

sindicatos['cnpj_numeros'] = sindicatos['cnpj'].replace('[^0-9]','', regex=True)

lista_df_sindicatos = []

for index,row in sindicatos.iterrows():

    print('Buscando CNPJ: ', row['cnpj_numeros'])

    resposta = acessa(row['cnpj_numeros'])

    if resposta == 'erro':
        df = pd.DataFrame({'situacao':['não encontrado/inválido']})
        print('erro')
    else:
        print('Extraindo dados...')
        df = get_dados(resposta)
        print('Extração Concluída')
        print(df)

    lista_df_sindicatos.append(df)

    print('---------------------------------------------------------------')


df_sindicatos = pd.concat(lista_df_sindicatos)

print(df_sindicatos)

df_sindicatos = df_sindicatos.reset_index()

df_sindicatos['nome_sindicato_controle'] = sindicatos['nome']

df_sindicatos['cnpj_sindicato_controle'] = sindicatos['cnpj']

df_sindicatos.to_excel('lista_sindicatos.xlsx',index=False)


