# Case Técnico — PM Pleno (Ecommerce App)

## Contexto

A Méliuz é uma plataforma de cashback e benefícios. No app, uma compra começa quando o usuário ativa o cashback em uma loja parceira e é direcionado para concluir a jornada no ambiente da loja.

Neste case, você vai analisar um teste A/B/C real relacionado ao **In-App Browser**, o navegador interno usado no app para abrir lojas parceiras. O material visual mostra as experiências testadas e as instrumentações (tracking URLs) geradas em pontos específicos do fluxo.

Seu objetivo é interpretar o problema de produto, reconstruir o teste a partir dos dados e recomendar uma decisão.

## Materiais

Você receberá:

1. **Material visual** com os fluxos das três versões testadas e exemplos de tracking URL bruta gerada pelo app.
2. **CSVs relacionais** com dados já processados pelo BI.
3. Este enunciado com as perguntas e regras do case.

## Teste A/B/C

O teste comparou três versões da experiência:

| Versão | Nome | Descrição visual |
|---|---|---|
| A | Controle | Fluxo padrão do In-App Browser. |
| B | Header | Experiência com opção de saída para navegador externo no header e fluxo de login social. |
| C | Config | Experiência com opção de saída para navegador externo no menu de configurações e fluxo de login social. |

## Como ler o material visual e os dados

O material visual mostra exemplos de tracking URL bruta gerada pelo app. Os CSVs mostram os dados depois do processamento no BI.

A tracking URL não vira uma única tabela. Parte dos parâmetros segue um ETL fixo, como os campos UTM, e aparece em `url_params`. Outros parâmetros são customizados do app, geralmente prefixados com `mz_`, e ficam no JSON de `visit_url_metadata`. Além disso, alguns dados importantes não vêm da URL: a loja/parceiro e o canal final da saída são registrados pelo próprio evento de saída.

Na prática:

| Dado na URL ou no evento | Como usar nos CSVs |
|---|---|
| `utm_content` | Identifica feature ou superfície em `url_params.utm_content`. Use `visits.url_param_id` para relacionar com `url_params.url_param_id`. |
| `utm_term` | Detalhe opcional em `url_params.utm_term`; pode estar vazio. Use `visits.url_param_id` para relacionar com `url_params.url_param_id`.|
| `mz_test_gotoexternalbrowser` | Identifica a variante A/B/C no JSON de `visit_url_metadata.tracking_url_params`. Use `visits.visit_id` para relacionar com `visit_url_metadata.visit_id`|
| `mz_redirect` | Indica o destino bruto no JSON de `visit_url_metadata` e o canal tratado em `channels.channel_name`. |
| Loja/parceiro | Não vem de UTM; use `visits.partner_id` relacionado com `partners.partner_id`. |
| Compra atribuída | Relacione `transactions.visit_id` com `visits.visit_id` para identificar compras atribuídas a cada saída. |

Observações importantes:

- Sempre que o usuário clica em ativar cashback, a aplicação chama a URL de redirecionamento e envia parâmetros que ajudam a identificar origem, feature, teste, versão e outros detalhes da saída.
- `utm_content` indica a feature ou superfície que gerou a saída.
- `utm_term` é um campo auxiliar livre. Ele pode estar vazio ou carregar um detalhe adicional da feature.
- Parâmetros customizados do app, como `mz_test_gotoexternalbrowser`, `mz_redirect` ou qualquer `mz_*`, podem ser enviados na tracking URL e ficar disponíveis em `visit_url_metadata.tracking_url_params` quando não existem como colunas fixas do ETL de UTMs.
- A loja/parceiro não deve ser inferida por `utm_term`. Ela já vem registrada na saída e deve ser analisada por `visits.partner_id`.
- Nos CSVs, alguns valores de UTM foram normalizados para facilitar análise: por exemplo, `external_browser_modal` aparece como `EXTERNAL_BROWSER_MODAL`.

## Exemplos de tracking URLs brutas

O material visual ajuda a entender a jornada. Para evitar ambiguidade na leitura das URLs, abaixo estão exemplos brutos de tracking URL geradas pelo app em cada tipo de saída.

| Situação | Exemplo |
|---|---|
| Controle A - saída base InApp | `https://www.meliuz.com.br/redirecionar?utm_source=app&utm_medium=ios&utm_content=partner_page&utm_term=&user_id=USER_123&mz_test_gotoexternalbrowser=a&mz_redirect=inapp` |
| Header B - saída base InApp | `https://www.meliuz.com.br/redirecionar?utm_source=app&utm_medium=ios&utm_content=partner_page&utm_term=&user_id=USER_123&mz_test_gotoexternalbrowser=b&mz_redirect=inapp` |
| Header B - saída pelo header | `https://www.meliuz.com.br/redirecionar?utm_source=app&utm_medium=ios&utm_content=external_browser_modal&utm_term=header&user_id=USER_123&mz_test_gotoexternalbrowser=b&mz_redirect=browserdefault` |
| Header B - saída por login social | `https://www.meliuz.com.br/redirecionar?utm_source=app&utm_medium=ios&utm_content=external_browser_modal&utm_term=login&user_id=USER_123&mz_test_gotoexternalbrowser=b&mz_redirect=browserdefault` |
| Config C - saída base InApp | `https://www.meliuz.com.br/redirecionar?utm_source=app&utm_medium=ios&utm_content=partner_page&utm_term=&user_id=USER_123&mz_test_gotoexternalbrowser=c&mz_redirect=inapp` |
| Config C - saída pelo menu Config | `https://www.meliuz.com.br/redirecionar?utm_source=app&utm_medium=ios&utm_content=external_browser_modal&utm_term=config&user_id=USER_123&mz_test_gotoexternalbrowser=c&mz_redirect=browserdefault` |
| Config C - saída por login social | `https://www.meliuz.com.br/redirecionar?utm_source=app&utm_medium=ios&utm_content=external_browser_modal&utm_term=login&user_id=USER_123&mz_test_gotoexternalbrowser=c&mz_redirect=browserdefault` |

## Dados entregues

| Arquivo | Grão | Descrição |
|---|---|---|
| `visits.csv` | Uma linha por saída/click | Saídas do usuário para loja parceira, com IDs anonimizados e chaves para dimensões. |
| `transactions.csv` | Uma linha por compra atribuída | Compras atribuídas a uma saída, com valores financeiros. |
| `url_params.csv` | Uma linha por conjunto de parâmetros | Parâmetros de origem e acionamento capturados na URL de tracking. |
| `visit_url_metadata.csv` | Uma linha por saída/click | JSON com parâmetros customizados da tracking URL. |
| `partners.csv` | Uma linha por parceiro | Parceiros anonimizados. |
| `channels.csv` | Uma linha por canal | Canal final registrado para a saída. |

## O que você precisa entregar?

### Entrega 1 — Análise do teste e recomendação

Responda:

1. Por que um app de cashback teria um In-App Browser?
2. Qual problema de produto este teste parece tentar resolver?
3. Qual trade-off existe entre manter o usuário no In-App Browser e permitir saída para navegador externo?
4. Qual hipótese cada variante parece testar?
5. Como você definiria e calcularia a métrica de sucesso do teste usando os dados disponíveis?
6. Qual versão deve ser implementada para os usuários? Por quê?
7. Assumindo que você fosse responsável por analisar dezenas de testes como este por semana ou por mês, como estruturaria uma solução escalável para ingestão dos dados, análise, discussão dos resultados e geração de relatórios para os times envolvidos?

Além das respostas, esperamos que sua entrega inclua:

1. **Análise estruturada dos dados**
   - Limpeza e tratamento dos dados.
   - Identificação das variantes A, B e C a partir dos parâmetros disponíveis.
   - Visualizações ou tabelas que suportem sua conclusão.

2. **Recomendação fundamentada**
   - Qual versão implementar.
   - Qual o impacto esperado.
   - Quais riscos, limitações ou cuidados considerar.

3. **Insights adicionais**
   - O que os dados revelam além da pergunta principal.
   - Como interpretar as saídas normais da tela do parceiro e as saídas externas geradas por `login`, `header` e `config`.
   - Que novas perguntas você faria se tivesse mais tempo ou dados.

4. **Processo, ferramentas e escalabilidade**
   - Descrição do processo de análise, ferramentas usadas e decisões tomadas durante a análise.
   - Como você validou os resultados e reduziu risco de erro na análise.
   - Como sua abordagem poderia ser reutilizada para analisar outros testes de forma recorrente.

### Entrega 2 — Próxima melhoria

Responda:

1. Com base nos aprendizados da Entrega 1, qual deve ser a próxima melhoria ou teste do In-App Browser? Por quê?
2. Como você construiria a PRD dessa melhoria, considerando o contexto do produto e os trade-offs envolvidos?
3. Quais parâmetros de tracking você usaria para instrumentar essa melhoria e como validaria a instrumentação antes do lançamento?
4. Como você testaria essa melhoria e quais critérios usaria para decidir se ela é um sucesso, fracasso ou precisa de iteração?
5. Como você levaria a sua PRD para engenharia desenvolver? A resposta esperada deve ser o material que você entregaria para que o time de engenharia consiga transformar especificação técnica e plano de implementação.

Esperamos que suas respostas contenham:

1. **PRD da melhoria proposta**
   - Contexto de negócio.
   - Problema e oportunidade.
   - Hipótese.
   - Solução proposta.
   - Escopo do MVP.
   - Critérios de aceite.
   - Instrumentação.
   - Métricas de sucesso e guardrails.
   - Riscos, dependências e fora de escopo.
   - Outros pontos que você considerar relevantes.

2. **Quebra da PRD em tasks para engenharia**
   - Quais entregáveis técnicos seriam necessários para implementar a melhoria.
   - Quais parâmetros de tracking, eventos e propriedades seriam necessários.
   - Se for necessário, como você dividiria o trabalho em pequenos entregáveis.

3. **Diagnóstico e hipótese**
   - Qual problema ou oportunidade você identificou.
   - Por que vale priorizar isso agora.

4. **Plano de instrumentação**
   - UTMs, parâmetros `mz_*`, eventos e propriedades necessários.
   - Exemplo de tracking URL ou payload.
   - Como validar a instrumentação antes do lançamento.

5. **Plano de coleta e análise**
   - Como testaria a melhoria.
   - Métrica primária, métricas secundárias e guardrails.
   - Como decidir sucesso, fracasso ou iteração.

## Regras gerais

- **Prazo:** 5 dias corridos a partir do recebimento.
- **Formato de entrega:** Pode ser repositório no GitHub, planilha, apresentação, PDF, ou outro formato que deixe seu raciocínio, análise e proposta fáceis de revisar.
- **Ferramentas:** use o que preferir, incluindo ferramentas de IA como ChatGPT, Codex, Claude Code, Gemini, GitHub Copilot ou outras.
- **Dúvidas:** podem ser enviadas por e-mail.

## O que avaliamos

| Competência | Entrega 1 | Entrega 2 |
|---|---|---|
| Pensamento analítico | Rigor na reconstrução do teste, métricas corretas e leitura crítica | Diagnóstico conectado aos dados |
| Tomada de decisão | Recomendação clara e bem fundamentada | Priorização e trade-offs do MVP |
| Product thinking | Interpretação do comportamento do usuário | Qualidade da solução proposta |
| Instrumentação | Uso correto dos parâmetros disponíveis | UTMs, parâmetros `mz_*`, eventos, propriedades e validação |
| Execução com engenharia | Clareza do caminho de decisão | PRD traduzida em pequenos entregáveis executáveis |
| Design de experimento | Consciência estatística e limitações | Plano de teste e critérios de decisão |
| Processo e escalabilidade | Método, reprodutibilidade, uso consciente de ferramentas e proposta escalável | Capacidade de transformar análise recorrente em sistema/processo |
| Comunicação | Clareza da narrativa e visualizações | Storytelling da PRD e da proposta |
