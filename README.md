# DataMagi

Bem-vindo(a) ao DataMagi, uma ferramenta repleta de recursos para manipulação e automação de dados em planilhas Excel e CSV. Este projeto foi concebido para facilitar a vida de quem lida diariamente com grandes (ou pequenos) volumes de informações, simplificando atividades repetitivas como remoção de duplicidades, unificação de planilhas, filtragens avançadas e muito mais.

---

## Tabela de Conteúdo

1. **Descrição Geral**  
2. **Principais Recursos**  
3. **Categorias de Funcionalidades**  
   - Filtros Únicos  
   - Filtros Múltiplos  
   - Remoções  
   - Adições/Unificações  
   - Formatações  
   - Mapeamento de Colunas  
   - Outras Funcionalidades  
4. **Bibliotecas Utilizadas**  
5. **Como Obter o Projeto**  
6. **Instalando Dependências**  
7. **Como Executar**  
8. **Fluxo Típico de Uso**  
9. **Boas Práticas de Manipulação**  
10. **Contribuições**  
11. **Licença**  
12. **Contato**

---

## 1. Descrição Geral

O DataMagi foi criado para atender a demandas frequentes no tratamento de dados tabulares. Com sua interface interativa de linha de comando, você poderá:

- Converter, mesclar e filtrar arquivos Excel ou CSV com poucos cliques.  
- Organizar colunas e remover duplicidades de modo rápido e seguro.  
- Formatar campos (CPF, RG, datas, valores monetários etc.) de acordo com padrões padronizados.  
- Criar fluxos de limpeza e unificação de dados de acordo com múltiplos critérios.

O foco está em fornecer uma experiência amigável, mesmo para quem não tem amplo conhecimento em programação, simplificando processos que muitas vezes exigiriam diversas etapas em aplicativos de planilha.

---

## 2. Principais Recursos

- **Leitura automatizada** de arquivos CSV ou Excel em diversos formatos (".csv", ".xlsx", ".xls").  
- **Fallback de encoding** (utf-8, latin-1 etc.) para lidar com problemas de codificação em arquivos CSV.  
- **Filtros dinâmicos** para valores exatos, intervalos numéricos e colunas múltiplas.  
- **Remoção inteligente** de linhas indesejadas, duplicidades ou dados que pertençam a listas de exclusão (blacklist).  
- **Formatações padronizadas** (CPF para 11 dígitos, datas, monetário, prefixos telefônicos etc.).  
- **Validação e limpeza** de colunas específicas (endereços, nomes, telefones, agências bancárias etc.).  
- **Unificação de planilhas** baseada em colunas-chave (CPF, por exemplo) ou na detecção de colunas comuns.  
- **Interface interativa** que orienta o usuário passo a passo.

---

## 3. Categorias de Funcionalidades

### 3.1 Filtros Únicos
Permitem a aplicação de um único critério de filtragem em um arquivo de dados. Exemplos:
- Selecionar todas as linhas em que uma coluna específica possua um valor exato.  
- Escolher apenas dados que sejam numéricos e acima de um limite.  

Normalmente, são usados em cenários simples em que precisamos de um único critério (ex.: "Manter apenas os registros com status APROVADO").

### 3.2 Filtros Múltiplos
Diferenciam-se dos Filtros Únicos por aceitar múltiplos critérios simultaneamente. Assim, você pode, por exemplo, filtrar apenas linhas onde a "Cidade" seja "São Paulo" e "Status" seja "ATIVO". Esse módulo possibilita:
- Empilhar condições lógicas (equalidade, intervalos numéricos etc.).  
- Manter registro somente se ele atender a todos os filtros escolhidos.

### 3.3 Remoções
Nesta categoria, diversas rotinas de exclusão de linhas ou valores indesejados:
- Remover duplicidades (CPF duplicado, telefone duplicado etc.).  
- Excluir linhas se um determinado valor constar em uma blacklist.  
- Remover linhas inteiras que contenham células vazias em colunas específicas.  
- Filtrar e remover registros por nome, CPF, telefone ou colunas personalizadas.

### 3.4 Adições/Unificações
Englobam operações em que se combinam arquivos diferentes para gerar um único resultado:
- Unir planilhas com a mesma estrutura.  
- Fazer merges de dados baseados em chaves (CPF, por exemplo).  
- Concatenar arquivos CSV ou Excel em subpastas, respeitando limites de tamanho de arquivo, se necessário.  
- Ajustar duplicidades entre arquivos, dando prioridade ao mais recente.

### 3.5 Formatações
Inclui qualquer transformação pontual nos valores:
- Ajustar colunas de CPF para 11 dígitos, adicionando zeros à esquerda se necessário.  
- Padronizar datas para um mesmo formato (por exemplo, "dd/MM/yyyy").  
- Converter valores para formato monetário (123400 -> "1.234,00").  
- Inserir prefixos de telefonia em números (adicionar ou remover "55").  
- Reformatar valores que indiquem agência bancária ou RG, validando consistência de tamanho.

### 3.6 Mapeamento de Colunas
Permite ao usuário escolher um "arquivo modelo" e um "arquivo de dados" para mesclar valores em colunas específicas. Semelhante a um "VLOOKUP" mais interativo:
- Mapeia colunas de um arquivo de origem para o arquivo de destino.  
- Cria um novo arquivo que segue a estrutura do arquivo modelo, preenchendo com dados equivalentes.

### 3.7 Outras Funcionalidades
- Extração de DDD e número de celular em colunas separadas.  
- Inclusão de coluna de idade baseada em data de nascimento (considerando fuso horário do Brasil).  
- Remoção de linhas com dados vazios ou suspeitos.  
- Conversão automatizada de todos os arquivos de uma pasta para CSV, ou unificação de planilhas em um só documento.

---

## 4. Bibliotecas Utilizadas

Abaixo, uma lista das principais bibliotecas que tornam possível o funcionamento do DataMagi:
- **InquirerPy**: Fornece prompts interativos no terminal, guiando o usuário na escolha de filtros e colunas.  
- **pandas**: Principal biblioteca para manipulação de dados (leitura e gravação de CSV, Excel, remoção de duplicidades, filtragens).  
- **requests**: Faz chamadas HTTP em funções específicas que necessitam de validações externas (quando usadas).  
- **rich**: Facilita a criação de mensagens coloridas e barras de progresso, melhorando a experiência do usuário no terminal.  
- **pytz**: Gerencia fuso horário para o cálculo de datas (por exemplo, quando se calcula a idade).  
- **chardet**: Ajuda a detectar encoding em arquivos CSV, fundamental no fallback de leitura para lidar com caracteres especiais.

---

## 5. Como Obter o Projeto

Para clonar o repositório oficial, basta utilizar:
git clone https://github.com/llongaray/DataMagi.git

Isso criará uma pasta local com todos os arquivos do projeto, incluindo o arquivo principal de aplicação e o arquivo de requisitos.

---

## 6. Instalando Dependências

Dentro da pasta clonada, execute o comando:
pip install -r requirements.txt

Essa ação irá instalar as bibliotecas listadas no arquivo requirements.txt, garantindo que o DataMagi disponha de todas as dependências necessárias para funcionar.

---

## 7. Como Executar

1. Certifique-se de ter instalado o Python 3 e o Pip.  
2. No terminal, acesse a pasta do projeto.  
3. Inicie a aplicação principal (por exemplo, nomeado "app.py") executando python app.py ou python3 app.py.  
4. Siga as instruções interativas que aparecerem no console, escolhendo a categoria e a função desejadas.

---

## 8. Fluxo Típico de Uso

1. **Selecione uma categoria** (Filtros Únicos, Filtros Múltiplos, Remoções, Adições/Unificações, Formatações, Mapeamento de Colunas).  
2. **Escolha a funcionalidade** (por ex.: Filtrar CPFs duplicados, Formatador de datas, Remoção de blacklist etc.).  
3. **Informe caminhos de arquivos** e selecione colunas (CPF, Nomes, Telefones).  
4. **Defina parâmetros** (por exemplo, valor mínimo ou máximo em filtros numéricos).  
5. **Aguarde o processamento** com o auxílio das barras de progresso e mensagens coloridas fornecidas pela biblioteca rich.  
6. **Verifique o arquivo de saída** ou subpasta de destino. Repita o processo com outras funções, se necessário.

---

## 9. Boas Práticas de Manipulação

- Mantenha sempre um backup de seus arquivos originais antes de aplicar filtros ou remoções.  
- Use nomes de colunas padronizados (sem espaços ou caracteres especiais) para facilitar a seleção e o mapeamento.  
- Valide os arquivos resultantes, principalmente quando aplicar múltiplos filtros complexos ou unificações extensas.  
- Caso haja problemas de codificação, verifique se o fallback de encoding está sendo reconhecido (a biblioteca chardet auxilia nessa identificação).

---

## 10. Contribuições

Sinta-se à vontade para enviar sugestões de melhorias ou reportar problemas via *Issues* no repositório do GitHub. Pull requests que adicionem novas funções ou melhorem as existentes também são bem-vindos, desde que sigam a estrutura e estilo do projeto. Acreditamos na comunidade para tornar o DataMagi ainda mais robusto.

---

## 11. Licença

Este projeto está disponível sob uma licença aberta que permite modificações e distribuição. Confira o arquivo LICENSE presente no repositório para detalhes completos. Respeitar os termos de licenciamento contribui para manter a comunidade saudável e colaborativa.

---

## 12. Contato

Para dúvidas, sugestões ou feedback, utilize:
- A aba de *Issues* no repositório oficial do GitHub.  
- Ou, se preferir, busque pelos canais de suporte mencionados na documentação.

Sua participação e seus comentários são valiosos para o crescimento e a evolução deste projeto. Esperamos que o DataMagi seja útil em suas rotinas de limpeza e tratamento de dados!

Muito obrigado por utilizar o DataMagi!