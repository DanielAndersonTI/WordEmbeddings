# AI Usage

Registro das decisões relevantes tomadas com apoio de IA neste laboratório.
Não registra todas as conversas — apenas as decisões que mudaram o rumo do trabalho,
no formato **sugestão do agente / decisão minha / justificativa**.
O registro é acrescentado ao fim de cada user story.

---

## US-00 — Planejamento e critérios de execução

Antes de escrever qualquer código, defini com o agente um protocolo de trabalho (user stories,
modelagem, specification, constitution, tasks, TDD) e registrei os critérios em `docs/`.
As decisões abaixo valem para o laboratório inteiro.

### Planejamento

**Sugestão do agente:** aplicar o ciclo completo de TDD — RED, revisão, GREEN, revisão, REFACTOR —
a todas as células do laboratório.

**Decisão:** Rejeitei parcialmente.

**Justificativa:** boa parte do laboratório é exploratória (carregar modelos, gerar gráficos,
analisar saídas), não lógica de domínio. Apliquei o ciclo completo só nas duas tarefas com lógica
determinística de verdade — o avaliador de analogias (Parte 2.1) e o eixo de gênero (Parte 5.1) —
e, no resto, especificação curta seguida de execução e inspeção da saída.

### Especificação

**Sugestão do agente:** ler as células que o professor já entregou prontas e listar, antes de
implementar, tudo o que elas exigem do meu código.

**Decisão:** Aceitei.

**Justificativa:** encontramos exigências que não estão escritas no enunciado — por exemplo, a
coluna `acertou@1` que a célula de erros da Parte 2.2 usa, e os nomes `palavras`, `rotulos`,
`cores` e `X` que a função de plotagem já consome. Sem esse levantamento, esses problemas só
apareceriam como erro na hora de rodar.

### Comportamento não especificado no enunciado

**Sugestão do agente:** no cálculo do acc@1 e do acc@5, remover os termos da consulta (a, b, c) da
lista de vizinhos antes de verificar a posição da resposta.

**Decisão:** Aceitei.

**Justificativa:** é o que faz o avaliador original de Mikolov et al. (2013), que é a referência
citada na Parte 1. Sem esse filtro, uma palavra da própria consulta pode ocupar a primeira posição
e inflar o resultado, deixando meus números incomparáveis com os da Parte 1.

### Declaração de uso de IA

**Sugestão do agente:** declarar o uso de IA na Parte 6 citando as ferramentas e as partes em que
elas foram usadas, de forma consistente com este arquivo.

**Decisão:** Aceitei.

**Justificativa:** o enunciado permite o uso de IA desde que declarado e desde que eu consiga
explicar cada trecho entregue.

---

## US-1 — Avaliação intrínseca

### Montagem da tabela comparativa

**Sugestão do agente:** completar a célula 1.2 avaliando o `wv50` com a mesma função da Parte 1.1
e montar a tabela com uma linha por modelo, usando o coeficiente de Spearman de
`evaluate_word_pairs`.

**Decisão:** Aceitei.

**Justificativa:** é o que o enunciado pede; o agente lembrou que o retorno é
`(pearson, spearman, oov_ratio)` e que portanto o valor útil é `[1][0]`, não `[0][0]`.

### Um erro do agente que só apareceu na execução

**Sugestão do agente:** no gráfico de barras da Parte 1.2, juntar `df50` e `df100` com
`suffixes=(" 50d", " 100d")` e ordenar por `" 100d"`.

**Decisão:** Aceitei, e estava errado.

**Justificativa:** no pandas o sufixo é acrescentado ao nome que já existe, então a coluna se
chama `acurácia 100d` e a ordenação deu `KeyError: ' 100d'`. O erro derrubou a execução inteira
do notebook no primeiro teste de ponta a ponta. Corrigi para `sort_values("acurácia 100d")` e
passei a executar o notebook depois de cada alteração — nenhum teste automatizado cobria essa
célula, porque ela é montagem de gráfico, não regra de negócio.

---

## US-2 — Analogias próprias

### Filtrar os termos da consulta

**Sugestão do agente:** remover `a`, `b` e `c` da lista de vizinhos antes de calcular acc@1 e
acc@5.

**Decisão:** Aceitei.

**Justificativa:** é o que faz o avaliador original de Mikolov et al. (2013). Sem o filtro, uma
palavra da própria consulta pode ocupar a primeira posição e inflar o resultado. O agente
escreveu um teste que reproduz exatamente essa armadilha: com `b` igual a `a`, a consulta cai
sobre `c` e, sem o filtro, `c` seria a primeira resposta.

### Escolha das categorias

**Sugestão do agente:** três categorias fora das que já existem no Google Analogy —
animal → filhote, instrumento → músico, esporte → equipamento.

**Decisão:** Aceitei.

**Justificativa:** são as sugestões do próprio enunciado, e todas as 60 palavras existem no
vocabulário do GloVe (conferi antes de rodar, para não gastar analogias com palavras fora do
vocabulário).

---

## US-3 — `doesnt_match` e polissemia

### Grupos difíceis

**Sugestão do agente:** três grupos difíceis em que o intruso é do mesmo domínio — cores + uma
que também é fruta, animais domésticos + um selvagem, instrumentos de corda + um de percussão.

**Decisão:** Aceitei.

**Justificativa:** o terceiro grupo foi o mais interessante do laboratório justamente porque
**falhou**: o modelo apontou `harp` e não `drum`. Isso deu conteúdo real para a Pergunta 3.1, que
pede um acerto e um erro. Foi sorte de desenho, não planejado.

---

## US-4 — Visualização em espaços reduzidos

### Par "difícil" de categorias

**Sugestão do agente:** usar frutas e cores como o par difícil, porque *orange*, *peach* e
*lemon* pertencem às duas listas.

**Decisão:** Aceitei.

**Justificativa:** é o exemplo que o enunciado sugere, e cria sobreposição de vocabulário de
verdade entre os dois grupos, não apenas proximidade semântica. O resultado confirmou a escolha:
no PCA, frutas e cores são justamente as duas categorias mais próximas, e `orange` cai dentro da
nuvem das cores.

### Parâmetros do t-SNE

**Sugestão do agente:** usar `random_state=42` e `init="pca"`, além da `perplexity` pedida.

**Decisão:** Aceitei.

**Justificativa:** sem semente o layout muda a cada execução e não haveria como comparar as
perplexities; o `init="pca"` torna a posição inicial determinística.

---

## US-5 — Viés de gênero

### Extrair as duas fórmulas como funções

**Sugestão do agente:** em vez de calcular o eixo e as projeções direto na célula, criar
`gender_axis()` e `projection_on_axis()` e chamá-las.

**Decisão:** Aceitei.

**Justificativa:** assim o agente conseguiu testar a fórmula com um espaço vetorial minúsculo,
sem carregar o GloVe, e o teste verificou a fórmula que o enunciado pede — média das diferenças
**normalizadas**, e não a média das diferenças cruas. As duas dão resultados diferentes, e o
teste confirma que ele distingue uma da outra.

### Um erro do agente que o próprio teste pegou

**Sugestão do agente:** usar `sort_values()` para ordenar as projeções.

**Decisão:** Rejeitei depois de ver o teste falhar.

**Justificativa:** a ordenação padrão do pandas não é estável, então profissões com a mesma
projeção trocavam de lugar entre execuções. Trocamos por `sort_values(kind="stable")`. Não
aparecia nenhum número errado na tela — era um ranking que não se repetia.

### Um erro meu, no teste

**Sugestão do agente:** escrever os controles neutros do teste com coordenadas "ortogonais"
arredondadas à mão.

**Decisão:** Rejeitei depois de ver o teste falhar.

**Justificativa:** os controles arredondados não eram exatamente perpendiculares ao eixo
analítico calculado a partir dos pares, e a projeção deles ficava em `3,3e-05` em vez de zero. O
teste acusou. Passei a derivar os controles do próprio eixo calculado no módulo. A lição que
anotei: uma tolerância larga o bastante para aceitar constantes arredondadas também aceitaria um
efeito real — o teste tem de exigir quase zero de verdade.

---

## US-6 — Reflexão final

### Declaração de uso de IA

**Sugestão do agente:** declarar o uso de IA marcando as opções e descrevendo as partes, de
forma consistente com este arquivo.

**Decisão:** Aceitei.

**Justificativa:** o enunciado permite IA desde que declarada e desde que eu consiga explicar
cada trecho entregue. O texto das respostas foi redigido com o agente a partir das saídas reais
do notebook, e a revisão e a responsabilidade final sobre ele são minhas.

### Testes fora do notebook

**Sugestão do agente:** manter os testes em `tests/` (pytest), fora do entregável, e avisar o
professor na própria declaração.

**Decisão:** Aceitei.

**Justificativa:** o enunciado pede só o notebook executado. Os testes ficam no repositório
como material extra e são mencionados na declaração, sem alterar o formato do entregável.

---

## US-B — Bônus: Word2Vec no text8

### Hiperparâmetro variado

**Sugestão do agente:** variar `sg` (CBOW vs Skip-gram), mantendo todo o resto fixo.

**Decisão:** Aceitei.

**Justificativa:** das duas opções que o enunciado sugere, é a que dá mais conteúdo para a
Pergunta B.1 — as duas arquiteturas usam o contexto de formas diferentes, o que conecta direto
com as métricas da Parte 1. O resultado confirmou: o Skip-gram ganhou nas três métricas.

### Um detalhe que só apareceu ao testar

**Sugestão do agente:** guardar o `text8` numa variável e passar essa variável para os dois
treinos.

**Decisão:** Aceitei, depois de conferir.

**Justificativa:** `api.load("text8")` devolve um iterável preguiçoso, não uma lista, e o mesmo
objeto precisa poder ser percorrido duas vezes — uma por treino. Testei isso antes de rodar o
notebook inteiro, e a segunda passagem funciona. Também descobri que o corpus vem em 1701
blocos de ~10 mil palavras, e não uma frase por linha.
