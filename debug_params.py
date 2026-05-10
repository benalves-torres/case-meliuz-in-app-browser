import pandas as pd

df = pd.read_csv('dados_consolidados.csv')

print("--- VALORES MAIS COMUNS EM TRACKING_URL_PARAMS ---")
# Mostra os 20 valores que mais aparecem para entendermos o padrão
print(df['tracking_url_params'].value_counts().head(20))