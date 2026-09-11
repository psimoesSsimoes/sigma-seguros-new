# Publicação

O site é servido directamente a partir do ramo `main` (GitHub Pages, "Deploy from
a branch"). Não há passo de build no servidor: os `.html` são gerados localmente
por `build.py` e commitados tal como ficam.

**Settings -> Pages -> Source: Deploy from a branch -> `main` / `(root)`**

Com este modo, o ficheiro `CNAME` na raiz **é usado** e define o domínio
personalizado (`sigma-seguros.eu`). O `.nojekyll` impede que o GitHub tente
processar o site com Jekyll.

## Alterar o site

```sh
python3 build.py
git add -A && git commit -m "..." && git push
```

O GitHub publica em ~1 minuto.

## Se um dia quiseres usar GitHub Actions

Existe um workflow de exemplo no histórico (commit `aa20eeb`, ficheiro
`.github/workflows/deploy.yml`). Para o repor é preciso um token com o scope
`workflow`. Nesse modo, atenção: o `CNAME` passa a ser ignorado e o domínio
tem de ser definido apenas nas Settings.
