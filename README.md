# psidiananogueira.com.br

Site institucional da psicóloga Diana Nogueira (CRP 06/234614). Site estático, sem build step, servido pelo GitHub Pages.

## Estrutura

```
index.html          página única (todas as seções)
assets/logo.png     logotipo
assets/foto.png     foto de perfil
assets/favicon.png  favicon
CNAME               domínio custom do GitHub Pages
robots.txt
sitemap.xml
```

## Editar conteúdo

Todo o texto está em `index.html`. CSS e JS são inline — um arquivo só, sem dependências além das Google Fonts.

## Google Analytics (GA4)

O site já vem com o snippet do GA4 (`gtag.js`) preparado no `<head>` de
`index.html`, junto com eventos customizados (`contact_click`) disparados
nos botões de WhatsApp e no link de e-mail (hero, seção de contato, rodapé
e botão flutuante), identificando de onde veio o clique via
`data-track-location`.

Para ativar:

1. Crie uma propriedade GA4 em [analytics.google.com](https://analytics.google.com) e copie o Measurement ID (formato `G-XXXXXXXXXX`).
2. Em `index.html`, substitua as duas ocorrências de `G-XXXXXXXXXX` (na tag `<script>` que define `window.GA_MEASUREMENT_ID` e na URL do `gtag/js?id=...`) pelo ID real.
3. Publique. Sem um ID válido, o script simplesmente não envia dados — não é preciso removê-lo em ambiente de testes.

## Animações

Efeitos de entrada (hero) e de revelação ao rolar a página (`.reveal` /
`.reveal-group`) são feitos com CSS + `IntersectionObserver` e respeitam
`prefers-reduced-motion`. O link ativo no menu também é destacado
automaticamente conforme a seção visível.

## Deploy

Push na branch `main` publica automaticamente (GitHub Pages → Source: Deploy from a branch → `main` / root).

## Pendências

- `assets/logo.png` e `assets/foto.png` foram extraídos do preview do Canva em baixa resolução
  (o design tem exportação bloqueada). Substituir pelos arquivos originais mantendo os mesmos nomes.
- Corrigido em relação ao Canva: e-mail era `psidiananogueira@gmail.com.br`, o correto é `psidiananogueira@gmail.com`.

## DNS (registro.br)

```
@    A      185.199.108.153
@    A      185.199.109.153
@    A      185.199.110.153
@    A      185.199.111.153
www  CNAME  cesarnog.github.io.
```
