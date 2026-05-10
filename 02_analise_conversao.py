import pandas as pd

# 1. Carregar a base
df = pd.read_csv('dados_consolidados.csv')

# 2. Nova função de rótulo baseada nos dados reais
def rotular_variante(params):
    params = str(params).lower()
    # Buscamos o valor da chave mz_test_gotoexternalbrowser
    if '"mz_test_gotoexternalbrowser":"b"' in params:
        return 'B - Header'
    elif '"mz_test_gotoexternalbrowser":"c"' in params:
        return 'C - Config'
    elif '"mz_test_gotoexternalbrowser":"a"' in params:
        return 'A - Controle'
    else:
        return 'Outros/Invalido'

df['variant_group'] = df['tracking_url_params'].apply(rotular_variante)

# 3. Cálculo de Conversão
analise = df.groupby('variant_group').agg({
    'visit_id': 'nunique',
    'transaction_id': 'nunique',
    'sale_amount': 'sum'
}).rename(columns={'visit_id': 'Visitas', 'transaction_id': 'Compras', 'sale_amount': 'GMV'})

analise['CR_%'] = (analise['Compras'] / analise['Visitas']) * 100

# 4. Análise de Comportamento (O diferencial do seu case)
# Vamos ver quem clicou para sair do App (browserdefault)
df['saiu_do_app'] = df['tracking_url_params'].str.contains('browserdefault').fillna(False)
saida_app = df.groupby('variant_group')['saiu_do_app'].sum()

analise['Usuarios_Saíram_App'] = saida_app

print("\n--- RESULTADOS FINAIS DO TESTE ---")
print(analise.sort_values(by='CR_%', ascending=False))

analise.to_csv('resultado_final_teste.csv')