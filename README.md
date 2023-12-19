# **Bot Emissão Nota Fiscal de Serviço NFS**

Este projeto automatiza a extração e conversão de dados de um sistema de gerenciamento de hospitalidade. Ele é composto por dois componentes principais:

1. Módulo Hospedin (`app/hospedin/init.py`):

    - Usa o Selenium para automatizar interações com o sistema de gerenciamento de hospitalidade.

    - Faz login no sistema, navega nos relatórios desejados, aplica filtros e faz o download de dados.

    - Salva dados em pastas especificadas.

    - Observação: Este módulo requer o ChromeDriver, que deve estar instalado localmente, e o Chrome instalado. O projeto é projetado para ser executado em modo headless.


2. Módulo de Conversão (`app/conversion/init.py`):

    - Converte dados baixados em um formato estruturado.

    - Mescla dados de diferentes fontes e cria uma saída final.


## **Dependências**

Para configurar o projeto, execute:

```bash
make setup
```

Isso instalará as dependências necessárias do arquivo requirements.txt.


## **Uso**

### **Baixar Dados**
Para baixar dados, use o seguinte comando:

```bash
python app/__main__.py --download --user <seu_nome_de_usuário> --password <sua_senha>
```

ou

```bash
make hospedin
```

Substitua <seu_nome_de_usuário> e <sua_senha> por suas credenciais reais.

### **Converter Dados**

Para converter os dados baixados, use:

```bash
python app/__main__.py --convert
```

ou

```bash
make convert
```

Isso converterá os dados baixados em arquivos CSV estruturados.


## **Estrutura do Projeto**
- `app/main.py`: Script principal para controlar o fluxo do projeto.
- `app/hospedin/init.py`: Módulo para automatizar interações com o sistema de gerenciamento de hospitalidade.
- `app/conversion/init.py`: Módulo para converter e mesclar dados.

## **Estrutura de Pastas**

- `downloads`: Dados brutos baixados.
    - `bronze`: Dados baixados inicialmente.
    - `silver`: Dados convertidos.
    - `gold`: Dados mesclados e finais.
