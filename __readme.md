# XBIOM-1

## Particle Swarm Optimization (PSO)
Particle Swarm Optimization (PSO) je přírodou inspirovaný optimalizační algoritmus, který byl poprvé představen Jamesem Kennedym a Russellem Eberhartem v roce 1995. Inspiraci čerpá z kolektivního chování živočichů, zejména hejn ptáků nebo rojů hmyzu, které hledají potravu v prostoru.

Principem PSO je to, že každá částice (angl. particle) představuje kandidátní řešení v prostoru hledání. Celé hejno částic se pohybuje v tomto prostoru a iterativně upravuje svou pozici podle dvou hlavních faktorů:

Vlastní zkušenost – každá částice si pamatuje nejlepší řešení, které dosud sama objevila, tzv. personal best nebo $p_{best}$.

Kolektivní zkušenost – částice sleduje také nejlepší řešení nalezené celým rojem, tzv. global best nebo $g_{best}$.

Pohyb částice je určen její rychlostí, která se v každé iteraci aktualizuje podle rovnice:

$$
v_i(t+1)=w.v_i(t)+c_1.r_1.(p_{best,i}-x_i(t))+c_2.r_2.(g_{best,i}-x_i(t))
$$

$$
x_i(t+1)=x_i(t)+v_i(t+1)
$$

Kde:

$x_i$ = pozice částice

$v_i$ = rychlost částice

$w$ = váha setrvačnosti, která udržuje pohuyb částice

$c_1,c_2$ = koeficienty učení (určují vliv vlastní a kolektivní zkušenosti)

$r_1,r_2$ = náhodná čísla z intervalu $[0,1]$

Díky těmto rovnicím částice oscilují mezi svým osobním nejlepším řešením a globálním nejlepším řešením, což umožňuje kombinovat **exploraci** (prozkoumávání prostoru) a **exploataci** (zpřesňování řešení).

### Vlastnosti
Je jednoduchý na implementaci – stačí pracovat s vektory pozic a rychlostí.

Je stochastický algoritmus – obsahuje náhodné složky, takže může procházet různými oblastmi prostoru.

Může snadno pracovat s více dimenzemi (každá částice má souřadnice ve vícerozměrném prostoru).

## Kapur's entropy
Kapurův algoritmus je globální metoda prahování obrazu, která hledá optimální práh (nebo prahy) tím, že maximalizuje Shannonovu entropii oddělených tříd.

Jinými slovy:
- rozdělení histogramu obrazu na dvě části podle prahu $T$
- výpočet míry neuspořádanosti (informace) v každé části
- výběr prahu $T$, který maximalizuje součet entropií obou částí

Entropie je vysoká, když jsou hodnoty ve třídě rovnoměrně rozloženy (více informací).
Pokud je práh „na správném místě“, tak třídy před a za prahem mají maximum informací → to znamená, že práh dobře odděluje dvě různé oblasti obrazu.
Když je práh špatný, jedna třída má málo hodnot a entropie klesá.

Představme si, že histogram obrazu má $L$ úrovní šedé: $0,1,2,...,L-1$.

Počty pixelů na jednotlivých úrovních jsou $h_0,h_1,...,h_{L-1}$.

Normalizovaný histogram (pravděpodobnosti) je:

$$
p_i=\frac{h_i}{\sum_{j=0}^{L-1}h_j}
$$

Pokud zvolíme práh $T$:
- Třída 1: úrovně $0 ... T$

    Pravděpodobnostní distribuce: $p_0,p_1,...,p_T$

    Součet pravděpodobností: 

    $$
    P_1=\sum_{i=0}^{T}p_i
    $$

- Třída 2: úrovně $T+1 ... L-1$
    Součet pravděpodobností:

    $$
    P_2=\sum_{i=T+1}^{L-1}p_i
    $$

Entropie každé třídy:

$$
H_1=-\sum_{i=0}^{T}\frac{p_i}{P_1}\ln{\frac{p_i}{P_1}}
$$

$$
H_2=-\sum_{i=T+1}^{L-1}\frac{p_i}{P_2}\ln{\frac{p_i}{P_2}}
$$

Celková entropie:

$$
H(T)=H_1+H_2
$$

### Optimalizace
- Pro každý možný práh $T$ se vypočte $H(T)$.
- Vybere se takový $T^*$, pro který je $H(T)$ maximální.

To se dá udělat:
- **Brute force** (pro všechny možné prahy, pokud máš málo úrovní)

- **Optimalizací** (např. PSO, GA, ACO) pro rychlost při větším počtu prahů.

### Poznámky k implementaci
Protože byl algoritmus nestabilní, musel jsem provést dodatečné úpravy. Konkrétně jsem zavedl penalizaci pro cástice, které se dostanou mimo rozsah. To zvýšilo stabilitu výsledné masky.

## Proč je to dobré na termální snímky
Na termálním snímku mají studené oblasti jiný rozptyl intenzit než horké.

Kapur hledá práh, kde rozdělení pixelů na „studené“ a „horké“ maximalizuje informaci. To obvykle odpovídá místu, kde histogram má přirozený „zlom“.

# Block clustering
Tato metoda je inspirovaná tím, že místo práce s jednotlivými pixely (kterých mohou být miliony v každém snímku) se obraz rozdělí na bloky pevné velikosti (např. 8×8 nebo 16×16 pixelů). Každý blok je pak reprezentován jednou hodnotou – obvykle průměrnou intenzitou (v případě grayscale obrazu) nebo průměrem přes barevné kanály. Tím se počet dat dramaticky sníží.

## Rozdělení obrazu na bloky
Nechť máme obraz

$$
I \in \mathbb{R}^{H \times W}
$$

, kde $H$ je výška a $W$ šířka obrazu.  
Obraz rozdělíme na bloky o velikosti $B \times B$. Celkový počet bloků je:

$$
N = \frac{H}{B} \cdot \frac{W}{B}.
$$

Každý blok $k$ reprezentujeme jednou hodnotou (průměrná intenzita):

$$
m_k = \frac{1}{B^2} \sum_{i=1}^{B} \sum_{j=1}^{B} I_{k}(i,j),
$$

kde $I_{k}(i,j)$ jsou pixely v bloku $k$.

Dostaneme tedy vektor průměrů:

$$
\mathbf{m} = (m_1, m_2, \dots, m_N).
$$

## Clustering bloků
Chceme rozdělit bloky do $C$ clusterů (typicky $C=2$: horké/studené).  
Označme centroidy

$$
\mathbf{c} = (c_1, c_2, \dots, c_C)
$$.

Každý blok $m_k$ se přiřadí ke clusteru:

$$
\text{assign}(m_k) = \arg\min_{j \in \{1,\dots,C\}} \; |m_k - c_j|.
$$

## Optimalizační problém
Klasické clusteringové kritérium (jako v k-means) minimalizuje tzv. **sum of squared errors (SSE)**:

$$
J(\mathbf{c}) = \sum_{k=1}^{N} \min_{j \in \{1,\dots,C\}} \; (m_k - c_j)^2.
$$

Naším cílem je nalézt centroidy $\mathbf{c}^*$, které minimalizují $J$:

$$
\mathbf{c}^* = \arg\min_{\mathbf{c}} J(\mathbf{c}).
$$

# PSO + Kapurova entropie pro segmentaci obrazu
## Proč tuto kombinaci?
Nevýhoda Kapurovy metody je, že při vícenásobném prahování (multi-level thresholding) roste výpočetní složitost exponenciálně – pro 2 prahy je třeba prohledat $255^2$ kombinací, pro 3 prahy už $255^3$.
Proto se hodí použít optimalizační algoritmus, který efektivně prohledá prostor možných prahů bez nutnosti testovat všechny kombinace.

## Proč PSO?
PSO je vhodné, protože dokáže rychle prohledávat velký spojitý prostor a najít řešení blízké globálnímu maximu.
Každá částice v PSO zde reprezentuje kandidátní sadu prahů $[T_1,T_2,...T_k]$.

Hodnotící funkce (fitness) je dána Kapurovou entropií – čím větší entropie, tím lepší je segmentace.

PSO tak iterativně hledá optimální kombinace prahů, aniž by bylo nutné zkoušet všechny možnosti.

## Jak to funguje krok za krokem:
### Inicializace:
Vygeneruje se roj částic, kde každá částice má náhodné prahy $[T_1,T_2,...T_k]$ v intervalu $[0,255]$.

### Vyhodnocení (fitness):
Pro každou částici se spočítá Kapurova entropie pro prahy, které částice nese.

Pokud hledáme jednoúrovňový práh → fitness = entropie rozdělení obrazu na dvě třídy.

Pokud vícenásobný → fitness = součet entropií všech tříd.

### Aktualizace pozic:
Podle PSO rovnic každá částice upraví svoje prahy tak, aby se přiblížila vlastnímu dosavadnímu nejlepšímu řešení a globálně nejlepšímu řešení roje.

### Iterace:
Proces se opakuje, dokud se nezlepší řešení nebo nevyčerpá maximální počet iterací.

### Výsledek:
Nejlepší nalezená kombinace prahů je použita pro prahování obrazu, čímž získáme masku horkých oblastí.

## Výhody tohoto přístupu
Rychlost – PSO umožní řešit multi-level prahování, které by brute force metodou nebylo výpočetně možné.

**Kvalita segmentace – protože fitness funkce je přímo Kapurova entropie, výsledné prahy maximalizují informační obsah obrazu.**

Flexibilita – snadno lze měnit počet hledaných prahů (např. rozdělit termosnímek na chladné, středně teplé a horké oblasti).


# PSO + Block clustering

## Použití PSO pro hledání centroidů
Místo klasického iteračního k-means použijeme **heuristickou optimalizaci** PSO a fitness funkci:

  $$
  \text{fitness}(\mathbf{c}) = - J(\mathbf{c}),
  $$

  protože PSO maximalizuje fitness.

### Výsledná maska
Po nalezení optimálních centroidů $\mathbf{c}^*$ se každý blok přiřadí ke clusteru. Typicky vybereme „horký cluster“:

$$
\text{hot} = \arg \max_{j} \; c_j,
$$

a výstupní maska $M \in \{0,255\}^{H \times W}$ je definována takto:

$$
M(i,j) =
\begin{cases}
255 & \text{pokud blok } (i,j) \in \text{cluster hot}, \\
0   & \text{jinak}.
\end{cases}
$$

## Implementace
### [**pso_processors.py**](src/pso_processors.py)

```PSO```

vlastní algoritmus PSO

```PSOKapurEntropy```

implementace PSO pro Kapurovu entropii

```PSOKapurEntropyProcessor```

image processing Kapurovou entropií s předzpracováním vstupního snímku

```PSOBlockClustering```

implementace PSO pro block clustering

```PSOBlockClusteringProcessor```

image processing bock clusteringem s předzpracováním vstupního snímku

### [**camera_capture.py**](src/camera_capture.py)

```CameraCapture```

GUI aplikace pro zobrazeni snímků kamery

### [**camera_test.py**](src/camera_test.py)
spouštěcí skript aplikace s možností skládat vedle sebe jednotlivé procesory s různými nastaveními.
