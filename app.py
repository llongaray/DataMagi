from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import requests
import pandas as pd
import os
from rich import print
from rich.progress import track
import time
import logging

# Configuração do logger
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExcelFilter:
    def __init__(self):
        self.df = None
        self.filepath = None
        self.headers = None
        
    def load_excel(self, filepath):
        """Carrega o arquivo Excel e extrai os cabeçalhos"""
        try:
            self.filepath = filepath
            self.df = pd.read_excel(filepath)
            self.headers = list(self.df.columns)
            return True
        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")
            return False

    def get_unique_values(self, column):
        """Retorna valores únicos de uma coluna específica"""
        return self.df[column].unique().tolist()

    def filter_and_save(self, column, value, output_path):
        """Filtra o DataFrame e salva em novo arquivo"""
        filtered_df = self.df[self.df[column] == value]
        output_file = os.path.join(output_path, f'filtered_{os.path.basename(self.filepath)}')
        filtered_df.to_excel(output_file, index=False)
        return output_file

    def filter_and_save_multiple(self, filters, output_path):
        """Filtra o DataFrame com múltiplos critérios e salva em novo arquivo"""
        print("\n[bold yellow]╔══ Iniciando Filtragem Múltipla ══╗[/bold yellow]\n")
        
        filtered_df = self.df.copy()
        total_inicial = len(filtered_df)
        
        steps = len(filters)
        step_size = 100 // steps
        
        for column, value in filters.items():
            for _ in track(range(step_size), description=f"[cyan]Aplicando filtro para {column}...[/cyan]"):
                time.sleep(0.01)
            filtered_df = filtered_df[filtered_df[column] == value]
        
        output_file = os.path.join(output_path, f'filtered_{os.path.basename(self.filepath)}')
        filtered_df.to_excel(output_file, index=False)
        
        print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
        print(f"[white]► Registros originais:[/white]    {total_inicial:,}")
        print(f"[white]► Registros após filtros:[/white] {len(filtered_df):,}")
        print(f"[white]► Registros filtrados:[/white]    {total_inicial - len(filtered_df):,}")
        print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[/dim]\n")
        
        return output_file

    def get_unique_values_filtered(self, column, current_filters):
        """Retorna valores únicos de uma coluna com filtros aplicados"""
        filtered_df = self.df.copy()
        for col, val in current_filters.items():
            filtered_df = filtered_df[filtered_df[col] == val]
        return filtered_df[column].unique().tolist()

    def keep_columns(self, columns, output_path):
        """Mantém apenas as colunas selecionadas"""
        print("\n[bold yellow]╔══ Iniciando Seleção de Colunas ══╗[/bold yellow]\n")
        
        total_colunas = len(self.df.columns)
        
        for _ in track(range(100), description="[cyan]Processando colunas...[/cyan]"):
            time.sleep(0.01)
        
        filtered_df = self.df[columns].copy()
        output_file = os.path.join(output_path, f'kept_columns_{os.path.basename(self.filepath)}')
        filtered_df.to_excel(output_file, index=False)
        
        print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
        print(f"[white]► Total de colunas original:[/white] {total_colunas:,}")
        print(f"[white]► Colunas mantidas:[/white]        {len(columns):,}")
        print(f"[white]► Colunas removidas:[/white]       {total_colunas - len(columns):,}")
        print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[/dim]\n")
        
        return output_file

    def remove_columns(self, columns, output_path):
        """Remove as colunas selecionadas"""
        print("\n[bold yellow]╔══ Iniciando Remoção de Colunas ══╗[/bold yellow]\n")
        
        total_colunas = len(self.df.columns)
        
        for _ in track(range(100), description="[cyan]Processando colunas...[/cyan]"):
            time.sleep(0.01)
        
        filtered_df = self.df.drop(columns=columns).copy()
        output_file = os.path.join(output_path, f'removed_columns_{os.path.basename(self.filepath)}')
        filtered_df.to_excel(output_file, index=False)
        
        print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
        print(f"[white]► Total de colunas original:[/white] {total_colunas:,}")
        print(f"[white]► Colunas removidas:[/white]        {len(columns):,}")
        print(f"[white]► Colunas restantes:[/white]        {len(filtered_df.columns):,}")
        print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[/dim]\n")
        
        return output_file

    def filter_numeric_greater_than(self, column, value, output_path):
        """Filtra valores numéricos maiores que o valor especificado"""
        filtered_df = self.df[self.df[column] > value]
        output_file = os.path.join(output_path, f'numeric_filtered_{os.path.basename(self.filepath)}')
        filtered_df.to_excel(output_file, index=False)
        return output_file

    def filter_numeric_between(self, column, min_value, max_value, output_path):
        """Filtra valores numéricos entre dois valores"""
        filtered_df = self.df[(self.df[column] >= min_value) & (self.df[column] <= max_value)]
        output_file = os.path.join(output_path, f'numeric_filtered_{os.path.basename(self.filepath)}')
        filtered_df.to_excel(output_file, index=False)
        return output_file

    def is_numeric_column(self, column):
        """Verifica se uma coluna é numérica"""
        return pd.api.types.is_numeric_dtype(self.df[column])

    @staticmethod
    def unify_excel_files(directory_path, output_path):
        """Unifica arquivos Excel baseado no CPF"""
        all_files = [f for f in os.listdir(directory_path) if f.endswith(('.xlsx', '.xls'))]
        if not all_files:
            print("Nenhum arquivo Excel encontrado no diretório.")
            return None

        dfs = []
        for file in all_files:
            df = pd.read_excel(os.path.join(directory_path, file))
            if 'CPF' not in df.columns:
                print(f"Arquivo {file} não contém a coluna 'CPF'. Ignorando...")
                continue
            dfs.append(df)

        if not dfs:
            print("Nenhum arquivo válido encontrado.")
            return None

        unified_df = pd.concat(dfs, ignore_index=True)
        unified_df = unified_df.drop_duplicates(subset=['CPF'], keep='first')
        
        output_file = os.path.join(output_path, 'unified_excel.xlsx')
        unified_df.to_excel(output_file, index=False)
        return output_file

    def normalize_cpf(self, cpf):
        """Normaliza o CPF removendo caracteres especiais e espaços"""
        # Converte para string primeiro
        cpf_str = str(cpf)
        return ''.join(filter(str.isdigit, cpf_str))

    def unify_excel_files_with_cpf(self, base_file_path, second_file_path, base_cpf_column, second_cpf_column, output_path):
        """Unifica dois arquivos Excel baseado no CPF"""
        print("\n[bold yellow]╔═�� Iniciando Unificação por CPF ══╗[/bold yellow]\n")
        
        base_df = pd.read_excel(base_file_path)
        second_df = pd.read_excel(second_file_path)
        total_base = len(base_df)
        total_second = len(second_df)

        # Normaliza os CPFs
        for _ in track(range(33), description="[cyan]Normalizando CPFs do arquivo base...[/cyan]"):
            time.sleep(0.01)
        base_df[base_cpf_column] = base_df[base_cpf_column].apply(self.normalize_cpf)
        
        for _ in track(range(33), description="[cyan]Normalizando CPFs do segundo arquivo...[/cyan]"):
            time.sleep(0.01)
        second_df[second_cpf_column] = second_df[second_cpf_column].apply(self.normalize_cpf)
        
        # Realiza o merge
        for _ in track(range(34), description="[cyan]Unificando arquivos...[/cyan]"):
            time.sleep(0.01)
        merged_df = pd.merge(base_df, second_df, left_on=base_cpf_column, right_on=second_cpf_column, how='inner')
        
        output_file = os.path.join(output_path, 'unified_by_cpf.xlsx')
        merged_df.to_excel(output_file, index=False)
        
        print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
        print(f"[white]► Registros no arquivo base:[/white]    {total_base:,}")
        print(f"[white]► Registros no segundo arquivo:[/white] {total_second:,}")
        print(f"[white]► Registros após unificação:[/white]    {len(merged_df):,}")
        print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[/dim]\n")
        
        return output_file

    def filter_cpf_removal(self, base_file_path, removal_file_path, base_cpf_column, removal_cpf_column, output_path):
        """Remove do arquivo base os CPFs que existem no arquivo de remoção"""
        print("\n[bold yellow]╔══ Iniciando Remoção de CPFs ══╗[/bold yellow]\n")
        
        base_df = pd.read_excel(base_file_path)
        removal_df = pd.read_excel(removal_file_path)
        total_base = len(base_df)
        
        # Normaliza os CPFs
        for _ in track(range(33), description="[cyan]Normalizando CPFs do arquivo base...[/cyan]"):
            time.sleep(0.01)
        base_df[base_cpf_column] = base_df[base_cpf_column].apply(self.normalize_cpf)
        
        for _ in track(range(33), description="[cyan]Normalizando CPFs do arquivo de remoção...[/cyan]"):
            time.sleep(0.01)
        removal_df[removal_cpf_column] = removal_df[removal_cpf_column].apply(self.normalize_cpf)
        
        # Remove as linhas
        for _ in track(range(34), description="[cyan]Removendo CPFs...[/cyan]"):
            time.sleep(0.01)
        filtered_df = base_df[~base_df[base_cpf_column].isin(removal_df[removal_cpf_column])].copy()
        
        # Formata os CPFs
        filtered_df[base_cpf_column] = filtered_df[base_cpf_column].apply(self.format_cpf)
        
        output_file = os.path.join(output_path, f'cpf_filtered_{os.path.basename(base_file_path)}')
        filtered_df.to_excel(output_file, index=False)
        
        print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
        print(f"[white]► Registros originais:[/white]    {total_base:,}")
        print(f"[white]► Registros após remoção:[/white] {len(filtered_df):,}")
        print(f"[white]► Registros removidos:[/white]    {total_base - len(filtered_df):,}")
        print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[/dim]\n")
        
        return output_file

    

    def filter_cpf_duplicates(self, file_path, cpf_column, output_path):
        """Remove CPFs duplicados mantendo apenas a primeira ocorrência"""
        print("\n[bold yellow]╔══ Iniciando Remoção de Duplicatas ══╗[/bold yellow]\n")
        
        df = pd.read_excel(file_path)
        total = len(df)
        
        # Normaliza os CPFs
        for _ in track(range(50), description="[cyan]Normalizando CPFs...[/cyan]"):
            time.sleep(0.01)
        df[cpf_column] = df[cpf_column].apply(self.normalize_cpf)
        
        # Remove duplicatas
        for _ in track(range(50), description="[cyan]Removendo duplicatas...[/cyan]"):
            time.sleep(0.01)
        filtered_df = df.drop_duplicates(subset=[cpf_column], keep='first').copy()
        
        # Formata os CPFs
        filtered_df[cpf_column] = filtered_df[cpf_column].apply(self.format_cpf)
        
        output_file = os.path.join(output_path, f'unique_cpf_{os.path.basename(file_path)}')
        filtered_df.to_excel(output_file, index=False)
        
        duplicatas = total - len(filtered_df)
        
        print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
        print(f"[white]► Registros originais:[/white]    {total:,}")
        print(f"[white]► Registros únicos:[/white]      {len(filtered_df):,}")
        print(f"[white]► Duplicatas removidas:[/white]  {duplicatas:,}")
        print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[/dim]\n")
        
        return output_file

    def format_cpf(self, cpf):
        """Formata o CPF para ter 11 dígitos, adicionando zeros à esquerda se necessário"""
        # Primeiro normaliza o CPF para ter apenas dígitos
        cpf_clean = self.normalize_cpf(cpf)
        # Adiciona zeros à esquerda se necessário para ter 11 dígitos
        return cpf_clean.zfill(11)

def filter_single_excel():
    filter_system = ExcelFilter()
    
    print("\n[bold yellow]╔══ Iniciando Filtro Único ══╗[/bold yellow]\n")
    
    excel_path = inquirer.text(
        message="Digite o caminho do arquivo Excel:"
    ).execute()
    
    if not filter_system.load_excel(excel_path):
        print("[bold red]✗ Erro ao carregar arquivo![/bold red]\n")
        return
    
    selected_header = inquirer.select(
        message="Selecione o cabeçalho para filtrar:",
        choices=filter_system.headers
    ).execute()
    
    unique_values = filter_system.get_unique_values(selected_header)
    
    selected_value = inquirer.select(
        message=f"Selecione o valor para filtrar em '{selected_header}':",
        choices=unique_values
    ).execute()
    
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo filtrado:"
    ).execute()
    
    total_registros = len(filter_system.df)
    
    for _ in track(range(100), description="[cyan]Aplicando filtro...[/cyan]"):
        time.sleep(0.01)
    
    filtered_df = filter_system.df[filter_system.df[selected_header] == selected_value].copy()
    output_file = filter_system.filter_and_save(selected_header, selected_value, output_dir)
    
    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Registros originais:[/white]    {total_registros:,}")
    print(f"[white]► Registros filtrados:[/white]    {len(filtered_df):,}")
    print(f"[white]► Registros removidos:[/white]    {total_registros - len(filtered_df):,}")
    print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
    print(f"[dim]📁 Arquivo salvo em: {output_file}[/dim]\n")

def filter_multiple_excel():
    filter_system = ExcelFilter()
    
    excel_path = inquirer.text(
        message="Digite o caminho do arquivo Excel:"
    ).execute()
    
    if not filter_system.load_excel(excel_path):
        return
    
    filters = {}
    while True:
        # Pergunta se quer adicionar mais um filtro
        should_continue = inquirer.confirm(
            message="Deseja adicionar um filtro?",
            default=True
        ).execute()
        
        if not should_continue:
            break
            
        # Seleciona o cabeçalho
        selected_header = inquirer.select(
            message="Selecione o cabeçalho para filtrar:",
            choices=filter_system.headers
        ).execute()
        
        # Obtém valores únicos considerando filtros anteriores
        unique_values = filter_system.get_unique_values_filtered(selected_header, filters)
        
        if not unique_values:
            print("Não há valores disponíveis com os filtros atuais.")
            break
            
        # Seleciona o valor
        selected_value = inquirer.select(
            message=f"Selecione o valor para filtrar em '{selected_header}':",
            choices=unique_values
        ).execute()
        
        filters[selected_header] = selected_value
    
    if filters:
        output_dir = inquirer.text(
            message="Digite o caminho para salvar o arquivo filtrado:"
        ).execute()
        
        output_file = filter_system.filter_and_save_multiple(filters, output_dir)
        print(f"\nArquivo filtrado salvo em: {output_file}")

def select_columns():
    """Função auxiliar para selecionar múltiplas colunas"""
    filter_system = ExcelFilter()
    
    excel_path = inquirer.text(
        message="Digite o caminho do arquivo Excel:"
    ).execute()
    
    if not filter_system.load_excel(excel_path):
        return None, None
    
    selected_columns = []
    while True:
        should_continue = inquirer.confirm(
            message="Deseja selecionar uma coluna?",
            default=True
        ).execute()
        
        if not should_continue:
            break
        
        remaining_columns = [col for col in filter_system.headers if col not in selected_columns]
        if not remaining_columns:
            print("Todas as colunas já foram selecionadas.")
            break
            
        selected_header = inquirer.select(
            message="Selecione a coluna:",
            choices=remaining_columns
        ).execute()
        
        selected_columns.append(selected_header)
        
    return filter_system, selected_columns

def keep_selected_columns():
    filter_system, selected_columns = select_columns()
    
    if not filter_system or not selected_columns:
        return
    
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo:"
    ).execute()
    
    output_file = filter_system.keep_columns(selected_columns, output_dir)
    print(f"\nArquivo salvo com as colunas selecionadas em: {output_file}")

def remove_selected_columns():
    filter_system, selected_columns = select_columns()
    
    if not filter_system or not selected_columns:
        return
    
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo:"
    ).execute()
    
    output_file = filter_system.remove_columns(selected_columns, output_dir)
    print(f"\nArquivo salvo sem as colunas selecionadas em: {output_file}")

def filter_numeric():
    """Função para filtrar valores numéricos"""
    filter_system = ExcelFilter()
    
    print("\n[bold yellow]╔══ Iniciando Filtro Numérico ══╗[/bold yellow]\n")
    
    excel_path = inquirer.text(
        message="Digite o caminho do arquivo Excel:"
    ).execute()
    
    if not filter_system.load_excel(excel_path):
        print("[bold red]✗ Erro ao carregar arquivo![/bold red]\n")
        return

    # Filtra apenas colunas numéricas
    numeric_columns = [col for col in filter_system.headers if filter_system.is_numeric_column(col)]
    if not numeric_columns:
        print("[bold red]✗ Não há colunas numéricas neste arquivo![/bold red]\n")
        return

    selected_header = inquirer.select(
        message="Selecione a coluna numérica para filtrar:",
        choices=numeric_columns
    ).execute()

    filter_type = inquirer.select(
        message="Selecione o tipo de filtro:",
        choices=[
            Choice("1", "Maior que"),
            Choice("2", "Entre valores")
        ]
    ).execute()

    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo filtrado:"
    ).execute()

    total_registros = len(filter_system.df)

    if filter_type == "1":
        value = float(inquirer.text(
            message="Digite o valor mínimo:"
        ).execute())
        
        for _ in track(range(100), description="[cyan]Aplicando filtro...[/cyan]"):
            time.sleep(0.01)
            
        filtered_df = filter_system.df[filter_system.df[selected_header] > value].copy()
        output_file = filter_system.filter_numeric_greater_than(selected_header, value, output_dir)
        
        print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
        print(f"[white]► Registros originais:[/white]    {total_registros:,}")
        print(f"[white]► Registros > {value}:[/white]    {len(filtered_df):,}")
        print(f"[white]► Registros removidos:[/white]    {total_registros - len(filtered_df):,}")
        
    else:
        min_value = float(inquirer.text(
            message="Digite o valor mínimo:"
        ).execute())
        max_value = float(inquirer.text(
            message="Digite o valor máximo:"
        ).execute())
        
        for _ in track(range(100), description="[cyan]Aplicando filtro...[/cyan]"):
            time.sleep(0.01)
            
        filtered_df = filter_system.df[(filter_system.df[selected_header] >= min_value) & 
                                     (filter_system.df[selected_header] <= max_value)].copy()
        output_file = filter_system.filter_numeric_between(selected_header, min_value, max_value, output_dir)
        
        print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
        print(f"[white]► Registros originais:[/white]    {total_registros:,}")
        print(f"[white]► Registros entre {min_value} e {max_value}:[/white]    {len(filtered_df):,}")
        print(f"[white]► Registros removidos:[/white]    {total_registros - len(filtered_df):,}")

    print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
    print(f"[dim]📁 Arquivo salvo em: {output_file}[/dim]\n")

def unify_excel_files():
    """Função para unificar arquivos Excel"""
    print("\n[bold yellow]╔══ Iniciando Unificação de Arquivos ══╗[/bold yellow]\n")
    print("[white]► Requisitos: os arquivos precisam ter colunas com mesmo nome[/white]")
    print("[white]► Coluna obrigatória: 'CPF'[/white]\n")
    
    directory_path = inquirer.text(
        message="Digite o caminho da pasta com os arquivos Excel:"
    ).execute()
    
    if not os.path.isdir(directory_path):
        print("[bold red]✗ Diretório inválido![/bold red]\n")
        return

    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo unificado:"
    ).execute()

    for _ in track(range(100), description="[cyan]Unificando arquivos...[/cyan]"):
        time.sleep(0.01)

    output_file = ExcelFilter.unify_excel_files(directory_path, output_dir)
    
    if output_file:
        print("\n[bold green]✓ Processo concluído com sucesso![/bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[/dim]\n")
    else:
        print("[bold red]✗ Erro ao unificar arquivos![/bold red]\n")

def unify_excel_files_with_cpf():
    """Função para unificar arquivos Excel com base no CPF"""
    filter_system = ExcelFilter()

    base_file_path = inquirer.text(
        message="Digite o caminho do arquivo base (.xlsx):"
    ).execute()

    if not filter_system.load_excel(base_file_path):
        return

    # Seleciona a coluna de CPF do arquivo base
    base_cpf_column = inquirer.select(
        message="Selecione a coluna de CPF do arquivo base:",
        choices=filter_system.headers
    ).execute()

    second_file_path = inquirer.text(
        message="Digite o caminho do segundo arquivo (.xlsx):"
    ).execute()

    if not filter_system.load_excel(second_file_path):
        return

    # Seleciona a coluna de CPF do segundo arquivo
    second_cpf_column = inquirer.select(
        message="Selecione a coluna de CPF do segundo arquivo:",
        choices=filter_system.headers
    ).execute()

    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo unificado:"
    ).execute()

    output_file = filter_system.unify_excel_files_with_cpf(base_file_path, second_file_path, base_cpf_column, second_cpf_column, output_dir)
    print(f"\nArquivo unificado salvo em: {output_file}")

def adicionar_coluna_idade():

    import pandas as pd
    import os
    from datetime import datetime
    from pytz import timezone
    from InquirerPy import inquirer
    from rich import print

    """
    Recebe um arquivo CSV, permite a seleção de uma coluna de data de nascimento
    e adiciona uma nova coluna "idade" calculada com base na data atual (Brasil - São Paulo).
    - Detecta automaticamente o delimitador do CSV.
    - Ignora linhas problemáticas ao carregar o arquivo.
    - Trata a coluna "idade" como string para evitar formatação decimal.
    """
    print("\n[bold yellow]╔══ Adicionar Coluna de Idade ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo CSV
    file_path = inquirer.text(
        message="Digite o caminho do arquivo CSV:"
    ).execute()

    # Tenta detectar o delimitador automaticamente
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            first_line = file.readline()
            delimiter = ";" if ";" in first_line else ","
    except Exception as e:
        print(f"[bold red]✗ Erro ao ler o arquivo: {e}[bold red]\n")
        return

    print(f"[cyan]✓ Delimitador detectado: '{delimiter}'[cyan]")

    try:
        # Lê o CSV ignorando erros e pulando linhas inconsistentes
        df = pd.read_csv(file_path, dtype=str, sep=delimiter, on_bad_lines="skip", encoding="utf-8")
        
        if df.empty:
            print("[bold red]✗ O arquivo CSV está vazio ou não contém dados válidos.[bold red]\n")
            return
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo CSV: {e}[bold red]\n")
        return

    # Seleciona a coluna de data de nascimento
    date_column = inquirer.select(
        message="Selecione a coluna de Data de Nascimento:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Calculando idades...[/cyan]")

    # Define o fuso horário do Brasil - São Paulo
    brasil_tz = timezone("America/Sao_Paulo")
    today = datetime.now(brasil_tz).date()  # Obtém a data atual no fuso horário correto

    # Função para calcular idade
    def calcular_idade(data_nascimento):
        try:
            data_nasc = datetime.strptime(data_nascimento, "%d/%m/%Y").date()
            idade = today.year - data_nasc.year - ((today.month, today.day) < (data_nasc.month, data_nasc.day))
            return str(idade)  # Converte para string para evitar valores decimais
        except Exception:
            return None  # Retorna None caso a data seja inválida

    # Aplica a função de cálculo de idade
    df["idade"] = df[date_column].apply(calcular_idade)

    # Exclui linhas com idade vazia (datas inválidas)
    df = df.dropna(subset=["idade"])

    # Converte a coluna "idade" explicitamente para string
    df["idade"] = df["idade"].astype(str)

    # Pergunta o diretório para salvar o arquivo final
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o novo arquivo CSV:"
    ).execute()

    # Define o caminho do arquivo de saída
    output_file = os.path.join(output_dir, f'arquivo_com_idade_{os.path.basename(file_path)}')

    print("\n[cyan]Salvando arquivo final...[/cyan]")
    try:
        # Salva o arquivo atualizado garantindo que a coluna "idade" seja string
        df.to_csv(output_file, index=False, encoding="utf-8", sep=delimiter, quoting=1)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[bold red]\n")


def filter_cpf_removal():
    """Função para remover CPFs de um arquivo base que existem em outro arquivo"""
    filter_system = ExcelFilter()
    
    # Arquivo base
    base_file_path = inquirer.text(
        message="Digite o caminho do arquivo base (.xlsx):"
    ).execute()
    
    if not filter_system.load_excel(base_file_path):
        return
        
    # Seleciona coluna CPF do arquivo base
    base_cpf_column = inquirer.select(
        message="Selecione a coluna de CPF do arquivo base:",
        choices=filter_system.headers
    ).execute()
    
    # Arquivo de remoção
    removal_file_path = inquirer.text(
        message="Digite o caminho do arquivo com CPFs a serem removidos (.xlsx):"
    ).execute()
    
    if not filter_system.load_excel(removal_file_path):
        return
        
    # Seleciona coluna CPF do arquivo de remoção
    removal_cpf_column = inquirer.select(
        message="Selecione a coluna de CPF do arquivo de remoção:",
        choices=filter_system.headers
    ).execute()
    
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo filtrado:"
    ).execute()
    
    output_file = filter_system.filter_cpf_removal(base_file_path, removal_file_path, 
                                                 base_cpf_column, removal_cpf_column, output_dir)
    print(f"\nArquivo filtrado salvo em: {output_file}")

def filter_cpf_duplicates():
    """Função para remover CPFs duplicados"""
    filter_system = ExcelFilter()
    
    file_path = inquirer.text(
        message="Digite o caminho do arquivo (.xlsx):"
    ).execute()
    
    if not filter_system.load_excel(file_path):
        return
        
    cpf_column = inquirer.select(
        message="Selecione a coluna de CPF:",
        choices=filter_system.headers
    ).execute()
    
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo filtrado:"
    ).execute()
    
    output_file = filter_system.filter_cpf_duplicates(file_path, cpf_column, output_dir)
    print(f"\nArquivo com CPFs únicos salvo em: {output_file}")

def filter_phone_numbers_csv():
    """Função para verificar números de telefone com prefixo '55' e exatamente 11 dígitos em arquivos CSV."""
    print("\n[bold yellow]╔══ Iniciando Filtro de Números de Telefone (CSV) ══╗[/bold yellow]\n")

    # Solicita o caminho do arquivo CSV
    csv_path = inquirer.text(
        message="Digite o caminho do arquivo CSV:"
    ).execute()

    try:
        # Carrega o arquivo CSV em um DataFrame
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar arquivo CSV: {e}[/bold red]\n")
        return

    # Lista os cabeçalhos e solicita ao usuário para selecionar a coluna de telefone
    selected_header = inquirer.select(
        message="Selecione a coluna que contém os números de telefone:",
        choices=df.columns.tolist()
    ).execute()

    # Inicializa contadores
    total_registros = len(df)
    registros_removidos = 0

    # Processa cada linha e remove as inválidas
    indices_to_drop = []
    for index in track(df.index, description="[cyan]Filtrando registros...[cyan]", total=total_registros):
        value = str(df.at[index, selected_header]).strip()

        # Remove caracteres não numéricos
        clean_value = ''.join(filter(str.isdigit, value))

        # Verifica se o número é válido
        if len(clean_value) != 13 or not clean_value.startswith('55'):
            indices_to_drop.append(index)
            registros_removidos += 1

    # Remove os índices coletados
    df.drop(indices_to_drop, inplace=True)

    # Calcula total de registros após remoção
    registros_restantes = len(df)

    # Exibe resumo da operação
    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Registros originais:[/white]    {total_registros:,}")
    print(f"[white]► Registros removidos:[/white]    {registros_removidos:,}")
    print(f"[white]► Registros restantes:[/white]   {registros_restantes:,}")

    # Solicita o diretório de saída
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo filtrado:"
    ).execute()

    # Salva o arquivo alterado com prefixo no nome
    output_file = os.path.join(output_dir, f'filtro_cel_num_{os.path.basename(csv_path)}')
    try:
        df.to_csv(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[/bold red]\n")

def adjust_cpfs_to_11_digits():
    """Função para ajustar CPFs em um arquivo Excel, garantindo que todos tenham 11 dígitos."""
    filter_system = ExcelFilter()

    print("\n[bold yellow]╔══ Iniciando Ajuste de CPFs ══╗[/bold yellow]\n")

    # Solicita o caminho do arquivo Excel
    excel_path = inquirer.text(
        message="Digite o caminho do arquivo Excel:"
    ).execute()

    if not filter_system.load_excel(excel_path):
        print("[bold red]✗ Erro ao carregar arquivo![/bold red]\n")
        return

    # Lista os cabeçalhos e solicita ao usuário para selecionar a coluna de CPF
    selected_header = inquirer.select(
        message="Selecione a coluna que contém os CPFs:",
        choices=filter_system.headers
    ).execute()

    # Converte a coluna para string antes de normalizar os CPFs
    filter_system.df[selected_header] = filter_system.df[selected_header].astype(str)

    # Inicializa contadores
    total_registros = len(filter_system.df)
    registros_normalizados = 0

    # Ajusta os CPFs na coluna selecionada
    for index in track(filter_system.df.index, description="[cyan]Ajustando CPFs...[cyan]", total=total_registros):
        value = str(filter_system.df.at[index, selected_header]).strip()

        # Remove caracteres não numéricos
        clean_value = ''.join(filter(str.isdigit, value))

        # Ajusta para 11 dígitos adicionando zeros à esquerda
        if clean_value and len(clean_value) <= 11:
            normalized_cpf = clean_value.zfill(11)
            filter_system.df.at[index, selected_header] = normalized_cpf
            registros_normalizados += 1

    # Exibe resumo da operação
    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Registros originais:[/white]       {total_registros:,}")
    print(f"[white]► CPFs ajustados:[/white]          {registros_normalizados:,}")

    # Solicita o diretório de saída
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo com CPFs ajustados:"
    ).execute()

    # Salva o arquivo alterado com prefixo no nome
    output_file = os.path.join(output_dir, f'cpfs_ajustados_{os.path.basename(excel_path)}')
    try:
        filter_system.df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[/bold red]\n")

def format_values_to_money():
    """
    Formata valores de uma coluna para o formato monetário (123400 -> 1234,00).
    """
    print("\n[bold yellow]╔══ Iniciando Formatação Monetária ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[bold red]\n")
        return

    # Seleciona a coluna de valores
    selected_column = inquirer.select(
        message="Selecione a coluna com os valores a formatar:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Formatando valores...[/cyan]")

    # Formata os valores para o padrão monetário
    def format_money(value):
        try:
            # Divide por 100 e converte para string no formato monetário
            formatted_value = f"{int(value) / 100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return formatted_value
        except (ValueError, TypeError):
            return value  # Retorna o valor original se não for possível formatar

    # Aplica a formatação
    for _ in track(range(100), description="[cyan]Processando valores...[/cyan]"):
        df[selected_column] = df[selected_column].apply(format_money)

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo formatado:"
    ).execute()

    # Adiciona o prefixo ao nome do arquivo de saída
    output_file = os.path.join(output_dir, f"format_money_{os.path.basename(file_path)}")

    try:
        df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[bold red]\n")

def filter_and_format_rgs():
    """Função para filtrar RGS inválidos e formatar os válidos para 10 dígitos."""

    print("\n[bold yellow]╔══ Iniciando Filtragem e Formatação de RGs ══╗[/bold yellow]\n")

    # Recebe o arquivo base
    base_file_path = inquirer.text(
        message="Digite o caminho do arquivo base (.xlsx):"
    ).execute()

    try:
        base_df = pd.read_excel(base_file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo base: {e}[/bold red]\n")
        return

    # Seleciona a coluna de RG no arquivo base
    rg_column = inquirer.select(
        message="Selecione a coluna de RG:",
        choices=base_df.columns.tolist()
    ).execute()

    print("\n[cyan]Verificando e filtrando RGs inválidos...[/cyan]")
    for _ in track(range(100), description="[cyan]Processando RGs...[/cyan]"):
        time.sleep(0.01)

    # Verifica RGs inválidos
    def is_valid_rg(value):
        if pd.isna(value):  # Verifica valores nulos
            return False
        value = str(value).strip()
        if not value.isdigit():  # Verifica se contém apenas dígitos
            return False
        if len(value) < 5:  # Verifica se tem pelo menos 5 dígitos
            return False
        return True

    # Filtra os registros válidos e inválidos
    base_df['RG_VALIDO'] = base_df[rg_column].apply(is_valid_rg)
    invalid_rgs = base_df[~base_df['RG_VALIDO']].copy()
    valid_rgs = base_df[base_df['RG_VALIDO']].copy()

    # Formata os RGs válidos para 10 dígitos
    print("\n[cyan]Formatando RGs válidos para 10 dígitos...[/cyan]")
    valid_rgs[rg_column] = valid_rgs[rg_column].astype(str).str.zfill(10)

    # Exibe resumo da operação
    total_registros = len(base_df)
    total_validos = len(valid_rgs)
    total_invalidos = len(invalid_rgs)

    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Registros originais:[/white]    {total_registros:,}")
    print(f"[white]► RGs válidos:[/white]           {total_validos:,}")
    print(f"[white]► RGs inválidos:[/white]         {total_invalidos:,}")

    # Recebe o diretório de saída
    output_dir = inquirer.text(
        message="Digite o caminho para salvar os arquivos filtrados:"
    ).execute()

    # Salva os arquivos filtrados
    valid_output_file = os.path.join(output_dir, f'valid_rgs_{os.path.basename(base_file_path)}')
    invalid_output_file = os.path.join(output_dir, f'invalid_rgs_{os.path.basename(base_file_path)}')

    try:
        valid_rgs.drop(columns=['RG_VALIDO'], inplace=True)
        invalid_rgs.drop(columns=['RG_VALIDO'], inplace=True)

        valid_rgs.to_excel(valid_output_file, index=False)
        invalid_rgs.to_excel(invalid_output_file, index=False)

        print("\n[bold green]✓ Processo concluído com sucesso![/bold green]")
        print(f"[dim]📁 RGs válidos salvos em: {valid_output_file}[/dim]")
        print(f"[dim]📁 RGs inválidos salvos em: {invalid_output_file}[/dim]\n")

    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar os arquivos: {e}[/bold red]\n")

def formatar_coluna_data():
    """Função para formatar colunas de data em um arquivo Excel."""
    print("\n[bold yellow]╔══ Iniciando Formatação de Datas ══╗[/bold yellow]\n")

    # Recebe o arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[/bold red]\n")
        return

    # Seleciona a coluna de data
    date_column = inquirer.select(
        message="Selecione a coluna de data:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Formatando dados...[/cyan]")

    for _ in track(range(100), description="[cyan]Processando...[/cyan]"):
        pass

    # Converte as datas para o formato dd/MM/YYYY
    try:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.strftime('%d/%m/%Y')
    except Exception as e:
        print(f"[bold red]✗ Erro ao formatar as datas: {e}[/bold red]\n")
        return

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo formatado:"
    ).execute()

    output_file = os.path.join(output_dir, f"data_formatada_{os.path.basename(file_path)}")

    try:
        df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[/bold red]\n")


def dois_unify_excel_files_with_cpf():
    """
    Unifica 2 arquivos (XLSX ou CSV) por CPF:
      1) Pergunta o caminho do arquivo base.
      2) Seleciona a coluna de CPF.
      3) Pergunta o caminho do segundo arquivo.
      4) Seleciona a coluna de CPF do segundo.
      5) Normaliza CPFs (removendo não dígitos e zfill(11)).
      6) Faz merge (inner) e salva o arquivo final (XLSX) num caminho escolhido.
    """

    import os
    import pandas as pd
    import time
    from InquirerPy import inquirer
    from rich import print
    from rich.progress import track

    # --------------------- Função auxiliar de carregamento --------------------- #
    def load_file_generic(file_path):
        """Carrega XLSX ou CSV (tentando ; depois ,) e retorna DataFrame como string."""
        if file_path.lower().endswith(".xlsx"):
            return pd.read_excel(file_path, engine="openpyxl", dtype=str)
        elif file_path.lower().endswith(".csv"):
            try:
                return pd.read_csv(file_path, sep=';', dtype=str)
            except:
                return pd.read_csv(file_path, sep=',', dtype=str)
        else:
            raise ValueError("Formato de arquivo não suportado! Use .xlsx ou .csv.")

    # --------------------- Função de normalização de CPF --------------------- #
    def normalize_cpf(cpf):
        """Remove caracteres não numéricos e zera à esquerda para 11 dígitos."""
        if pd.isna(cpf):
            return ""
        digits = "".join(ch for ch in str(cpf) if ch.isdigit())
        return digits.zfill(11)

    # 1) Recebe e carrega arquivo base
    print("\n[bold yellow]╔══ Iniciando Unificação por CPF ══╗[/bold yellow]\n")

    base_file_path = inquirer.text(
        message="Digite o caminho do arquivo base (.xlsx ou .csv):"
    ).execute()

    if not os.path.isfile(base_file_path):
        print(f"[bold red]✗ O caminho '{base_file_path}' não é válido![bold red]")
        return

    try:
        base_df = load_file_generic(base_file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar arquivo base: {e}[/bold red]")
        return

    if base_df.empty:
        print("[bold red]✗ O arquivo base está vazio ou não contém dados válidos.[/bold red]")
        return

    # Seleciona a coluna de CPF do arquivo base
    base_cpf_column = inquirer.select(
        message="Selecione a coluna de CPF do arquivo base:",
        choices=base_df.columns.tolist()
    ).execute()

    total_base = len(base_df)

    # 2) Recebe e carrega o segundo arquivo
    second_file_path = inquirer.text(
        message="Digite o caminho do segundo arquivo (.xlsx ou .csv):"
    ).execute()

    if not os.path.isfile(second_file_path):
        print(f"[bold red]✗ O caminho '{second_file_path}' não é válido![bold red]")
        return

    try:
        second_df = load_file_generic(second_file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o segundo arquivo: {e}[/bold red]")
        return

    if second_df.empty:
        print("[bold red]✗ O segundo arquivo está vazio ou não contém dados válidos.[/bold red]")
        return

    # Seleciona a coluna de CPF do segundo arquivo
    second_cpf_column = inquirer.select(
        message="Selecione a coluna de CPF do segundo arquivo:",
        choices=second_df.columns.tolist()
    ).execute()

    total_second = len(second_df)

    # 3) Pergunta onde salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo unificado:"
    ).execute()

    if not os.path.isdir(output_dir):
        print(f"[bold red]✗ O caminho '{output_dir}' não é uma pasta válida![bold red]")
        return

    print("\n[bold yellow]╔══ Normalizando e Unificando CPF ══╗[/bold yellow]\n")

    # 4) Normaliza os CPFs (com barra de progresso)
    for _ in track(range(33), description="[cyan]Normalizando CPFs do arquivo base...[/cyan]"):
        time.sleep(0.01)
    base_df[base_cpf_column] = base_df[base_cpf_column].apply(normalize_cpf)

    for _ in track(range(33), description="[cyan]Normalizando CPFs do segundo arquivo...[/cyan]"):
        time.sleep(0.01)
    second_df[second_cpf_column] = second_df[second_cpf_column].apply(normalize_cpf)

    # 5) Faz merge (INNER) => só CPFs existentes nos 2 arquivos
    for _ in track(range(34), description="[cyan]Unificando arquivos...[/cyan]"):
        time.sleep(0.01)

    merged_df = pd.merge(base_df, second_df, left_on=base_cpf_column, right_on=second_cpf_column, how='inner')

    # 6) Salva o arquivo final como XLSX (por padrão)
    #    Se preferir salvar no formato do arquivo base, é possível, mas aqui manteremos XLSX
    import os
    output_file = os.path.join(output_dir, "unified_by_cpf.xlsx")
    try:
        merged_df.to_excel(output_file, index=False, engine="openpyxl")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar arquivo unificado: {e}[/bold red]")
        return

    # 7) Exibe resumo
    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Registros no arquivo base:[/white]    {total_base:,}")
    print(f"[white]► Registros no segundo arquivo:[/white] {total_second:,}")
    print(f"[white]► Registros após unificação:[/white]    {len(merged_df):,}")
    print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
    print(f"[dim]📁 Arquivo salvo em: {output_file}[/dim]\n")


def unifique_one():
    """
    Unifica todas as planilhas .xlsx de uma pasta em um único arquivo.
    """
    print("\n[bold yellow]╔══ Unificação de Planilhas ══╗[/bold yellow]\n")

    # Recebe o caminho da pasta com as planilhas
    folder_path = inquirer.text(
        message="Digite o caminho da pasta contendo as planilhas .xlsx:"
    ).execute()

    if not os.path.exists(folder_path):
        print(f"[bold red]✗ A pasta especificada não existe: {folder_path}[bold red]\n")
        return

    # Lista todas as planilhas .xlsx na pasta
    files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]
    if not files:
        print(f"[bold red]✗ Não foram encontradas planilhas .xlsx na pasta: {folder_path}[bold red]\n")
        return

    print(f"[cyan]Encontradas {len(files)} planilhas para unificação...[/cyan]\n")

    # Unifica todas as planilhas em um único DataFrame
    unified_df = pd.DataFrame()
    for file in files:
        try:
            file_path = os.path.join(folder_path, file)
            df = pd.read_excel(file_path)
            unified_df = pd.concat([unified_df, df], ignore_index=True)
            print(f"[green]✓ Unificada: {file}[green]")
        except Exception as e:
            print(f"[bold red]✗ Erro ao unificar {file}: {e}[bold red]")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo unificado:"
    ).execute()

    if not os.path.exists(output_dir):
        print(f"[bold red]✗ A pasta especificada para salvar não existe: {output_dir}[bold red]\n")
        return

    # Caminho do arquivo de saída
    output_file = os.path.join(output_dir, "unifique_one_result.xlsx")

    # Salva o arquivo unificado
    try:
        unified_df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Arquivo unificado salvo com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo unificado: {e}[bold red]\n")

def filter_remove_by_name():
    """Função para filtrar e remover registros por nome."""

    print("\n[bold yellow]╔══ Iniciando Filtragem e Remoção por Nome ══╗[/bold yellow]\n")

    # Recebe o arquivo base
    base_file_path = inquirer.text(
        message="Digite o caminho do arquivo base (.xlsx):"
    ).execute()

    try:
        base_df = pd.read_excel(base_file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo base: {e}[/bold red]\n")
        return

    # Seleciona a coluna de nome no arquivo base
    base_name_column = inquirer.select(
        message="Selecione a coluna de NOME no arquivo base:",
        choices=base_df.columns.tolist()
    ).execute()

    # Recebe o arquivo de blacklist
    blacklist_file_path = inquirer.text(
        message="Digite o caminho do arquivo de blacklist (.xlsx):"
    ).execute()

    try:
        blacklist_df = pd.read_excel(blacklist_file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo de blacklist: {e}[/bold red]\n")
        return

    # Seleciona a coluna de nome no arquivo de blacklist
    blacklist_name_column = inquirer.select(
        message="Selecione a coluna de NOME no arquivo de blacklist:",
        choices=blacklist_df.columns.tolist()
    ).execute()

    # Converte os nomes para caixa alta
    print("\n[cyan]Normalizando nomes para caixa alta...[/cyan]")
    for _ in track(range(100), description="[cyan]Processando...[/cyan]"):
        time.sleep(0.01)

    base_df[base_name_column] = base_df[base_name_column].str.upper().fillna("")
    blacklist_df[blacklist_name_column] = blacklist_df[blacklist_name_column].str.upper().fillna("")

    # Filtra os registros
    print("\n[cyan]Removendo registros encontrados na blacklist...[/cyan]")
    blacklist_names = set(blacklist_df[blacklist_name_column].tolist())
    filtered_df = base_df[~base_df[base_name_column].isin(blacklist_names)].copy()

    # Exibe resumo da operação
    total_registros = len(base_df)
    registros_removidos = total_registros - len(filtered_df)

    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Registros originais:[/white]    {total_registros:,}")
    print(f"[white]► Registros removidos:[/white]    {registros_removidos:,}")
    print(f"[white]► Registros restantes:[/white]   {len(filtered_df):,}")

    # Recebe o diretório de saída
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo filtrado:"
    ).execute()

    # Salva o arquivo filtrado com o prefixo
    output_file = os.path.join(output_dir, f'filtra_name_remove_{os.path.basename(base_file_path)}')
    try:
        filtered_df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[/dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[/bold red]\n")

def filter_agencies():
    """Função para filtrar agências bancárias com base em critérios específicos."""
    
    print("\n[bold yellow]╔══ Iniciando Filtro de Agências ══╗[/bold yellow]\n")

    # Recebe o arquivo Excel
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[/bold red]\n")
        return

    # Seleciona a coluna de agência
    agency_column = inquirer.select(
        message="Selecione a coluna de agência bancária:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Filtrando agências...[/cyan]")

    # Critérios de filtragem
    initial_count = len(df)
    filtered_df = df[df[agency_column].astype(str).str.len() >= 4]
    filtered_df = filtered_df[filtered_df[agency_column].notnull()]

    final_count = len(filtered_df)
    removed_count = initial_count - final_count

    # Resumo da operação
    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Registros originais:[/white]    {initial_count:,}")
    print(f"[white]► Registros removidos:[/white]    {removed_count:,}")
    print(f"[white]► Registros restantes:[/white]   {final_count:,}")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo filtrado:"
    ).execute()

    # Salva o arquivo filtrado
    output_file = os.path.join(output_dir, f"filtro_agencias_{os.path.basename(file_path)}")

    try:
        filtered_df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[bold red]\n")


def map_columns_and_merge():
    """Função para mapear colunas de um modelo e preencher com dados de outro arquivo."""

    # Recebe o arquivo modelo
    print("\n[bold yellow]╔══ Iniciando Mapeamento de Colunas ══╗[/bold yellow]\n")
    model_file_path = inquirer.text(
        message="Digite o caminho do arquivo modelo (.xlsx):"
    ).execute()

    try:
        model_df = pd.read_excel(model_file_path)
        model_columns = model_df.columns.tolist()
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo modelo: {e}[/bold red]\n")
        return

    if not model_columns:
        print("[bold red]✗ O arquivo modelo não possui cabeçalhos![bold red]\n")
        return

    # Recebe o arquivo com dados
    data_file_path = inquirer.text(
        message="Digite o caminho do arquivo de dados (.xlsx):"
    ).execute()

    try:
        data_df = pd.read_excel(data_file_path)
        data_columns = data_df.columns.tolist()
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo de dados: {e}[/bold red]\n")
        return

    if not data_columns:
        print("[bold red]✗ O arquivo de dados não possui cabeçalhos![bold red]\n")
        return

    # Inicializa o DataFrame de saída com as mesmas colunas do modelo
    output_df = pd.DataFrame(columns=model_columns)

    # Mapeamento das colunas
    column_mapping = {}
    used_columns = set()
    print("\n[cyan]Mapeie as colunas do arquivo modelo com as do arquivo de dados:[/cyan]\n")

    for model_col in model_columns:
        available_columns = [col for col in data_columns if col not in used_columns] + ["Ignorar"]
        mapped_column = inquirer.select(
            message=f"Selecione a coluna correspondente para '{model_col}' no arquivo de dados:",
            choices=available_columns,
        ).execute()

        if mapped_column != "Ignorar":
            column_mapping[model_col] = mapped_column
            used_columns.add(mapped_column)

    # Preenchendo o DataFrame de saída com os dados mapeados
    for model_col, data_col in column_mapping.items():
        output_df[model_col] = data_df[data_col]

    # Exibindo resumo
    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Linhas no arquivo modelo:[/white]       {len(model_df):,}")
    print(f"[white]► Linhas no arquivo de dados:[/white]    {len(data_df):,}")
    print(f"[white]► Colunas no arquivo modelo:[/white]     {len(model_columns):,}")
    print(f"[white]► Colunas no arquivo de dados:[/white]   {len(data_columns):,}")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo resultante:"
    ).execute()

    output_file = os.path.join(output_dir, f"resultado_{os.path.basename(model_file_path)}")

    try:
        output_df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[bold red]\n")

def validate_address_number():
    """Valida números de endereço e preenche células vazias com 0, converte para texto no final."""
    print("\n[bold yellow]╔══ Iniciando Validação de Números de Endereço ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[/bold red]\n")
        return

    # Seleciona a coluna de números de endereço
    column_name = inquirer.select(
        message="Selecione a coluna que contém os números de endereço:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Validando números de endereço...[/cyan]")

    # Processando e preenchendo valores vazios
    for _ in track(range(100), description="[cyan]Processando...[/cyan]"):
        pass

    try:
        df[column_name] = df[column_name].fillna(0)
        df[column_name] = df[column_name].apply(lambda x: int(str(x).strip()) if str(x).strip().isdigit() else 0)
    except Exception as e:
        print(f"[bold red]✗ Erro durante a validação: {e}[/bold red]\n")
        return

    # Convertendo todas as células para texto
    df[column_name] = df[column_name].astype(str)

    # Exibindo resumo
    total_linhas = len(df)
    linhas_vazias = (df[column_name] == "0").sum()

    print("\n[bold green]╔══ Resumo da Validação ══╗[/bold green]")
    print(f"[white]► Total de linhas no arquivo:[/white] {total_linhas:,}")
    print(f"[white]► Linhas vazias na coluna:[/white]   {linhas_vazias:,}")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo validado:"
    ).execute()

    output_file = os.path.join(output_dir, f"validated_address_numbers_{os.path.basename(file_path)}")

    try:
        df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[bold red]\n")

def delete_rows_with_empty_cells():
    """Remove linhas de um arquivo Excel onde a célula na coluna selecionada está vazia."""
    print("\n[bold yellow]╔══ Iniciando Remoção de Linhas com Células Vazias ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[/bold red]\n")
        return

    # Seleciona a coluna para verificar células vazias
    column_name = inquirer.select(
        message="Selecione a coluna para verificar células vazias:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Removendo linhas com células vazias...[/cyan]")

    try:
        # Remove linhas com células vazias na coluna selecionada
        initial_row_count = len(df)
        df = df.dropna(subset=[column_name])
        final_row_count = len(df)
        removed_rows = initial_row_count - final_row_count
    except Exception as e:
        print(f"[bold red]✗ Erro durante a remoção: {e}[/bold red]\n")
        return

    # Exibindo resumo
    print("\n[bold green]╔══ Resumo da Remoção ══╗[/bold green]")
    print(f"[white]► Total de linhas no arquivo original:[/white] {initial_row_count:,}")
    print(f"[white]► Linhas removidas:[/white]                 {removed_rows:,}")
    print(f"[white]► Total de linhas no arquivo final:[/white] {final_row_count:,}")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo atualizado:"
    ).execute()

    output_file = os.path.join(output_dir, f"rows_removed_{os.path.basename(file_path)}")

    try:
        df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[bold red]\n")

def format_benefit_file():
    """Formata as colunas de sexo e tipo_beneficio em um arquivo Excel."""
    print("\n[bold yellow]╔══ Iniciando Formatação de Benefício ══╗[/bold yellow]\n")

    # Recebe o arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[/bold red]\n")
        return

    # Seleciona a coluna de sexo
    sexo_column = inquirer.select(
        message="Selecione a coluna de sexo:",
        choices=df.columns.tolist()
    ).execute()

    # Seleciona a coluna de tipo_beneficio
    beneficio_column = inquirer.select(
        message="Selecione a coluna de tipo_beneficio:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Formatando dados...[/cyan]")

    # Formata a coluna de sexo
    for _ in track(range(50), description="[cyan]Formatando coluna de sexo...[/cyan]"):
        pass

    df[sexo_column] = df[sexo_column].replace({'M': 'Masculino', 'F': 'Feminino'})

    # Formata a coluna de tipo_beneficio
    for _ in track(range(50), description="[cyan]Formatando coluna de tipo_beneficio...[/cyan]"):
        pass

    df[beneficio_column] = df[beneficio_column].astype(str).str[:2]

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo formatado:"
    ).execute()

    output_file = os.path.join(output_dir, f"format_benf_{os.path.basename(file_path)}")

    try:
        df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[/bold red]\n")

def format_agency_column():
    """
    Formata uma coluna de agência, removendo o último dígito para agências com dois ou mais dígitos,
    substituindo valores vazios, nulos ou iguais a '0' por '1', e salvando o arquivo com prefixo 'agencia_format_'.
    """
    print("\n[bold yellow]╔══ Iniciando Formatação de Agências ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[bold red]\n")
        return

    # Seleciona a coluna de agência
    agency_column = inquirer.select(
        message="Selecione a coluna de agência:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Formatando valores da coluna de agência...[/cyan]")

    # Função para formatar os valores da coluna de agência
    def format_agency(value):
        if pd.isna(value) or str(value).strip() in ('', '0'):
            return '1'  # Substituir valores vazios, nulos ou iguais a 0 por '1'
        value = str(value).strip()  # Remove espaços
        if len(value) > 1:  # Se o valor tiver dois ou mais dígitos, remove o último dígito
            return value[:-3]
        return value

    # Aplica a formatação e conta alterações
    total_rows = len(df)
    original_column = df[agency_column].astype(str).copy()  # Copia os valores originais como string
    df[agency_column] = df[agency_column].apply(format_agency)
    modified_rows = (original_column != df[agency_column]).sum()  # Conta as linhas modificadas

    # Resumo da operação
    print("\n[bold green]╔══ Resumo da Formatação ══╗[/bold green]")
    print(f"[white]► Total de linhas no arquivo original:[/white] {total_rows:,}")
    print(f"[white]► Linhas modificadas:[/white] {modified_rows:,}")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo atualizado:"
    ).execute()

    # Define o caminho do arquivo de saída
    output_file = os.path.join(output_dir, f"agencia_format_{os.path.basename(file_path)}")

    # Salva o arquivo atualizado
    try:
        df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[bold red]\n")

def validate_and_format_cep():
    """Valida, verifica existência e busca detalhes de CEPs usando a API OpenCEP."""
    print("\n[bold yellow]╔══ Iniciando Validação e Busca de CEP ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[bold red]\n")
        return

    # Seleciona as colunas necessárias
    cep_column = inquirer.select(
        message="Selecione a coluna que contém os CEPs:",
        choices=df.columns.tolist()
    ).execute()

    endereco_column = inquirer.select(
        message="Selecione a coluna de Endereço:",
        choices=df.columns.tolist()
    ).execute()

    bairro_column = inquirer.select(
        message="Selecione a coluna de Bairro:",
        choices=df.columns.tolist()
    ).execute()

    cidade_column = inquirer.select(
        message="Selecione a coluna de Cidade:",
        choices=df.columns.tolist()
    ).execute()

    estado_column = inquirer.select(
        message="Selecione a coluna de Estado:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Validando CEPs...[/cyan]")

    # Validação inicial do CEP
    def validate_cep(value):
        if pd.isna(value):
            return None
        cep = str(value).strip().replace("-", "")
        if len(cep) != 8 or not cep.isdigit():
            return None
        return cep

    # Aplicar validação
    df[cep_column] = df[cep_column].apply(validate_cep)

    # Remove linhas com CEP inválido
    initial_row_count = len(df)
    df_invalid = df[df[cep_column].isna()].copy()
    df = df.dropna(subset=[cep_column]).copy()

    print(f"[bold green]✓ Linhas removidas devido a CEPs inválidos: {len(df_invalid)}[/bold green]\n")

    # Fase 1: Verificar se o CEP existe
    print("[cyan]Verificando a existência dos CEPs...[/cyan]")

    def check_cep_exists(cep):
        try:
            response = requests.get(f"https://opencep.com/v1/{cep}.json", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return "erro" not in data  # Retorna True se o CEP existir
            return False
        except Exception as e:
            logging.warning(f"Erro ao verificar CEP {cep}: {e}")
            return False

    # Adiciona uma nova coluna para marcar CEPs existentes
    df["EXISTE"] = False
    for index in track(df.index, description="[cyan]Verificando CEPs...[/cyan]"):
        cep = df.at[index, cep_column]
        df.at[index, "EXISTE"] = check_cep_exists(cep)
        print(f"Verificando linha {index + 1}/{len(df)} - CEP: {cep}")

    # Fase 2: Obter detalhes dos CEPs existentes
    print("[cyan]Buscando detalhes dos CEPs existentes...[/cyan]")
    valid_indices = []

    def fetch_cep_details(cep):
        try:
            response = requests.get(f"https://opencep.com/v1/{cep}.json")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logging.warning(f"Erro ao buscar detalhes do CEP {cep}: {e}")
            return None

    for index in track(df.index, description="[cyan]Processando CEPs existentes...[/cyan]"):
        if df.at[index, "EXISTE"]:
            cep = df.at[index, cep_column]
            address_data = fetch_cep_details(cep)
            if address_data:
                valid_indices.append(index)
                df.at[index, endereco_column] = address_data.get("logradouro", df.at[index, endereco_column])
                df.at[index, bairro_column] = address_data.get("bairro", df.at[index, bairro_column])
                df.at[index, cidade_column] = address_data.get("localidade", df.at[index, cidade_column])
                df.at[index, estado_column] = address_data.get("uf", df.at[index, estado_column])
                print(f"Detalhes obtidos para CEP: {cep}")
            else:
                print(f"Falha ao buscar detalhes para o CEP: {cep}")

    # Remove CEPs não existentes do DataFrame
    df_invalid = pd.concat([df_invalid, df[~df["EXISTE"]]])
    df_valid = df.loc[valid_indices].copy()
    df.drop(columns=["EXISTE"], inplace=True)

    # Resumo final
    print("\n[bold green]╔══ Resumo Final ══╗[/bold green]")
    print(f"[white]► Total de linhas no arquivo original:[/white] {initial_row_count:,}")
    print(f"[white]► CEPs válidos encontrados e detalhados:[/white] {len(df_valid):,}")
    print(f"[white]► Linhas removidas (CEPs inválidos ou inexistentes):[/white] {len(df_invalid):,}")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar os arquivos:"
    ).execute()

    # Caminhos para os arquivos de saída
    valid_output_file = os.path.join(output_dir, f"cep_validos_{os.path.basename(file_path)}")
    invalid_output_file = os.path.join(output_dir, f"cep_invalidos_{os.path.basename(file_path)}")

    # Salva os arquivos
    try:
        df_valid.to_excel(valid_output_file, index=False)
        df_invalid.to_excel(invalid_output_file, index=False)
        print(f"\n[bold green]✓ Arquivos salvos com sucesso![bold green]")
        print(f"[dim]📁 Arquivo com CEPs válidos salvo em: {valid_output_file}[dim]")
        print(f"[dim]📁 Arquivo com CEPs inválidos salvo em: {invalid_output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar os arquivos: {e}[bold red]\n")

def validador_de_bancos():
    """
    Valida colunas de banco, agência e conta.
    Remove linhas que não atendem aos critérios:
    - Banco: 1 a 3 dígitos
    - Agência: 1 a 4 dígitos
    - Conta: Não pode ter letras, espaços ou estar vazia.
    """
    print("\n[bold yellow]╔══ Iniciando Validação de Banco ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[bold red]\n")
        return

    # Seleciona as colunas necessárias
    banco_column = inquirer.select(
        message="Selecione a coluna de Banco:",
        choices=df.columns.tolist()
    ).execute()

    agencia_column = inquirer.select(
        message="Selecione a coluna de Agência:",
        choices=df.columns.tolist()
    ).execute()

    conta_column = inquirer.select(
        message="Selecione a coluna de Conta:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Validando dados...[/cyan]")

    # Funções de validação
    def is_valid_banco(value):
        return str(value).isdigit() and 1 <= len(str(value)) <= 3

    def is_valid_agencia(value):
        return str(value).isdigit() and 1 <= len(str(value)) <= 4

    def is_valid_conta(value):
        return str(value).isdigit() and len(str(value)) > 0

    # Inicializa contadores
    initial_row_count = len(df)

    # Aplica validação para todas as colunas e filtra as linhas inválidas
    df["VALIDO"] = df[banco_column].apply(is_valid_banco) & \
                   df[agencia_column].apply(is_valid_agencia) & \
                   df[conta_column].apply(is_valid_conta)

    df_invalid = df[~df["VALIDO"]].copy()  # Linhas inválidas
    df = df[df["VALIDO"]].copy()           # Linhas válidas

    # Remove a coluna auxiliar "VALIDO"
    df.drop(columns=["VALIDO"], inplace=True)
    df_invalid.drop(columns=["VALIDO"], inplace=True)

    # Resumo da validação
    linhas_invalidas = len(df_invalid)
    linhas_validas = len(df)

    print("\n[bold green]╔══ Resumo da Validação ══╗[/bold green]")
    print(f"[white]► Linhas originais:[/white]    {initial_row_count:,}")
    print(f"[white]► Linhas válidas:[/white]      {linhas_validas:,}")
    print(f"[white]► Linhas inválidas:[/white]    {linhas_invalidas:,}")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar os arquivos filtrados:"
    ).execute()

    # Adiciona prefixo aos nomes dos arquivos de saída
    valid_output_file = os.path.join(output_dir, f"filtrar_bank_validos_{os.path.basename(file_path)}")
    invalid_output_file = os.path.join(output_dir, f"filtrar_bank_invalidos_{os.path.basename(file_path)}")

    # Salva os arquivos
    try:
        df.to_excel(valid_output_file, index=False)
        df_invalid.to_excel(invalid_output_file, index=False)
        print(f"\n[bold green]✓ Arquivos salvos com sucesso![bold green]")
        print(f"[dim]📁 Arquivo com dados válidos salvo em: {valid_output_file}[dim]")
        print(f"[dim]📁 Arquivo com dados inválidos salvo em: {invalid_output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar os arquivos: {e}[bold red]\n")

def validate_sex_column():
    """Valida a coluna de sexo, convertendo 'M' e 'F' para 'Masculino' e 'Feminino',
    removendo linhas com valores inválidos."""
    print("\n[bold yellow]╔══ Iniciando Validação da Coluna de Sexo ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[/bold red]\n")
        return

    # Seleciona a coluna de sexo
    column_name = inquirer.select(
        message="Selecione a coluna que contém os valores de sexo:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Validando a coluna de sexo...[/cyan]")

    # Processando os valores
    valid_sex_values = {"M": "Masculino", "F": "Feminino"}
    try:
        df[column_name] = df[column_name].apply(lambda x: valid_sex_values.get(str(x).strip(), x))

        # Filtra as linhas válidas
        valid_rows = df[column_name].isin(["Masculino", "Feminino"])
        filtered_df = df[valid_rows].copy()

        invalid_rows_count = len(df) - len(filtered_df)

    except Exception as e:
        print(f"[bold red]✗ Erro durante a validação: {e}[/bold red]\n")
        return

    # Exibindo resumo
    total_linhas = len(df)
    linhas_validas = len(filtered_df)

    print("\n[bold green]╔══ Resumo da Validação ══╗[/bold green]")
    print(f"[white]► Total de linhas no arquivo:[/white] {total_linhas:,}")
    print(f"[white]► Linhas válidas:[/white] {linhas_validas:,}")
    print(f"[white]► Linhas removidas:[/white] {invalid_rows_count:,}")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo validado:"
    ).execute()

    output_file = os.path.join(output_dir, f"validated_sex_column_{os.path.basename(file_path)}")

    try:
        filtered_df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[bold red]\n")

def extract_ddd_and_number():
    """Função para extrair DDD e número de uma coluna de celular."""
    print("\n[bold yellow]╔══ Iniciando Extração de DDD e Número ══╗[/bold yellow]\n")

    # Recebe o arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[/bold red]\n")
        return

    # Seleciona a coluna de números de celular
    phone_column = inquirer.select(
        message="Selecione a coluna que contém os números de celular (DDD+Número):",
        choices=df.columns.tolist()
    ).execute()

    # Seleciona a coluna de saída para DDD
    ddd_column = inquirer.select(
        message="Selecione a coluna onde será inserido o DDD extraído:",
        choices=df.columns.tolist()
    ).execute()

    # Inicializa contadores
    total_registros = len(df)
    registros_validos = 0
    registros_invalidos = 0

    # Processa cada linha e separa o DDD do número
    def process_phone(value):
        nonlocal registros_validos, registros_invalidos
        if pd.isna(value):
            registros_invalidos += 1
            return None, None

        value = str(value).strip()
        if len(value) == 11 and value.isdigit():
            registros_validos += 1
            return value[:2], value[2:]
        else:
            registros_invalidos += 1
            return None, None

    print("\n[cyan]Processando números...[/cyan]")

    df[ddd_column], df[phone_column] = zip(*df[phone_column].apply(process_phone))

    # Exibe resumo da operação
    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Registros totais:[/white]    {total_registros:,}")
    print(f"[white]► Registros válidos:[/white]   {registros_validos:,}")
    print(f"[white]► Registros inválidos:[/white] {registros_invalidos:,}")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo atualizado:"
    ).execute()

    output_file = os.path.join(output_dir, f"extracted_number_ddd_{os.path.basename(file_path)}")

    try:
        df.to_excel(output_file, index=False)
        print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[bold red]\n")

def whitelist_blacklist_removal_num():
    """
    Remove (troca por '0') os números de telefone do arquivo base (CPF + colunas de telefone)
    que aparecem em um segundo arquivo de blacklist (CPF + telefone_incorreto),
    convertendo sempre os arquivos Excel (.xlsx) para CSV,
    e gerando SEMPRE um arquivo final em CSV.

    Fluxo resumido:
      1) Recebe ARQUIVO BASE (pode ser .xlsx ou .csv).
         - Se .xlsx, converte para CSV temporário e trabalha com ele.
         - Pergunta coluna de CPF e colunas de telefone.
      2) Recebe ARQUIVO BLACKLIST (pode ser .xlsx ou .csv).
         - Se .xlsx, converte para CSV temporário.
         - Pergunta coluna de CPF e coluna de telefone incorreto.
      3) Para cada (CPF, telefone_incorreto) no arquivo de blacklist,
         se o telefone estiver em alguma coluna do base, troca por '0'.
      4) Gera um arquivo final SEMPRE em CSV, com prefixo 'tel_incorretos_removidos_'.
    """

    import os
    import pandas as pd
    from InquirerPy import inquirer
    from rich.console import Console
    console = Console()
    from pathlib import Path
    import uuid

    console.print("\n[bold yellow]╔══ Remoção de Telefones Incorretos por CPF (Saída CSV) ══╗[/bold yellow]\n")

    # --------------------- Função para converter XLSX -> CSV --------------------- #
    def convert_xlsx_to_csv(xlsx_path, output_dir=None):
        """
        Converte um arquivo XLSX para um CSV temporário usando sep=';'.
        Retorna o caminho do CSV gerado.
        Se output_dir não for informado, gera no mesmo diretório do xlsx.
        """
        if output_dir is None:
            output_dir = os.path.dirname(xlsx_path)

        df = pd.read_excel(xlsx_path, engine="openpyxl", dtype=str)
        temp_name = f"{Path(xlsx_path).stem}_temp_{uuid.uuid4().hex[:6]}.csv"
        temp_path = os.path.join(output_dir, temp_name)
        df.to_csv(temp_path, index=False, sep=';', encoding='utf-8')
        return temp_path

    # --------------------- Função auxiliar de fallback p/ ler CSV --------------------- #
    def load_csv_fallback(csv_path):
        """
        Tenta ler CSV com sep=';' e UTF-8 → se falhar, sep=';' e latin-1
        → se falhar, sep=',' e UTF-8 → se falhar, ',' e latin-1.
        Retorna df com dtype=str e low_memory=False para evitar warnings.
        """
        # 1) tenta ; + utf-8
        try:
            try:
                return pd.read_csv(csv_path, sep=';', encoding='utf-8', dtype=str, low_memory=False)
            except UnicodeDecodeError:
                return pd.read_csv(csv_path, sep=';', encoding='latin-1', dtype=str, low_memory=False)
        except:
            # 2) tenta , + utf-8
            try:
                try:
                    return pd.read_csv(csv_path, sep=',', encoding='utf-8', dtype=str, low_memory=False)
                except UnicodeDecodeError:
                    return pd.read_csv(csv_path, sep=',', encoding='latin-1', dtype=str, low_memory=False)
            except Exception as e:
                raise e

    # --------------------- Passo 1: Carrega o ARQUIVO BASE --------------------- #
    base_file_path = inquirer.text(
        message="Digite o caminho do ARQUIVO BASE (XLSX ou CSV):"
    ).execute()

    if not os.path.isfile(base_file_path):
        console.print(f"[bold red]✗ O caminho '{base_file_path}' não é um arquivo válido![bold red]\n")
        return

    # Se for XLSX, converte para CSV temporário
    if base_file_path.lower().endswith(".xlsx"):
        console.print("[cyan]Convertendo arquivo base de XLSX para CSV temporário...[/cyan]")
        try:
            base_csv_path = convert_xlsx_to_csv(base_file_path)
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao converter XLSX para CSV: {e}[bold red]\n")
            return
    elif base_file_path.lower().endswith(".csv"):
        base_csv_path = base_file_path
    else:
        console.print("[bold red]✗ Formato de arquivo base não suportado (use .xlsx ou .csv)![bold red]")
        return

    # Tenta carregar base como CSV (fallback)
    try:
        base_df = load_csv_fallback(base_csv_path)
        if base_df.empty:
            console.print("[bold red]✗ O arquivo base está vazio ou não possui dados válidos.[bold red]\n")
            return
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao carregar o arquivo base como CSV: {e}[bold red]\n")
        return

    # --------------------- Escolhe colunas no base --------------------- #
    cpf_base_col = inquirer.select(
        message="Selecione a coluna de CPF no arquivo base:",
        choices=base_df.columns.tolist()
    ).execute()

    # Pode haver várias colunas de telefone
    phone_cols = []
    while True:
        remaining = [c for c in base_df.columns if c not in phone_cols and c != cpf_base_col]
        if not remaining:
            break

        question = inquirer.confirm(
            message="Deseja selecionar mais uma coluna de telefone no arquivo base?",
            default=True
        ).execute()

        if not question and not phone_cols:
            console.print("[bold red]✗ É preciso selecionar ao menos uma coluna de telefone![bold red]")
            return
        if not question:
            break

        chosen_phone = inquirer.select(
            message="Selecione a coluna de telefone:",
            choices=remaining
        ).execute()
        phone_cols.append(chosen_phone)

    if not phone_cols:
        console.print("[bold red]✗ Nenhuma coluna de telefone foi selecionada, encerrando...[bold red]")
        return

    console.print("\n[cyan]Exibindo exemplo de valor em cada coluna de telefone (se houver dados)...[/cyan]")
    for col_ in phone_cols:
        example_val = None
        for _, val in base_df[col_].items():
            if pd.notna(val) and val.strip():
                example_val = val.strip()
                break
        if example_val:
            console.print(f" - [white]{col_}[/white]: [cyan]{example_val}[/cyan]")
        else:
            console.print(f" - [white]{col_}[/white]: [bold yellow]Nenhum valor preenchido[/bold yellow]")

    # --------------------- Passo 2: Carrega o ARQUIVO BLACKLIST --------------------- #
    blacklist_file_path = inquirer.text(
        message="Digite o caminho do arquivo de BLACKLIST (XLSX ou CSV):"
    ).execute()

    if not os.path.isfile(blacklist_file_path):
        console.print(f"[bold red]✗ O caminho '{blacklist_file_path}' não é um arquivo válido![bold red]\n")
        return

    # Se for XLSX, converte para CSV temporário
    if blacklist_file_path.lower().endswith(".xlsx"):
        console.print("[cyan]Convertendo arquivo blacklist de XLSX para CSV temporário...[/cyan]")
        try:
            black_csv_path = convert_xlsx_to_csv(blacklist_file_path)
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao converter XLSX para CSV: {e}[bold red]\n")
            return
    elif blacklist_file_path.lower().endswith(".csv"):
        black_csv_path = blacklist_file_path
    else:
        console.print("[bold red]✗ Formato de arquivo blacklist não suportado (use .xlsx ou .csv)![bold red]")
        return

    # Tenta carregar blacklist como CSV (fallback)
    try:
        black_df = load_csv_fallback(black_csv_path)
        if black_df.empty:
            console.print("[bold red]✗ O arquivo de blacklist está vazio ou não possui dados válidos.[bold red]\n")
            return
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao carregar o arquivo de blacklist como CSV: {e}[bold red]\n")
        return

    # Escolhe colunas
    cpf_black_col = inquirer.select(
        message="Selecione a coluna de CPF no arquivo de blacklist:",
        choices=black_df.columns.tolist()
    ).execute()

    phone_black_col = inquirer.select(
        message="Selecione a coluna de TELEFONE incorreto no arquivo de blacklist:",
        choices=[c for c in black_df.columns if c != cpf_black_col]
    ).execute()

    # --------------------- 3) Monta dict CPF -> set(telefones incorretos) --------------------- #
    console.print("\n[cyan]Agrupando telefones incorretos por CPF...[/cyan]")
    from collections import defaultdict
    black_dict = defaultdict(set)

    for idx, row in black_df.iterrows():
        c = str(row[cpf_black_col]).strip()
        p = str(row[phone_black_col]).strip()
        if c and p:
            black_dict[c].add(p)

    console.print(f"[white]Total de CPFs na blacklist:[/white] {len(black_dict):,}")

    # --------------------- 4) Para cada linha do base, se (cpf, phone) -> '0' --------------------- #
    console.print("\n[cyan]Removendo telefones incorretos no arquivo base...[/cyan]")

    total_rows = len(base_df)
    replaced_count = 0

    for idx in range(total_rows):
        cpf_val = str(base_df.at[idx, cpf_base_col]).strip()
        if cpf_val in black_dict:
            phones_to_remove = black_dict[cpf_val]
            # Checa cada coluna de telefone
            for pc in phone_cols:
                val = base_df.at[idx, pc]
                if pd.notna(val):
                    val_str = str(val).strip()
                    if val_str in phones_to_remove:
                        base_df.at[idx, pc] = "0"
                        replaced_count += 1

    # --------------------- 5) Pergunta onde salvar e SALVA SEMPRE EM CSV --------------------- #
    console.print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    console.print(f"[white]► Total de linhas no arquivo base:[/white] {total_rows:,}")
    console.print(f"[white]► Telefones substituídos por '0':[/white] {replaced_count:,}")

    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo final (CSV):"
    ).execute()

    if not os.path.isdir(output_dir):
        console.print(f"[bold red]✗ O caminho '{output_dir}' não é uma pasta válida![bold red]\n")
        return

    final_file = os.path.join(output_dir, f"tel_incorretos_removidos_{Path(base_file_path).stem}.csv")

    console.print("\n[cyan]Salvando arquivo final em CSV...[/cyan]")
    try:
        base_df.to_csv(final_file, index=False, sep=';', encoding='utf-8')
        console.print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        console.print(f"[dim]📁 Arquivo final salvo em CSV: {final_file}[dim]\n")
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao salvar o arquivo final em CSV: {e}[bold red]\n")


def whitelist_blacklist_removal_cpf():
    """
    Remove linhas do arquivo base que possuem CPFs contidos no arquivo de blacklist.
    Suporta arquivos XLSX ou CSV, sempre carregando e salvando como string (dtype=str).
    Mantém o mesmo formato de saída (XLSX ou CSV) do arquivo base.
    """
    import os
    import pandas as pd
    from InquirerPy import inquirer
    from pathlib import Path
    from rich.progress import track

    print("\n[bold yellow]╔══ Remoção de Linhas com CPFs na Blacklist ══╗[/bold yellow]\n")

    # Função auxiliar para carregar XLSX ou CSV como string
    def load_file_generic(file_path):
        if file_path.lower().endswith(".xlsx"):
            return pd.read_excel(file_path, engine="openpyxl", dtype=str)
        elif file_path.lower().endswith(".csv"):
            try:
                return pd.read_csv(file_path, sep=';', dtype=str)
            except:
                return pd.read_csv(file_path, sep=',', dtype=str)
        else:
            raise ValueError("Formato de arquivo não suportado! Use .xlsx ou .csv.")

    # 1) Carrega o arquivo base
    base_file_path = inquirer.text(
        message="Digite o caminho do arquivo base (XLSX ou CSV):"
    ).execute()

    if not os.path.isfile(base_file_path):
        print(f"[bold red]✗ O caminho '{base_file_path}' não é um arquivo válido![bold red]\n")
        return

    try:
        base_df = load_file_generic(base_file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo base: {e}[bold red]\n")
        return

    if base_df.empty:
        print("[bold red]✗ O arquivo base está vazio ou não possui dados válidos.[bold red]\n")
        return

    # Seleciona a coluna de CPF no arquivo base
    base_cpf_col = inquirer.select(
        message="Selecione a coluna de CPF no arquivo base:",
        choices=base_df.columns.tolist()
    ).execute()

    # 2) Carrega o arquivo de blacklist
    blacklist_file_path = inquirer.text(
        message="Digite o caminho do arquivo de blacklist (XLSX ou CSV):"
    ).execute()

    if not os.path.isfile(blacklist_file_path):
        print(f"[bold red]✗ O caminho '{blacklist_file_path}' não é um arquivo válido![bold red]\n")
        return

    try:
        blacklist_df = load_file_generic(blacklist_file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo de blacklist: {e}[bold red]\n")
        return

    if blacklist_df.empty:
        print("[bold red]✗ O arquivo de blacklist está vazio ou não possui dados válidos.[bold red]\n")
        return

    # Seleciona a coluna de CPF no arquivo de blacklist
    blacklist_cpf_col = inquirer.select(
        message="Selecione a coluna de CPF no arquivo de blacklist:",
        choices=blacklist_df.columns.tolist()
    ).execute()

    print("\n[cyan]Removendo do arquivo base os CPFs presentes na blacklist...[/cyan]")

    # 3) Cria um conjunto com os CPFs da blacklist (padronizando tudo como string sem espaços)
    black_set = set(blacklist_df[blacklist_cpf_col].astype(str).str.strip())

    initial_row_count = len(base_df)

    # 4) Marca quem NÃO está na blacklist como VALIDO
    base_df["VALIDO"] = ~base_df[base_cpf_col].astype(str).str.strip().isin(black_set)

    valid_df = base_df[base_df["VALIDO"]].drop(columns=["VALIDO"]).copy()    # Linhas válidas
    invalid_df = base_df[~base_df["VALIDO"]].drop(columns=["VALIDO"]).copy() # Linhas removidas

    linhas_removidas = len(invalid_df)
    linhas_restantes = len(valid_df)

    # Exibe resumo da operação
    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Total de linhas no arquivo base:[/white] {initial_row_count:,}")
    print(f"[white]► Linhas removidas (CPF na blacklist):[/white] {linhas_removidas:,}")
    print(f"[white]► Linhas restantes:[/white] {linhas_restantes:,}")

    # 5) Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar os arquivos filtrados:"
    ).execute()

    if not os.path.isdir(output_dir):
        print(f"[bold red]✗ O caminho '{output_dir}' não é uma pasta válida![bold red]\n")
        return

    # 6) Define nomes dos arquivos de saída (mantendo extensão do base)
    base_stem = Path(base_file_path).stem
    ext = Path(base_file_path).suffix.lower()

    valid_output_file = os.path.join(output_dir, f"whitelist_{base_stem}{ext}")
    invalid_output_file = os.path.join(output_dir, f"blacklist_{base_stem}{ext}")

    # 7) Salva no mesmo formato do base
    def save_in_same_format(df_local, path_out):
        if ext == ".xlsx":
            df_local.to_excel(path_out, index=False, engine="openpyxl")
        elif ext == ".csv":
            df_local.to_csv(path_out, sep=';', index=False, encoding='utf-8')
        else:
            raise ValueError("Formato de arquivo não suportado!")

    try:
        save_in_same_format(valid_df, valid_output_file)
        save_in_same_format(invalid_df, invalid_output_file)
        print(f"\n[bold green]✓ Arquivos salvos com sucesso![bold green]")
        print(f"[dim]📁 Arquivo com CPFs válidos salvo em: {valid_output_file}[dim]")
        print(f"[dim]📁 Arquivo com CPFs removidos salvo em: {invalid_output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar os arquivos: {e}[bold red]\n")


def filter_num_nine():
    """
    Formata números de celular adicionando o dígito '9' após o DDD em números de 12 dígitos.
    Remove linhas com números que não possuem 12 ou 13 dígitos.
    """
    print("\n[bold yellow]╔══ Formatação de Números com '9' ══╗[/bold yellow]\n")
    print("[bold cyan]Observação: Certifique-se de que os números estejam no formato correto, começando com '55' seguido do DDD e número.[/bold cyan]\n")

    # Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[bold red]\n")
        return

    # Seleciona a coluna de números
    number_column = inquirer.select(
        message="Selecione a coluna de números de celular:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Formatando números...[/cyan]")

    # Função para verificar e corrigir números
    def format_number(value):
        try:
            value = str(value).strip()
            if len(value) == 12:  # Número com 12 dígitos (faltando o 9)
                return value[:4] + "9" + value[4:]
            elif len(value) == 13:  # Número já no formato correto
                return value
            return None  # Número inválido
        except Exception:
            return None

    # Aplica a formatação e filtra números inválidos
    initial_row_count = len(df)
    df[number_column] = df[number_column].apply(format_number)

    df_invalid = df[df[number_column].isna()].copy()  # Números inválidos
    df = df.dropna(subset=[number_column]).copy()     # Números válidos

    # Resumo da formatação
    linhas_invalidas = len(df_invalid)
    linhas_validas = len(df)

    print("\n[bold green]╔══ Resumo da Formatação ══╗[/bold green]")
    print(f"[white]► Linhas originais:[/white] {initial_row_count:,}")
    print(f"[white]► Números formatados:[/white] {linhas_validas:,}")
    print(f"[white]► Linhas removidas (números inválidos):[/white] {linhas_invalidas:,}")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar os arquivos formatados:"
    ).execute()

    # Adiciona prefixo aos nomes dos arquivos de saída
    valid_output_file = os.path.join(output_dir, f"filtrer_num_nine_validos_{os.path.basename(file_path)}")
    invalid_output_file = os.path.join(output_dir, f"filtrer_num_nine_invalidos_{os.path.basename(file_path)}")

    # Salva os arquivos
    try:
        df.to_excel(valid_output_file, index=False)
        df_invalid.to_excel(invalid_output_file, index=False)
        print(f"\n[bold green]✓ Arquivos salvos com sucesso![bold green]")
        print(f"[dim]📁 Arquivo com números válidos salvo em: {valid_output_file}[dim]")
        print(f"[dim]📁 Arquivo com números inválidos salvo em: {invalid_output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar os arquivos: {e}[bold red]\n")

def filter_back_age():
    """
    Valida banco, agência e conta e remove linhas que atendem aos critérios de remoção:
    - Contém letras
    - Contém espaços
    - Está vazio
    - É igual a zero
    """
    print("\n[bold yellow]╔══ Iniciando Validação de Banco, Agência e Conta ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[bold red]\n")
        return

    # Seleciona as colunas necessárias
    banco_column = inquirer.select(
        message="Selecione a coluna de Banco:",
        choices=df.columns.tolist()
    ).execute()

    agencia_column = inquirer.select(
        message="Selecione a coluna de Agência:",
        choices=df.columns.tolist()
    ).execute()

    conta_column = inquirer.select(
        message="Selecione a coluna de Conta:",
        choices=df.columns.tolist()
    ).execute()

    print("\n[cyan]Validando dados...[/cyan]")

    # Função de validação
    def is_invalid(value):
        """Verifica se o valor contém letras, espaços, está vazio ou é igual a zero."""
        if pd.isna(value) or str(value).strip() == "" or str(value).strip() == "0":
            return True
        if any(char.isalpha() for char in str(value)) or " " in str(value):
            return True
        return False

    # Aplica a validação e filtra as linhas inválidas
    initial_row_count = len(df)
    df["VALIDO"] = ~(
        df[banco_column].apply(is_invalid) |
        df[agencia_column].apply(is_invalid) |
        df[conta_column].apply(is_invalid)
    )

    df_invalid = df[~df["VALIDO"]].copy()  # Linhas inválidas
    df = df[df["VALIDO"]].copy()           # Linhas válidas

    # Remove a coluna auxiliar "VALIDO"
    df.drop(columns=["VALIDO"], inplace=True)
    df_invalid.drop(columns=["VALIDO"], inplace=True)

    # Resumo da validação
    linhas_invalidas = len(df_invalid)
    linhas_validas = len(df)

    print("\n[bold green]╔══ Resumo da Validação ══╗[/bold green]")
    print(f"[white]► Linhas originais:[/white] {initial_row_count:,}")
    print(f"[white]► Linhas válidas:[/white]   {linhas_validas:,}")
    print(f"[white]► Linhas inválidas:[/white] {linhas_invalidas:,}")

    # Pergunta o diretório para salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar os arquivos filtrados:"
    ).execute()

    # Adiciona prefixo aos nomes dos arquivos de saída
    valid_output_file = os.path.join(output_dir, f"filter_back_age_validos_{os.path.basename(file_path)}")
    invalid_output_file = os.path.join(output_dir, f"filter_back_age_invalidos_{os.path.basename(file_path)}")

    # Salva os arquivos
    try:
        df.to_excel(valid_output_file, index=False)
        df_invalid.to_excel(invalid_output_file, index=False)
        print(f"\n[bold green]✓ Arquivos salvos com sucesso![bold green]")
        print(f"[dim]📁 Arquivo com dados válidos salvo em: {valid_output_file}[dim]")
        print(f"[dim]📁 Arquivo com dados inválidos salvo em: {invalid_output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar os arquivos: {e}[bold red]\n")

def merge_ddd_number():
    """
    Une as colunas DDD e Número em uma nova coluna.
    - DDD deve ter 2 dígitos.
    - Número deve ter 9 dígitos.
    - Linhas fora desses critérios são excluídas.
    """
    print("\n[bold yellow]╔══ Unificação de Colunas DDD + Número ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        # Lê apenas o cabeçalho do arquivo para selecionar colunas
        columns = pd.read_excel(file_path, nrows=0).columns.tolist()
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o cabeçalho do arquivo: {e}[bold red]\n")
        return

    # Seleciona as colunas necessárias
    ddd_column = inquirer.select(
        message="Selecione a coluna do DDD:",
        choices=columns
    ).execute()

    number_column = inquirer.select(
        message="Selecione a coluna do número:",
        choices=columns
    ).execute()

    print("\n[cyan]Unificando colunas DDD e Número...[/cyan]")

    try:
        # Lê o arquivo completo
        df = pd.read_excel(file_path)

        # Filtros de validação
        def is_valid_ddd(value):
            return isinstance(value, str) and value.isdigit() and len(value) == 2

        def is_valid_number(value):
            return isinstance(value, str) and value.isdigit() and len(value) == 9

        # Aplica filtros de validação
        df["VALIDO"] = df[ddd_column].astype(str).apply(is_valid_ddd) & \
                       df[number_column].astype(str).apply(is_valid_number)

        df_valid = df[df["VALIDO"]].copy()  # Linhas válidas
        df_invalid = df[~df["VALIDO"]].copy()  # Linhas inválidas

        # Remove a coluna auxiliar "VALIDO"
        df_valid.drop(columns=["VALIDO"], inplace=True)
        df_invalid.drop(columns=["VALIDO"], inplace=True)

        # Cria a nova coluna unificada para linhas válidas
        df_valid["DDD+Número"] = df_valid[ddd_column].astype(str).str.strip() + \
                                 df_valid[number_column].astype(str).str.strip()

    except Exception as e:
        print(f"[bold red]✗ Erro ao processar o arquivo: {e}[bold red]\n")
        return

    # Pergunta o diretório para salvar os arquivos
    output_dir = inquirer.text(
        message="Digite o caminho para salvar os arquivos formatados:"
    ).execute()

    # Caminhos para os arquivos de saída
    valid_output_file = os.path.join(output_dir, f"merged_ddd_number_validos_{os.path.basename(file_path)}")
    invalid_output_file = os.path.join(output_dir, f"merged_ddd_number_invalidos_{os.path.basename(file_path)}")

    # Salva os arquivos
    try:
        df_valid.to_excel(valid_output_file, index=False)
        df_invalid.to_excel(invalid_output_file, index=False)
        print(f"\n[bold green]✓ Arquivo salvo com sucesso![bold green]")
        print(f"[dim]📁 Arquivo com números válidos salvo em: {valid_output_file}[dim]")
        print(f"[dim]📁 Arquivo com números inválidos salvo em: {invalid_output_file}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar os arquivos: {e}[bold red]\n")

def format_numbers_with_prefix():
    """
    Adiciona o prefixo '55' a números que tenham exatamente 11 dígitos
    em uma ou mais colunas selecionadas. Mantém todas as linhas e
    só altera o valor da(s) coluna(s) escolhida(s).
    """

    import os
    import pandas as pd
    from InquirerPy import inquirer
    from pathlib import Path
    from rich.progress import track

    print("\n[bold yellow]╔══ Iniciando Adição de Prefixo '55' a Números de 11 Dígitos ══╗[/bold yellow]\n")

    # 1) Recebe caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo (XLSX ou CSV):"
    ).execute()

    if not os.path.isfile(file_path):
        print(f"[bold red]✗ O caminho '{file_path}' não é um arquivo válido![bold red]")
        return

    # Função auxiliar para carregar XLSX ou CSV
    def load_file_generic(file_path):
        if file_path.lower().endswith(".xlsx"):
            return pd.read_excel(file_path, engine="openpyxl", dtype=str)
        elif file_path.lower().endswith(".csv"):
            # Tenta primeiro separador ;
            try:
                return pd.read_csv(file_path, sep=';', dtype=str)
            except:
                return pd.read_csv(file_path, sep=',', dtype=str)
        else:
            raise ValueError("Formato de arquivo não suportado! Use .xlsx ou .csv.")

    # Carrega o DataFrame (tudo como string)
    try:
        df = load_file_generic(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar arquivo: {e}[/bold red]")
        return

    if df.empty:
        print("[bold red]✗ O arquivo está vazio ou não possui dados válidos.[bold red]")
        return

    # 2) Usuário seleciona colunas (múltiplas)
    print("\n[cyan]Selecione as colunas onde deseja adicionar o prefixo '55' (valores com 11 dígitos)...[/cyan]")
    selected_columns = []
    while True:
        remaining_cols = [c for c in df.columns if c not in selected_columns]
        if not remaining_cols:
            break

        want_more = inquirer.confirm(
            message="Deseja selecionar mais uma coluna?",
            default=True
        ).execute()

        if not want_more and not selected_columns:
            print("[bold red]✗ É preciso selecionar ao menos uma coluna para continuar.[bold red]")
            return
        if not want_more:
            break

        chosen_col = inquirer.select(
            message="Selecione a coluna de números:",
            choices=remaining_cols
        ).execute()
        selected_columns.append(chosen_col)

    if not selected_columns:
        print("[bold yellow]Nenhuma coluna foi selecionada. Encerrando...[bold yellow]")
        return

    # 3) Para cada coluna, exibimos um exemplo não vazio para confirmar
    for col in selected_columns:
        example_val = None
        for idx, val in df[col].items():
            if pd.notna(val) and val.strip():
                example_val = val.strip()
                break

        if example_val:
            print(f"\n[cyan]Exemplo de valor na coluna '{col}':[/cyan] {example_val}")
            confirm_col = inquirer.confirm(
                message="Confirmar que esta coluna contém números de telefone?",
                default=True
            ).execute()
            if not confirm_col:
                print(f"[bold red]Removendo coluna '{col}' da lista de formatações.[bold red]")
                selected_columns.remove(col)
        else:
            print(f"[bold yellow]A coluna '{col}' não possui valores preenchidos para exemplificar.[bold yellow]")

    if not selected_columns:
        print("[bold yellow]Nenhuma coluna confirmada. Encerrando...[bold yellow]")
        return

    # 4) Aplica a formatação (adicionando '55' a quem tiver 11 dígitos)
    def add_55_prefix(value):
        if pd.isna(value):
            return value
        v = str(value).strip()
        # Se for exatamente 11 dígitos
        if len(v) == 11 and v.isdigit():
            return '55' + v
        return v

    total_rows = len(df)
    changed_count = 0

    for col in selected_columns:
        for idx in track(df.index, description=f"[cyan]Formatando coluna '{col}'...[/cyan]"):
            old_val = df.at[idx, col]
            new_val = add_55_prefix(old_val)
            if new_val != old_val:
                df.at[idx, col] = new_val
                changed_count += 1

    # 5) Pergunta onde salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo formatado:"
    ).execute()

    if not os.path.isdir(output_dir):
        print(f"[bold red]✗ O caminho '{output_dir}' não é uma pasta válida![bold red]")
        return

    # Monta nome de saída (mantendo formato original)
    base_stem = Path(file_path).stem
    ext = Path(file_path).suffix
    output_name = f"num_format_{base_stem}{ext}"
    output_path = os.path.join(output_dir, output_name)

    try:
        if file_path.lower().endswith(".xlsx"):
            df.to_excel(output_path, index=False, engine="openpyxl")
        else:
            df.to_csv(output_path, sep=';', index=False, encoding='utf-8')
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[/bold red]")
        return

    # 6) Exibe resumo
    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Total de linhas no arquivo:[/white] {total_rows:,}")
    print(f"[white]► Colunas de telefone formatadas:[/white] {', '.join(selected_columns)}")
    print(f"[white]► Números convertidos para '55' + 11 dígitos:[/white] {changed_count:,}")
    print(f"[dim]📁 Arquivo salvo em: {output_path}[/dim]\n")


def validar_numeros_celular():
    from rich.console import Console
    from rich.progress import Progress
    console = Console()

    """
    Valida números de celular em uma coluna específica.
    - Números válidos: exatamente 11 dígitos.
    - Separa números válidos e inválidos em planilhas diferentes.
    - Gera arquivos contendo apenas CPFs com números válidos e inválidos.
    """
    console.print("\n[bold yellow]╔══ Validação de Números de Celular ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo Excel
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        # Lê apenas o cabeçalho do arquivo para selecionar colunas
        columns = pd.read_excel(file_path, nrows=0).columns.tolist()
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao carregar o cabeçalho do arquivo: {e}[bold red]\n")
        return

    # Seleciona a coluna de números de celular
    celular_column = inquirer.select(
        message="Selecione a coluna de números de celular:",
        choices=columns
    ).execute()

    # Seleciona a coluna de CPF
    cpf_column = inquirer.select(
        message="Selecione a coluna de CPF:",
        choices=columns
    ).execute()

    try:
        # Lê o arquivo Excel e mantém apenas as colunas selecionadas
        df = pd.read_excel(file_path, usecols=[cpf_column, celular_column], dtype=str)

        # Converte o DataFrame para CSV apenas com as colunas selecionadas
        csv_file_path = file_path.replace(".xlsx", "_cpf_celular.csv")
        df.to_csv(csv_file_path, index=False, sep=';', encoding='utf-8')
        console.print(f"[cyan]✓ Arquivo convertido para CSV: {csv_file_path}[cyan]\n")
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[bold red]\n")
        return

    console.print("\n[cyan]Validando números de celular...[/cyan]")

    try:
        # Lê o arquivo CSV completo
        df = pd.read_csv(csv_file_path, sep=';', dtype=str)

        # Função de validação para números de celular
        def is_valid_number(value):
            if pd.isna(value):
                return False
            value = str(value).strip()
            return value.isdigit() and len(value) == 11

        # Aplica a validação com barra de progresso
        with Progress() as progress:
            task = progress.add_task("Validando números", total=len(df))
            df["VALIDO"] = df[celular_column].apply(lambda x: is_valid_number(x))
            progress.update(task, advance=len(df))

        # Separa números válidos e inválidos, mantendo apenas a coluna CPF
        df_validos = df[df["VALIDO"] == True][[cpf_column]].copy()
        df_invalidos = df[df["VALIDO"] == False][[cpf_column]].copy()

        # Resumo da validação
        linhas_validas = len(df_validos)
        linhas_invalidas = len(df_invalidos)

        console.print("\n[bold green]╔══ Resumo da Validação ══╗[/bold green]")
        console.print(f"[white]► CPFs com números válidos:[/white] {linhas_validas:,}")
        console.print(f"[white]► CPFs com números inválidos:[/white] {linhas_invalidas:,}")

        # Pergunta o diretório para salvar os arquivos
        output_dir = inquirer.text(
            message="Digite o caminho para salvar os arquivos filtrados:"
        ).execute()

        # Caminhos para os arquivos de saída
        valid_output_file = os.path.join(output_dir, f"Valido_{os.path.basename(csv_file_path)}")
        invalid_output_file = os.path.join(output_dir, f"Invalido_{os.path.basename(csv_file_path)}")

        # Salva os arquivos com barra de progresso
        with Progress() as progress:
            task_save = progress.add_task("Salvando arquivos", total=2)

            try:
                df_validos.to_csv(valid_output_file, index=False, sep=';', encoding='utf-8')
                progress.update(task_save, advance=1)
                df_invalidos.to_csv(invalid_output_file, index=False, sep=';', encoding='utf-8')
                progress.update(task_save, advance=1)

                console.print(f"\n[bold green]✓ Arquivos salvos com sucesso![bold green]")
                console.print(f"[dim]📁 Arquivo com números válidos salvo em: {valid_output_file}[dim]")
                console.print(f"[dim]📁 Arquivo com números inválidos salvo em: {invalid_output_file}[dim]\n")
            except Exception as e:
                console.print(f"[bold red]✗ Erro ao salvar os arquivos: {e}[bold red]\n")
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao processar o arquivo: {e}[bold red]\n")



def formatar_numeros_para_11_digitos():
    """
    Formata números de celular para 11 dígitos.
    - Números com 12 dígitos: remove o último dígito (zero extra no final).
    - O cabeçalho do arquivo é lido diretamente do XLSX para identificar as colunas.
    - O CSV é usado para manipulação dos dados e o arquivo final é salvo em XLSX.
    """
    print("\n[bold yellow]╔══ Formatação de Números para 11 Dígitos ══╗[/bold yellow]\n")

    # Recebe o caminho do arquivo Excel
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel (.xlsx):"
    ).execute()

    try:
        # Lê apenas a primeira linha para obter o cabeçalho
        df_header = pd.read_excel(file_path, nrows=1, engine="openpyxl")
        header = df_header.columns.tolist()
        if not header:
            print("[bold red]✗ O arquivo não possui cabeçalho válido.[bold red]\n")
            return
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o cabeçalho do arquivo: {e}[bold red]\n")
        return

    # Mapeia as colunas para suas posições (exemplo: A, B, C, etc.)
    column_positions = [f"{chr(65 + i)}" for i in range(len(header))]
    choices = [f"{col_positions} - {header[i]}" for i, col_positions in enumerate(column_positions)]

    # Usuário seleciona a coluna com base na posição
    selected_column_choice = inquirer.select(
        message="Selecione a coluna de números de celular:",
        choices=choices
    ).execute()

    # Extrai o índice da coluna selecionada
    column_index = choices.index(selected_column_choice)
    column_name = header[column_index]

    try:
        # Lê apenas a segunda linha do arquivo para validar o conteúdo
        df_sample = pd.read_excel(file_path, nrows=2, engine="openpyxl")
        second_row_value = df_sample.iloc[1, column_index]
        print(f"\n[cyan]Conteúdo da célula A2 (coluna '{column_name}'): {second_row_value}[cyan]\n")

        confirm = inquirer.confirm(
            message=f"Essa é a coluna correta para '{column_name}'?",
            default=True
        ).execute()

        if not confirm:
            print("[bold red]✗ Operação cancelada pelo usuário.[bold red]\n")
            return

    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar a segunda linha do arquivo: {e}[bold red]\n")
        return

    print("\n[cyan]Convertendo arquivo para CSV para otimizar a manipulação...[/cyan]")

    try:
        # Converte o arquivo completo para CSV
        csv_file_path = file_path.replace(".xlsx", ".csv")
        df = pd.read_excel(file_path, engine="openpyxl")
        df.to_csv(csv_file_path, index=False, encoding='utf-8')
        print(f"[cyan]✓ Arquivo convertido para CSV: {csv_file_path}[cyan]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao converter o arquivo para CSV: {e}[bold red]\n")
        return

    print("\n[cyan]Formatando números de celular...[/cyan]")

    try:
        # Lê o CSV completo
        df = pd.read_csv(csv_file_path, dtype=str)

        # Função para formatar números
        def format_number(value):
            value = str(value).strip()
            if value.isdigit() and len(value) == 12:
                return value[:-1]  # Remove o último dígito
            return value  # Retorna o valor original

        # Aplica a formatação na coluna selecionada
        df[column_name] = df[column_name].apply(format_number)

        # Pergunta o diretório para salvar o arquivo formatado
        output_dir = inquirer.text(
            message="Digite o caminho para salvar o arquivo formatado:"
        ).execute()

        # Caminho do arquivo de saída em CSV
        formatted_csv_path = os.path.join(output_dir, f"formatado_11_digitos_{os.path.basename(csv_file_path)}")

        # Salva o arquivo formatado como CSV
        df.to_csv(formatted_csv_path, index=False, encoding='utf-8')
        print(f"[cyan]✓ Arquivo formatado salvo como CSV: {formatted_csv_path}[cyan]\n")

        # Converte o CSV final para XLSX
        final_xlsx_path = formatted_csv_path.replace(".csv", ".xlsx")
        df.to_excel(final_xlsx_path, index=False)
        print(f"\n[bold green]✓ Arquivo final salvo como XLSX:[bold green]")
        print(f"[dim]📁 Arquivo salvo em: {final_xlsx_path}[dim]\n")

    except Exception as e:
        print(f"[bold red]✗ Erro ao processar o arquivo: {e}[bold red]\n")


def remover_duplicatas_cpfs():
    """
    Recebe um arquivo XLSX ou CSV, seleciona a coluna de CPF, normaliza e remove duplicatas.
    Mantém a primeira ocorrência de cada CPF, ignorando as linhas subsequentes duplicadas.
    Agora com fallback de encoding para CSV.
    """

    import os
    import pandas as pd
    from InquirerPy import inquirer
    from rich.console import Console
    console = Console()

    console.print("\n[bold yellow]╔══ Remoção de Duplicatas por CPF ══╗[/bold yellow]\n")

    def load_file_generic(file_path):
        """
        Carrega XLSX ou CSV (tentando ; depois ,) sempre como string (dtype=str).
        Se for CSV, tenta utf-8 primeiro. Se falhar, tenta latin-1.
        """
        if file_path.lower().endswith(".xlsx"):
            return pd.read_excel(file_path, engine="openpyxl", dtype=str)
        elif file_path.lower().endswith(".csv"):
            # Tentar com UTF-8
            try:
                # Primeiro ; depois ,
                try:
                    return pd.read_csv(file_path, sep=';', dtype=str, encoding='utf-8')
                except UnicodeDecodeError:
                    return pd.read_csv(file_path, sep=';', dtype=str, encoding='latin-1')
            except Exception:
                # Se ainda falhar, tentamos sep=','
                try:
                    return pd.read_csv(file_path, sep=',', dtype=str, encoding='utf-8')
                except UnicodeDecodeError:
                    return pd.read_csv(file_path, sep=',', dtype=str, encoding='latin-1')
        else:
            raise ValueError("Formato de arquivo não suportado. Use .xlsx ou .csv.")

    # 1) Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo (.xlsx ou .csv):"
    ).execute()

    if not os.path.isfile(file_path):
        console.print(f"[bold red]✗ O caminho '{file_path}' não é um arquivo válido![bold red]\n")
        return

    # 2) Tenta carregar
    try:
        df = load_file_generic(file_path)
        if df.empty:
            console.print("[bold red]✗ O arquivo está vazio ou não contém dados válidos.[bold red]\n")
            return
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[bold red]\n")
        return

    # 3) Seleciona a coluna de CPF
    cpf_column = inquirer.select(
        message="Selecione a coluna de CPF no arquivo:",
        choices=df.columns.tolist()
    ).execute()

    console.print("\n[cyan]Normalizando CPFs...[/cyan]")

    try:
        # Remove tudo que não for dígito e força 11 dígitos com zfill
        df[cpf_column] = (
            df[cpf_column]
            .astype(str)
            .str.replace(r'\D', '', regex=True)
            .str.zfill(11)
        )

        # Remove duplicatas mantendo a primeira ocorrência
        df_deduplicated = df.drop_duplicates(subset=[cpf_column], keep='first')

    except Exception as e:
        console.print(f"[bold red]✗ Erro ao normalizar ou remover duplicatas: {e}[bold red]\n")
        return

    # Resumo da operação
    total_linhas = len(df)
    total_linhas_unicas = len(df_deduplicated)
    duplicatas_removidas = total_linhas - total_linhas_unicas

    console.print("\n[bold green]╔══ Resumo da Remoção de Duplicatas ══╗[/bold green]")
    console.print(f"[white]► Total de linhas no arquivo original:[/white] {total_linhas:,}")
    console.print(f"[white]► Linhas únicas (sem duplicatas):[/white]      {total_linhas_unicas:,}")
    console.print(f"[white]► Duplicatas removidas:[/white]              {duplicatas_removidas:,}")

    # 4) Pergunta onde salvar o arquivo final
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo sem duplicatas:"
    ).execute()

    if not os.path.isdir(output_dir):
        console.print(f"[bold red]✗ O caminho '{output_dir}' não é uma pasta válida![bold red]\n")
        return

    # Define o caminho de saída
    base_name = os.path.basename(file_path)  # ex: "dados.xlsx"
    output_file = os.path.join(output_dir, f"sem_duplicatas_{base_name}")

    console.print("\n[cyan]Salvando arquivo final...[/cyan]")
    try:
        if file_path.lower().endswith(".xlsx"):
            df_deduplicated.to_excel(output_file, index=False, engine="openpyxl")
        else:
            # CSV, usaremos sep=';' e utf-8 ao salvar
            df_deduplicated.to_csv(output_file, index=False, sep=';', encoding='utf-8')
        console.print(f"\n[bold green]✓ Arquivo salvo com sucesso![bold green]")
        console.print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[bold red]\n")

def remover_duplicatas_phones():
    """
    Remove duplicatas com base em uma coluna de telefone.
    1) Carrega XLSX ou CSV como string (fallback de encoding).
    2) Usuário seleciona a coluna de telefone.
    3) Mostra a primeira linha não vazia como exemplo p/ confirmar.
    4) Remove duplicatas mantendo a primeira ocorrência.
    5) Exibe resumo e salva o resultado.
    """

    import os
    import pandas as pd
    from InquirerPy import inquirer
    from rich.console import Console
    console = Console()

    console.print("\n[bold yellow]╔══ Remoção de Duplicatas por Telefone ══╗[/bold yellow]\n")

    # --------------------- Função auxiliar p/ carregar XLSX ou CSV --------------------- #
    def load_file_generic(file_path):
        """
        Carrega XLSX ou CSV (tentando ; depois ,) sempre como string (dtype=str).
        Se for CSV, tenta utf-8 primeiro. Se der UnicodeDecodeError, tenta latin-1.
        """
        if file_path.lower().endswith(".xlsx"):
            return pd.read_excel(file_path, engine="openpyxl", dtype=str)
        elif file_path.lower().endswith(".csv"):
            # Tenta com UTF-8 + sep=';'
            try:
                try:
                    return pd.read_csv(file_path, sep=';', dtype=str, encoding='utf-8')
                except UnicodeDecodeError:
                    return pd.read_csv(file_path, sep=';', dtype=str, encoding='latin-1')
            except Exception:
                # Se ainda falhar, tentamos sep=','
                try:
                    try:
                        return pd.read_csv(file_path, sep=',', dtype=str, encoding='utf-8')
                    except UnicodeDecodeError:
                        return pd.read_csv(file_path, sep=',', dtype=str, encoding='latin-1')
                except Exception as e:
                    raise e
        else:
            raise ValueError("Formato de arquivo não suportado. Use .xlsx ou .csv.")

    # 1) Recebe o caminho do arquivo
    file_path = inquirer.text(
        message="Digite o caminho do arquivo (.xlsx ou .csv):"
    ).execute()

    if not os.path.isfile(file_path):
        console.print(f"[bold red]✗ O caminho '{file_path}' não é um arquivo válido![bold red]\n")
        return

    # 2) Carrega o arquivo
    try:
        df = load_file_generic(file_path)
        if df.empty or df.columns.empty:
            console.print("[bold red]✗ O arquivo está vazio ou não contém dados válidos.[bold red]\n")
            return
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[bold red]\n")
        return

    # 3) Usuário seleciona a coluna de telefone
    phone_col = inquirer.select(
        message="Selecione a coluna de telefone no arquivo:",
        choices=df.columns.tolist()
    ).execute()

    # Mostra a primeira linha não vazia como exemplo
    example_value = None
    for _, val in df[phone_col].items():
        if pd.notna(val) and val.strip():
            example_value = val.strip()
            break

    if example_value:
        console.print(f"\n[cyan]Exemplo de valor encontrado na coluna '{phone_col}':[/cyan] {example_value}")
        confirm_col = inquirer.confirm(
            message="Confirma que esta é realmente a coluna de telefone?",
            default=True
        ).execute()
        if not confirm_col:
            console.print("[bold red]Operação cancelada, coluna não confirmada como telefone.[bold red]\n")
            return
    else:
        console.print(f"[bold yellow]A coluna '{phone_col}' não possui valores preenchidos para exemplificar.[bold yellow]")

    console.print("\n[cyan]Removendo duplicatas com base na coluna selecionada...[/cyan]")

    try:
        # Converte a coluna em string e strip
        df[phone_col] = df[phone_col].astype(str).str.strip()

        # Remove duplicatas, mantendo a 1ª ocorrência
        df_deduplicated = df.drop_duplicates(subset=[phone_col], keep='first')

    except Exception as e:
        console.print(f"[bold red]✗ Erro ao remover duplicatas: {e}[bold red]\n")
        return

    total_linhas = len(df)
    total_unicas = len(df_deduplicated)
    removidas = total_linhas - total_unicas

    console.print("\n[bold green]╔══ Resumo da Remoção de Duplicatas ══╗[/bold green]")
    console.print(f"[white]► Total de linhas no arquivo original:[/white] {total_linhas:,}")
    console.print(f"[white]► Linhas únicas (sem duplicatas):[/white]      {total_unicas:,}")
    console.print(f"[white]► Duplicatas removidas:[/white]              {removidas:,}")

    # 4) Pergunta onde salvar o arquivo final
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo sem duplicatas:"
    ).execute()

    if not os.path.isdir(output_dir):
        console.print(f"[bold red]✗ O caminho '{output_dir}' não é uma pasta válida![bold red]\n")
        return

    # Define o caminho de saída
    base_name = os.path.basename(file_path)
    output_file = os.path.join(output_dir, f"sem_duplicatas_{base_name}")

    console.print("\n[cyan]Salvando arquivo final...[/cyan]")
    try:
        if file_path.lower().endswith(".xlsx"):
            df_deduplicated.to_excel(output_file, index=False, engine="openpyxl")
        else:
            df_deduplicated.to_csv(output_file, index=False, sep=';', encoding='utf-8')
        console.print(f"\n[bold green]✓ Arquivo salvo com sucesso![bold green]")
        console.print(f"[dim]📁 Arquivo salvo em: {output_file}[dim]\n")
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao salvar o arquivo: {e}[bold red]\n")
        return



def unify_data_multiple_search_by_cpf_csv():
    """
    Unifica dados de um arquivo base (XLSX ou CSV) e múltiplos arquivos de pesquisa,
    combinando por CPF, gerando SEMPRE arquivos finais em CSV.

    Fluxo:
      1) Recebe caminho do arquivo base e seleciona a coluna de CPF.
      2) Normaliza os CPFs p/ 11 dígitos.
      3) Pergunta se quer adicionar 1..N arquivos de pesquisa.
      4) Cada arquivo de pesquisa também XLSX ou CSV; ao carregar:
         - Seleciona a coluna de CPF.
         - Normaliza CPFs.
         - Constrói dict CPF->linha (primeira ocorrência).
         - Tenta casar esses CPFs com os ainda não encontrados.
      5) Gera 2 arquivos CSV no fim:
         - 'cpf_corresp_{NOME_BASE}.csv': CPFs encontrados + colunas do arquivo de pesquisa
         - 'semnada_{NOME_BASE}.csv': CPFs não encontrados em lugar nenhum
    """
    import os
    import pandas as pd
    from InquirerPy import inquirer

    print("\n[bold yellow]╔══ Iniciando Unificação Múltipla por CPF (Saída CSV) ══╗[/bold yellow]\n")

    # 1) Carrega arquivo base
    base_file_path = inquirer.text(
        message="Digite o caminho do arquivo base (XLSX ou CSV):"
    ).execute()

    def load_any_file_to_df(file_path):
        """
        Carrega XLSX ou CSV para um DataFrame (forçando string).
        Se for CSV, tenta primeiro ; depois ,.
        """
        if file_path.lower().endswith(".xlsx"):
            return pd.read_excel(file_path, engine="openpyxl", dtype=str)
        elif file_path.lower().endswith(".csv"):
            try:
                return pd.read_csv(file_path, sep=';', dtype=str)
            except:
                return pd.read_csv(file_path, sep=',', dtype=str)
        else:
            raise ValueError("Formato de arquivo não suportado! Use .xlsx ou .csv.")

    # Tenta carregar
    try:
        base_df = load_any_file_to_df(base_file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar arquivo base: {e}[/bold red]\n")
        return

    if base_df.empty:
        print("[bold red]✗ O arquivo base está vazio ou não possui dados válidos.[/bold red]\n")
        return

    # Seleciona a coluna de CPF no arquivo base
    base_cpf_column = inquirer.select(
        message="Selecione a coluna de CPF no arquivo base:",
        choices=base_df.columns.tolist()
    ).execute()

    # Função de normalizar CPFs
    def normalize_cpf(cpf):
        digits = "".join(ch for ch in str(cpf) if ch.isdigit())
        return digits.zfill(11)

    print("[cyan]Normalizando CPFs do arquivo base...[/cyan]")
    base_df[base_cpf_column] = base_df[base_cpf_column].apply(normalize_cpf)

    # Monta conjunto com todos os CPFs não encontrados ainda
    unmatched_cpfs = set(base_df[base_cpf_column].unique())

    # Lista (de dicionários) das linhas correspondidas
    matched_rows = []

    # 2) Loop para adicionar arquivos de pesquisa
    while True:
        add_more = inquirer.confirm(
            message="Deseja adicionar um arquivo de pesquisa?",
            default=True
        ).execute()

        if not add_more:
            break

        pesquisa_path = inquirer.text(
            message="Digite o caminho do arquivo de pesquisa (XLSX ou CSV):"
        ).execute()

        # Carrega o arquivo de pesquisa
        try:
            pesquisa_df = load_any_file_to_df(pesquisa_path)
        except Exception as e:
            print(f"[bold red]✗ Erro ao carregar arquivo de pesquisa: {e}[/bold red]\n")
            continue

        if pesquisa_df.empty:
            print("[bold red]✗ O arquivo de pesquisa está vazio ou não possui dados válidos.[/bold red]\n")
            continue

        pesquisa_cpf_col = inquirer.select(
            message="Selecione a coluna de CPF no arquivo de pesquisa:",
            choices=pesquisa_df.columns.tolist()
        ).execute()

        # Normaliza CPF
        print(f"[cyan]Normalizando CPFs do arquivo: {pesquisa_path}[/cyan]")
        pesquisa_df[pesquisa_cpf_col] = pesquisa_df[pesquisa_cpf_col].apply(normalize_cpf)

        # Cria dicionário CPF->linha (primeira ocorrência)
        dict_pesquisa = {}
        for idx, row_ in pesquisa_df.iterrows():
            cpf_val = row_[pesquisa_cpf_col]
            if cpf_val not in dict_pesquisa:
                dict_pesquisa[cpf_val] = row_

        # Agora, percorre apenas CPFs ainda não encontrados
        still_unmatched = list(unmatched_cpfs)

        for cpf_ in still_unmatched:
            if cpf_ in dict_pesquisa:
                # Monta dict => CPF + colunas do arquivo de pesquisa
                matched_dict = {"CPF": cpf_}
                for col in pesquisa_df.columns:
                    if col != pesquisa_cpf_col:
                        matched_dict[col] = dict_pesquisa[cpf_][col]

                matched_rows.append(matched_dict)
                unmatched_cpfs.remove(cpf_)

        if not unmatched_cpfs:
            print("[bold green]Todos os CPFs já foram encontrados![/bold green]")
            break

    # 3) Monta DF final de correspondências
    if matched_rows:
        # Descobre colunas que apareceram
        all_cols = set()
        for dic in matched_rows:
            all_cols.update(dic.keys())
        all_cols = list(all_cols)

        matched_df = pd.DataFrame(matched_rows, columns=all_cols)
        # Se quiser CPF na frente
        if "CPF" in all_cols:
            col_sem_cpf = [c for c in all_cols if c != "CPF"]
            matched_df = matched_df[["CPF"] + col_sem_cpf]
    else:
        matched_df = pd.DataFrame(columns=["CPF"])

    # 4) Monta DF de não encontrados
    if unmatched_cpfs:
        unmatched_df = pd.DataFrame(list(unmatched_cpfs), columns=["CPF"])
    else:
        unmatched_df = pd.DataFrame(columns=["CPF"])

    # 5) Pergunta onde salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar os arquivos de saída (em CSV):"
    ).execute()

    # Extrai só o "nome" base do arquivo sem extensão
    from pathlib import Path
    base_stem = Path(base_file_path).stem  # ex: se for "dados.xlsx", vira "dados"
    
    matched_file_name = os.path.join(output_dir, f"cpf_corresp_{base_stem}.csv")
    unmatched_file_name = os.path.join(output_dir, f"semnada_{base_stem}.csv")

    # 6) Salva TUDO como CSV
    try:
        matched_df.to_csv(matched_file_name, index=False, sep=';', encoding='utf-8')
        unmatched_df.to_csv(unmatched_file_name, index=False, sep=';', encoding='utf-8')
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar arquivos de saída: {e}[/bold red]\n")
        return

    # 7) Resumo
    total_base_cpfs = len(base_df)
    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Total de CPFs no arquivo base:[/white] {total_base_cpfs:,}")
    print(f"[white]► Correspondências encontradas:[/white]   {len(matched_df):,}")
    print(f"[white]► Sem correspondência:[/white]            {len(unmatched_df):,}")
    print(f"[white]► Arquivos de pesquisa usados:[/white]    (depende de quantos adicionados)")

    print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
    print(f"[dim]📁 Arquivo com correspondências salvo em: {matched_file_name}[/dim]")
    print(f"[dim]📁 Arquivo sem correspondência salvo em:  {unmatched_file_name}[/dim]\n")



def validate_multiple_phone_columns_simple_split():
    """
    Gera dois arquivos:
      1) Arquivo com todas as linhas onde a PRIMEIRA coluna de telefone é válida
      2) Arquivo com todas as linhas onde a PRIMEIRA coluna de telefone é inválida

    Validação de número:
      - Remove caracteres não numéricos
      - Deve ter exatamente 11 dígitos
    """

    import os
    import pandas as pd
    from InquirerPy import inquirer
    from rich import print

    print("\n[bold yellow]╔══ Iniciando Separação de Linhas por Telefone (Coluna 1) ══╗[/bold yellow]\n")

    # 1) Recebe o caminho do arquivo (XLSX ou CSV)
    file_path = inquirer.text(
        message="Digite o caminho do arquivo Excel ou CSV:"
    ).execute()

    # Função auxiliar para carregar XLSX ou CSV com fallback de encoding
    def load_file_generic(fp):
        if fp.lower().endswith(".xlsx"):
            return pd.read_excel(fp, engine="openpyxl", dtype=str)  # força leitura como string
        elif fp.lower().endswith(".csv"):
            # Tentamos primeiro com sep=';' e encoding='utf-8'
            try:
                try:
                    return pd.read_csv(fp, sep=';', dtype=str, encoding='utf-8')
                except UnicodeDecodeError:
                    # Se falhar, tentamos latin-1
                    return pd.read_csv(fp, sep=';', dtype=str, encoding='latin-1')
            except:
                # Se ainda falhar, tentamos sep=',' e repetimos encoding
                try:
                    try:
                        return pd.read_csv(fp, sep=',', dtype=str, encoding='utf-8')
                    except UnicodeDecodeError:
                        return pd.read_csv(fp, sep=',', dtype=str, encoding='latin-1')
                except Exception as e:
                    raise e
        else:
            raise ValueError("Formato de arquivo não suportado! Use .xlsx ou .csv.")

    # Tenta carregar o arquivo
    try:
        df = load_file_generic(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[/bold red]\n")
        return

    if df.empty or df.columns.empty:
        print("[bold red]✗ O arquivo não possui cabeçalhos ou está vazio.[/bold red]\n")
        return

    all_columns = df.columns.tolist()

    # 2) Deixa o usuário selecionar UMA OU MAIS colunas, mas só a primeira influenciará a divisão
    selected_columns = []
    while True:
        remaining_columns = [col for col in all_columns if col not in selected_columns]
        if not remaining_columns:
            break

        should_continue = inquirer.confirm(
            message="Deseja selecionar mais uma coluna de telefone?",
            default=True
        ).execute()

        if not should_continue and not selected_columns:
            print("[bold red]✗ É preciso selecionar pelo menos uma coluna para prosseguir.[/bold red]")
            return

        if not should_continue:
            break

        chosen_column = inquirer.select(
            message="Selecione a coluna de telefone:",
            choices=remaining_columns
        ).execute()

        selected_columns.append(chosen_column)

    # Se o usuário não selecionou nada, encerra
    if not selected_columns:
        return

    print("\n[cyan]Separando linhas válidas e inválidas com base na PRIMEIRA coluna selecionada...[/cyan]")

    # 3) Define função para verificar se o número é válido (remover não numéricos e ter 11 dígitos)
    def is_valid_phone(value):
        if pd.isna(value):
            return False
        clean = "".join(ch for ch in str(value) if ch.isdigit())
        return len(clean) == 11

    # 4) Cria uma máscara booleana: se a PRIMEIRA coluna de telefone for válida => True
    first_phone_col = selected_columns[0]
    mask_valid = df[first_phone_col].apply(is_valid_phone)

    # 5) Separa em dois DataFrames
    df_valid = df[mask_valid].copy()
    df_invalid = df[~mask_valid].copy()

    # Exibe estatísticas
    total_rows = len(df)
    valid_count = len(df_valid)
    invalid_count = len(df_invalid)

    print(f"[cyan]→ Coluna principal de telefone usada: [bold]{first_phone_col}[/bold][/cyan]\n")

    # 6) Pergunta diretório de saída
    output_dir = inquirer.text(
        message="Digite o caminho para salvar os arquivos de saída:"
    ).execute()

    if not os.path.isdir(output_dir):
        print(f"[bold red]✗ O caminho '{output_dir}' não é uma pasta válida.[/bold red]\n")
        return

    # Gera nomes de saída, mudando somente o prefixo
    base_name = os.path.basename(file_path)
    valid_file = os.path.join(output_dir, f"val_mult_phone_valid_{base_name}")
    invalid_file = os.path.join(output_dir, f"val_mult_phone_invalid_{base_name}")

    # 7) Salva cada DataFrame no formato original (XLSX ou CSV)
    try:
        if file_path.lower().endswith(".xlsx"):
            df_valid.to_excel(valid_file, index=False, engine="openpyxl")
            df_invalid.to_excel(invalid_file, index=False, engine="openpyxl")
        else:
            # CSV => salvamos com ; e utf-8
            df_valid.to_csv(valid_file, index=False, sep=';', encoding='utf-8')
            df_invalid.to_csv(invalid_file, index=False, sep=';', encoding='utf-8')
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar os arquivos: {e}[/bold red]\n")
        return

    # 8) Exibe um resumo
    print("\n[bold green]╔══ Resumo da Operação ══╗[/bold green]")
    print(f"[white]► Total de linhas no arquivo:[/white]      {total_rows:,}")
    print(f"[white]► Linhas com número VÁLIDO (coluna {first_phone_col}):[/white] {valid_count:,}")
    print(f"[white]► Linhas com número INVÁLIDO (coluna {first_phone_col}):[/white] {invalid_count:,}")
    print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
    print(f"[dim]📁 Arquivo com válidos:   {valid_file}[dim]")
    print(f"[dim]📁 Arquivo com inválidos: {invalid_file}[dim]\n")


def apply_blacklist_phones():
    """
    Aplica uma blacklist de celulares por CPF.
    
    Lógica:
      1) Recebe um arquivo base (XLSX ou CSV).
         - Usuário seleciona coluna de CPF e de numero_celular.
      2) Recebe um arquivo blacklist (XLSX ou CSV).
         - Usuário seleciona coluna de CPF e de numero_celular.
      3) Para cada linha no arquivo de blacklist => se (CPF, numero) constar no base => 
         substitui o número no base por '0'.
    """
    print("\n[bold yellow]╔══ Iniciando Aplicação de Blacklist de Celulares ══╗[/bold yellow]\n")

    import os
    import pandas as pd
    from InquirerPy import inquirer

    # --------------------- Função auxiliar de carregamento --------------------- #
    def load_file_generic(file_path):
        """
        Carrega XLSX ou CSV (tentando ; depois ,) e retorna DataFrame com strings.
        """
        if file_path.lower().endswith(".xlsx"):
            return pd.read_excel(file_path, engine="openpyxl", dtype=str)
        elif file_path.lower().endswith(".csv"):
            try:
                return pd.read_csv(file_path, sep=';', dtype=str)
            except:
                return pd.read_csv(file_path, sep=',', dtype=str)
        else:
            raise ValueError("Formato de arquivo não suportado! Use .xlsx ou .csv.")

    # --------------------- Normalização auxiliar --------------------- #
    def normalize_cpf(cpf):
        """Remove tudo que não seja dígito e zera à esquerda para 11 caracteres."""
        digits = "".join(ch for ch in str(cpf) if ch.isdigit())
        return digits.zfill(11)

    def normalize_phone(phone):
        """Remove tudo que não seja dígito. (Opcional, se quiser unificar.)"""
        digits = "".join(ch for ch in str(phone) if ch.isdigit())
        return digits

    # --------------------- Passo 1: Carrega arquivo base --------------------- #
    base_file_path = inquirer.text(
        message="Digite o caminho do arquivo base (XLSX ou CSV):"
    ).execute()

    try:
        base_df = load_file_generic(base_file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar arquivo base: {e}[/bold red]\n")
        return

    if base_df.empty:
        print("[bold red]✗ O arquivo base está vazio ou não possui dados válidos.[/bold red]\n")
        return

    # Seleciona as colunas de CPF e celular
    base_cpf_col = inquirer.select(
        message="Selecione a coluna de CPF no arquivo base:",
        choices=base_df.columns.tolist()
    ).execute()

    base_phone_col = inquirer.select(
        message="Selecione a coluna de número de celular no arquivo base:",
        choices=base_df.columns.tolist()
    ).execute()

    # Normaliza CPF e telefone no base (se desejar unificar)
    print("[cyan]Normalizando dados do arquivo base...[/cyan]")
    base_df[base_cpf_col] = base_df[base_cpf_col].apply(normalize_cpf)
    base_df[base_phone_col] = base_df[base_phone_col].apply(normalize_phone)

    # --------------------- Passo 2: Carrega arquivo blacklist --------------------- #
    blacklist_file_path = inquirer.text(
        message="Digite o caminho do arquivo de blacklist (XLSX ou CSV):"
    ).execute()

    try:
        black_df = load_file_generic(blacklist_file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar arquivo de blacklist: {e}[/bold red]\n")
        return

    if black_df.empty:
        print("[bold red]✗ O arquivo blacklist está vazio ou não possui dados válidos.[/bold red]\n")
        return

    # Seleciona as colunas de CPF e celular no blacklist
    black_cpf_col = inquirer.select(
        message="Selecione a coluna de CPF no arquivo de blacklist:",
        choices=black_df.columns.tolist()
    ).execute()

    black_phone_col = inquirer.select(
        message="Selecione a coluna de número de celular no arquivo de blacklist:",
        choices=black_df.columns.tolist()
    ).execute()

    # Normaliza CPF e telefone no blacklist (se desejar unificar)
    print("[cyan]Normalizando dados do arquivo blacklist...[/cyan]")
    black_df[black_cpf_col] = black_df[black_cpf_col].apply(normalize_cpf)
    black_df[black_phone_col] = black_df[black_phone_col].apply(normalize_phone)

    # --------------------- Passo 3: Cria estrutura para localizar combinações (CPF, phone) --------------------- #
    print("[cyan]Criando conjunto de blacklist (CPF, phone)...[/cyan]")
    black_set = set()
    for idx, row_ in black_df.iterrows():
        c = row_[black_cpf_col]
        p = row_[black_phone_col]
        # Evita adicionar linhas com CPF vazio ou phone vazio, se quiser
        if c and p:
            black_set.add((c, p))

    print(f"[white]Total de combinações (CPF, phone) na blacklist:[/white] {len(black_set):,}\n")

    # --------------------- Passo 4: Aplica blacklist no base --------------------- #
    print("[cyan]Comparando base com a blacklist...[/cyan]")
    from rich.progress import track

    total_rows = len(base_df)
    replaced_count = 0

    # Percorre cada linha da base; se (CPF, phone) estiver na blacklist => substitui por "0"
    for idx in track(base_df.index, description="[cyan]Processando base...[/cyan]"):
        cpf_val = base_df.at[idx, base_cpf_col]
        phone_val = base_df.at[idx, base_phone_col]
        if (cpf_val, phone_val) in black_set:
            # Substitui por '0'
            base_df.at[idx, base_phone_col] = "0"
            replaced_count += 1

    print("\n[bold green]╔══ Resumo da Blacklist ══╗[/bold green]")
    print(f"[white]► Linhas analisadas no arquivo base:[/white] {total_rows:,}")
    print(f"[white]► Telefones substituídos por '0':[/white]   {replaced_count:,}")

    # --------------------- Passo 5: Pergunta onde salvar arquivo final --------------------- #
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo atualizado:"
    ).execute()

    # Define um nome final
    import os
    from pathlib import Path
    base_stem = Path(base_file_path).stem  # ex: "arquivo_base" se "arquivo_base.xlsx"

    # Vamos manter o mesmo formato do arquivo base
    base_ext = Path(base_file_path).suffix.lower()

    # Nome do arquivo final
    final_name = f"blacklist_aplicado_{base_stem}{base_ext}"
    final_path = os.path.join(output_dir, final_name)

    # --------------------- Salvar no mesmo formato do base --------------------- #
    try:
        if base_ext == ".xlsx":
            base_df.to_excel(final_path, index=False, engine="openpyxl")
        else:
            # pressupondo CSV
            base_df.to_csv(final_path, index=False, sep=';', encoding='utf-8')
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar arquivo final: {e}[/bold red]")
        return

    # --------------------- Conclusão --------------------- #
    print(f"\n[bold green]✓ Processo concluído com sucesso![/bold green]")
    print(f"[dim]📁 Arquivo final salvo em: {final_path}[/dim]\n")

def merge_folder_files_to_csv():
    """
    1) Pergunta se o usuário quer unificar arquivos XLSX ou CSV em uma pasta.
    2) Detecta colunas monetárias olhando a segunda linha (se existir) do primeiro arquivo não-vazio.
    3) Carrega cada arquivo como string (com fallback de encoding para CSV), converte colunas monetárias, e mescla.
    4) Salva em um único CSV final "merged_files.csv" no diretório de saída.
    """

    import os
    import pandas as pd
    import csv
    from InquirerPy import inquirer
    from pathlib import Path
    from rich.progress import track
    from rich import print

    print("\n[bold yellow]╔══ Iniciando Conversão e Mesclagem de Arquivos (Auto Monetárias) ══╗[/bold yellow]\n")

    # ---------------------------------------------------------------------------
    # 1) Escolher se quer unir XLSX ou CSV
    # ---------------------------------------------------------------------------
    file_type = inquirer.select(
        message="Selecione o tipo de arquivo para unificar:",
        choices=[
            ("XLSX", ".xlsx"),
            ("CSV", ".csv")
        ]
    ).execute()

    ext_to_unify = file_type  # ".xlsx" ou ".csv"

    # Pergunta o caminho da pasta
    folder_path = inquirer.text(
        message=f"Digite o caminho da pasta que contém os arquivos {ext_to_unify}:"
    ).execute()

    if not os.path.isdir(folder_path):
        print(f"[bold red]✗ O caminho '{folder_path}' não é uma pasta válida![/bold red]\n")
        return

    # Lista os arquivos com a extensão escolhida
    all_files = [f for f in os.listdir(folder_path) if f.lower().endswith(ext_to_unify)]
    if not all_files:
        print(f"[bold red]✗ Não há arquivos {ext_to_unify} na pasta '{folder_path}'![bold red]\n")
        return

    # Pergunta onde salvar o CSV final
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o CSV final unificado:"
    ).execute()

    if not os.path.isdir(output_dir):
        print(f"[bold red]✗ O caminho '{output_dir}' não é uma pasta válida![/bold red]\n")
        return

    print("\n[cyan]Detectando colunas monetárias com base no primeiro arquivo não-vazio...[/cyan]\n")

    # ---------------------------------------------------------------------------
    # Função auxiliar para ler CSV com fallback (utf-8 -> latin-1)
    # ---------------------------------------------------------------------------
    def load_csv_fallback(file_path, as_str=False):
        """
        Tenta ler CSV primeiro com sep=';' e encoding='utf-8'.
        Se falhar, tenta sep=';' e encoding='latin-1'.
        Se ainda falhar, tenta sep=',' e encoding='utf-8' e depois latin-1.
        Usa low_memory=False para evitar DtypeWarning.
        Se as_str=True, força dtype=str.
        """
        import pandas as pd

        dtype_option = str if as_str else None

        # 1) tentamos sep=';' + utf-8
        try:
            try:
                return pd.read_csv(file_path, sep=';', encoding='utf-8',
                                   low_memory=False, dtype=dtype_option)
            except UnicodeDecodeError:
                return pd.read_csv(file_path, sep=';', encoding='latin-1',
                                   low_memory=False, dtype=dtype_option)
        except:
            # 2) se falhar, tentamos sep=',' e repetimos encodings
            try:
                try:
                    return pd.read_csv(file_path, sep=',', encoding='utf-8',
                                       low_memory=False, dtype=dtype_option)
                except UnicodeDecodeError:
                    return pd.read_csv(file_path, sep=',', encoding='latin-1',
                                       low_memory=False, dtype=dtype_option)
            except Exception as e:
                raise e

    # ---------------------------------------------------------------------------
    # Função para detectar colunas monetárias (sem dtype=str)
    # ---------------------------------------------------------------------------
    def detect_monetary_columns_any(file_path):
        """
        Se for XLSX -> lê normal (sem dtype=str).
        Se for CSV  -> tenta load_csv_fallback(file_path, as_str=False).
        Retorna: (df_detect, monetary_cols)
          - df_detect: DataFrame carregado (ou None)
          - monetary_cols: lista de colunas consideradas monetárias
        """
        import pandas as pd

        if file_path.lower().endswith(".xlsx"):
            # Tenta ler normal (conversão automática de tipos)
            df_temp = pd.read_excel(file_path, engine="openpyxl")
        else:
            # CSV sem dtype=str => Pandas fará conversão de tipos
            df_temp = load_csv_fallback(file_path, as_str=False)

        if df_temp is None or df_temp.empty:
            return None, []

        # Se tiver menos de 2 linhas, usamos index=0
        if len(df_temp) < 2:
            row_idx = 0
        else:
            row_idx = 1

        monetary_cols = []
        for col in df_temp.columns:
            try:
                val = df_temp[col].iloc[row_idx]
            except:
                continue

            # Tenta converter para float
            try:
                float_val = float(val)
                # Se der certo, marcamos como monetário
                monetary_cols.append(col)
            except:
                pass

        return df_temp, monetary_cols

    # ---------------------------------------------------------------------------
    # Detectamos o primeiro arquivo que não esteja vazio
    # ---------------------------------------------------------------------------
    first_file = None
    df_first_detect = None
    monetary_columns = []

    for f in all_files:
        fpath = os.path.join(folder_path, f)
        try:
            tmp_df, tmp_monetary = detect_monetary_columns_any(fpath)
            if tmp_df is not None and not tmp_df.empty:
                first_file = f
                df_first_detect = tmp_df
                monetary_columns = tmp_monetary
                break
        except:
            continue

    if not first_file or df_first_detect is None or df_first_detect.empty:
        print("[bold red]✗ Todos os arquivos estão vazios ou inválidos![bold red]")
        return

    print("[cyan]→ Colunas monetárias detectadas (pela 2ª linha quando possível):[/cyan]")
    for c_ in monetary_columns:
        print(f" - {c_}")

    print("\n[cyan]Convertendo e mesclando arquivos agora...[/cyan]")

    # ---------------------------------------------------------------------------
    # Função que converte valor monetário: substitui '.' por ',' e envolve em aspas
    # ---------------------------------------------------------------------------
    def convert_to_monetary(value) -> str:
        import pandas as pd
        if pd.isna(value) or value is None:
            return '""'
        val_str = str(value)
        # Troca ponto por vírgula
        val_str = val_str.replace('.', ',')
        # Envolve em aspas
        return f"\"{val_str}\""

    # ---------------------------------------------------------------------------
    # Função para carregar como string
    # ---------------------------------------------------------------------------
    def load_as_string(file_path):
        """
        Carrega XLSX ou CSV forçando tudo como string, com fallback.
        """
        import pandas as pd

        if file_path.lower().endswith(".xlsx"):
            # XLSX com dtype=str
            return pd.read_excel(file_path, engine="openpyxl", dtype=str)
        else:
            # CSV com fallback, as_str=True
            return load_csv_fallback(file_path, as_str=True)

    # ---------------------------------------------------------------------------
    # Lê o primeiro arquivo como string e aplica conversão monetária
    # ---------------------------------------------------------------------------
    first_path = os.path.join(folder_path, first_file)
    df_first_str = load_as_string(first_path)
    if df_first_str.empty:
        print(f"[bold red]✗ O primeiro arquivo '{first_file}' está vazio após leitura como string.[bold red]")
        return

    for col in monetary_columns:
        if col in df_first_str.columns:
            df_first_str[col] = df_first_str[col].apply(convert_to_monetary)

    master_df = df_first_str.copy()
    master_columns = master_df.columns.tolist()

    # ---------------------------------------------------------------------------
    # Processar os demais arquivos
    # ---------------------------------------------------------------------------
    remaining_files = [x for x in all_files if x != first_file]

    for f_ in track(remaining_files, description="[cyan]Processando arquivos subsequentes...[/cyan]"):
        fpath = os.path.join(folder_path, f_)
        try:
            df_str = load_as_string(fpath)
        except Exception as e:
            print(f"[bold red]✗ Erro ao carregar '{f_}': {e}[bold red]")
            continue

        if df_str.empty:
            print(f"[bold yellow]Arquivo '{f_}' está vazio. Ignorando...[/bold yellow]")
            continue

        # Aplica conversão monetária
        for col in monetary_columns:
            if col in df_str.columns:
                df_str[col] = df_str[col].apply(convert_to_monetary)

        # Reindexa e concatena
        df_str = df_str.reindex(columns=master_columns)
        master_df = pd.concat([master_df, df_str], ignore_index=True)

        # (Opcional) Salva CSV individual
        csv_stem = Path(f_).stem
        csv_path = os.path.join(folder_path, f"{csv_stem}.csv")
        try:
            df_str.to_csv(
                csv_path,
                index=False,
                sep=';',
                encoding='utf-8',
                quoting=csv.QUOTE_NONE,
                escapechar='\\'
            )
        except Exception as e:
            print(f"[bold red]✗ Erro ao salvar CSV individual '{csv_path}': {e}[bold red]")

    # ---------------------------------------------------------------------------
    # Salva CSV final unificado
    # ---------------------------------------------------------------------------
    if master_df.empty:
        print("\n[bold red]✗ Nenhum dado válido após processar todos os arquivos![bold red]")
        return

    final_csv_name = "merged_files.csv"
    final_csv_path = os.path.join(output_dir, final_csv_name)

    try:
        master_df.to_csv(
            final_csv_path,
            index=False,
            sep=';',
            encoding='utf-8',
            quoting=csv.QUOTE_NONE,
            escapechar='\\'
        )
        print(f"\n[bold green]✓ Arquivo unificado gerado com sucesso![bold green]")
        print(f"[dim]📁 Arquivo salvo em: {final_csv_path}[dim]\n")
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar arquivo unificado: {e}[bold red]\n")



def remove_55_prefix_from_phone_columns():
    """
    1) Recebe caminho de um arquivo (XLSX ou CSV).
    2) Usuário seleciona uma ou mais colunas de telefone.
    3) Para cada coluna, pegamos a primeira linha preenchida como exemplo e perguntamos se é realmente telefone.
    4) Perguntamos se é para remover o '55' dos números que tiverem 13 dígitos e comecem com '55'.
    5) Faz a formatação, removendo o '55' no início de cada telefone que atenda às condições.
    6) Salva o arquivo final.
    """

    import os
    import pandas as pd
    from InquirerPy import inquirer
    from pathlib import Path
    from rich.progress import track

    print("\n[bold yellow]╔══ Iniciando Remoção de Prefixo '55' das Colunas de Telefone ══╗[/bold yellow]\n")

    # --------------------- Função auxiliar de carregamento --------------------- #
    def load_file_generic(file_path):
        """
        Carrega XLSX ou CSV (tentando ; depois ,) e retorna DataFrame com strings.
        """
        if file_path.lower().endswith(".xlsx"):
            return pd.read_excel(file_path, engine="openpyxl", dtype=str)
        elif file_path.lower().endswith(".csv"):
            # Tenta ler com separador ; depois ,
            try:
                return pd.read_csv(file_path, sep=';', dtype=str)
            except:
                return pd.read_csv(file_path, sep=',', dtype=str)
        else:
            raise ValueError("Formato de arquivo não suportado! Use .xlsx ou .csv.")

    # --------------------- Passo 1: Recebe o caminho do arquivo --------------------- #
    file_path = inquirer.text(
        message="Digite o caminho do arquivo (XLSX ou CSV):"
    ).execute()

    if not os.path.isfile(file_path):
        print(f"[bold red]✗ O caminho '{file_path}' não é um arquivo válido![bold red]")
        return

    # Carrega o arquivo
    try:
        df = load_file_generic(file_path)
    except Exception as e:
        print(f"[bold red]✗ Erro ao carregar o arquivo: {e}[bold red]")
        return

    if df.empty:
        print("[bold red]✗ O arquivo está vazio ou não possui dados válidos.[bold red]")
        return

    # Passo 2: Seleciona as colunas de telefone (múltiplas)
    print("\n[cyan]Selecione as colunas que contêm números de telefone...[/cyan]\n")
    phone_cols = []
    while True:
        # Exibe as colunas ainda não escolhidas
        remaining_cols = [c for c in df.columns if c not in phone_cols]
        if not remaining_cols:
            break

        want_more = inquirer.confirm(
            message="Deseja selecionar mais uma coluna de telefone?",
            default=True
        ).execute()

        if not want_more and not phone_cols:
            print("[bold red]✗ É preciso selecionar ao menos uma coluna para continuar.[bold red]")
            return
        if not want_more:
            break

        chosen_col = inquirer.select(
            message="Selecione a coluna de telefone:",
            choices=remaining_cols
        ).execute()
        phone_cols.append(chosen_col)

    # Se não escolheu nada, encerra
    if not phone_cols:
        return

    # Passo 3: Para cada coluna, pegamos a primeira linha não vazia como exemplo e confirmamos
    for col in phone_cols:
        example_value = None
        for idx, val in df[col].items():
            if pd.notna(val) and val.strip():
                example_value = val.strip()
                break

        # Se não achou nenhum valor
        if not example_value:
            print(f"[bold yellow]A coluna '{col}' não possui valores preenchidos para mostrar exemplo.[bold yellow]")
        else:
            # Pergunta ao usuário se esse valor confere
            print(f"\n[cyan]Exemplo encontrado na coluna '{col}':[/cyan] {example_value}")
            confirm_col = inquirer.confirm(
                message="Confirma que esta coluna é realmente de telefone?",
                default=True
            ).execute()
            if not confirm_col:
                # Se o usuário negar, podemos remover a coluna da lista
                print(f"[bold red]Removendo coluna '{col}' da lista de telefones.[bold red]")
                phone_cols.remove(col)

    # Se não sobrou nada
    if not phone_cols:
        print("[bold yellow]Nenhuma coluna de telefone confirmada. Encerrando...[bold yellow]")
        return

    # Passo 4: Pergunta se é para remover '55' (prefixo) dos números com 13 dígitos que começam com '55'
    remove_55 = inquirer.confirm(
        message="Deseja remover o '55' (prefixo) dos números que tiverem 13 dígitos e iniciarem com '55'?",
        default=True
    ).execute()

    if not remove_55:
        print("[bold yellow]Nada a ser feito, pois o usuário optou por não remover.[bold yellow]")
        return

    # Passo 5: Faz a formatação e remove '55' se o tamanho é 13 e começa com '55'
    def remove_55_prefix(value):
        if pd.isna(value):
            return value
        v = str(value).strip()
        # Se tiver 13 dígitos e começar com '55'
        if len(v) == 13 and v.startswith('55'):
            return v[2:]  # remove os 2 primeiros caracteres
        return v

    # Aplica a formatação
    total_rows = len(df)
    changed_count = 0

    for col in phone_cols:
        for idx in track(df.index, description=f"[cyan]Removendo '55' na coluna '{col}'...[/cyan]"):
            old_val = df.at[idx, col]
            new_val = remove_55_prefix(old_val)
            if new_val != old_val:
                df.at[idx, col] = new_val
                changed_count += 1

    print("\n[bold green]╔══ Resumo da Formatação ══╗[/bold green]")
    print(f"[white]► Colunas de telefone tratadas:[/white] {phone_cols}")
    print(f"[white]► Total de linhas no arquivo:[/white]     {total_rows:,}")
    print(f"[white]► Substituições aplicadas:[/white]       {changed_count:,}")

    # Passo 6: Pergunta onde salvar
    output_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo final:"
    ).execute()

    if not os.path.isdir(output_dir):
        print(f"[bold red]✗ O caminho '{output_dir}' não é uma pasta válida![bold red]")
        return

    import os
    from pathlib import Path
    base_stem = Path(file_path).stem
    ext = Path(file_path).suffix.lower()

    final_name = f"{base_stem}_remov55{ext}"
    final_path = os.path.join(output_dir, final_name)

    # Salva com o mesmo formato do arquivo original
    try:
        if ext == ".xlsx":
            df.to_excel(final_path, index=False, engine="openpyxl")
        else:
            # supõe CSV
            df.to_csv(final_path, index=False, sep=';', encoding='utf-8')
    except Exception as e:
        print(f"[bold red]✗ Erro ao salvar arquivo final: {e}[/bold red]")
        return

    print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
    print(f"[dim]📁 Arquivo final salvo em: {final_path}[dim]\n")

def check_phone_correctness_by_cpf():
    """
    1) Carrega um ARQUIVO BASE (XLSX ou CSV):
       - Seleciona a coluna de CPF
       - Seleciona >=1 colunas de telefone
    2) Carrega um ARQUIVO REFERÊNCIA (XLSX ou CSV):
       - Seleciona a coluna de CPF
       - Seleciona a coluna de telefone
       * O mesmo CPF pode aparecer várias vezes, cada vez com um telefone diferente.
    3) Gera três arquivos CSV:
       - found_matched.csv:   CPF existe no arquivo 2 e ALGUM telefone do base coincide com um telefone do set do CPF
       - found_mismatch.csv:  CPF existe no arquivo 2, mas NENHUM telefone do base coincide com o set do CPF
       - not_found.csv:       CPF não existe no arquivo 2
    """

    import os
    import pandas as pd
    from pathlib import Path
    from InquirerPy import inquirer
    from rich.console import Console
    console = Console()

    console.print("\n[bold yellow]╔══ Conferência de Telefones por CPF (Várias Linhas no Arquivo 2) ══╗[/bold yellow]\n")

    # ---------------------------------------------------------
    # Função para converter XLSX -> CSV temporário se necessário
    # ---------------------------------------------------------
    import uuid
    def convert_xlsx_to_csv(xlsx_path, output_dir=None):
        if output_dir is None:
            output_dir = os.path.dirname(xlsx_path)
        df_xlsx = pd.read_excel(xlsx_path, engine="openpyxl", dtype=str)
        temp_name = f"{Path(xlsx_path).stem}_temp_{uuid.uuid4().hex[:6]}.csv"
        temp_path = os.path.join(output_dir, temp_name)
        df_xlsx.to_csv(temp_path, index=False, sep=';', encoding='utf-8')
        return temp_path

    # ---------------------------------------------------------
    # Função fallback p/ carregar CSV (utf-8 -> latin-1)
    # ---------------------------------------------------------
    def load_csv_fallback(csv_path):
        try:
            try:
                return pd.read_csv(csv_path, sep=';', encoding='utf-8', dtype=str, low_memory=False)
            except UnicodeDecodeError:
                return pd.read_csv(csv_path, sep=';', encoding='latin-1', dtype=str, low_memory=False)
        except:
            try:
                try:
                    return pd.read_csv(csv_path, sep=',', encoding='utf-8', dtype=str, low_memory=False)
                except UnicodeDecodeError:
                    return pd.read_csv(csv_path, sep=',', encoding='latin-1', dtype=str, low_memory=False)
            except Exception as e:
                raise e

    # ---------------------------------------------------------
    # 1) Carrega o ARQUIVO BASE
    # ---------------------------------------------------------
    base_path = inquirer.text(
        message="Digite o caminho do ARQUIVO BASE (XLSX ou CSV):"
    ).execute()

    if not os.path.isfile(base_path):
        console.print(f"[bold red]✗ O caminho '{base_path}' não é um arquivo válido![bold red]\n")
        return

    # Converte XLSX -> CSV, se necessário
    if base_path.lower().endswith(".xlsx"):
        console.print("[cyan]Convertendo ARQUIVO BASE de XLSX -> CSV temporário...[/cyan]")
        try:
            base_csv = convert_xlsx_to_csv(base_path)
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao converter XLSX para CSV: {e}[bold red]\n")
            return
    elif base_path.lower().endswith(".csv"):
        base_csv = base_path
    else:
        console.print("[bold red]✗ Formato do arquivo base não suportado (use .xlsx ou .csv)![bold red]")
        return

    # Carrega CSV base com fallback
    try:
        base_df = load_csv_fallback(base_csv)
        if base_df.empty:
            console.print("[bold red]✗ O arquivo base está vazio ou não tem dados válidos.[bold red]\n")
            return
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao carregar CSV base: {e}[bold red]\n")
        return

    # Pergunta a coluna de CPF
    cpf_base_col = inquirer.select(
        message="Selecione a coluna de CPF no arquivo base:",
        choices=base_df.columns.tolist()
    ).execute()

    # Seleciona >=1 colunas de telefone
    phone_cols = []
    while True:
        remaining = [c for c in base_df.columns if c not in phone_cols and c != cpf_base_col]
        if not remaining:
            break

        wants_more = inquirer.confirm(
            message="Deseja selecionar mais uma coluna de telefone no arquivo base?",
            default=True
        ).execute()
        if not wants_more and not phone_cols:
            console.print("[bold red]✗ É preciso ao menos uma coluna de telefone![bold red]")
            return
        if not wants_more:
            break

        chosen_phone = inquirer.select(
            message="Selecione a coluna de telefone:",
            choices=remaining
        ).execute()
        phone_cols.append(chosen_phone)

    if not phone_cols:
        console.print("[bold red]✗ Nenhuma coluna de telefone selecionada. Encerrando...[bold red]")
        return

    # ---------------------------------------------------------
    # 2) Carrega o ARQUIVO 2 (que pode ter várias linhas p/ mesmo CPF)
    # ---------------------------------------------------------
    ref_path = inquirer.text(
        message="Digite o caminho do ARQUIVO 2 (XLSX ou CSV), contendo CPF + TELEFONE (pode repetir o CPF):"
    ).execute()

    if not os.path.isfile(ref_path):
        console.print(f"[bold red]✗ O caminho '{ref_path}' não é um arquivo válido![bold red]\n")
        return

    # Converte XLSX -> CSV, se necessário
    if ref_path.lower().endswith(".xlsx"):
        console.print("[cyan]Convertendo ARQUIVO 2 de XLSX -> CSV temporário...[/cyan]")
        try:
            ref_csv = convert_xlsx_to_csv(ref_path)
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao converter XLSX para CSV: {e}[bold red]\n")
            return
    elif ref_path.lower().endswith(".csv"):
        ref_csv = ref_path
    else:
        console.print("[bold red]✗ Formato do arquivo 2 não suportado![bold red]")
        return

    # Carrega CSV ref com fallback
    try:
        ref_df = load_csv_fallback(ref_csv)
        if ref_df.empty:
            console.print("[bold red]✗ O arquivo 2 está vazio ou não tem dados válidos.[bold red]\n")
            return
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao carregar CSV ref: {e}[bold red]\n")
        return

    # Escolhe colunas do ref
    cpf_ref_col = inquirer.select(
        message="Selecione a coluna de CPF no arquivo 2:",
        choices=ref_df.columns.tolist()
    ).execute()

    phone_ref_col = inquirer.select(
        message="Selecione a coluna de TELEFONE no arquivo 2:",
        choices=[c for c in ref_df.columns if c != cpf_ref_col]
    ).execute()

    # ---------------------------------------------------------
    # 3) Monta dict: CPF -> set({todos os telefones testados})
    # ---------------------------------------------------------
    console.print("\n[cyan]Mapeando CPF -> conjunto de telefones no arquivo 2...[/cyan]")
    from collections import defaultdict
    ref_dict = defaultdict(set)

    for _, row in ref_df.iterrows():
        c = str(row[cpf_ref_col]).strip()
        p = str(row[phone_ref_col]).strip()
        if c and p:
            ref_dict[c].add(p)

    console.print(f"[white]Total de CPFs no arquivo 2:[/white] {len(ref_dict):,}")

    # ---------------------------------------------------------
    # 4) Classifica cada linha do base em 3 grupos
    # ---------------------------------------------------------
    console.print("\n[cyan]Verificando correspondências CPF + telefone...[/cyan]")

    found_matched_rows = []
    found_mismatch_rows = []
    not_found_rows = []

    for index, row in base_df.iterrows():
        base_cpf = str(row[cpf_base_col]).strip()
        if base_cpf not in ref_dict:
            not_found_rows.append(row)
        else:
            # Monta set com todos os phones no base (para essa linha)
            phone_set_base = set()
            for pc in phone_cols:
                val = row[pc]
                if pd.notna(val):
                    phone_set_base.add(val.strip())

            # Intersect com ref_dict[base_cpf]
            if phone_set_base.intersection(ref_dict[base_cpf]):
                # Se houver interseção, found_matched
                found_matched_rows.append(row)
            else:
                # found_mismatch
                found_mismatch_rows.append(row)

    console.print(f"[white]Total linhas no base:[/white] {len(base_df):,}")

    console.print("\n[bold green]╔══ Resumo da Classificação ══╗[/bold green]")
    console.print(f"[white]► found_matched  :[/white] {len(found_matched_rows):,}")
    console.print(f"[white]► found_mismatch :[/white] {len(found_mismatch_rows):,}")
    console.print(f"[white]► not_found     :[/white] {len(not_found_rows):,}")

    # Converte cada lista de rows para DataFrame
    matched_df = pd.DataFrame(found_matched_rows, columns=base_df.columns)
    mismatch_df = pd.DataFrame(found_mismatch_rows, columns=base_df.columns)
    notfound_df = pd.DataFrame(not_found_rows, columns=base_df.columns)

    # ---------------------------------------------------------
    # 5) Pergunta onde salvar e salva 3 CSVs
    # ---------------------------------------------------------
    out_dir = inquirer.text(
        message="Digite o caminho para salvar os 3 arquivos CSV (found_matched, found_mismatch, not_found):"
    ).execute()

    if not os.path.isdir(out_dir):
        console.print(f"[bold red]✗ O caminho '{out_dir}' não é uma pasta válida![bold red]\n")
        return

    base_stem = Path(base_path).stem

    matched_file  = os.path.join(out_dir, f"{base_stem}_found_matched.csv")
    mismatch_file = os.path.join(out_dir, f"{base_stem}_found_mismatch.csv")
    notfound_file = os.path.join(out_dir, f"{base_stem}_not_found.csv")

    console.print("\n[cyan]Salvando arquivos CSV finais...[/cyan]")
    try:
        matched_df.to_csv(matched_file, index=False, sep=';', encoding='utf-8')
        mismatch_df.to_csv(mismatch_file, index=False, sep=';', encoding='utf-8')
        notfound_df.to_csv(notfound_file, index=False, sep=';', encoding='utf-8')
        console.print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        console.print(f"[dim]📁 found_matched:   {matched_file}[dim]")
        console.print(f"[dim]📁 found_mismatch:  {mismatch_file}[dim]")
        console.print(f"[dim]📁 not_found:       {notfound_file}[dim]\n")
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao salvar os arquivos finais: {e}[bold red]\n")

def remove_upag_blacklist():
    """
    Remove (exclui) todas as linhas do ARQUIVO BASE cuja UPAG apareça
    em um ARQUIVO BLACKLIST de UPAGs.

    Fluxo:
    1) Recebe ARQUIVO BASE (XLSX ou CSV):
       - Se for XLSX, converte para CSV temporário.
       - Carrega CSV com fallback (utf-8 -> latin-1).
       - Usuário seleciona a coluna "UPAG".

    2) Recebe ARQUIVO BLACKLIST (XLSX ou CSV):
       - Se for XLSX, converte para CSV temporário.
       - Carrega CSV com fallback.
       - Usuário seleciona a coluna "UPAG" também.

    3) Gera um CSV final:
       - Remove todas as linhas do BASE que tenham UPAG presente
         no conjunto de UPAGs da blacklist.
    """

    import os
    import pandas as pd
    from InquirerPy import inquirer
    from rich.console import Console
    from pathlib import Path
    import uuid

    console = Console()

    console.print("\n[bold yellow]╔══ Remoção de UPAGs em Blacklist ══╗[/bold yellow]\n")

    # ---------------------------------------------------------------------------
    # 1) Função para converter XLSX → CSV (temporário)
    # ---------------------------------------------------------------------------
    def convert_xlsx_to_csv(xlsx_path, output_dir=None):
        if output_dir is None:
            output_dir = os.path.dirname(xlsx_path)
        df_xlsx = pd.read_excel(xlsx_path, engine="openpyxl", dtype=str)
        temp_name = f"{Path(xlsx_path).stem}_temp_{uuid.uuid4().hex[:6]}.csv"
        temp_path = os.path.join(output_dir, temp_name)
        df_xlsx.to_csv(temp_path, index=False, sep=';', encoding='utf-8')
        return temp_path

    # ---------------------------------------------------------------------------
    # 2) Função de fallback para ler CSV (utf-8 -> latin-1)
    # ---------------------------------------------------------------------------
    def load_csv_fallback(csv_path):
        """
        Tenta ler CSV:
          - sep=';' + utf-8 → se falhar, sep=';' + latin-1
          - se falhar, sep=',' + utf-8 → se falhar, sep=',' + latin-1
        Retorna df (dtype=str, low_memory=False).
        """
        import pandas as pd
        try:
            try:
                return pd.read_csv(csv_path, sep=';', encoding='utf-8', dtype=str, low_memory=False)
            except UnicodeDecodeError:
                return pd.read_csv(csv_path, sep=';', encoding='latin-1', dtype=str, low_memory=False)
        except:
            try:
                try:
                    return pd.read_csv(csv_path, sep=',', encoding='utf-8', dtype=str, low_memory=False)
                except UnicodeDecodeError:
                    return pd.read_csv(csv_path, sep=',', encoding='latin-1', dtype=str, low_memory=False)
            except Exception as e:
                raise e

    # ---------------------------------------------------------------------------
    # 3) Carrega o ARQUIVO BASE
    # ---------------------------------------------------------------------------
    base_file = inquirer.text(
        message="Digite o caminho do ARQUIVO BASE (XLSX ou CSV):"
    ).execute()

    if not os.path.isfile(base_file):
        console.print(f"[bold red]✗ O caminho '{base_file}' não é um arquivo válido![bold red]\n")
        return

    # Se for XLSX, converte
    if base_file.lower().endswith(".xlsx"):
        console.print("[cyan]Convertendo arquivo base de XLSX -> CSV temporário...[/cyan]")
        try:
            base_csv = convert_xlsx_to_csv(base_file)
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao converter XLSX para CSV: {e}[bold red]\n")
            return
    elif base_file.lower().endswith(".csv"):
        base_csv = base_file
    else:
        console.print("[bold red]✗ Formato do arquivo base não suportado (use .xlsx ou .csv)![bold red]")
        return

    # Tenta carregar
    try:
        base_df = load_csv_fallback(base_csv)
        if base_df.empty:
            console.print("[bold red]✗ O arquivo base está vazio ou não contém dados válidos.[bold red]\n")
            return
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao carregar CSV base: {e}[bold red]\n")
        return

    # Usuário seleciona a coluna de UPAG
    upag_base_col = inquirer.select(
        message="Selecione a coluna de UPAG no arquivo base:",
        choices=base_df.columns.tolist()
    ).execute()

    # ---------------------------------------------------------------------------
    # 4) Carrega o ARQUIVO BLACKLIST
    # ---------------------------------------------------------------------------
    blacklist_file = inquirer.text(
        message="Digite o caminho do ARQUIVO BLACKLIST (XLSX ou CSV):"
    ).execute()

    if not os.path.isfile(blacklist_file):
        console.print(f"[bold red]✗ O caminho '{blacklist_file}' não é um arquivo válido![bold red]\n")
        return

    if blacklist_file.lower().endswith(".xlsx"):
        console.print("[cyan]Convertendo arquivo blacklist de XLSX -> CSV temporário...[/cyan]")
        try:
            black_csv = convert_xlsx_to_csv(blacklist_file)
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao converter XLSX para CSV: {e}[bold red]\n")
            return
    elif blacklist_file.lower().endswith(".csv"):
        black_csv = blacklist_file
    else:
        console.print("[bold red]✗ Formato do arquivo blacklist não suportado (use .xlsx ou .csv)![bold red]")
        return

    # Tenta carregar blacklist
    try:
        blacklist_df = load_csv_fallback(black_csv)
        if blacklist_df.empty:
            console.print("[bold red]✗ O arquivo de blacklist está vazio ou não contém dados válidos.[bold red]\n")
            return
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao carregar CSV blacklist: {e}[bold red]\n")
        return

    upag_black_col = inquirer.select(
        message="Selecione a coluna de UPAG no arquivo de blacklist:",
        choices=blacklist_df.columns.tolist()
    ).execute()

    # ---------------------------------------------------------------------------
    # 5) Cria um set com as UPAGs da blacklist
    # ---------------------------------------------------------------------------
    console.print("\n[cyan]Criando conjunto de UPAGs da blacklist...[/cyan]")
    black_upags = set()

    for idx, row in blacklist_df.iterrows():
        val = str(row[upag_black_col]).strip()
        if val:
            black_upags.add(val)

    console.print(f"[white]Total de UPAGs na blacklist:[/white] {len(black_upags):,}")

    # ---------------------------------------------------------------------------
    # 6) Filtra o base_df removendo UPAGs que constam na blacklist
    # ---------------------------------------------------------------------------
    console.print("[cyan]Removendo linhas do arquivo base que tenham UPAG na blacklist...[/cyan]")
    initial_count = len(base_df)

    # Marca as linhas que **não** estão na blacklist => VALIDO
    base_df["VALIDO"] = ~base_df[upag_base_col].astype(str).str.strip().isin(black_upags)

    valid_df = base_df[base_df["VALIDO"]].drop(columns=["VALIDO"]).copy()
    invalid_df = base_df[~base_df["VALIDO"]].drop(columns=["VALIDO"]).copy()

    linhas_removidas = len(invalid_df)
    linhas_restantes = len(valid_df)

    console.print("\n[bold green]╔══ Resumo da Remoção por UPAG ══╗[/bold green]")
    console.print(f"[white]► Total de linhas no arquivo base:[/white] {initial_count:,}")
    console.print(f"[white]► Linhas removidas (UPAG na blacklist):[/white] {linhas_removidas:,}")
    console.print(f"[white]► Linhas restantes:[/white] {linhas_restantes:,}")

    # ---------------------------------------------------------------------------
    # 7) Pergunta onde salvar o arquivo final
    # ---------------------------------------------------------------------------
    out_dir = inquirer.text(
        message="Digite o caminho para salvar o arquivo FINAL (CSV):"
    ).execute()

    if not os.path.isdir(out_dir):
        console.print(f"[bold red]✗ O caminho '{out_dir}' não é uma pasta válida![bold red]\n")
        return

    # Gera o nome do arquivo final CSV
    base_stem = Path(base_file).stem
    final_name = f"sem_blacklist_upag_{base_stem}.csv"
    final_path = os.path.join(out_dir, final_name)

    console.print("\n[cyan]Salvando arquivo final em CSV...[/cyan]")
    try:
        valid_df.to_csv(final_path, index=False, sep=';', encoding='utf-8')
        console.print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
        console.print(f"[dim]📁 Arquivo final salvo em: {final_path}[dim]\n")
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao salvar o arquivo final em CSV: {e}[bold red]\n")

def select_common_columns_and_reduce():
    """
    1) Recebe uma pasta contendo múltiplos arquivos (XLSX ou CSV).
    2) Para cada arquivo:
       - Se for XLSX, converte para CSV.
       - Lê como CSV (fallback).
       - Coleta o conjunto de colunas.
    3) Faz a intersecção de colunas em todos os arquivos.
    4) Usuário seleciona quais colunas (entre as comuns) deseja manter.
    5) Cria uma subpasta "only_selected_cols" (ou outro nome) para salvar.
    6) Gera CSVs finais de cada arquivo com apenas as colunas selecionadas.
    """

    import os
    import pandas as pd
    from InquirerPy import inquirer
    from pathlib import Path
    import uuid
    from rich.console import Console
    console = Console()

    console.print("\n[bold yellow]╔══ Seleção de Colunas Comuns em Vários Arquivos ══╗[/bold yellow]\n")

    # --------------------- Função para converter XLSX -> CSV temporário --------------------- #
    def convert_xlsx_to_csv(xlsx_path, out_dir=None):
        """
        Converte um arquivo XLSX para CSV (sep=';', encoding='utf-8'),
        retorna o caminho do CSV gerado.
        """
        if out_dir is None:
            out_dir = os.path.dirname(xlsx_path)
        df_xlsx = pd.read_excel(xlsx_path, engine="openpyxl", dtype=str)
        temp_name = f"{Path(xlsx_path).stem}_temp_{uuid.uuid4().hex[:6]}.csv"
        temp_path = os.path.join(out_dir, temp_name)
        df_xlsx.to_csv(temp_path, index=False, sep=';', encoding='utf-8')
        return temp_path

    # --------------------- Função de fallback p/ carregar CSV (utf-8 -> latin-1) --------------------- #
    def load_csv_fallback(csv_path):
        """
        Tenta ler CSV:
          - sep=';' + utf-8 → se falhar, sep=';' + latin-1
          - se falhar, sep=',' + utf-8 → se falhar, sep=',' + latin-1
        Retorna df com dtype=str, low_memory=False para evitar warnings.
        """
        try:
            try:
                return pd.read_csv(csv_path, sep=';', encoding='utf-8', dtype=str, low_memory=False)
            except UnicodeDecodeError:
                return pd.read_csv(csv_path, sep=';', encoding='latin-1', dtype=str, low_memory=False)
        except:
            try:
                try:
                    return pd.read_csv(csv_path, sep=',', encoding='utf-8', dtype=str, low_memory=False)
                except UnicodeDecodeError:
                    return pd.read_csv(csv_path, sep=',', encoding='latin-1', dtype=str, low_memory=False)
            except Exception as e:
                raise e

    # --------------------- Pergunta a pasta contendo os arquivos --------------------- #
    folder_path = inquirer.text(
        message="Digite o caminho da pasta contendo os arquivos (XLSX ou CSV):"
    ).execute()

    if not os.path.isdir(folder_path):
        console.print(f"[bold red]✗ O caminho '{folder_path}' não é uma pasta válida![bold red]\n")
        return

    # Lista todos os arquivos XLSX ou CSV
    all_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.xlsx') or f.lower().endswith('.csv')]
    if not all_files:
        console.print(f"[bold red]✗ Não foram encontrados arquivos XLSX ou CSV em '{folder_path}'![bold red]\n")
        return

    console.print(f"[cyan]→ Encontrados {len(all_files)} arquivos na pasta.[/cyan]\n")

    # Vamos percorrer cada arquivo e convertê-lo (se XLSX) e carregá-lo como CSV
    common_columns = None
    file_csv_map = {}  # Map original_file -> csv_file_path (após conversão)

    # 1) Converte e encontra colunas
    for idx, fname in enumerate(all_files, 1):
        full_path = os.path.join(folder_path, fname)

        # Verifica se XLSX ou CSV
        if fname.lower().endswith(".xlsx"):
            console.print(f"[cyan]({idx}/{len(all_files)}) Convertendo '{fname}' para CSV temporário...[/cyan]")
            try:
                csv_path = convert_xlsx_to_csv(full_path)
            except Exception as e:
                console.print(f"[bold red]✗ Erro ao converter '{fname}': {e}[bold red]")
                continue
        else:
            # É CSV
            csv_path = full_path

        # Carrega CSV com fallback
        try:
            df_temp = load_csv_fallback(csv_path)
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao carregar '{fname}' como CSV: {e}[bold red]")
            continue

        if df_temp.empty:
            console.print(f"[bold yellow]Arquivo '{fname}' está vazio. Ignorando...[bold yellow]")
            continue

        # Pega as colunas e faz intersecção
        cols_set = set(df_temp.columns.tolist())
        if common_columns is None:
            common_columns = cols_set
        else:
            common_columns = common_columns.intersection(cols_set)

        file_csv_map[fname] = csv_path

        console.print(f" - Colunas no arquivo '{fname}': [dim]{len(cols_set)} colunas[/dim]. "
                      f"[dim]Arquivo CSV (temp) em: {csv_path}[/dim]")

    # Se não conseguimos processar nada ou se common_columns for vazio, encerramos
    if not file_csv_map:
        console.print("[bold red]✗ Nenhum arquivo válido foi processado. Encerrando...[bold red]")
        return

    if not common_columns:
        console.print("[bold red]✗ Não há colunas em comum entre os arquivos processados![bold red]")
        return

    console.print(f"\n[cyan]→ Colunas comuns em TODOS os arquivos:[/cyan]")
    for col in sorted(common_columns):
        console.print(f" - {col}")

    # 2) Usuário seleciona colunas a manter (de entre as colunas comuns)
    selected_cols = inquirer.checkbox(
        message="Selecione as colunas que deseja manter (use espaço para marcar):",
        choices=sorted(list(common_columns))
    ).execute()

    if not selected_cols:
        console.print("[bold red]✗ É preciso selecionar ao menos uma coluna para manter![bold red]")
        return

    # 3) Criamos uma subpasta para os arquivos de saída
    subfolder_name = "only_selected_cols"
    output_dir = os.path.join(folder_path, subfolder_name)
    try:
        os.makedirs(output_dir, exist_ok=True)
        console.print(f"\n[cyan]Subpasta para saída: '{output_dir}'[/cyan]")
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao criar subpasta '{output_dir}': {e}[bold red]")
        return

    # 4) Para cada arquivo, recarregamos seu CSV (fallback) e salvamos com as colunas selecionadas
    from rich.progress import track
    for fname in track(file_csv_map.keys(), description="[cyan]Gerando arquivos finais...[/cyan]"):
        csv_path = file_csv_map[fname]
        try:
            df_csv = load_csv_fallback(csv_path)
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao recarregar '{fname}' (CSV): {e}[bold red]")
            continue

        # Filtra para manter apenas as colunas selecionadas
        # Observação: se faltarem colunas (caso uma falte), podemos reindexar ou descartar
        missing_in_this_file = [c for c in selected_cols if c not in df_csv.columns]
        if missing_in_this_file:
            console.print(f"[bold yellow]Aviso: No arquivo '{fname}' faltam as colunas: {missing_in_this_file}.[bold yellow]")
        df_csv_reduced = df_csv.reindex(columns=selected_cols, fill_value='')

        # Gera o nome de saída
        out_name = f"{Path(fname).stem}_reduced.csv"
        out_path = os.path.join(output_dir, out_name)

        try:
            df_csv_reduced.to_csv(out_path, index=False, sep=';', encoding='utf-8')
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao salvar '{out_name}': {e}[bold red]")
            continue

    console.print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
    console.print(f"[dim]Arquivos finais salvos em: {output_dir}[dim]\n")

def deduplicate_cpfs_across_files():
    """
    Deduplica CPFs em múltiplos arquivos (XLS[X|B], XLS, ou CSV), removendo duplicatas
    dentro de cada arquivo individualmente primeiro, e depois mantendo o CPF somente
    no arquivo mais recente, removendo-o dos arquivos mais antigos.

    Fluxo:
      1) Usuário seleciona a pasta e a extensão dos arquivos (XLSX, XLSB, XLS, CSV).
      2) Lista os arquivos com essa extensão.
      3) Garante que todos tenham colunas em comum e obtém a interseção.
      4) Usuário seleciona a coluna de CPF (entre as colunas comuns).
      5) Cada arquivo passa por remoção de duplicatas internas (mantém a 1ª ocorrência do CPF).
      6) Usuário define a prioridade dos arquivos (1 = mais recente, maior = mais antigo).
      7) Processamos os arquivos em ordem crescente (do mais recente ao mais antigo), removendo CPFs repetidos.
      8) Os arquivos resultantes são salvos em CSV dentro de uma subpasta `dedup_priority`.
    """

    import os
    import pandas as pd
    from InquirerPy import inquirer
    from pathlib import Path
    import uuid
    from rich.console import Console

    console = Console()

    console.print("\n[bold yellow]╔══ Deduplicação de CPFs entre múltiplos arquivos ══╗[/bold yellow]\n")

    # 1) Escolha da pasta e extensão dos arquivos
    folder_path = inquirer.text(
        message="Digite o caminho da pasta com os arquivos:"
    ).execute()

    if not os.path.isdir(folder_path):
        console.print(f"[bold red]✗ O caminho '{folder_path}' não é uma pasta válida![bold red]\n")
        return

    # Pergunta qual extensão será filtrada
    file_ext = inquirer.select(
        message="Selecione a extensão dos arquivos para deduplicação:",
        choices=[".xlsx", ".xlsb", ".xls", ".csv"]
    ).execute()

    # Lista apenas arquivos dessa extensão
    all_files = [f for f in os.listdir(folder_path) if f.lower().endswith(file_ext)]
    if not all_files:
        console.print(f"[bold red]✗ Não há arquivos com extensão '{file_ext}' na pasta '{folder_path}'![bold red]")
        return

    console.print(f"[cyan]→ Encontrados {len(all_files)} arquivos com extensão '{file_ext}'.[/cyan]\n")

    # 2) Funções auxiliares --------------------------------------------------------

    def convert_excel_to_csv(excel_path, out_dir=None):
        """ Converte arquivos Excel (XLS, XLSX, XLSB) para CSV. """
        if out_dir is None:
            out_dir = os.path.dirname(excel_path)
        df_excel = pd.read_excel(excel_path, engine="openpyxl", dtype=str)
        temp_name = f"{Path(excel_path).stem}_temp_{uuid.uuid4().hex[:6]}.csv"
        temp_path = os.path.join(out_dir, temp_name)
        df_excel.to_csv(temp_path, index=False, sep=';', encoding='utf-8')
        return temp_path

    def load_csv_fallback(csv_path):
        """ Tenta carregar CSV, com diferentes delimitadores e encodings. """
        try:
            try:
                return pd.read_csv(csv_path, sep=';', encoding='utf-8', dtype=str, low_memory=False)
            except UnicodeDecodeError:
                return pd.read_csv(csv_path, sep=';', encoding='latin-1', dtype=str, low_memory=False)
        except:
            try:
                try:
                    return pd.read_csv(csv_path, sep=',', encoding='utf-8', dtype=str, low_memory=False)
                except UnicodeDecodeError:
                    return pd.read_csv(csv_path, sep=',', encoding='latin-1', dtype=str, low_memory=False)
            except Exception as e:
                raise e

    # 3) Conversão de arquivos Excel e detecção de colunas comuns ----------------------

    common_columns = None
    file_csv_map = {}

    for idx, fname in enumerate(all_files, 1):
        original_path = os.path.join(folder_path, fname)
        console.print(f"[cyan]({idx}/{len(all_files)}) Preparando '{fname}'...[/cyan]")

        # Se for CSV, mantém; se for Excel, converte
        if file_ext == ".csv":
            csv_path = original_path
        else:
            try:
                csv_path = convert_excel_to_csv(original_path)
            except Exception as e:
                console.print(f"[bold red]✗ Erro ao converter '{fname}' para CSV: {e}[bold red]")
                continue

        # Carregar para identificar colunas
        try:
            df_temp = load_csv_fallback(csv_path)
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao carregar CSV '{fname}': {e}[bold red]")
            continue

        if df_temp.empty or df_temp.columns.empty:
            console.print(f"[bold yellow]Aviso: '{fname}' está vazio ou sem colunas. Ignorando...[bold yellow]")
            continue

        cols_set = set(df_temp.columns)
        if common_columns is None:
            common_columns = cols_set
        else:
            common_columns = common_columns.intersection(cols_set)

        file_csv_map[fname] = csv_path
        console.print(f" → {len(cols_set)} colunas no arquivo.")

    if not file_csv_map:
        console.print("[bold red]✗ Nenhum arquivo pôde ser processado. Encerrando...[bold red]")
        return

    if not common_columns:
        console.print("[bold red]✗ Não há colunas em comum entre todos os arquivos![bold red]")
        return

    console.print("\n[cyan]Colunas em comum detectadas:[/cyan]")
    for c_ in sorted(common_columns):
        console.print(f" - {c_}")

    # 4) Usuário seleciona a coluna de CPF
    cpf_col = inquirer.select(
        message="Selecione a coluna de CPF (entre as colunas comuns):",
        choices=sorted(list(common_columns))
    ).execute()

    # 5) Remoção de duplicatas dentro de cada arquivo individualmente ----------------
    console.print("\n[cyan]Removendo duplicatas dentro de cada arquivo...[/cyan]")
    
    file_dedup_map = {}
    for fname, csv_path in file_csv_map.items():
        try:
            df_temp = load_csv_fallback(csv_path)
            df_temp = df_temp.drop_duplicates(subset=[cpf_col], keep="first")  # Mantém a primeira ocorrência
            file_dedup_map[fname] = df_temp
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao remover duplicatas em '{fname}': {e}[bold red]")

    # 6) Usuário define prioridades (1 = mais recente, maior = mais antigo) ----------
    file_list = list(file_dedup_map.keys())
    order_map = {}

    console.print("\n[cyan]Defina a prioridade dos arquivos (1 = mais recente, maior = mais antigo):[/cyan]")
    for fname in file_list:
        order_num = inquirer.text(
            message=f"Prioridade do arquivo '{fname}'? (1=mais recente, maior=mais antigo)"
        ).execute()
        try:
            order_val = int(order_num)
        except:
            order_val = 999999  # fallback
        order_map[fname] = order_val

    file_list_sorted = sorted(file_list, key=lambda x: order_map[x])

    # 7) Removendo CPFs duplicados entre arquivos na ordem definida -------------------
    console.print("\n[cyan]Removendo CPFs repetidos entre arquivos...[/cyan]")
    seen_cpfs = set()
    final_dfs = {}

    for fname in file_list_sorted:
        df_temp = file_dedup_map[fname]
        df_temp = df_temp[~df_temp[cpf_col].astype(str).isin(seen_cpfs)]
        seen_cpfs.update(df_temp[cpf_col].unique())
        final_dfs[fname] = df_temp

    # 8) Salvar arquivos finais na subpasta `dedup_priority` -------------------------
    subfolder_name = "dedup_priority"
    output_dir = os.path.join(folder_path, subfolder_name)
    os.makedirs(output_dir, exist_ok=True)

    for fname in file_list_sorted:
        out_df = final_dfs[fname]
        out_df.to_csv(os.path.join(output_dir, f"{Path(fname).stem}_dedup.csv"), index=False, sep=';', encoding='utf-8')

    console.print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]\n")



def unify_csv_in_chunks_1m_lines():
    """
    1) Recebe uma pasta contendo apenas arquivos CSV.
    2) Descobre a interseção de colunas (colunas em comum em todos os arquivos).
    3) Concatena todos os arquivos (apenas as colunas comuns).
    4) Divide em arquivos CSV de até 1.000.000 linhas cada.
    5) Salva em uma subpasta 'unified_csv_1m' dentro da pasta original.
    """

    import os
    import pandas as pd
    import csv
    from InquirerPy import inquirer
    from pathlib import Path
    import chardet
    from rich.console import Console
    console = Console()

    console.print("\n[bold yellow]╔══ Unificar CSVs em Blocos de 1 Milhão de Linhas ══╗[/bold yellow]\n")

    # 1) Recebe a pasta
    folder_path = inquirer.text(
        message="Digite o caminho da pasta contendo APENAS arquivos CSV:"
    ).execute()

    if not os.path.isdir(folder_path):
        console.print(f"[bold red]✗ O caminho '{folder_path}' não é uma pasta válida![bold red]\n")
        return

    # Lista os arquivos CSV
    all_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".csv")]
    if not all_files:
        console.print(f"[bold red]✗ Não há arquivos CSV na pasta '{folder_path}'![bold red]\n")
        return

    console.print(f"[cyan]→ Encontrados {len(all_files)} arquivos CSV na pasta.[/cyan]\n")

    # ---------------------------------------------------------------------------
    # 2) Descobrir colunas comuns (lendo só o cabeçalho de cada CSV).
    # ---------------------------------------------------------------------------
    def load_csv_header(csv_path):
        """Tenta ler somente o cabeçalho (primeira linha) para descobrir colunas."""
        with open(csv_path, "rb") as f:
            raw = f.read(2048)
            enc_guess = chardet.detect(raw)
            encoding_used = enc_guess["encoding"] if enc_guess["confidence"] > 0.5 else "utf-8"

        import csv
        with open(csv_path, "r", encoding=encoding_used, newline='') as f:
            reader = csv.reader(f, delimiter=';')
            header = next(reader, None)
            if not header:  # Tentar delimiter=',' se falhar
                f.seek(0)
                reader = csv.reader(f, delimiter=',')
                header = next(reader, None)
            return header if header else []

    common_columns = None
    for idx, fname in enumerate(all_files, 1):
        csv_path = os.path.join(folder_path, fname)
        console.print(f"[cyan]({idx}/{len(all_files)}) Lendo cabeçalho de '{fname}'...[/cyan]")

        header_cols = load_csv_header(csv_path)
        if not header_cols:
            console.print(f"[bold yellow]Arquivo '{fname}' está vazio ou sem cabeçalho.[/bold yellow]")
            continue

        cols_set = set(header_cols)
        if common_columns is None:
            common_columns = cols_set
        else:
            common_columns = common_columns.intersection(cols_set)

    if not common_columns:
        console.print("[bold red]✗ Não há colunas em comum entre todos os arquivos CSV![/bold red]")
        return

    console.print(f"\n[cyan]→ Colunas em comum detectadas: {len(common_columns)}[/cyan]")
    sorted_common_cols = sorted(common_columns)
    for c_ in sorted_common_cols:
        console.print(f" - {c_}")

    # ---------------------------------------------------------------------------
    # 3) Ler todos os arquivos CSV com fallback e concatenar apenas as colunas comuns.
    # ---------------------------------------------------------------------------
    console.print("\n[cyan]Lendo todos os arquivos (apenas colunas comuns) e unificando...[/cyan]")
    all_data = []
    total_lines = 0

    def fallback_read_csv_with_subset(path, usecols):
        """
        Tenta ler CSV com ; ou , e codificação utf-8 ou latin-1, usando apenas as colunas 'usecols'.
        Força dtype=str para tratar tudo como texto.
        """
        # Tenta ; + utf-8
        try:
            try:
                return pd.read_csv(path, sep=';', encoding='utf-8', dtype=str, low_memory=False, usecols=usecols)
            except UnicodeDecodeError:
                return pd.read_csv(path, sep=';', encoding='latin-1', dtype=str, low_memory=False, usecols=usecols)
        except:
            # Tenta , + utf-8
            try:
                try:
                    return pd.read_csv(path, sep=',', encoding='utf-8', dtype=str, low_memory=False, usecols=usecols)
                except UnicodeDecodeError:
                    return pd.read_csv(path, sep=',', encoding='latin-1', dtype=str, low_memory=False, usecols=usecols)
            except Exception as e:
                raise e

    for idx, fname in enumerate(all_files, 1):
        csv_path = os.path.join(folder_path, fname)
        console.print(f"[cyan]({idx}/{len(all_files)}) Unificando '{fname}'...[/cyan]")
        try:
            df_temp = fallback_read_csv_with_subset(csv_path, usecols=sorted_common_cols)
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao ler '{fname}' (colunas comuns): {e}[/bold red]")
            continue

        lines_now = len(df_temp)
        total_lines += lines_now
        console.print(f" → Linhas lidas: {lines_now:,}")

        all_data.append(df_temp)

    if not all_data:
        console.print("[bold red]✗ Nenhum dado foi carregado. Encerrando...[bold red]")
        return

    df_unified = pd.concat(all_data, ignore_index=True)
    del all_data  # Libera memória

    console.print(f"[cyan]DataFrame unificado possui {len(df_unified):,} linhas e {len(df_unified.columns):,} colunas.[/cyan]")

    # ---------------------------------------------------------------------------
    # 4) Dividir df_unified em blocos de 1 milhão de linhas e salvar
    # ---------------------------------------------------------------------------
    chunk_size = 1_000_000
    total_rows = len(df_unified)

    subfolder_name = "unified_csv_1m"
    output_dir = os.path.join(folder_path, subfolder_name)
    try:
        os.makedirs(output_dir, exist_ok=True)
        console.print(f"\n[cyan]Subpasta criada/aberta: {output_dir}[/cyan]")
    except Exception as e:
        console.print(f"[bold red]✗ Erro ao criar subpasta '{output_dir}': {e}[/bold red]")
        return

    num_chunks = (total_rows // chunk_size) + (1 if total_rows % chunk_size else 0)
    console.print(f"[cyan]Gerando {num_chunks} arquivos de até {chunk_size:,} linhas cada...[/cyan]\n")

    start_idx = 0
    for chunk_index in range(num_chunks):
        end_idx = start_idx + chunk_size
        df_chunk = df_unified.iloc[start_idx:end_idx].copy()

        chunk_name = f"unified_chunk_{chunk_index + 1}.csv"
        chunk_path = os.path.join(output_dir, chunk_name)

        # QUOTE_NONE -> não coloca aspas em campos
        # Nenhuma célula será envolvida por aspas mesmo que contenha caracteres especiais
        # Substituir escapechar se desejar (evitar perda de dados).
        df_chunk.to_csv(
            chunk_path,
            index=False,
            sep=';',
            encoding='utf-8',
            quoting=csv.QUOTE_NONE,
            escapechar='\\'
        )
        console.print(f"[green]✓ Salvo: {chunk_path} com {len(df_chunk):,} linhas.[/green]")

        start_idx = end_idx

    console.print(f"\n[bold green]✓ Processo concluído com sucesso![bold green]")
    console.print(f"[dim]Arquivos finais em: {output_dir}[dim]\n")




def main():
    while True:
        choice = inquirer.select(
            message="Selecione uma categoria:",
            choices=[
                Choice("1", "Filtros Únicos"),
                Choice("2", "Filtros Múltiplos"),
                Choice("3", "Remoções"),
                Choice("4", "Adições/Unificações"),
                Choice("5", "Formatações"),
                Choice("6", "Mapeamento de Colunas"),
                Choice("7", "Formatação de Datas"),
                Choice("8", "Buscar e Validar CEPs"),
                Choice("9", "Sair")
            ]
        ).execute()

        if choice == "1":
            filtros_unicos()
        elif choice == "2":
            filtros_multiplos()
        elif choice == "3":
            remocoes()
        elif choice == "4":
            adicoes_unificacoes()
        elif choice == "5":
            formatacoes()
        elif choice == "6":
            map_columns_and_merge()
        elif choice == "7":
            formatar_coluna_data()
        elif choice == "8":
            validate_and_format_cep()
        elif choice == "9":
            print("Programa encerrado!")
            break

def filtros_unicos():
    while True:
        choice = inquirer.select(
            message="Selecione um filtro único:",
            choices=[
                Choice("1", "Filtrar Excel (único)"),
                Choice("2", "Filtrar valores numéricos"),
                Choice("3", "Extração de DDD e Números"),
                Choice("4", "Filtrar Agências"),
                Choice("5", "Validador de Bancos"),
                Choice("6", "Validador Banco, Agência e Conta"),
                Choice("7", "Validar Números de Celular (simples)"),
                Choice("8", "Validar várias colunas de celular (nova função)"),  # <-- Nova opção
                Choice("9", "Voltar")
            ]
        ).execute()

        if choice == "1":
            filter_single_excel()
        elif choice == "2":
            filter_numeric()
        elif choice == "3":
            extract_ddd_and_number()
        elif choice == "4":
            filter_agencies()
        elif choice == "5":
            validador_de_bancos()
        elif choice == "6":
            filter_back_age()
        elif choice == "7":
            validar_numeros_celular()
        elif choice == "8":
            validate_multiple_phone_columns_simple_split()  # <-- Chama a nova função
        elif choice == "9":
            break



def filtros_multiplos():
    while True:
        choice = inquirer.select(
            message="Selecione um filtro múltiplo:",
            choices=[
                Choice("1", "Filtrar Excel (múltiplo)"),
                Choice("2", "Selecionar colunas comuns e reduzir [NOVO]"),
                Choice("3", "Deduplicar CPFs entre arquivos [NOVO]"), 
                Choice("4", "Unificar CSVs em blocos de 1 milhão [NOVO]"),  # <-- Nova função
                Choice("5", "Voltar")
            ]
        ).execute()

        if choice == "1":
            filter_multiple_excel()
        elif choice == "2":
            select_common_columns_and_reduce()  # Função já existente
        elif choice == "3":
            deduplicate_cpfs_across_files()     # Função já existente
        elif choice == "4":
            unify_csv_in_chunks_1m_lines()      # <-- Chamada da nova função
        elif choice == "5":
            break


def remocoes():
    while True:
        choice = inquirer.select(
            message="Selecione uma remoção:",
            choices=[
                Choice("1", "Filtrar CPF - Remoção"),
                Choice("2", "Filtrar e remover por nome"),
                Choice("3", "Remover números fixos e células vazias"),
                Choice("4", "Remover Linhas com Células Vazias"),
                Choice("5", "Remover Números (por CPF) da Blacklist [NOVA FUNÇÃO]"),
                Choice("6", "Remover CPFs da Blacklist (CPF)"),
                Choice("7", "Remover Duplicatas por CPF"),
                Choice("8", "Aplicar Blacklist de Celulares (CPF)"),
                Choice("9", "Remover Duplicatas por Telefone [NOVO]"),
                Choice("10", "Remover Linhas com UPAG da Blacklist [NOVO]"),  # <-- Nova opção
                Choice("11", "Voltar")
            ]
        ).execute()

        if choice == "1":
            filter_cpf_removal()
        elif choice == "2":
            filter_remove_by_name()
        elif choice == "3":
            filter_phone_numbers_csv()
        elif choice == "4":
            delete_rows_with_empty_cells()
        elif choice == "5":
            whitelist_blacklist_removal_num()
        elif choice == "6":
            whitelist_blacklist_removal_cpf()  # remove CPFs da blacklist
        elif choice == "7":
            remover_duplicatas_cpfs()
        elif choice == "8":
            apply_blacklist_phones()
        elif choice == "9":
            remover_duplicatas_phones()
        elif choice == "10":
            remove_upag_blacklist()  # <-- Chamada da nova função
        elif choice == "11":
            break





def adicoes_unificacoes():
    while True:
        choice = inquirer.select(
            message="Selecione uma adição ou unificação:",
            choices=[
                Choice("1", "Unificar arquivos Excel"),
                Choice("2", "Unificar arquivos Excel com base no CPF"),
                Choice("3", "Adicionar dados de CPFs entre arquivos"),
                Choice("4", "Unificar todas as planilhas em uma pasta"),
                Choice("5", "Unificar colunas DDD e Número"),
                Choice("6", "Unificar dados (sem duplicar CPFs) [NOVA OPÇÃO]"),
                Choice("7", "Mesclar XLSX da pasta em um CSV [NOVA FUNÇÃO]"),
                Choice("8", "Voltar")
            ]
        ).execute()

        if choice == "1":
            unify_excel_files()
        elif choice == "2":
            unify_excel_files_with_cpf()
        elif choice == "3":
            dois_unify_excel_files_with_cpf()
        elif choice == "4":
            unifique_one()
        elif choice == "5":
            merge_ddd_number()
        elif choice == "6":
            unify_data_multiple_search_by_cpf_csv()
        elif choice == "7":
            merge_folder_files_to_csv()  # <-- Chamada para a nova função
        elif choice == "8":
            break

def formatacoes():
    while True:
        choice = inquirer.select(
            message="Selecione uma formatação:",
            choices=[
                Choice("1", "Ajustar CPFs para 11 dígitos"),
                Choice("2", "Formatar coluna de valores para padrão monetário"),
                Choice("3", "Formatar Números com Prefixo '55'"),
                Choice("4", "Filtrar e formatar RGs"),
                Choice("5", "Formatar Benefícios"),
                Choice("6", "Validar Número de Endereço"),
                Choice("7", "Validar Coluna de Sexo"),
                Choice("8", "Formatar Coluna de Agência"),
                Choice("9", "Formatar Números de Celular sem '9'"),
                Choice("10", "Formatar Números de Celular para 11 Dígitos"),
                Choice("11", "Adicionar Coluna de Idade"),
                Choice("12", "Remover prefixo '55' de colunas de telefone"),
                Choice("13", "Verificar Telefone x CPF [novo]"),  # <-- Nova opção
                Choice("14", "Voltar")
            ]
        ).execute()

        if choice == "1":
            adjust_cpfs_to_11_digits()
        elif choice == "2":
            format_values_to_money()
        elif choice == "3":
            format_numbers_with_prefix()
        elif choice == "4":
            filter_and_format_rgs()
        elif choice == "5":
            format_benefit_file()
        elif choice == "6":
            validate_address_number()
        elif choice == "7":
            validate_sex_column()
        elif choice == "8":
            format_agency_column()
        elif choice == "9":
            filter_num_nine()
        elif choice == "10":
            formatar_numeros_para_11_digitos()
        elif choice == "11":
            adicionar_coluna_idade()
        elif choice == "12":
            remove_55_prefix_from_phone_columns()
        elif choice == "13":
            # Aqui chamamos a nova função, por ex.:
            check_phone_correctness_by_cpf()  # <-- Nova chamada
        elif choice == "14":
            break




if __name__ == "__main__":
    main()