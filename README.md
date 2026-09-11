# sigma-seguros.eu

Site institucional da SIGMA. HTML estático, sem dependências externas em tempo
de execução.

## Estrutura

```
build.py              Gera as páginas (conteúdo PT e EN)
assets/css/           Folha de estilos
assets/fonts/         Inter (SIL Open Font License)
assets/img/           Logótipo, fotografias e ícones
index.html, en/, ...  Páginas geradas — commitadas tal como ficam
```

## Alterar o site

O conteúdo vive em `build.py`, nas constantes `*_PT` e `*_EN`. Depois de editar:

```sh
python3 build.py
git add -A && git commit -m "..." && git push
```

As páginas são servidas directamente a partir do ramo `main`, sem passo de
build no servidor. Fica publicado cerca de um minuto depois do push.

## Pré-visualizar localmente

```sh
python3 -m http.server 8000
```

## Licenças

Inter está sob a SIL Open Font License 1.1. O restante conteúdo — textos,
logótipo e imagens — é propriedade da SIGMA.
