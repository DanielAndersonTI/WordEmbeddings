# Laboratório: Word Embeddings com Gensim

**Disciplina:** Modelos de Linguagem de Grande Escala, UFCG  
**Pré-requisito:** notebook *Tutorial: Word Embeddings com Gensim*  
**Entrega:** este notebook executado (Arquivo > Baixar > `.ipynb`), com todas as células rodadas e as respostas escritas preenchidas.

|           Nome               | Matrícula    |
|Daniel Anderson de Souza Silva|0126015852-52M|
|                              |              |

## Objetivos

Ao final do laboratório você deverá ser capaz de:

1. Avaliar embeddings de forma intrínseca (analogias e similaridade de pares) e interpretar os números.
2. Construir e testar analogias e conjuntos de `doesnt_match`, explicando os acertos e os erros.
3. Investigar polissemia em embeddings estáticos.
4. Projetar o espaço vetorial em 2D e discutir o que PCA e t-SNE preservam e distorcem.
5. Medir um viés de gênero no espaço vetorial e refletir sobre suas consequências.

## Regras

- Células marcadas com `# TODO` devem ser completadas por você. Células com **✍️ Resposta** pedem texto curto (3 a 6 linhas).
- **Uso de IA é permitido** para gerar ou ajustar código, desde que você preencha a declaração na Parte 6 e seja capaz de explicar o que cada trecho faz.
- As respostas escritas devem se apoiar nos **resultados que você obteve**, citando números e exemplos do seu notebook.

## Distribuição de pontos

| Parte | Tema | Pontos |
|---|---|---:|
| 1 | Avaliação intrínseca | 2,0 |
| 2 | Analogias próprias | 2,0 |
| 3 | `doesnt_match` e polissemia | 1,5 |
| 4 | Visualização em espaços reduzidos | 2,0 |
| 5 | Viés de gênero | 1,5 |
| 6 | Reflexão final e declaração de uso de IA | 1,0 |
| Bônus | Treinar e comparar Word2Vec no text8 | +1,0 |

---

## Parte 0: Configuração (não vale pontos)

```python
!pip install -q gensim

# Se aparecer erro de compatibilidade com numpy/scipy, reinicie a sessão
# (Ambiente de execução > Reiniciar sessão) e rode novamente a partir daqui.
```

```python
import gensim
import gensim.downloader as api
from gensim.models import Word2Vec
from gensim.test.utils import datapath

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

print("gensim", gensim.__version__)
```

```python
# Carrega dois modelos GloVe (Wikipedia + Gigaword) com dimensões diferentes.
# O download leva 1–3 minutos na primeira vez.
wv50  = api.load("glove-wiki-gigaword-50")
wv100 = api.load("glove-wiki-gigaword-100")
wv = wv100   # modelo principal do laboratório

print(f"Vocabulário: {len(wv):,} palavras | dimensões: {wv50.vector_size} e {wv100.vector_size}")
```

## Parte 1: Avaliação intrínseca (2,0 pontos)

Como saber se um embedding é "bom"? Uma forma é a **avaliação intrínseca**, que testa o espaço vetorial diretamente em tarefas linguísticas, sem treinar um classificador em cima dele. O gensim já traz três conjuntos clássicos:

- **Google Analogy** (`questions-words.txt`, Mikolov et al., 2013): cerca de 19 mil analogias em 14 categorias. As 5 primeiras são **semânticas** (capitais, moedas, família...) e as 9 últimas, **sintáticas** (plural, comparativo, tempo verbal...).
- **WordSim-353**: pares de palavras com notas humanas de **relação** (*relatedness*), por exemplo *coffee–cup* recebe nota alta.
- **SimLex-999**: pares com notas humanas de **similaridade estrita**, por exemplo *coffee–cup* recebe nota baixa, porque café não é parecido com xícara.

Para os pares, a métrica é a **correlação de Spearman** entre as notas humanas e as similaridades de cosseno do modelo.

### 1.1 Analogias por categoria

A célula abaixo já está pronta. Ela avalia o modelo de 100 dimensões e mostra a acurácia por categoria.

```python
def avaliar_analogias_google(modelo, restrict_vocab=100_000):
    acc_total, secoes = modelo.evaluate_word_analogies(
        datapath("questions-words.txt"), restrict_vocab=restrict_vocab
    )
    linhas = []
    for s in secoes:
        n = len(s["correct"]) + len(s["incorrect"])
        if n and s["section"] != "Total accuracy":
            linhas.append({"categoria": s["section"], "n": n,
                           "acurácia": len(s["correct"]) / n})
    return acc_total, pd.DataFrame(linhas)

acc100, df100 = avaliar_analogias_google(wv100)
print(f"Acurácia total (100d): {acc100:.3f}")
df100.style.format({"acurácia": "{:.3f}"})
```

### 1.2 TODO: compare 50d e 100d

Complete a célula para:

1. Avaliar também o `wv50` nas analogias.
2. Avaliar **os dois modelos** em WordSim-353 e SimLex-999 com `modelo.evaluate_word_pairs(datapath("wordsim353.tsv"))` e `datapath("simlex999.txt")`. O método retorna `(pearson, spearman, oov_ratio)`; use o coeficiente de **Spearman** (`spearman[0]`).
3. Montar um `DataFrame` com uma linha por modelo e as colunas `analogias`, `wordsim353` e `simlex999`.

```python
# TODO: avalie wv50 nas analogias
acc50, df50 = ...

# TODO: avalie os dois modelos em WordSim-353 e SimLex-999 (Spearman)
resultados = []
for nome, modelo, acc in [("GloVe 50d", wv50, acc50), ("GloVe 100d", wv100, acc100)]:
    ws  = ...   # Spearman no wordsim353
    sl  = ...   # Spearman no simlex999
    resultados.append({"modelo": nome, "analogias": acc, "wordsim353": ws, "simlex999": sl})

tabela = pd.DataFrame(resultados).set_index("modelo")
tabela.round(3)
```

```python
# TODO: gráfico de barras comparando a acurácia por categoria (50d vs 100d)
# Dica: junte df50 e df100 pela coluna "categoria" e use .plot.barh()
```

**Pergunta 1.1** Quais categorias de analogia o modelo resolve melhor e quais resolve pior? Levante uma hipótese que explique a diferença (pense em frequência das palavras e em quanto o contexto local revela cada relação).

**✍️ Resposta 1.1:**

_(escreva aqui)_

**Pergunta 1.2** O que aconteceu ao passar de 50 para 100 dimensões? Por que a correlação no SimLex-999 é bem menor que no WordSim-353 para os dois modelos?

**✍️ Resposta 1.2:**

_(escreva aqui)_

---

## Parte 2: Suas próprias analogias (2,0 pontos)

### 2.1 TODO: implemente o avaliador

Complete `avaliar_analogias`, que recebe uma lista de tuplas `(a, b, c, d)` representando *a : b :: c : d* e calcula:

- **acc@1**: fração em que `d` é a **primeira** resposta;
- **acc@5**: fração em que `d` está entre as **5 primeiras**.

O parâmetro `metodo` escolhe entre `"add"` (3CosAdd, `most_similar`) e `"mul"` (3CosMul, `most_similar_cosmul`). Analogias com palavras fora do vocabulário devem ser ignoradas e contadas à parte.

```python
def avaliar_analogias(wv, analogias, metodo="add", topn=5):
    acertos1, acertos5, avaliadas, oov = 0, 0, 0, 0
    detalhes = []   # lista de dicts com a, b, c, esperado, previsto_top5
    for a, b, c, d in analogias:
        # TODO: pule (e conte em oov) analogias com palavras fora do vocabulário
        # TODO: chame wv.most_similar ou wv.most_similar_cosmul conforme `metodo`
        # TODO: atualize acertos1, acertos5, avaliadas e detalhes
        pass
    return {"acc@1": acertos1 / max(avaliadas, 1),
            "acc@5": acertos5 / max(avaliadas, 1),
            "avaliadas": avaliadas, "oov": oov}, pd.DataFrame(detalhes)
```

### 2.2 TODO: crie seu conjunto de analogias

Crie **pelo menos 12 analogias**, com no mínimo 4 em cada uma de **3 categorias diferentes** de sua escolha. Evite as categorias que já existem no Google Analogy (capitais, moedas, plural...). Sugestões: animal → filhote, instrumento → músico, país → idioma, empresa → produto, ferramenta → ação, esporte → equipamento, cor → objeto típico.

Lembre-se: o vocabulário do GloVe está **em inglês e em minúsculas**.

```python
minhas_analogias = {
    "categoria_1": [
        # ("dog", "puppy", "cat", "kitten"),
    ],
    "categoria_2": [
    ],
    "categoria_3": [
    ],
}
```

```python
# Avalia cada categoria com os dois métodos (pronto, apenas execute)
linhas, todos_detalhes = [], []
for cat, lista in minhas_analogias.items():
    for metodo in ["add", "mul"]:
        res, det = avaliar_analogias(wv, lista, metodo=metodo)
        linhas.append({"categoria": cat, "método": "3CosAdd" if metodo == "add" else "3CosMul", **res})
        if metodo == "add":
            todos_detalhes.append(det.assign(categoria=cat))

display(pd.DataFrame(linhas).round(2))
detalhes = pd.concat(todos_detalhes, ignore_index=True)
detalhes[~detalhes["acertou@1"]]   # apenas os erros (3CosAdd)
```

**Pergunta 2.1** Compare as categorias e os dois métodos. Em seguida, escolha **dois erros** da tabela acima e explique cada um: a resposta do modelo é absurda ou "quase certa"? Ela revela algo sobre os dados de treino ou sobre a própria relação?

**✍️ Resposta 2.1:**

_(escreva aqui)_

---

## Parte 3: `doesnt_match` e polissemia (1,5 pontos)

### 3.1 TODO: grupos com intruso

Crie **6 grupos** de 4 a 6 palavras, cada um com um intruso:

- 3 grupos **fáceis** (o intruso é de outro domínio, ex.: frutas + um teclado);
- 3 grupos **difíceis** (o intruso é do mesmo domínio, mas difere em algum traço, ex.: animais domésticos + um selvagem, ou cores + uma que também é fruta).

```python
grupos = [
    # (lista_de_palavras, intruso_esperado, "fácil" ou "difícil")
    # (["breakfast", "lunch", "dinner", "car"], "car", "fácil"),
]

for palavras, esperado, nivel in grupos:
    previsto = wv.doesnt_match(palavras)
    marca = "✅" if previsto == esperado else "❌"
    print(f"{marca} [{nivel:7s}] {palavras} → previsto: {previsto} | esperado: {esperado}")
```

### 3.2 TODO: separando sentidos com aritmética vetorial

Embeddings estáticos atribuem **um único vetor** a cada palavra, que mistura todos os seus sentidos. Para cada palavra ambígua da lista:

1. Mostre os 8 vizinhos mais próximos.
2. **Subtraia** uma palavra associada a um dos sentidos e veja os vizinhos que sobram. Exemplo: `wv.most_similar(positive=["bank"], negative=["money"])`.

Complete o dicionário com mais **três** palavras ambíguas à sua escolha.

```python
ambiguas = {
    # palavra: (palavra de um sentido, palavra do outro sentido)
    "bank":  ("money", "river"),
    "apple": ("iphone", "fruit"),
    # TODO: adicione mais 3
}

for palavra, (s1, s2) in ambiguas.items():
    print(f"\n=== {palavra} ===")
    print("vizinhos:       ", [w for w, _ in wv.most_similar(palavra, topn=8)])
    print(f"menos '{s1}':", [w for w, _ in wv.most_similar(positive=[palavra], negative=[s1], topn=8)])
    print(f"menos '{s2}':", [w for w, _ in wv.most_similar(positive=[palavra], negative=[s2], topn=8)])
```

**Pergunta 3.1** Os grupos difíceis enganaram o modelo? Analise um acerto e um erro com base no mecanismo do `doesnt_match`, que calcula a média dos vetores e retorna a palavra mais distante dela.

**✍️ Resposta 3.1:**

_(escreva aqui)_

**Pergunta 3.2** A subtração vetorial conseguiu "isolar" sentidos? Qual sentido é dominante em cada palavra e por quê? Que tipo de modelo resolveria esse problema de forma mais fundamentada?

**✍️ Resposta 3.2:**

_(escreva aqui)_

---

## Parte 4: Visualização em espaços reduzidos (2,0 pontos)

### 4.1 TODO: escolha suas categorias

Defina **5 categorias** com **8 palavras** cada. Ao menos **uma** delas deve ser "difícil" de separar de outra (ex.: *frutas* e *cores*, *esportes* e *países*, *emoções positivas* e *emoções negativas*).

```python
categorias = {
    # "nome": ["palavra1", ..., "palavra8"],
}

palavras, rotulos = [], []
for cat, lista in categorias.items():
    for p in lista:
        if p in wv:
            palavras.append(p); rotulos.append(cat)
        else:
            print("fora do vocabulário:", p)
X = np.array([wv[p] for p in palavras])
cores = dict(zip(categorias, plt.cm.tab10.colors))
print(X.shape)
```

```python
def plotar_2d(coords, titulo, ax=None):
    ax = ax or plt.figure(figsize=(9, 7)).gca()
    for cat in categorias:
        idx = [i for i, r in enumerate(rotulos) if r == cat]
        ax.scatter(coords[idx, 0], coords[idx, 1], color=cores[cat], label=cat, s=40)
        for i in idx:
            ax.annotate(palavras[i], coords[i], xytext=(3, 2), textcoords="offset points", fontsize=8)
    ax.set_title(titulo); ax.grid(alpha=.3)
    return ax
```

### 4.2 TODO: PCA e t-SNE lado a lado

Gere uma figura com **4 subplots**: PCA e t-SNE com `perplexity` igual a 5, 15 e 30. Use `random_state=42`. Mostre no título do PCA a **variância explicada** pelos 2 componentes.

```python
fig, axes = plt.subplots(2, 2, figsize=(16, 13))

# TODO: PCA em axes[0, 0]

# TODO: t-SNE com perplexity 5, 15 e 30 nos demais eixos

axes[0, 0].legend()
plt.tight_layout(); plt.show()
```

### 4.3 TODO: uma relação como direção

Escolha uma **relação** (diferente de gênero e de país → capital, que já aparecem no tutorial) e pelo menos **6 pares** que a exemplifiquem. Use a função `plotar_relacoes` do tutorial, copiada abaixo, para desenhar as setas no plano do PCA.

```python
def plotar_relacoes(pares, titulo):
    ps = [p for par in pares for p in par]
    coords = PCA(n_components=2, random_state=42).fit_transform(np.array([wv[p] for p in ps]))
    plt.figure(figsize=(9, 7))
    for i in range(0, len(ps), 2):
        (x0, y0), (x1, y1) = coords[i], coords[i + 1]
        plt.arrow(x0, y0, x1 - x0, y1 - y0, head_width=0.08, length_includes_head=True, color="gray", alpha=.7)
        plt.scatter([x0], [y0], color="tab:blue"); plt.scatter([x1], [y1], color="tab:red")
        plt.annotate(ps[i], (x0, y0), xytext=(4, 3), textcoords="offset points")
        plt.annotate(ps[i + 1], (x1, y1), xytext=(4, 3), textcoords="offset points")
    plt.title(titulo); plt.grid(alpha=.3); plt.show()

# TODO: defina seus pares e chame plotar_relacoes
meus_pares = []
```

**Pergunta 4.1** Compare PCA e t-SNE: qual separa melhor as suas categorias? O que muda quando a `perplexity` aumenta? Em qual método é legítimo comparar a **distância entre grupos diferentes**? Comente o par de categorias "difícil" que você escolheu.

**✍️ Resposta 4.1:**

_(escreva aqui)_

**Pergunta 4.2** As setas da sua relação ficaram aproximadamente paralelas? Por que esse teste deve ser feito com PCA e não com t-SNE? O que o paralelismo diz sobre o funcionamento das analogias da Parte 2?

**✍️ Resposta 4.2:**

_(escreva aqui)_

---

## Parte 5: Medindo viés de gênero (1,5 pontos)

Bolukbasi et al. (2016) mostraram que é possível identificar uma **direção de gênero** no espaço vetorial e medir o quanto palavras supostamente neutras, como profissões, se inclinam para um dos lados.

### 5.1 TODO: construa o eixo de gênero

1. Calcule o eixo como a **média** das diferenças normalizadas `wv[m] - wv[f]` para os pares definidos abaixo e normalize o resultado (norma 1).
2. Para cada profissão, calcule a **similaridade de cosseno** com o eixo. Valores positivos significam inclinação ao masculino; negativos, ao feminino.
3. Faça um gráfico de barras horizontais ordenado pelo valor.

```python
pares_genero = [("he", "she"), ("man", "woman"), ("his", "her"),
                ("male", "female"), ("boy", "girl"), ("father", "mother")]

profissoes = ["doctor", "nurse", "engineer", "teacher", "programmer", "secretary",
              "scientist", "receptionist", "pilot", "librarian", "ceo", "housekeeper",
              "surgeon", "dancer", "mechanic", "hairdresser", "architect", "nanny",
              "lawyer", "designer"]

def normalizar(v):
    return v / np.linalg.norm(v)

# TODO: eixo de gênero
eixo = ...

# TODO: projeções (cosseno entre wv[p] normalizado e o eixo)
projecoes = pd.Series({p: ... for p in profissoes}).sort_values()

# TODO: gráfico de barras horizontais (cores diferentes para valores positivos e negativos)
```

```python
# Sanidade: palavras com gênero definido devem ficar nos extremos e palavras neutras perto de zero.
# TODO: calcule a projeção de 4 palavras com gênero explícito (ex.: "king", "queen", "actor", "actress")
#       e de 4 palavras que você considera neutras (ex.: "table", "water", "computer", "tree").
```

**Pergunta 5.1** Quais profissões são mais "masculinas" e mais "femininas" no espaço? As palavras de controle se comportaram como esperado? De onde vem esse viés e cite **um** cenário concreto em que ele poderia causar dano em um sistema real que usa esses embeddings.

**✍️ Resposta 5.1:**

_(escreva aqui)_

---

## Parte 6: Reflexão final (1,0 ponto)

**Pergunta 6.1** Em até 8 linhas: você usaria esses embeddings estáticos como representação de entrada em uma aplicação real hoje? Para que tipo de tarefa ainda faz sentido, e em que casos você preferiria embeddings contextuais? Use pelo menos dois resultados deste laboratório como argumento.

**✍️ Resposta 6.1:**

_(escreva aqui)_

### Declaração de uso de IA

Marque e descreva brevemente:

- [ ] Não usei ferramentas de IA.
- [ ] Usei IA para gerar ou corrigir código nas partes: ______
- [ ] Usei IA para revisar o texto das respostas.

**Ferramenta(s) usada(s) e como:** _(ex.: "pedi ao assistente X para implementar o t-SNE em subplots; ajustei os títulos e entendi o parâmetro perplexity")_

> Respostas escritas copiadas de IA sem relação com os **seus** resultados não recebem nota.

---

## Bônus: treinando e comparando Word2Vec (+1,0 ponto)

Treine **dois** modelos Word2Vec no corpus *text8* (≈17 milhões de tokens da Wikipédia em inglês) que difiram em **um único** hiperparâmetro. Sugestões: `sg=0` (CBOW) vs. `sg=1` (Skip-gram), ou `window=2` vs. `window=10`. Avalie os dois com as mesmas métricas da Parte 1 (use `restrict_vocab=30_000` nas analogias) e compare os vizinhos de 3 palavras à sua escolha.

⏱️ Cada treino leva aproximadamente 2 a 6 minutos no Colab, com `epochs=5` e `workers=4`.

```python
FAZER_BONUS = False

if FAZER_BONUS:
    text8 = api.load("text8")
    # TODO: treine modelo_a e modelo_b variando um único hiperparâmetro
    # TODO: tabela com analogias / wordsim353 / simlex999 para os dois
    # TODO: compare os vizinhos de 3 palavras
```

**Pergunta B.1** Qual modelo foi melhor em cada métrica? Relacione o resultado ao hiperparâmetro que você variou. Compare também com o GloVe da Parte 1: por que o GloVe pré-treinado é tão melhor?

**✍️ Resposta B.1:**

_(escreva aqui)_

---

## Referências

- Mikolov et al. (2013). *Efficient Estimation of Word Representations in Vector Space.*
- Pennington, Socher & Manning (2014). *GloVe: Global Vectors for Word Representation.*
- Levy & Goldberg (2014). *Linguistic Regularities in Sparse and Explicit Word Representations.*
- Hill, Reichart & Korhonen (2015). *SimLex-999: Evaluating Semantic Models with (Genuine) Similarity Estimation.*
- Bolukbasi et al. (2016). *Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings.*
- Gonen & Goldberg (2019). *Lipstick on a Pig: Debiasing Methods Cover up Systematic Gender Biases in Word Embeddings But do not Remove Them.*
