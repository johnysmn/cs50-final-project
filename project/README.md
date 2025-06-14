# GameReviews: A Flask-Based Web Application

**Autor:** Johny Saymon Melo de Menezes
**Localização:** Caruaru, Brazil
**GitHub:** https://github.com/johnysmn

---

### Vídeo de Apresentação

[Assista à demonstração completa do projeto no YouTube](https://youtu.be/ybTKoY8gtXQ)

---

## Descrição do Projeto

GameReviews é uma aplicação web totalmente funcional desenvolvida como projeto final para o curso CS50: Introduction to Computer Science de Harvard. Nascido do desejo de criar uma plataforma centralizada e focada na comunidade para entusiastas de videojogos, este projeto permite que usuários descubram, discutam e avaliem seus jogos favoritos.

A principal funcionalidade da aplicação gira em torno da integração com a API externa da RAWG.io, uma das maiores bases de dados de jogos disponíveis. Através dela, o GameReviews fornece informações ricas e atualizadas sobre um catálogo vasto de jogos. No entanto, o coração da plataforma é a sua própria comunidade. Com um sistema de autenticação robusto, os usuários podem criar contas, fazer login e contribuir com as suas próprias avaliações, criando assim um banco de dados de opiniões geradas pelos próprios jogadores.

O projeto foi intencionalmente construído com uma abordagem fundamental, utilizando Python e o micro-framework Flask para o backend, garantindo um entendimento profundo de cada componente da aplicação, desde o roteamento e gestão de sessões até a interação com o banco de dados e serviços externos.

## Descrição dos Arquivos do Projeto

Cada arquivo foi estruturado para ter uma responsabilidade clara dentro da arquitetura da aplicação.

### `app.py`
Este é o cérebro e o controlador central de toda a aplicação. Escrito em Python utilizando o framework Flask, este arquivo é responsável por:
* **Inicialização da Aplicação:** Configura e inicializa a instância do Flask, incluindo a gestão de sessões e a conexão com o banco de dados.
* **Definição de Rotas:** Mapeia as URLs (como `/`, `/login`, `/game/3498`) para funções Python específicas que lidam com a lógica de negócio para cada página.
* **Gestão de Requisições:** Processa tanto requisições `GET` (quando um usuário visita uma página) quanto `POST` (quando um usuário envia um formulário, como o de login ou de avaliação).
* **Interação com o Banco de Dados:** Executa todas as queries SQL para registrar novos usuários, verificar credenciais de login e, o mais importante, para inserir e buscar avaliações na tabela `reviews`.
* **Comunicação com a API Externa:** Constrói e envia requisições HTTP para a API da RAWG.io para buscar listas de jogos ou detalhes de um jogo específico, processando a resposta JSON para ser usada nos templates.
* **Lógica de Autenticação:** Gerencia o estado do usuário (logado ou não) através de sessões do Flask, garantindo que apenas usuários autenticados possam realizar ações como escrever uma avaliação.

### `schema.sql`
Este arquivo serve como a "planta" ou o "blueprint" do nosso banco de dados SQLite. Ele contém os comandos `CREATE TABLE` necessários para definir a estrutura de armazenamento de dados da aplicação. Sem ele, a aplicação não saberia como ou onde guardar as informações dos usuários e das suas avaliações. As duas tabelas principais são:
* **`users`:** Armazena as informações essenciais de cada usuário, como um `id` único, `username` (que também deve ser único) e o `hash` da senha, garantindo que as senhas nunca sejam armazenadas em texto puro.
* **`reviews`:** Guarda cada avaliação individual. Esta tabela está inteligentemente ligada à tabela `users` através de uma `FOREIGN KEY` (`user_id`), garantindo a integridade referencial dos dados (uma avaliação não pode existir sem um usuário correspondente). Ela também armazena o `game_id` (da API), a nota (`rating`) e o conteúdo em texto.

### `templates/`
Esta pasta contém todos os arquivos HTML que compõem a interface do usuário, utilizando a sintaxe do motor de templates Jinja para exibir dados dinâmicos enviados pelo `app.py`.
* **`layout.html`:** O arquivo mais importante desta pasta. É o template base que implementa o princípio DRY (Don't Repeat Yourself). Ele contém toda a estrutura HTML comum a todas as páginas (navbar, footer, links para CSS/JS), com blocos (`{% block %}`) que as outras páginas preenchem com seu conteúdo específico.
* **`index.html`:** A página inicial, que contém o formulário de busca.
* **`register.html` / `login.html`:** Contêm os formulários para registro e login de usuários.
* **`search_results.html`:** Renderiza a lista de jogos retornada pela API após uma busca.
* **`game_detail.html`:** A página mais complexa, que exibe tanto os dados de um jogo específico vindos da API quanto a lista de avaliações vindas do nosso próprio banco de dados.

### `static/`
Esta pasta armazena todos os arquivos estáticos, que são enviados para o navegador do cliente sem processamento pelo servidor.
* **`css/styles.css`:** O arquivo de folha de estilos que define toda a aparência visual do site, desde as cores e fontes até o layout responsivo dos elementos.
* **`js/script.js`:** Contém o código JavaScript do lado do cliente. No nosso caso, é usado para adicionar interatividade e melhorar a experiência do usuário, como a verificação em tempo real se as senhas coincidem no formulário de registro.

### `requirements.txt`
Este é um arquivo de texto padrão em projetos Python que lista todas as bibliotecas externas das quais o projeto depende (ex: `Flask`, `requests`, `cs50`). Ele permite que outros desenvolvedores instalem facilmente todas as dependências necessárias com um único comando (`pip install -r requirements.txt`), garantindo a reprodutibilidade do ambiente de desenvolvimento.

## Decisões de Design

Durante o desenvolvimento, algumas decisões importantes de arquitetura foram tomadas:

1.  **Escolha do Framework (Flask):** Optei por usar Flask em vez de um framework mais "completo" como Django. A razão foi pedagógica e alinhada com os objetivos do CS50. O Flask é um micro-framework que oferece as ferramentas essenciais (roteamento, templates) mas deixa muitas decisões (como a interação com o banco de dados ou a estrutura do projeto) para o desenvolvedor. Isso forçou um entendimento mais profundo de como cada parte de uma aplicação web se conecta, em vez de depender de componentes "mágicos" pré-configurados.

2.  **Renderização do Lado do Servidor:** A aplicação utiliza um modelo de renderização do lado do servidor (Server-Side Rendering), onde o Python/Flask processa os dados e gera o HTML completo, que é então enviado para o navegador. A alternativa seria uma Single-Page Application (SPA) com um framework JavaScript (como React ou Vue) no frontend, que faria suas próprias chamadas à API. A abordagem de SSR foi escolhida por ser mais direta, robusta para este tipo de aplicação, e por manter a complexidade focada no backend em Python, que era o foco principal do aprendizado.

3.  **Não Armazenar Dados da API em Cache:** Uma decisão consciente foi a de não criar um cache local (no nosso banco de dados) para os dados dos jogos que vêm da API da RAWG. A cada vez que um usuário visita uma página de detalhes, uma nova chamada à API é feita. Embora o cache pudesse otimizar o desempenho e reduzir o número de chamadas, optei por não implementá-lo para garantir que os dados exibidos (como nota do Metacritic ou link do site) sejam sempre os mais recentes fornecidos pela API, e para manter a complexidade do projeto focada nas suas funcionalidades centrais.

## Como Executar o Projeto

Para executar este projeto localmente, siga os seguintes passos...

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/johnysmn/projects
    cd project
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure a Chave da API:**
    É necessário obter uma chave da API em [rawg.io/apidocs](https://rawg.io/apidocs) e configurá-la como uma variável de ambiente.
    ```bash
    export API_KEY="SUA_CHAVE_AQUI"
    ```

4.  **Crie o banco de dados:**
    ```bash
    sqlite3 project.db < schema.sql
    ```

5.  **Execute a aplicação:**
    ```bash
    flask run
    ```
