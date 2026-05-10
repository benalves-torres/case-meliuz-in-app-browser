import pandas as pd

# 1. Lista de arquivos
arquivos = [
    'visit_url_metadata.csv', 
    'url_params.csv', 
    'transactions.csv', 
    'visits.csv', 
    'channels.csv', 
    'partners.csv'
]

# Dicionário para guardar os dados
dfs = {}

print("--- CARREGANDO DADOS ---")
for arq in arquivos:
    try:
        # Removi o nrows=1000 para carregar o arquivo TODO agora que você já testou
        dfs[arq.replace('.csv', '')] = pd.read_csv(arq)
        print(f"✅ {arq} carregado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao carregar {arq}: {e}")

# --- PROCESSO DE UNIÃO (JOIN) ---
print("\n--- CONSOLIDANDO BASE DE DADOS ---")

# Unindo Visitas com Metadados (onde está o grupo do teste A/B/C)
if 'visits' in dfs and 'visit_url_metadata' in dfs:
    # Criamos o df_master unindo visitas e os parâmetros de URL
    df_master = pd.merge(dfs['visits'], dfs['visit_url_metadata'], on='visit_id', how='left')
    
    # Unindo com Transações para saber quem comprou
    if 'transactions' in dfs:
        # Usamos how='left' para manter todas as visitas, mesmo as que não viraram compra
        df_master = pd.merge(df_master, dfs['transactions'], on='visit_id', how='left')
        
    # Salvando o resultado final
    df_master.to_csv('dados_consolidados.csv', index=False)
    print("🚀 Sucesso! Arquivo 'dados_consolidados.csv' gerado com todos os dados unidos.")
else:
    print("⚠️ Erro: Tabelas essenciais (visits ou visit_url_metadata) não encontradas.")