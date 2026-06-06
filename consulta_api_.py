import json, requests


nome = input("Qual nome deseja buscar?\nR: ")
resposta = requests.get(f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}")


dadosJson = json.loads(resposta.text)

print(dadosJson[0]['res'][0])