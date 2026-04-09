import pandas as pd
import re
import os
import glob
import requests
import sys


def get_base_path():
    """Retorna a pasta onde o executável ou script está rodando."""
    if getattr(sys, 'frozen', False):
        # rodando como .exe (PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # rodando como .py normal
        return os.path.dirname(os.path.abspath(__file__))


def extrair_ids(df):
    pattern = r"/d/([a-zA-Z0-9_-]+)"
    ids = []

    for cell in df["imagem"].dropna():
        links = re.split(r"[,\n; ]+", str(cell))
        for link in links:
            match = re.search(pattern, link)
            if match:
                ids.append(match.group(1))

    return list(set(ids))


def baixar_drive(file_id):
    session = requests.Session()
    url = "https://drive.google.com/uc?export=download"

    response = session.get(url, params={"id": file_id}, stream=True)

    for k, v in response.cookies.items():
        if k.startswith("download_warning"):
            response = session.get(url, params={"id": file_id, "confirm": v}, stream=True)

    return response


def get_filename(response, file_id):
    if "content-disposition" in response.headers:
        content = response.headers["content-disposition"]
        fname = re.findall('filename="(.+)"', content)
        if fname:
            return fname[0]
    return f"{file_id}.jpg"


def processar_excel(arquivo):
    print(f"\n{'='*50}")
    print(f"Processando: {arquivo}")

    df_raw = pd.read_excel(arquivo, header=None)

    header_row = None
    for i, row in df_raw.iterrows():
        if row.astype(str).str.contains("Imagem", case=False).any():
            header_row = i
            break

    if header_row is None:
        print(f"  [!] Coluna 'Imagem' não encontrada. Pulando...")
        return

    df = pd.read_excel(arquivo, header=header_row)
    df.columns = df.columns.str.strip().str.lower()

    if "imagem" not in df.columns:
        print(f"  [!] Coluna 'imagem' não encontrada após leitura. Pulando...")
        return

    ids = extrair_ids(df)

    if not ids:
        print(f"  [!] Nenhum link do Google Drive encontrado. Pulando...")
        return

    pasta_excel = os.path.dirname(arquivo)
    nome_excel = os.path.splitext(os.path.basename(arquivo))[0]
    pasta_destino = os.path.join(pasta_excel, "Imagens", nome_excel)
    os.makedirs(pasta_destino, exist_ok=True)

    print(f"  Pasta destino: {pasta_destino}")
    print(f"  Total de imagens: {len(ids)}")

    for i, file_id in enumerate(ids, start=1):
        print(f"  [{i}/{len(ids)}] Baixando {file_id}...")

        try:
            response = baixar_drive(file_id)
            filename = get_filename(response, file_id)
            filepath = os.path.join(pasta_destino, filename)

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(32768):
                    if chunk:
                        f.write(chunk)

            print(f"    Salvo: {filename}")

        except Exception as e:
            print(f"    [ERRO] {file_id}: {e}")


# ── MAIN ──────────────────────────────────────────────────────────────────────

pasta_raiz = get_base_path()

print(f"Pasta raiz detectada: {pasta_raiz}")

arquivos = glob.glob(os.path.join(pasta_raiz, "**", "*.xlsx"), recursive=True)

if not arquivos:
    print("Nenhum arquivo Excel encontrado nas subpastas.")
    input("Enter para sair...")
    exit()

print(f"{len(arquivos)} arquivo(s) Excel encontrado(s):\n")
for a in arquivos:
    print(f"  {a}")

print()

for arquivo in arquivos:
    processar_excel(arquivo)

print("\n" + "="*50)
print("Todos os downloads concluídos.")
input("\nEnter para sair...")