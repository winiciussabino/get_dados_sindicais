## get_dados_sindicais
Função utilizada para extrair, a partir do CNPJ de um sindicato, dados da carta sindical obtidos no portal do MTE - Ministério do Trabalho.
http://www3.mte.gov.br/sistemas/cnes/internet/reg_sindical_default.asp#
![image](https://user-images.githubusercontent.com/78553616/182382566-334a9396-ca76-4e0d-a231-a8f96dbea16e.png)

## Requisitos

python 3.9 ou superior

Bibliotecas de python necessárias:
* pandas
* requests



## Instalação

Instalar as bibliotecas:
```
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## Execução
A partir de um arquivo de excel chamado <b>sindicatos_cnpj.xlsx</b> com duas colunas no seguinte formato:

<table>
  <tr>
    <td align="center">
          <b>nome</b>
    </td>
    <td align="center">
          <b>cnpj</b>
    </td>
  </tr>
   <tr>
    <td align="center">
          Sindicato das Indústrias da Alimentação de Cáceres
    </td>
    <td align="center">
          24.753.535/0001-00
    </td>
  </tr>
    <tr>
    <td align="center"> ... </td>
    <td align="center"> ... </td>
  </tr>
</table>

Executa-se o código com:

```
python get_dados_sindicais.py
```

Como saída é gerada uma tabela com o nome <b>lista_sindicatos.xlsx</b> contendo os dados da carta sindical.

## Contribuidores<br>

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/winiciussabino">
        <img src="https://avatars1.githubusercontent.com/u/78553616" width="100px;" alt="Foto do Winicius Sabino"/><br>
        <sub>
          <b>Winicius Sabino</b>
        </sub>
      </a>
    </td>
  </tr>
</table>



## ⚖ Licença



## ℹ️ Informações do projeto
