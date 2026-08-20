# psidiananogueira.com.br

Site institucional da psicóloga Diana Nogueira (CRP 06/234614). Site estático, sem build step, servido pelo GitHub Pages.

## Estrutura

```
index.html                  página principal (todas as seções)
privacidade.html            política de privacidade / LGPD
assets/site.css             CSS compartilhado por todas as páginas (design system)
assets/logo.png             logotipo (arquivo de origem, em alta resolução)
assets/foto.png             foto de perfil (arquivo de origem, em alta resolução)
assets/logo-*.webp/.jpg     variantes responsivas do logo, exibido no topo do hero
assets/foto-about-*.webp/.jpg única foto dela no site, na seção "Sobre mim", em variantes responsivas
assets/og-image.jpg         imagem de compartilhamento (1200x630, logo + retrato + tipografia da marca)
assets/favicon.png          favicon
scripts/optimize-images.py  regera as variantes acima a partir dos originais
scripts/fonts/               fontes (Cormorant Garamond/Quicksand, licença SIL OFL) usadas para gerar a og-image
CNAME                        domínio custom do GitHub Pages
robots.txt
sitemap.xml
```

## Editar conteúdo

Todo o texto de cada página está no próprio HTML. O CSS é compartilhado via `assets/site.css`; o JS de cada página é inline, sem dependências além das Google Fonts.

## Design

O visual é uma identidade editorial "clínica particular calma": serifa **Cormorant Garamond** para títulos, sans-serif **Quicksand** para corpo/UI — a paleta e a tipografia originais do site, com cores neutras e restritas (off-white + lavanda/rosa suaves como acento, uma cor escura para texto) derivadas da marca já existente. Os tokens de cor e tipografia ficam no topo de `assets/site.css` (bloco `:root`).

Cada seção da página principal usa um tratamento visual diferente de propósito (para dar ritmo, evitar "tudo em card"): tira de confiança em colunas com divisórias finas, "Sobre mim" com foto + citação editorial, "Minha abordagem" como lista numerada (I–IV), "Psicoterapia para quê" com marcadores de borda lateral, "Benefícios" em colunas simples, e a seção final de contato como um bloco de cor sólida (o momento visual mais forte da página). O logotipo completo aparece no topo do hero (pequeno, ~300px, para não repetir o problema de nitidez de versões antigas) — a Diana pediu para mantê-lo visível, então o cabeçalho combina o logo com a marca tipográfica "Diana Nogueira".

A pedido dela, o site mostra só **uma** foto sua (na seção "Sobre mim") — o hero não repete uma segunda foto.

## Imagens e performance

`assets/logo.png` e `assets/foto.png` são os arquivos de origem, em alta resolução — não são carregados diretamente pelo site. As páginas usam `<picture>` com variantes menores em WebP (com fallback JPEG) geradas a partir deles, o que reduz o peso de cada imagem em mais de 90%. O corte de rosto/tronco (`FOTO_HERO_BOX`, em `scripts/optimize-images.py`) segue existindo só para compor o retrato da imagem de compartilhamento (og-image); o corpo inteiro (`FOTO_ABOUT_BOX`) é o único enquadramento usado na página em si.

Se um desses dois arquivos for substituído (nova foto, novo logo), regenere as variantes:

```
pip install pillow
python3 scripts/optimize-images.py
```

Isso recria `assets/logo-*`, `assets/foto-about-*` e `assets/og-image.jpg` (imagem usada nas prévias de compartilhamento no WhatsApp/redes sociais). Se a foto de origem mudar de pose/enquadramento, ajuste as coordenadas de recorte (`FOTO_HERO_BOX` / `FOTO_ABOUT_BOX`) no topo do script antes de rodar.

## Google Analytics (GA4)

O site já vem com o snippet do GA4 (`gtag.js`) preparado no `<head>` de cada página, junto com eventos customizados (`contact_click`) disparados nos botões de WhatsApp e no link de e-mail (hero, seção de contato, rodapé e botão flutuante), identificando de onde veio o clique via `data-track-location`.

Para ativar:

1. Crie uma propriedade GA4 em [analytics.google.com](https://analytics.google.com) e copie o Measurement ID (formato `G-XXXXXXXXXX`).
2. Substitua as duas ocorrências de `G-XXXXXXXXXX` em **cada** arquivo HTML (`index.html`, `privacidade.html`) — na tag `<script>` que define `window.GA_MEASUREMENT_ID` e na URL do `gtag/js?id=...`.
   ```
   grep -rl "G-XXXXXXXXXX" *.html
   ```
   ajuda a listar todos os arquivos que ainda precisam da troca.
3. Publique. Sem um ID válido, o script simplesmente não envia dados — não é preciso removê-lo em ambiente de testes.

O analytics só é ativado depois que a pessoa visitante aceita o aviso de cookies (ver seção "Privacidade e cookies (LGPD)" abaixo) — isso usa o Google Consent Mode v2, então o `gtag.js` carrega sempre, mas fica em modo "sem armazenamento" até o consentimento ser dado.

## Animações

Efeitos de entrada (hero) e de revelação ao rolar a página (`.reveal` / `.reveal-group`) são feitos com CSS + `IntersectionObserver` e respeitam `prefers-reduced-motion`. O link ativo no menu também é destacado automaticamente conforme a seção visível.

## Privacidade e cookies (LGPD)

Como o site agora coleta dados de navegação via GA4, foram adicionados:

- `privacidade.html`: política de privacidade explicando quais dados são coletados, cookies usados e os direitos da pessoa visitante conforme a LGPD.
- Um aviso de cookies (banner fixo no rodapé) que aparece na primeira visita, com opções "Aceitar" / "Recusar". A escolha é salva em `localStorage` (`diana-cookie-consent`) e controla o Google Consent Mode (`analytics_storage`).

Se o e-mail de contato do site mudar, atualize também o endereço citado em `privacidade.html`.

## Sobre a seção "Ética e confiança" (e por que não há depoimentos)

O site tem uma seção de credenciais/confiança (`#confianca` em `index.html`, hoje a "tira de confiança" logo abaixo do hero) no lugar de depoimentos de pacientes. Isso é proposital: o Código de Ética Profissional do Psicólogo restringe o uso de depoimentos/testemunhos de pacientes como estratégia de divulgação. Evitamos esse risco e, em vez disso, reforçamos sinais de confiança verificáveis (registro no CRP, sigilo profissional, regulamentação do atendimento online) logo no início da página, antes mesmo da seção "Sobre mim". Antes de adicionar qualquer depoimento no futuro, vale confirmar com as normas atuais do Conselho Federal de Psicologia.

## Próximos passos que exigem acesso de conta (fora do código)

Estes itens aumentam a visibilidade do site, mas dependem de login/verificação da própria Diana — não podem ser feitos só editando o repositório:

1. **Google Search Console**: cadastrar `https://psidiananogueira.com.br` em [search.google.com/search-console](https://search.google.com/search-console), verificar a propriedade (por DNS ou meta tag) e enviar `sitemap.xml`.
2. **Perfil da Empresa no Google** (Google Business Profile): cadastrar em [business.google.com](https://business.google.com) como "área de atendimento" (sem endereço público, já que o atendimento é 100% online) — costuma ser uma das fontes de tráfego mais fortes para buscas como "psicóloga online".
3. **GA4**: seguir os passos da seção acima para obter e configurar o Measurement ID real.

## Deploy

Push na branch `main` publica automaticamente (GitHub Pages → Source: Deploy from a branch → `main` / root).

## DNS (registro.br)

```
@    A      185.199.108.153
@    A      185.199.109.153
@    A      185.199.110.153
@    A      185.199.111.153
www  CNAME  cesarnog.github.io.
```
