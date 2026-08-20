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
