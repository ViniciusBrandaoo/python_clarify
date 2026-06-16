import requests
import pandas as pd
import sqlite3
import datetime
import time
import random
import os

from bs4 import BeautifulSoup

# =====================================
# CONFIGURAÇÕES
# =====================================

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0 Safari/537.36"
    )
}

baseURL = "https://www.sampaingressos.com.br/templates/ajax/lista_espetaculo.php"

filmes = []

data_hoje = datetime.date.today().strftime("%d-%m-%Y")

bancoDados = r"C:\Users\noturno\Desktop\Python _Vinicius B\banco_filmes.db"

saidaCSV = (
    f"C:/Users/noturno/Desktop/show_sampaingressos_{data_hoje}.csv"
)

pageLimite = 1

pagTempMin = 1
pagTempMax = 5

cardTempMin = 1
cardTempMax = 1

# =====================================
# WEB SCRAPING
# =====================================

for pagina in range(1, pageLimite + 1):

    url = f"{baseURL}?pagina={pagina}&tipoEspetaculo=shows"

    print(f"Coletando dados da página {pagina}: {url}")

    try:
        resposta = requests.get(url, headers=headers, timeout=20)
    except Exception as e:
        print(f"Erro ao acessar a página: {e}")
        continue

    if resposta.status_code != 200:
        print(
            f"Erro ao carregar a página {pagina}. "
            f"Código: {resposta.status_code}"
        )
        continue

    soup = BeautifulSoup(resposta.text, "html.parser")

    cards = soup.find_all("div", id="box_espetaculo")

    for card in cards:

        try:
            titulo_tag = card.find("b", class_="titulo")
            local_tag = card.find("span", class_="local")
            horario_tag = card.find("span", class_="horario")

            titulo = titulo_tag.text.strip() if titulo_tag else "N/A"
            local = local_tag.text.strip() if local_tag else "N/A"
            horario = horario_tag.text.strip() if horario_tag else "N/A"

            if titulo != "N/A":

                filmes.append(
                    {
                        "Titulo": titulo,
                        "Local": local,
                        "Horario": horario,
                    }
                )

            else:
                print("Cartão sem título (ignorado)")

            time.sleep(random.uniform(cardTempMin, cardTempMax))

        except Exception as e:
            print(f"Erro ao processar cartão: {e}")

    time.sleep(random.uniform(pagTempMin, pagTempMax))

# =====================================
# DATAFRAME
# =====================================

df = pd.DataFrame(filmes)

print("\nPrévia dos dados:")
print(df.head())

# =====================================
# EXPORTAR CSV
# =====================================

try:
    df.to_csv(
        saidaCSV,
        index=False,
        encoding="utf-8-sig",
        quotechar="'",
        quoting=1,
    )

    print(f"\nCSV salvo com sucesso:")
    print(saidaCSV)

except Exception as e:
    print(f"Erro ao salvar CSV: {e}")

# =====================================
# BANCO SQLITE
# =====================================

try:

    pasta_banco = os.path.dirname(bancoDados)

    if not os.path.exists(pasta_banco):
        raise FileNotFoundError(
            f"Pasta não encontrada: {pasta_banco}"
        )

    print(f"\nConectando ao banco:")
    print(bancoDados)

    conn = sqlite3.connect(bancoDados)

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Titulo TEXT,
            Local TEXT,
            Horario TEXT
        )
        """
    )

    for evento in filmes:

        try:

            cursor.execute(
                """
                INSERT INTO shows
                (Titulo, Local, Horario)
                VALUES (?, ?, ?)
                """,
                (
                    evento["Titulo"],
                    evento["Local"],
                    evento["Horario"],
                ),
            )

        except Exception as e:

            print(
                f"Erro ao inserir o evento "
                f"{evento['Titulo']} "
                f"no banco de dados. "
                f"Erro: {e}"
            )

    conn.commit()

    print("Dados inseridos com sucesso no SQLite.")

except Exception as e:

    print(f"\nErro ao trabalhar com o banco de dados:")
    print(e)

finally:

    try:
        conn.close()
    except:
        pass

# =====================================
# FINALIZAÇÃO
# =====================================

print("-------------------------------------")
print("Dados raspados com sucesso!")
print("Obrigado por usar o BOT")
print("Feito com amor por VSB")