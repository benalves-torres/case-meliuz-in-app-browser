# 📄 Relatório Final: Case In-App Browser (Méliuz)

Este documento detalha o processo de análise, o diagnóstico do experimento e o plano de implementação da solução recomendada.

---

## 🟢 PARTE 1: Entrega 1 — Análise e Recomendação

### 1.1 Diagnóstico Estratégico

**Por que um app de cashback usa um In-App Browser?**
É uma ferramenta de **atribuição e retenção**. Ele permite injetar cookies de rastreio de forma controlada para garantir que a Méliuz receba a comissão da loja e, consequentemente, o usuário receba seu cashback. Além disso, mantém o usuário no ecossistema da marca.

**Qual problema o teste tenta resolver?**
A fricção de **Login Social**. Navegadores internos muitas vezes bloqueiam pop-ups ou têm restrições que impedem o usuário de logar com Google/Facebook em lojas parceiras. Se o usuário não loga, ele não compra.

**Trade-off da Saída Externa:**
* **Vantagem:** Melhora a UX e resolve o gargalo técnico de login.
* **Risco:** Perda de **atribuição** (tracking) e dispersão do usuário (ele pode abrir outras abas e esquecer a compra).

### 1.2 Análise Estruturada dos Dados

**Processo e Ferramentas:**
1.  **Limpeza e União:** Utilizado Python (Pandas) para unificar 6 bases de dados (>100MB) via `visit_id`.
2.  **Identificação:** Variantes identificadas via JSON parsing na coluna `tracking_url_params` (chaves `mz_test_gotoexternalbrowser` "a", "b" e "c").
3.  **Validação:** Verificação de volumetria (amostragem equilibrada em ~380k visitas/grupo) para evitar viés.

**Resultados Consolidados:**

| Variante | Visitas | Compras | CR% (Conversão) | Saídas Externas | GMV Total |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A (Controle)** | 377.716 | 50.639 | **13,41%** | 0 | R$ 27,3M |
| **C (Config)** | 383.870 | 51.346 | **13,38%** | 7.717 | R$ 27,2M |
| **B (Header)** | 385.757 | 50.543 | **13,10%** | 9.443 | R$ 25,3M |

**Métrica de Sucesso:** Definida como a **Taxa de Conversão (CR%)** somada à **Manutenção do GMV**.

### 1.3 Recomendação Fundamentada

**Versão a implementar: Variante C (Config).**
* **Por quê?** Manteve a conversão estável (quase idêntica ao controle) enquanto resolveu o problema de login para 7.717 usuários. A **Variante B (Header)** falhou ao causar "dispersão ineficiente" (muitas saídas e menor CR%).
* **Impacto esperado:** Redução de churn no funil de login e aumento da satisfação do usuário (NPS).
* **Riscos:** Perda de comissão por falha de cookie no navegador externo.

### 1.4 Insights Adicionais e Escalabilidade

* **Interpretação das Saídas:** As saídas por `header` (B) foram impulsivas; as por `config` (C) foram deliberadas, indicando um usuário com real necessidade técnica.
* **Novas Perguntas:** "Qual o tempo médio de compra para quem sai do app?" e "Essas vendas externas estão sendo atribuídas corretamente pelos parceiros?".
* **Escalabilidade de Análise:** Proponho uma arquitetura baseada em **Lakehouse** com Pipelines automáticos carregando os dados brutos de visitas e transações no **Cloud Storage**. Além disso, proponho a utilização do **Databricks** para o processamento. Criaríamos um job padronizado que consome os dados, aplica as regras de negócio para unir os dados e limpa os parâmetros de tracking. Os dados processados seriam disponibilizados em tabelas Delta. As análises seriam automatizados via notebooks no Databricks, permitindo que qualquer pessoa consulte os resultados apenas inserindo o `experiment_id`.

---

## 🔵 PARTE 2: Entrega 2 — Próxima Melhoria (PRD & Execução)

### 2.1 Diagnóstico e Hipótese
**Oportunidade:** Identificamos que a saída externa é necessária, mas arriscada para a atribuição.
**Hipótese:** Se implementarmos um **"Safe Exit Tracking"** (persistência de parâmetros), garantiremos que os usuários da Variante C não percam o cashback ao sair do app.

### 2.2 PRD da Melhoria

* **Problema:** Possível quebra de tracking no navegador externo.
* **Solução:** Implementar a **Variante C** com injeção automática de `mz_click_id` e `mz_out=true` na URL de destino.
* **Escopo MVP:** Botão no menu de configurações + Página de transição (1.5s) confirmando o rastreio ativo.
* **Métricas:** CR% Externo (Métrica Primária) e Taxa de Re-atribuição (Métrica de Sucesso).
* **Guardrails:** O custo de suporte por "cashback não creditado" deve cair.

### 2.3 Handoff para Engenharia (Tasks)

1.  **Task UI (Front):** Adicionar item "Abrir no Navegador Externo" no menu de opções do In-App Browser, disparando o evento de analytics `click_external_browser`.
2.  **Task Tracking (Back/SDK):** Criar interceptor de URL que anexa os parâmetros de persistência (`mz_click_id` e `mz_out`) antes de disparar o `Intent` do sistema.
3.  **Task Data Engineering (Lakehouse/Databricks):**
    * Configurar pipeline de ingestão dos logs brutos para o **Cloud Storage**.
    * Desenvolver **Job no Databricks** (Spark) para unir visitas e transações via `click_id`.
    * Disponibilizar os dados em **Tabelas Delta** para garantir integridade e permitir auditoria histórica.

### 2.4 Plano de Coleta e Análise

* **Teste:** Roll-out faseado (10% -> 50% -> 100%) para monitorar instabilidade.
* **Decisão:**
    * **Sucesso:** CR% Externo estável vs Controle.
    * **Fracasso:** Queda drástica no GMV ou perda de parâmetros na URL.
    * **Iteração:** Ajustar a visibilidade do botão caso o uso seja menor que o esperado.

---
**Processo de Validação:** A análise foi validada através da consistência entre o volume de cliques em `browserdefault` e a queda proporcional de GMV na variante B, confirmando que a dispersão prejudica o negócio.