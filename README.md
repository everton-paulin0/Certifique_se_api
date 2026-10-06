Certifique-se é uma api ao qual irá gerar Certificados baseado em dados da lista de presença do cursos efetuados.


Segue abaixo a estrutura da Aplicação

├── core/                           # [Django - Configuração Global]
│   ├── settings.py                 # Configurações do banco SQL, apps e middlewares.
│   └── urls.py                     # Roteamento raiz da aplicação.
│
├── domain/                         # [Camada de Domínio - Regras de Negócio Puras]
│   ├── __init__.py
│   ├── models.py                   # Entidades (Aluno, Instrutor, Curso) em Python puro (Dataclasses).
│   ├── interfaces.py               # Contratos/Interfaces para os serviços (Ex: Interface do gerador de PDF).
│   └── use_cases/                  # [Casos de Uso da Aplicação]
│       ├── __init__.py
│       └── generate_certificates.py # Lógica de ordenação da lista de alunos e emissão dos certificados.
│
├── infrastructure/                 # [Camada de Infraestrutura - Detalhes Concretos]
│   ├── pdf/                        # [Serviço de PDF]
│   │   ├── __init__.py
│   │   └── generator.py            # Implementação real com ReportLab (desenho do PDF e inserção de imagens).
│   └── multitenancy/               # [Isolamento Multi-tenant]
│       ├── __init__.py
│       └── middleware.py           # Captura o Tenant (X-Tenant-ID) no cabeçalho HTTP de cada requisição.
│
├── certificates/                   # [Camada de Apresentação / Delivery Mechanics]
│   ├── serializers.py              # Valida os dados de entrada do JSON (DRF Serializers).
│   ├── views.py                    # Recebe a requisição HTTP, aciona o Caso de Uso e devolve o ZIP.
│   └── urls.py                     # Declara o endpoint da API (Ex: /api/generate-pdfs/).
│
├── presentation/
│   └── templates/
│       └── index.html              # Frontend simples para testar a API no navegador.
│
├── Dockerfile                      # Receita para criar a imagem da aplicação Python/Django.
├── docker-compose.yml              # Orquestrador que sobe o Django + Banco PostgreSQL juntos.
└── requirements.txt                # Lista de bibliotecas (Django, ReportLab, DRF, Psycopg2).