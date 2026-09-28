# Lista de Tarefas

Aplicação web simples para criar e listar tarefas, feita com **Flask** e
**PostgreSQL**, containerizada com Docker e Docker Compose.

Trabalho da disciplina de Computação em Nuvem — Engenharia de Software.

## Pré-requisitos

- [Docker](https://docs.docker.com/get-started/)
- Docker Compose (já incluso nas versões recentes do Docker Desktop)

## Como subir o ambiente

1. Clone o repositório:
   ```bash
   git clone <url-deste-repositorio>
   cd lista-tarefas
   ```

2. Copie o arquivo de variáveis de ambiente de exemplo:
   ```bash
   cp .env.example .env
   ```

3. Suba os containers:
   ```bash
   docker compose up -d --build
   ```

4. Acesse a aplicação em [http://localhost:8000](http://localhost:8000).

## Como usar

- Digite o nome de uma tarefa no campo de texto e clique em **Adicionar**.
- As tarefas cadastradas aparecem na lista abaixo do formulário.

## Persistência dos dados

Os dados do banco ficam em um volume nomeado (`dados`). Isso significa que:

- `docker compose down` encerra os containers, mas **preserva** os dados.
- `docker compose down -v` encerra os containers e **remove** o volume,
  apagando as tarefas cadastradas.

## Estrutura do repositório

```
lista-tarefas/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```
