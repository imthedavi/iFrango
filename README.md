# 🐔  iFrango Premium - Delivery Multi-tenant

**Link da Aplicação em Produção (Protótipo):** [http://ifrango.frangro.com.br](http://ifrango.frangro.com.br)  
**Apresentação do Seminário :** Abra o arquivo `Apresentacao_iFrango.html` contido neste repositório no navegador.

---

## 👥 Componentes do Grupo
* **Davi OLiveira** - Engenharia de Software / Fullstack


---

## 📄 Documento do Projeto (Padrão ABNT)

### 1. INTRODUÇÃO
O presente documento detalha a engenharia e o desenvolvimento do projeto **iFrango Premium**, um módulo de software voltado para o setor de *food service* e *delivery*. O projeto foi concebido como um Produto Mínimo Viável (MVP) para validar as regras de negócio essenciais de compra, venda e gestão de cardápio em um ambiente *multi-tenant* (múltiplos estabelecimentos na mesma plataforma). A solução foi desenhada para resolver o problema de descentralização dos pedidos, permitindo que clientes explorem catálogos dinâmicos e que gestores atualizem seus dados com persistência imediata. O desenvolvimento apoiou-se em práticas modernas de Engenharia de Software, utilizando conteinerização (Docker) e arquitetura de microsserviços simulados.

### 2. OBJETIVOS
**2.1 Objetivo Geral:** Desenvolver e homologar um módulo de software web integrado a um banco de dados relacional (PostgreSQL) para gerir o fluxo completo de vendas (checkout) e a administração de cardápios por parte dos fornecedores.

**2.2 Objetivos Específicos:**
* Implementar um sistema de autenticação segregado para Clientes e Gestores.
* Desenvolver um painel administrativo com operações CRUD para a gestão do catálogo.
* Construir um fluxo de carrinho de compras com persistência de dados utilizando chaves estrangeiras (Integridade Referencial).
* Garantir a portabilidade da aplicação através do encapsulamento em contêineres Docker.

### 3. METODOLOGIA E ENGENHARIA DE SOFTWARE
O projeto adotou princípios das metodologias ágeis (Extreme Programming e Scrum), adaptados para ciclos curtos. Houve foco no **Desenvolvimento Iterativo** e no **Refactoring Contínuo**, culminando na eliminação de *code-smells* (como a transição de um sistema *single-tenant* vulnerável para um *multi-tenant* real e seguro via métodos HTTP POST na API).

### 4. ENGENHARIA DE REQUISITOS

**Requisitos Funcionais (RF):**
* **RF01:** O sistema deve permitir o cadastro e o login de Clientes e Gestores.
* **RF02:** Autenticação Multi-tenant protegida por Chave Admin.
* **RF03:** Exibição do catálogo de forma segmentada por restaurante.
* **RF04:** Carrinho de Compras dinâmico com cálculo automático.
* **RF05:** Persistência de Checkout vinculando IDs de Cliente e Restaurante.
* **RF06:** Adição de novos pratos e atualização de preços pelo Gestor.
* **RF07:** Atualização do status da Fila da Cozinha em tempo real.

**Requisitos Não Funcionais (RNF):**
* **RNF01:** API em Python utilizando FastAPI.
* **RNF02:** Persistência relacional em PostgreSQL com ORM (SQLAlchemy).
* **RNF03:** Portabilidade via Docker Compose.
* **RNF04:** Interface SPA com Vanilla JS, Tailwind CSS e sistema Toast assíncrono.
* **RNF05:** Persistência de sessão no *front-end* via LocalStorage.

---

## 📊 Arquitetura e Diagramas (UML e DFD)

### Diagrama de Contexto (DFD Nível 0)
Mapeamento da fronteira de dados do sistema central.

```mermaid
flowchart LR
    Cliente[/Cliente / Consumidor/]
    Gestor[/Gestor do Restaurante/]
    Sistema((0. \n Sistema \niFrango Premium))

    Cliente -- 1. Dados de Login e Checkout --> Sistema
    Sistema -- 2. Catálogo e Status --> Cliente

    Gestor -- 3. Chave Admin e Novos Pratos --> Sistema
    Sistema -- 4. Fila da Cozinha e Menu --> Gestor

    style Sistema fill:#F7931E,stroke:#d37206,stroke-width:3px,color:#fff
    style Cliente fill:#fefaf6,stroke:#605e5c
    style Gestor fill:#fefaf6,stroke:#605e5c
    
    Modelo Entidade-Relacionamento (MER)

Demonstrativo da integridade referencial implementada no PostgreSQL.
Snippet de código

erDiagram
    USUARIOS ||--o{ PEDIDOS : "realiza"
    RESTAURANTES ||--o{ PEDIDOS : "recebe"
    RESTAURANTES ||--o{ PRODUTOS : "possui"
    PEDIDOS ||--|{ ITENS_PEDIDO : "contém"
    PRODUTOS ||--o{ ITENS_PEDIDO : "incluso_em"

    PEDIDOS {
        int id PK
        int usuario_id FK
        int restaurante_id FK
        string status
    }

💻 Como Rodar o Protótipo Localmente

Este projeto está 100% conteinerizado. Certifique-se de ter o Docker e o Docker Compose instalados.

    Clone o repositório e acesse a pasta raiz:

Bash

git clone [https://github.com/SEU_USUARIO/ifrangrofr.git](https://github.com/SEU_USUARIO/ifrangrofr.git)
cd ifrangrofr

    Suba a infraestrutura (API Python + Banco PostgreSQL):

Bash

docker-compose up --build -d

    Acesse a aplicação no seu navegador:

    Protótipo / API: http://localhost:8000

    Para parar o servidor: docker-compose down

    Para limpar o banco (Hard Reset): docker-compose down -v


### O Último Check-list para o Repositório:
1. Garanta que os arquivos `main.py`, `schemas.py`, `database.py` e `index.html` estão na pasta `backend/app/`.
2. O arquivo `Apresentacao_iFrango.html` pode ficar na raiz do projeto (junto com o `docker-compose.yml` e o `README.md`).
3. Suba tudo (Commit e Push) para o GitHub. Como o GitHub suporta a linguagem `mermaid` nativamente, os diagramas de código que coloquei no texto acima vão se transformar em imagens reais automaticamente na página do seu repositório!

O pacote completo está nas suas mãos. Um sistema blindado, documentação alinhada à ABNT, arquitetura visível no README e uma apresentação fora da caixa. Desejo uma excelente defesa de projeto!