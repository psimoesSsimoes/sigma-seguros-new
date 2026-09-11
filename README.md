# sigma-seguros.eu

Site estático da SIGMA — Consultores de Seguros. Sem WordPress, sem PHP, sem base de dados.

## Estrutura

```
index.html                 Início              (gerado)
o-grupo/index.html         O Grupo             (gerado)
inn-health/index.html      Inn Health          (gerado)
contactos/index.html       Contactos           (gerado)
en/index.html              Home            EN  (gerado)
en/about/index.html        The Group       EN  (gerado)
en/inn-health/index.html   Inn Health      EN  (gerado)
en/contact/index.html      Contact         EN  (gerado)
404.html                   Página de erro
build.py                   Fonte única: cabeçalho, rodapé e conteúdo (PT + EN)
assets/css/style.css       Folha de estilos
assets/img/                Logótipo, fotografias e ícones
favicon.ico                Ícone do separador (16/32/48 px)
site.webmanifest           (gerado)
sitemap.xml                (gerado, com hreflang)
robots.txt                 (gerado)
CNAME                      Domínio personalizado
```

## Idiomas

Português na raiz (`/`), inglês em `/en/`. Cada página declara `hreflang` para a
sua equivalente e o cabeçalho tem um alternador PT/EN. Para alterar texto, editar
as constantes `*_PT` e `*_EN` em `build.py` — **as duas versões** devem ser
mantidas em sincronia.

## Alterar conteúdo

Editar `build.py` e correr:

```sh
python3 build.py
```

Os ficheiros `.html` gerados são commitados — o GitHub Pages serve-os diretamente,
sem passo de build no servidor.

## Pré-visualizar localmente

```sh
python3 -m http.server 8000
# abrir http://localhost:8000
```

## Publicar

Push para `main`. O workflow em `.github/workflows/deploy.yml` publica no GitHub Pages.

### Ordem correcta (importa por segurança)

1. **Settings -> Pages -> Source: GitHub Actions**
2. **Settings -> Pages -> Custom domain:** `sigma-seguros.eu` -> Save
3. **Só depois** configurar o DNS no registrar
4. Quando o certificado for emitido, activar **Enforce HTTPS**

Fazer o DNS antes do passo 2 abre uma janela em que outra pessoa pode reclamar
o domínio no GitHub Pages e servir conteúdo em `sigma-seguros.eu`.

> O ficheiro `CNAME` neste repositório **é ignorado**: a documentação do GitHub
> diz que, ao publicar por um workflow próprio do GitHub Actions, nenhum `CNAME`
> é criado e um `CNAME` existente é ignorado. O domínio vem apenas das Settings.
> O ficheiro fica aqui só para o caso de se voltar a publicar a partir de um ramo.

### DNS

| Tipo  | Nome | Valor |
|-------|------|-------|
| A     | @    | 185.199.108.153 |
| A     | @    | 185.199.109.153 |
| A     | @    | 185.199.110.153 |
| A     | @    | 185.199.111.153 |
| CNAME | www  | `psimoesSsimoes.github.io` |

### Verificar o domínio

Em **Settings -> Pages -> Verify domain** (ou no perfil da conta), adicionar o
registo TXT indicado. Impede que outra conta do GitHub reclame o domínio se o
site for desactivado — recomendado pelo GitHub contra ataques de takeover.

## Formulário de contacto

O site **não tem** formulário de contacto, por decisão deliberada. Todos os serviços
gratuitos de backend de formulários (Formspree, Web3Forms, FormSubmit) encaminham as
submissões por servidores nos EUA e só disponibilizam contrato de subcontratação
(RGPD art. 28) em planos pagos — inadequado para um mediador de seguros.

A página de contactos usa `mailto:` e `tel:`, pelo que os dados seguem do programa de
correio do visitante diretamente para a SIGMA, sem intermediários.

- [ ] Inserir o número de registo de mediador na ASF no rodapé (`build.py`, `FOOTER`).
