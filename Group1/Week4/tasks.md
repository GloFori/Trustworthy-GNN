# method

## augmentations

we consider 2 types of augmentations on graphs:
1. feature-space augmentations ( operating on init node features ) ( e.g. masking or adding Gaussian noise )
2. structure-space augmentations and corruptings ( operating on graph structure ) ( e.g. adding or removing connectiveities, sub-sampling, generating global views using shortest dst or generating diffusion matrices )

former aug. problem:
1. bechmarks do not carry initial node features
2. degrades the performance

-> using aug.2

---

实验得 aug.2-generating diffusion matrices the best.

we treating the two matrices ( ori & diffusion ) as two congruent views of the same graph's structure

diffusion is formulated as Eq.1

$$
S = \Sigma_{k=0}^\infty \Theta_kT^k,\ S\in\mathbb{R}^{n\times n}  \tag{1}
$$

where $T$ is the generalized transition matrix.

$$
\begin{aligned}
adjacency\ matrix:\ &A\in\mathbb{R}^{n\times n}  \\
diagonal\ degree\ matrix:\ &D\in\mathbb{R}^{n\times n}  \\
\end{aligned}  \\
T = AD^{-1}
$$

so $T$ is normalize the adj mat ( $D^{-1}$ is the reciprocal of the **value** of $D$ )

in Eq.1 the $\Theta$ is the weighting coefficient which determines the ratio of global-local information.

$$
\Theta\;\ s.t.\ \Sigma_{k=0}^\infty\theta_k = 1,\ \theta_k\in [0,1]
$$

and for $\theta_k$

$$
\theta_k = \alpha(1-\alpha)^k = \frac{e^{-t}t^k}{k!}
$$

where $\alpha$ denotes teleport probability in a random walk, and $t$ is diffusion times

so the heat kernel & Personalized PageRank ( PPR ) is :

$$
\begin{aligned}
S^{heat} &= exp(tAD^{-1}-t)  \\
S^{PPR} &= \alpha[I_n - (1-\alpha)D^{-\frac{1}{2}}AD^{-\frac{1}{2}}]^{-1}
\end{aligned}
$$

<font size=5>**这里为什么这样，并且这样与 diffusion 有什么关系？**</font>

## Encoder

using GCN method

input: $A\ S\ X\ \Theta$
1. $A$ : ori adj mat $\in\mathbb{R}^{n\times n}$
2. $S$ : diffusion mat ( adj + ind ) $\in\mathbb{R}^{n\times n}$
3. $X$ : init node features $\in\mathbb{R}^{n\times d_x}$
4. $\Theta$ : the network parameters $\in\mathbb{R}^{d_x\times d_h}$
    - $d_x$ : dim of init node features
    - $d_h$ : dim of output features

GCN layer: $\sigma(\tilde{A}X\Theta)$ and $\sigma(SX\Theta)$

where $\tilde{A} = \tilde{D}^{-\frac{1}{2}}\hat{A}\tilde{D}^{-\frac{1}{2}}$ , $\tilde{D}$ is the degree mat of $\hat{A} = A+I_N$

$$
g_\theta(.)/g_\omega(.) : \mathbb{R}^{n\times n}[\cdot\mathbb{R}^{n\times d_x}\cdot\mathbb{R}^{d_x\times d_h}] \rightarrow \mathbb{R}^{n\times d_h}
$$

$\theta$ repre. original mat parameters  
$\omega$ repre. diffusion mat parameters  

And then 2 hidden layer MLP $f_\psi(x) = PReLU(w_\psi^Tx)$

$$
f_\psi(.) : \mathbb{R}^{n\times d_h} \rightarrow \mathbb{R}^{n\times d_h}
$$

so we have the two set of node features of ori & diffusion graph

$$
H^\alpha = f_\psi(g_\theta(.))  \\
H^\beta = f_\psi(g_\omega(.)) \in\mathbb{R}^{n\times d_h}
$$

---

then for each view, we use a readout function similar to JK-Net to aggregate the node repre.

$$
\vec{h_g} = \sigma(\Vert_{l=1}^L(\Sigma_{i=1}^n\vec{h_i^l})\cdot W)\in\mathbb{R}^{1\times d_h}  \tag{2}
$$

where $W\in\mathbb{R}^{(L\times d_h)\times d_h}$ is the network parameters.

Eq.2 sum all nodes' repre. of a GCN layer ( $\rightarrow\mathbb{R}^{1\times d_h}$ ) and concat all layers' res ( $\rightarrow\mathbb{R}^{L\times d_h}$ ). and then $\cdot W$ ( $\rightarrow\mathbb{R}^{1\times d_h}$ )

then 2 hidden layer MLP $f_\phi(x) = PReLU(w_\phi^Tx)$

finally get the graph repre. $\vec{h_g^\alpha}\ \vec{h_g^\beta}$ and node repre. $H^\alpha\ H^\beta$

for every view: init node features ---GCN1---> $\vec{h^1}$ ---GCN2---> ... ---GCNL---> $\vec{h^L}$ -> $\vec{h_g}$ & $H^{\cdot}$

## Training

so we have the fuction $g_\cdot\ f_\cdot$ ,and $g_\cdot$ is GCN fuction, $f_\cdot$ is MLP function, and the parameters index are $\theta\ \omega\ \psi\ \phi$

and we should learn the rich node and graph level repre. that are agnostic to down-stream tasks -> max the Deep InfoMax of diff. view

so our optimize function:

$$
max_{\theta\ \omega\ \psi\ \phi}\ \frac{1}{|\mathscr{G}|}\Sigma_{g\in\mathscr{G}}\{\frac{1}{|g|}\Sigma_{i=1}^{|g|}[MI(\vec{h_i^\alpha, h_g^\beta}) + MI(\vec{h_i^\beta, h_g^\alpha})]\}  \tag{3}
$$

$g$ is the sub-sampled graph of one view and select the exact nodes and edges from the other view. And $|\mathscr{G}|$ is the number of sub-sampled graphs.

$MI(.,.)$ takes in a node repre. from one view ( $\vec{h_i^\alpha}$ ) and a graph repre. from another view ( $\vec{h_g^\beta}$ ). Here we simply dot product between them

$$
MI(\vec{h_i^\alpha, h_g^\beta}) = \vec{h_i^\alpha}\cdot\vec{h_g^\beta}^T
$$

( $\mathbb{R}^{1\times d_h}\cdot\mathbb{R}^{d_h}\rightarrow\mathbb{R}$ )

<font size=5>**根据伪代码看，似乎用到的不是原始图和扩散图，而是扩散了两次？**</font>
