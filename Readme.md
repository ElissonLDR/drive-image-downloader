# 📥 Drive Image Downloader

Ferramenta para baixar automaticamente imagens do Google Drive a partir de links encontrados em arquivos Excel, organizando tudo em pastas por nome de arquivo.

## ✨ Funcionalidades

- Percorre todas as subpastas recursivamente a partir da pasta raiz
- Lê todos os arquivos `.xlsx` encontrados
- Detecta automaticamente a linha de cabeçalho com a coluna `Imagem`
- Suporta múltiplos links por célula (separados por vírgula, ponto e vírgula, espaço ou quebra de linha)
- Salva as imagens com o nome original do arquivo
- Cria uma pasta `Imagens/` ao lado de cada Excel, com subpasta pelo nome do arquivo
- Trata erros por download sem interromper o processo
- Funciona tanto como script `.py` quanto como executável `.exe`

## 📁 Estrutura esperada
Raiz/
├── baixar_imagens.exe
├── Categoria A/
│   ├── Subcategoria 1/
│   │   ├── arquivo.xlsx
│   │   └── Imagens/
│   │       └── arquivo/
│   └── Subcategoria 2/
│       ├── arquivo.xlsx
│       └── Imagens/
│           └── arquivo/
└── Categoria B/
└── Subcategoria 1/
├── arquivo.xlsx
└── Imagens/
└── arquivo/

## 🚀 Como usar

1. Coloque o executável (ou script) na pasta raiz (ex: `Raiz/`)
2. Execute o arquivo
3. As imagens serão baixadas automaticamente em cada subpasta correspondente

## 🛠️ Requisitos (para rodar como `.py`)

```bash
pip install pandas requests openpyxl
```

## 📦 Gerar o executável

```bash
pip install pyinstaller
pyinstaller --onefile baixar_imagens.py
```

## 📋 Formato esperado do Excel

A planilha deve conter uma coluna chamada **Imagem** com links do Google Drive no formato:
https://drive.google.com/file/d/FILE_ID/view