# Case Técnico Méliuz — Otimização do In-App Browser

Este repositório contém a análise de dados e a recomendação de produto para o experimento de melhoria do fluxo de login social no In-App Browser da Méliuz.

## 📂 Estrutura do Projeto

- `01_limpeza_e_uniao.py`: Script de pré-processamento e unificação das bases CSV.
- `02_analise_conversao.py`: Script de cálculo de métricas de conversão e comportamento (A/B/C).
- `03_diagnostico_e_recomendacao.md`: Documentação detalhada com as respostas do case.
- `dados_consolidados.csv`: (Ignorado via .gitignore) Base final unificada.

---

## 📊 Resumo do Experimento

O objetivo foi reduzir a fricção de login social permitindo que o usuário finalize a jornada em um navegador externo.

---

## 🛠️ Como Executar
1. Certifique-se de ter os arquivos CSV originais na pasta raiz.
2. Execute o script de união: `python 01_limpeza_e_uniao.py`.
3. Execute a análise de conversão: `python 02_analise_conversao.py`.