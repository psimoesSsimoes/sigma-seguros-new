#!/usr/bin/env python3
"""
Gera as paginas estaticas do site SIGMA, em portugues e ingles.

Ha uma unica fonte de verdade para o cabecalho, rodape e <head>; o conteudo de
cada pagina vive nas constantes *_PT e *_EN. Correr `python3 build.py` reescreve
os .html, que sao commitados tal como estao (o GitHub Pages serve ficheiros
estaticos, sem passo de build no servidor).

Portugues na raiz (/), ingles em /en/.
"""

import pathlib

SITE = "https://sigma-seguros.eu"
ROOT = pathlib.Path(__file__).parent

LANGS = {
    "pt": {"code": "pt-PT", "og": "pt_PT", "label": "PT"},
    "en": {"code": "en", "og": "en_GB", "label": "EN"},
}

NAV = {
    "pt": [("/", "Início"), ("/o-grupo/", "O Grupo"),
           ("/inn-health/", "Inn Health"), ("/contactos/", "Contactos")],
    "en": [("/en/", "Home"), ("/en/about/", "The Group"),
           ("/en/inn-health/", "Inn Health"), ("/en/contact/", "Contact")],
}

CTA = {"pt": ("/contactos/", "Fale connosco"), "en": ("/en/contact/", "Get in touch")}
SKIP = {"pt": "Saltar para o conteúdo", "en": "Skip to content"}
MENU = {"pt": "Abrir menu", "en": "Open menu"}
HOME_LABEL = {"pt": "SIGMA — página inicial", "en": "SIGMA — home"}
SWITCH_LABEL = {"pt": "View this page in English", "en": "Ver esta página em português"}

ADDRESS = {
    "pt": ("Avenida José Gomes Ferreira n.º 11, Escritório 53<br>\n"
           "          Edifício ATLAS II<br>\n"
           "          1495-139 Algés, Portugal"),
    "en": ("Avenida José Gomes Ferreira n.º 11, Office 53<br>\n"
           "          Edifício ATLAS II<br>\n"
           "          1495-139 Algés, Portugal"),
}

FOOTER_HEADS = {
    "pt": ("Navegação", "Contactos", "24 horas, 7 dias por semana",
           "SIGMA — Consultores de Seguros"),
    "en": ("Navigation", "Contact", "24 hours a day, 7 days a week",
           "SIGMA — Insurance Consultants"),
}

SCHEMA = """{
  "@context": "https://schema.org",
  "@type": "InsuranceAgency",
  "name": "SIGMA — Consultores de Seguros",
  "url": "https://sigma-seguros.eu/",
  "logo": "https://sigma-seguros.eu/assets/img/logo.png",
  "email": "geral@sigma-seguros.pt",
  "telephone": ["+351211990100", "+351211990200"],
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Avenida José Gomes Ferreira n.º 11, Escritório 53, Edifício ATLAS II",
    "postalCode": "1495-139",
    "addressLocality": "Algés",
    "addressCountry": "PT"
  },
  "image": "https://sigma-seguros.eu/assets/img/og-image.jpg",
  "alternateName": "SIGMA - Consultoria de Seguros",
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 38.7149254,
    "longitude": -9.2313631
  },
  "areaServed": "PT",
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "00:00",
    "closes": "23:59"
  }
}"""


def header(path, lang, alt_path):
    """Cabecalho com navegacao e alternador de idioma."""
    links = "\n".join(
        '      <a href="{}"{}>{}</a>'.format(
            href, ' aria-current="page"' if href == path else "", label
        )
        for href, label in NAV[lang]
    )
    cta_href, cta_label = CTA[lang]
    other = "en" if lang == "pt" else "pt"
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{NAV[lang][0][0]}" aria-label="{HOME_LABEL[lang]}">
      <img src="/assets/img/logo.png" width="363" height="263" alt="SIGMA — Consultores de Seguros">
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="{MENU[lang]}">
      <svg width="20" height="14" viewBox="0 0 20 14" fill="none" aria-hidden="true"><path d="M0 1h20M0 7h20M0 13h20" stroke="currentColor" stroke-width="2"/></svg>
    </button>
    <nav class="nav" id="nav">
{links}
      <a class="lang-switch" href="{alt_path}" lang="{LANGS[other]['code']}"
         hreflang="{LANGS[other]['code']}" title="{SWITCH_LABEL[lang]}">{LANGS[other]['label']}</a>
      <a class="btn btn--primary header-cta" href="{cta_href}">{cta_label}</a>
    </nav>
  </div>
</header>"""


def footer(lang):
    nav_head, contact_head, hours, name = FOOTER_HEADS[lang]
    links = "\n".join(
        f'          <li><a href="{href}">{label}</a></li>' for href, label in NAV[lang]
    )
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <img src="/assets/img/logo-white.png" width="363" height="263" alt="SIGMA — Consultores de Seguros">
        <address>
          {ADDRESS[lang]}
        </address>
      </div>
      <div>
        <h4>{nav_head}</h4>
        <ul>
{links}
        </ul>
      </div>
      <div>
        <h4>{contact_head}</h4>
        <ul>
          <li><a href="tel:+351211990100">211 990 100</a></li>
          <li><a href="tel:+351211990200">211 990 200</a></li>
          <li><a href="mailto:geral@sigma-seguros.pt">geral@sigma-seguros.pt</a></li>
          <li>{hours}</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© <span id="y">2026</span> {name}</p>
    </div>
  </div>
</footer>"""


SCRIPT = """<script>
  document.querySelector('.nav-toggle').addEventListener('click', function () {
    var nav = document.getElementById('nav');
    var open = this.getAttribute('aria-expanded') === 'true';
    this.setAttribute('aria-expanded', String(!open));
    nav.hidden = open;
  });
  function syncNav() {
    var nav = document.getElementById('nav');
    var btn = document.querySelector('.nav-toggle');
    if (window.matchMedia('(max-width: 880px)').matches) {
      if (btn.getAttribute('aria-expanded') !== 'true') nav.hidden = true;
    } else {
      nav.hidden = false;
    }
  }
  syncNav();
  window.addEventListener('resize', syncNav);
  document.getElementById('y').textContent = new Date().getFullYear();
</script>"""


def breadcrumbs(path, lang):
    """BreadcrumbList para paginas interiores (a inicial nao leva migalhas)."""
    home = NAV[lang][0]
    for href, label in NAV[lang][1:]:
        if href == path:
            import json
            data = {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": home[1],
                     "item": SITE + home[0]},
                    {"@type": "ListItem", "position": 2, "name": label,
                     "item": SITE + href},
                ],
            }
            return ('\n<script type="application/ld+json">\n'
                    + json.dumps(data, ensure_ascii=False, indent=2)
                    + '\n</script>')
    return ""


def page(path, lang, alt_path, title, description, body, og_desc=None, schema=False):
    canonical = SITE + path
    meta = LANGS[lang]
    ld = f'\n<script type="application/ld+json">\n{SCHEMA}\n</script>' if schema else ""
    ld += breadcrumbs(path, lang)
    pt_url = SITE + (path if lang == "pt" else alt_path)
    en_url = SITE + (path if lang == "en" else alt_path)
    return f"""<!DOCTYPE html>
<html lang="{meta['code']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="pt-PT" href="{pt_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{pt_url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{og_desc or description}">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="SIGMA — Consultores de Seguros">
<meta property="og:site_name" content="SIGMA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{og_desc or description}">
<meta name="twitter:image" content="{SITE}/assets/img/og-image.jpg">
<meta property="og:locale" content="{meta['og']}">
<meta name="theme-color" content="#00785E">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/assets/img/icon-32.png" sizes="32x32">
<link rel="icon" type="image/png" href="/assets/img/icon-16.png" sizes="16x16">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">{ld}
</head>
<body>
<a class="skip-link" href="#main">{SKIP[lang]}</a>

{header(path, lang, alt_path)}

<main id="main">
{body}
</main>

{footer(lang)}

{SCRIPT}
</body>
</html>
"""


def pic(base, widths, w, h, alt, sizes, ext="jpg", eager=False):
    """Constroi um <picture> com WebP e fallback, em larguras responsivas."""
    webp = ", ".join(f"/assets/img/{base}-{x}.webp {x}w" for x in widths)
    fall = ", ".join(f"/assets/img/{base}-{x}.{ext} {x}w" for x in widths)
    load = ('loading="eager" fetchpriority="high"' if eager else 'loading="lazy"')
    return (
        '<picture>\n'
        f'          <source type="image/webp" srcset="{webp}" sizes="{sizes}">\n'
        f'          <img src="/assets/img/{base}-{widths[-1]}.{ext}" srcset="{fall}" sizes="{sizes}"\n'
        f'               width="{w}" height="{h}" alt="{alt}" {load} decoding="async">\n'
        '        </picture>'
    )


# ---------------------------------------------------------------------------
# Conteudo das paginas
# ---------------------------------------------------------------------------
HOME_PT = """
  <section class="hero">
    <div class="container hero-grid">
      <div>
        <p class="eyebrow">Consultores de Seguros</p>
        <h1>Gestão de risco feita à medida de quem a usa.</h1>
        <p class="hero-lead">
          Aliamos uma longa experiência na atividade a um conhecimento profundo das soluções
          disponíveis no mercado segurador — para oferecer a clientes e seguradoras um serviço
          de qualidade superior, tecnologicamente bem suportado.
        </p>
        <div class="btn-row">
          <a class="btn btn--primary" href="/contactos/">Pedir um diagnóstico</a>
          <a class="btn btn--ghost" href="/o-grupo/">Conhecer a SIGMA</a>
        </div>
      </div>
      <div class="hero-media">
        {hero_img}
      </div>
    </div>
    <div class="container">
      <p class="hero-quote">
        Para a SIGMA não existem “produtos”, “coberturas” e “garantias”.<br>
        <strong>Existem soluções efetivas, exclusivas e com criação de valor.</strong>
      </p>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container">
      <dl class="strip">
        <div><dt>Âmbito</dt><dd>Particulares e empresas</dd></div>
        <div><dt>Cobertura</dt><dd>Todos os ramos</dd></div>
        <div><dt>Disponibilidade</dt><dd>24 horas, 7 dias</dd></div>
        <div><dt>Sede</dt><dd>Algés, Lisboa</dd></div>
      </dl>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="media-split media-split--flip">
        <div class="media-split__text">
          <p class="eyebrow">A diferenciação</p>
          <h2>O mercado vende proteção genérica. Nós partimos do seu risco.</h2>
          <p style="margin-top:22px">
            A oferta de seguros em Portugal tem seguido uma linha indiferenciadora: promove a
            aquisição de proteção contra riscos múltiplos sem atender às exigências específicas
            de quem usa o serviço. O resultado é, em muitos casos, uma inadequação entre os reais
            requisitos do cliente e o contrato assinado.
          </p>
          <p>
            Como entidade especializada na gestão de riscos, a SIGMA inverte a questão e
            coloca-se permanentemente na pele dos seus clientes, questionando qual é a melhor
            estratégia para cada um.
          </p>
        </div>
        <figure>{cliente_img}</figure>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <p class="eyebrow">Como trabalhamos</p>
      <h2 class="measure">Três princípios que sustentam cada proposta que fazemos.</h2>
      <div class="grid grid--3" style="margin-top:52px">
        <article class="card">
          <span class="card-num">01</span>
          <h3>Conhecimento</h3>
          <p>Domínio profundo da indústria seguradora e das soluções adequadas à atividade
             específica de cada cliente — não a um perfil médio.</p>
        </article>
        <article class="card">
          <span class="card-num">02</span>
          <h3>Profissionalismo</h3>
          <p>A base da relação com clientes, seguradoras e com os restantes intervenientes
             do mercado. Sem exceções e sem atalhos.</p>
        </article>
        <article class="card">
          <span class="card-num">03</span>
          <h3>Serviço ao cliente</h3>
          <p>Acompanhamento permanente da sua atividade: identificamos os riscos e ameaças
             principais, antecipamos soluções e acrescentamos valor ao negócio.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="container">
      <div class="media-split">
        <div class="media-split__text">
          <p class="eyebrow">Porquê o seguro</p>
          <h2>A forma mais eficaz de anular as consequências de um risco concreto.</h2>
          <p style="margin-top:22px">
            A segurança das pessoas e bens é uma necessidade incontornável nas sociedades
            modernas. A interdependência social e económica da vida atual torna vital a adoção
            de soluções que mitiguem as consequências de eventos danosos — de caráter natural
            ou resultantes da ação humana.
          </p>
          <p>
            O contrato de seguro é a forma mais eficaz de reduzir ou anular essas consequências,
            mantendo a estabilidade dos suportes da sociedade: as pessoas, as famílias e as
            empresas.
          </p>
        </div>
        <figure>{natureza_img}</figure>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <p class="eyebrow">Soluções</p>
      <h2 class="measure">Atuamos em todas as áreas de risco de pessoas e bens.</h2>
      <p class="measure-wide" style="margin-top:18px">
        Tendo como base uma análise profunda da atividade de cada cliente, elaboramos um
        diagnóstico completo dos riscos inerentes e aconselhamos um plano de seguros adequado.
        A título exemplificativo:
      </p>
      <div class="solutions" style="margin-top:48px">
        <article class="solution">
          <h3>Particulares e agregados familiares</h3>
          <ul class="tick-list">
            <li>Vida e reforma</li>
            <li>Saúde</li>
            <li>Património mobiliário e imobiliário</li>
            <li>Automóvel e outras viaturas</li>
            <li>Responsabilidades</li>
            <li>Assistência</li>
          </ul>
        </article>
        <article class="solution">
          <h3>Empresas e negócios</h3>
          <ul class="tick-list">
            <li>Colaboradores</li>
            <li>Complemento de reforma</li>
            <li>Saúde</li>
            <li>Ativos móveis e imóveis</li>
            <li>Vida</li>
            <li>Garantia de responsabilidades</li>
          </ul>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container">
      <div class="feature">
        <div>
          <p class="badge">Solução especializada</p>
          <h2 class="measure" style="margin-top:22px">Criação de valor na hotelaria e no alojamento local.</h2>
          <p class="measure" style="margin-top:18px">
            O Inn Health<sup>®</sup> foi desenhado para que os hóspedes usufruam da viagem e do
            alojamento com total paz de espírito: videoconsultas 24/7, prescrições enviadas para
            o telemóvel e nenhuma limitação por pré-existências, idade ou tipo de doença.
          </p>
          <div class="btn-row" style="margin-top:30px">
            <a class="btn btn--primary" href="/inn-health/">Conhecer o Inn Health</a>
          </div>
        </div>
        <div class="feature__media">{badge_img}</div>
      </div>
    </div>
  </section>

  <section class="section cta-band on-green">
    <div class="container">
      <p class="eyebrow eyebrow--center">Vamos falar</p>
      <h2>Exponha o seu caso. Respondemos de imediato.</h2>
      <p>
        Iniciamos a conceção de um plano de seguros com os melhores benefícios para a sua
        situação — sem compromisso e sem custo.
      </p>
      <div class="btn-row">
        <a class="btn btn--primary" href="/contactos/">Contacte-nos</a>
        <a class="btn btn--ghost" href="tel:+351211990100">211 990 100</a>
      </div>
    </div>
  </section>
"""

GRUPO_PT = """
  <section class="hero hero--compact">
    <div class="container">
      <p class="eyebrow">O Grupo</p>
      <h1>Uma entidade especializada na gestão de riscos.</h1>
      <p class="hero-lead">
        Existimos para gerar uma relação de confiança entre clientes e fornecedores do mercado
        segurador, disponibilizando conhecimento relevante e libertando os nossos clientes para
        o desenvolvimento da sua vida ou do seu negócio.
      </p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="media-split">
        <div class="media-split__text">
          <p class="eyebrow">A missão</p>
          <h2>Conhecimento relevante, para que possa dedicar-se ao que importa.</h2>
          <p style="margin-top:22px">
            O contexto atual da oferta de seguros no mercado português tem seguido uma linha
            indiferenciadora: promove a aquisição de proteção contra riscos múltiplos sem
            atender às exigências específicas de quem usa o serviço.
          </p>
          <p>
            O resultado é, em muitos casos, uma inadequação entre os reais requisitos dos
            clientes e o contrato assinado, bem como o desperdício de dinheiro em algo que é
            inadequado.
          </p>
          <p>
            A SIGMA inverte a questão e coloca-se permanentemente na pele dos seus clientes,
            questionando quais são as melhores estratégias para cada um. Para nós não existem
            “produtos”, “coberturas” e “garantias” — existem soluções efetivas, exclusivas e
            com criação de valor.
          </p>
        </div>
        <figure>{consulta_img}</figure>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <p class="eyebrow">Os nossos valores</p>
      <h2 class="measure">A nossa presença no mercado assenta em princípios que não negociamos.</h2>
      <dl class="values" style="margin-top:48px">
        <div class="value">
          <dt>Integridade</dt>
          <dd>Porque só uma atitude íntegra conquista o respeito e a confiança.</dd>
        </div>
        <div class="value">
          <dt>Verdade</dt>
          <dd>Porque somente através dela chegamos à solução.</dd>
        </div>
        <div class="value">
          <dt>Excelência</dt>
          <dd>Porque é através da sua busca que alcançamos o profissionalismo.</dd>
        </div>
        <div class="value">
          <dt>Responsabilidade</dt>
          <dd>Porque só o exercício de uma cidadania responsável contribuirá para as necessárias
              mudanças de paradigma da sociedade e dos negócios.</dd>
        </div>
        <div class="value">
          <dt>Solidariedade</dt>
          <dd>Porque é obrigação dos indivíduos e das empresas devolver à sociedade os
              benefícios, na direta medida em que a sociedade lhes proporciona as oportunidades.</dd>
        </div>
        <div class="value">
          <dt>Profissionalismo</dt>
          <dd>Como base fundamental da relação com todos os clientes, com as seguradoras e com
              os demais intervenientes no mercado.</dd>
        </div>
        <div class="value">
          <dt>Conhecimento</dt>
          <dd>Profundo da indústria seguradora e das soluções adequadas à atividade específica
              de cada um dos nossos clientes.</dd>
        </div>
        <div class="value">
          <dt>Serviço aos clientes</dt>
          <dd>Consubstanciado num acompanhamento permanente da sua atividade, ajudando-os a
              identificar os principais riscos e ameaças, antecipando as soluções e acrescentando
              valor ao seu negócio.</dd>
        </div>
      </dl>
    </div>
  </section>

  <section class="section cta-band on-green">
    <div class="container">
      <p class="eyebrow eyebrow--center">Diagnóstico</p>
      <h2>Começamos por perceber a sua atividade.</h2>
      <p>
        Com base numa análise profunda, elaboramos um diagnóstico completo dos riscos e ameaças
        inerentes e aconselhamos um plano de seguros adequado.
      </p>
      <div class="btn-row">
        <a class="btn btn--primary" href="/contactos/">Contacte-nos</a>
      </div>
    </div>
  </section>
"""

INN_PT = """
  <section class="hero hero--compact">
    <div class="container hero-grid">
      <div>
        <p class="badge">Solução especializada SIGMA</p>
        <h1 style="margin-top:22px">Inn Health<sup>®</sup></h1>
        <p class="hero-lead">
          Seja para descansar ou para visitar, é fundamental usufruir da viagem e do alojamento
          com total descontração e paz de espírito. Foi para isso que criámos o
          Inn Health<sup>®</sup> — uma solução dirigida à criação de valor na hotelaria e no
          alojamento local.
        </p>
        <div class="btn-row">
          <a class="btn btn--primary" href="/contactos/">Pedir informações</a>
        </div>
      </div>
      <div class="feature__media">{badge_img}</div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <p class="eyebrow">O que oferece</p>
      <h2 class="measure">Assistência médica para os seus hóspedes, sem fricção.</h2>
      <div class="grid grid--3" style="margin-top:52px">

        <article class="card">
          <span class="card-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="5" width="14" height="14" rx="2"/>
              <path d="M16 10l6-3v10l-6-3z"/>
            </svg>
          </span>
          <h3>Videoconsultas 24/7</h3>
          <p>
            Os hóspedes das unidades hoteleiras e dos alojamentos locais aderentes acedem a um
            serviço de medicina online à medida e em função das suas necessidades, com total
            independência de meios.
          </p>
        </article>

        <article class="card">
          <span class="card-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
              <rect x="6" y="2" width="12" height="20" rx="2.5"/>
              <path d="M12 8v6M9 11h6"/>
            </svg>
          </span>
          <h3>Prescrições no telemóvel</h3>
          <p>
            As prescrições de medicamentos e exames enviadas pela rede clínica chegam ao
            telemóvel, tablet ou computador. Os serviços podem depois ser obtidos diretamente
            ou através do alojamento.
          </p>
        </article>

        <article class="card">
          <span class="card-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2l8 3.5v6c0 5-3.4 8.9-8 10.5-4.6-1.6-8-5.5-8-10.5v-6L12 2z"/>
              <path d="M9 12l2 2 4-4"/>
            </svg>
          </span>
          <h3>Sem limitações nem exclusões</h3>
          <p>
            Um seguro adaptado a responder a qualquer necessidade clínica dos aderentes, sem
            impor limitações por pré-existências, exclusões, limites de idade ou tipologia de
            doença ou acidente.
          </p>
        </article>

      </div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="container">
      <div class="media-split media-split--flip">
        <div class="media-split__text">
          <p class="eyebrow">Cartão de saúde virtual</p>
          <h2>No telemóvel do hóspede, desde o primeiro dia.</h2>
          <p style="margin-top:22px">
            Cada aderente recebe um cartão de saúde virtual com acesso à rede clínica. Sem
            papéis, sem processos de adesão demorados e sem nada para instalar.
          </p>
          <p>
            O Inn Health<sup>®</sup> é subscrito pela unidade de alojamento e disponibilizado
            aos hóspedes como parte da estadia: acrescenta um serviço tangível à oferta,
            diferencia a unidade face à concorrência e responde a uma preocupação real de quem
            viaja — o que fazer se precisar de um médico longe de casa.
          </p>
        </div>
        <figure style="display:flex;justify-content:center">{card_img}</figure>
      </div>
    </div>
  </section>

  <section class="section cta-band on-green">
    <div class="container">
      <p class="eyebrow eyebrow--center">Inn Health<sup>®</sup></p>
      <h2>Quer saber como aplicar na sua unidade?</h2>
      <p>Explicamos as condições, o âmbito da cobertura e o processo de adesão.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="/contactos/">Pedir informações</a>
        <a class="btn btn--ghost" href="tel:+351211990100">211 990 100</a>
      </div>
    </div>
  </section>
"""

CONTACTOS_PT = """
  <section class="hero hero--compact">
    <div class="container">
      <p class="eyebrow">Contactos</p>
      <h1>Exponha o seu caso.</h1>
      <p class="hero-lead">
        Entraremos em contacto de imediato para iniciarmos a conceção do plano de seguros com
        os melhores benefícios para a sua situação.
      </p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="split">

        <div>
          <p class="eyebrow">Fale connosco</p>
          <dl class="contact-list">
            <div>
              <dt>Telefone</dt>
              <dd>
                <a href="tel:+351211990100">211 990 100</a><br>
                <a href="tel:+351211990200">211 990 200</a>
                <small>Chamada para a rede fixa nacional</small>
              </dd>
            </div>
            <div>
              <dt>Email</dt>
              <dd><a href="mailto:geral@sigma-seguros.pt">geral@sigma-seguros.pt</a></dd>
            </div>
            <div>
              <dt>Horário</dt>
              <dd>24 horas por dia<small>7 dias por semana</small></dd>
            </div>
            <div>
              <dt>Morada</dt>
              <dd>
                Avenida José Gomes Ferreira n.º 11, Escritório 53
                <small>Edifício ATLAS II &middot; 1495-139 Algés, Portugal</small>
              </dd>
            </div>
          </dl>
        </div>

        <div>
          <p class="eyebrow">Prefere escrever?</p>
          <div class="contact-panel">
            <h2>Escreva-nos diretamente.</h2>
            <p>
              Descreva brevemente a sua situação ou a sua atividade. Entraremos em contacto de
              imediato para iniciarmos a conceção do seu plano de seguros.
            </p>
            <div class="btn-row" style="margin-top:28px">
              <a class="btn btn--primary"
                 href="mailto:geral@sigma-seguros.pt?subject=Pedido%20de%20contacto%20%E2%80%94%20SIGMA">
                Enviar email
              </a>
              <a class="btn btn--ghost" href="tel:+351211990100">Telefonar</a>
            </div>
            <p class="form-note" style="margin-top:24px">
              A mensagem segue do seu próprio programa de correio diretamente para a SIGMA.
              Os seus dados não passam por serviços de terceiros.
            </p>
          </div>
        </div>

      </div>
    </div>
  </section>

  <section class="section section--tight section--alt">
    <div class="container">
      <p class="eyebrow">Onde estamos</p>
      <iframe class="map" title="Localização da SIGMA em Algés — Avenida José Gomes Ferreira 11, Edifício ATLAS II"
        loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps/embed?origin=mfe&amp;pb=!1m3!2m1!1sSigma+-+Consultoria+de+Seguros,+Alg%C3%A9s!6i17"
        style="margin-top:28px"></iframe>
    </div>
  </section>
"""


# ---------------------------------------------------------------------------
# Imagens
# ---------------------------------------------------------------------------

HOME_EN = """
  <section class="hero">
    <div class="container hero-grid">
      <div>
        <p class="eyebrow">Insurance Consultants</p>
        <h1>Risk management built around the people who use it.</h1>
        <p class="hero-lead">
          We combine long experience in the field with deep knowledge of what the insurance
          market offers — to give clients and insurers a superior service, backed by the right
          technology.
        </p>
        <div class="btn-row">
          <a class="btn btn--primary" href="/en/contact/">Request an assessment</a>
          <a class="btn btn--ghost" href="/en/about/">About SIGMA</a>
        </div>
      </div>
      <div class="hero-media">
        {hero_img}
      </div>
    </div>
    <div class="container">
      <p class="hero-quote">
        At SIGMA there are no “products”, “covers” or “guarantees”.<br>
        <strong>There are effective, exclusive solutions that create value.</strong>
      </p>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container">
      <dl class="strip">
        <div><dt>Scope</dt><dd>Individuals and businesses</dd></div>
        <div><dt>Coverage</dt><dd>Every line of business</dd></div>
        <div><dt>Availability</dt><dd>24 hours, 7 days</dd></div>
        <div><dt>Head office</dt><dd>Algés, Lisbon</dd></div>
      </dl>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <div class="media-split media-split--flip">
        <div class="media-split__text">
          <p class="eyebrow">What sets us apart</p>
          <h2>The market sells generic protection. We start from your risk.</h2>
          <p style="margin-top:22px">
            Insurance in Portugal has followed an undifferentiated path: it promotes cover
            against multiple risks without attending to the specific requirements of the person
            using the service. The result, in many cases, is a mismatch between what the client
            actually needs and the contract they sign.
          </p>
          <p>
            As a specialist in risk management, SIGMA turns the question around and puts itself
            in its clients' shoes, asking what the right strategy is for each one.
          </p>
        </div>
        <figure>{cliente_img}</figure>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <p class="eyebrow">How we work</p>
      <h2 class="measure">Three principles behind every proposal we make.</h2>
      <div class="grid grid--3" style="margin-top:52px">
        <article class="card">
          <span class="card-num">01</span>
          <h3>Knowledge</h3>
          <p>A deep command of the insurance industry and of the solutions suited to each
             client's specific activity — not to an average profile.</p>
        </article>
        <article class="card">
          <span class="card-num">02</span>
          <h3>Professionalism</h3>
          <p>The basis of our relationship with clients, insurers and everyone else operating
             in the market. No exceptions and no shortcuts.</p>
        </article>
        <article class="card">
          <span class="card-num">03</span>
          <h3>Client service</h3>
          <p>Continuous support for your activity: we identify the main risks and threats,
             anticipate solutions and add value to your business.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="container">
      <div class="media-split">
        <div class="media-split__text">
          <p class="eyebrow">Why insurance</p>
          <h2>The most effective way to undo the consequences of a concrete risk.</h2>
          <p style="margin-top:22px">
            The safety of people and property is an unavoidable need in modern societies. The
            social and economic interdependence of daily life makes it vital to adopt solutions
            that mitigate the consequences of damaging events — whether natural or caused by
            human action.
          </p>
          <p>
            The insurance contract is the most effective way to reduce or remove those
            consequences, preserving the stability of what holds society together: individuals,
            families and companies.
          </p>
        </div>
        <figure>{natureza_img}</figure>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <p class="eyebrow">Solutions</p>
      <h2 class="measure">We work across every area of risk to people and property.</h2>
      <p class="measure-wide" style="margin-top:18px">
        Starting from a thorough analysis of each client's activity, we produce a complete
        assessment of the risks involved and recommend an appropriate insurance plan.
        By way of example:
      </p>
      <div class="solutions" style="margin-top:48px">
        <article class="solution">
          <h3>Individuals and households</h3>
          <ul class="tick-list">
            <li>Life and retirement</li>
            <li>Health</li>
            <li>Movable and immovable property</li>
            <li>Motor and other vehicles</li>
            <li>Liability</li>
            <li>Assistance</li>
          </ul>
        </article>
        <article class="solution">
          <h3>Companies and businesses</h3>
          <ul class="tick-list">
            <li>Employees</li>
            <li>Supplementary retirement</li>
            <li>Health</li>
            <li>Movable and immovable assets</li>
            <li>Life</li>
            <li>Liability cover</li>
          </ul>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container">
      <div class="feature">
        <div>
          <p class="badge">Specialised solution</p>
          <h2 class="measure" style="margin-top:22px">Creating value in hotels and short-term rentals.</h2>
          <p class="measure" style="margin-top:18px">
            Inn Health<sup>®</sup> was designed so guests can enjoy their trip and their stay
            with complete peace of mind: video consultations 24/7, prescriptions sent to their
            phone, and no limits based on pre-existing conditions, age or type of illness.
          </p>
          <div class="btn-row" style="margin-top:30px">
            <a class="btn btn--primary" href="/en/inn-health/">Explore Inn Health</a>
          </div>
        </div>
        <div class="feature__media">{badge_img}</div>
      </div>
    </div>
  </section>

  <section class="section cta-band on-green">
    <div class="container">
      <p class="eyebrow eyebrow--center">Let's talk</p>
      <h2>Tell us your situation. We reply straight away.</h2>
      <p>
        We will begin designing an insurance plan with the best possible benefits for your
        circumstances — with no obligation and no cost.
      </p>
      <div class="btn-row">
        <a class="btn btn--primary" href="/en/contact/">Get in touch</a>
        <a class="btn btn--ghost" href="tel:+351211990100">211 990 100</a>
      </div>
    </div>
  </section>
"""

GRUPO_EN = """
  <section class="hero hero--compact">
    <div class="container">
      <p class="eyebrow">The Group</p>
      <h1>A specialist in risk management.</h1>
      <p class="hero-lead">
        We exist to build a relationship of trust between clients and the insurance market,
        providing relevant knowledge and freeing our clients to get on with their lives and
        their businesses.
      </p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="media-split">
        <div class="media-split__text">
          <p class="eyebrow">Our mission</p>
          <h2>Relevant knowledge, so you can focus on what matters.</h2>
          <p style="margin-top:22px">
            Insurance in Portugal has followed an undifferentiated path: it promotes cover
            against multiple risks without attending to the specific requirements of the person
            using the service.
          </p>
          <p>
            The result, in many cases, is a mismatch between what clients actually need and the
            contract they sign — and money wasted on something that does not fit.
          </p>
          <p>
            SIGMA turns the question around and puts itself in its clients' shoes, asking what
            the right strategy is for each one. For us there are no “products”, “covers” or
            “guarantees” — there are effective, exclusive solutions that create value.
          </p>
        </div>
        <figure>{consulta_img}</figure>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container">
      <p class="eyebrow">Our values</p>
      <h2 class="measure">Our place in the market rests on principles we do not negotiate.</h2>
      <dl class="values" style="margin-top:48px">
        <div class="value">
          <dt>Integrity</dt>
          <dd>Because only an honest approach earns respect and trust.</dd>
        </div>
        <div class="value">
          <dt>Truth</dt>
          <dd>Because it is the only route to the right solution.</dd>
        </div>
        <div class="value">
          <dt>Excellence</dt>
          <dd>Because pursuing it is how we reach professionalism.</dd>
        </div>
        <div class="value">
          <dt>Responsibility</dt>
          <dd>Because only responsible citizenship will bring about the shifts society and
              business need.</dd>
        </div>
        <div class="value">
          <dt>Solidarity</dt>
          <dd>Because individuals and companies are obliged to return to society the benefits
              it affords them, in direct measure to the opportunities they receive.</dd>
        </div>
        <div class="value">
          <dt>Professionalism</dt>
          <dd>As the foundation of our relationship with every client, with insurers and with
              everyone else operating in the market.</dd>
        </div>
        <div class="value">
          <dt>Knowledge</dt>
          <dd>A deep command of the insurance industry and of the solutions suited to each of
              our clients' specific activities.</dd>
        </div>
        <div class="value">
          <dt>Client service</dt>
          <dd>Expressed in continuous support for your activity, helping identify the main risks
              and threats, anticipating solutions and adding value to your business.</dd>
        </div>
      </dl>
    </div>
  </section>

  <section class="section cta-band on-green">
    <div class="container">
      <p class="eyebrow eyebrow--center">Assessment</p>
      <h2>We start by understanding what you do.</h2>
      <p>
        From a thorough analysis, we produce a complete assessment of the risks and threats
        involved and recommend an appropriate insurance plan.
      </p>
      <div class="btn-row">
        <a class="btn btn--primary" href="/en/contact/">Get in touch</a>
      </div>
    </div>
  </section>
"""

INN_EN = """
  <section class="hero hero--compact">
    <div class="container hero-grid">
      <div>
        <p class="badge">A specialised SIGMA solution</p>
        <h1 style="margin-top:22px">Inn Health<sup>®</sup></h1>
        <p class="hero-lead">
          Whether the trip is for rest or for sightseeing, what matters is enjoying the journey
          and the stay with complete peace of mind. That is why we created Inn Health<sup>®</sup>
          — a solution built to create value in hotels and short-term rentals.
        </p>
        <div class="btn-row">
          <a class="btn btn--primary" href="/en/contact/">Request information</a>
        </div>
      </div>
      <div class="feature__media">{badge_img}</div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <p class="eyebrow">What it offers</p>
      <h2 class="measure">Medical support for your guests, without the friction.</h2>
      <div class="grid grid--3" style="margin-top:52px">

        <article class="card">
          <span class="card-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="5" width="14" height="14" rx="2"/>
              <path d="M16 10l6-3v10l-6-3z"/>
            </svg>
          </span>
          <h3>Video consultations 24/7</h3>
          <p>
            Guests of participating hotels and short-term rentals get online medical care
            tailored to what they need, whenever they need it, independently of any other
            arrangement.
          </p>
        </article>

        <article class="card">
          <span class="card-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
              <rect x="6" y="2" width="12" height="20" rx="2.5"/>
              <path d="M12 8v6M9 11h6"/>
            </svg>
          </span>
          <h3>Prescriptions on the phone</h3>
          <p>
            Prescriptions for medicines and tests issued by the clinical network arrive on the
            guest's phone, tablet or computer. They can then be filled directly or through the
            accommodation.
          </p>
        </article>

        <article class="card">
          <span class="card-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2l8 3.5v6c0 5-3.4 8.9-8 10.5-4.6-1.6-8-5.5-8-10.5v-6L12 2z"/>
              <path d="M9 12l2 2 4-4"/>
            </svg>
          </span>
          <h3>No limits, no exclusions</h3>
          <p>
            Cover designed to meet any clinical need a member may have, with no restrictions
            for pre-existing conditions, exclusions, age limits, or any category of illness or
            accident.
          </p>
        </article>

      </div>
    </div>
  </section>

  <section class="section section--wash">
    <div class="container">
      <div class="media-split media-split--flip">
        <div class="media-split__text">
          <p class="eyebrow">Virtual health card</p>
          <h2>On the guest's phone, from day one.</h2>
          <p style="margin-top:22px">
            Every member receives a virtual health card giving access to the clinical network.
            No paperwork, no drawn-out enrolment and nothing to install.
          </p>
          <p>
            Inn Health<sup>®</sup> is taken out by the property and offered to guests as part of
            the stay: it adds a tangible service to what you provide, sets you apart from
            competitors, and answers a real concern for travellers — what to do if they need a
            doctor far from home.
          </p>
        </div>
        <figure style="display:flex;justify-content:center">{card_img}</figure>
      </div>
    </div>
  </section>

  <section class="section cta-band on-green">
    <div class="container">
      <p class="eyebrow eyebrow--center">Inn Health<sup>®</sup></p>
      <h2>Want to know how it would work for your property?</h2>
      <p>We will walk you through the terms, the scope of cover and how to sign up.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="/en/contact/">Request information</a>
        <a class="btn btn--ghost" href="tel:+351211990100">211 990 100</a>
      </div>
    </div>
  </section>
"""

CONTACTOS_EN = """
  <section class="hero hero--compact">
    <div class="container">
      <p class="eyebrow">Contact</p>
      <h1>Tell us your situation.</h1>
      <p class="hero-lead">
        We will be in touch straight away so we can start designing the insurance plan with the
        best possible benefits for your circumstances.
      </p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="split">

        <div>
          <p class="eyebrow">Talk to us</p>
          <dl class="contact-list">
            <div>
              <dt>Telephone</dt>
              <dd>
                <a href="tel:+351211990100">211 990 100</a><br>
                <a href="tel:+351211990200">211 990 200</a>
                <small>Calls to a Portuguese landline</small>
              </dd>
            </div>
            <div>
              <dt>Email</dt>
              <dd><a href="mailto:geral@sigma-seguros.pt">geral@sigma-seguros.pt</a></dd>
            </div>
            <div>
              <dt>Hours</dt>
              <dd>24 hours a day<small>7 days a week</small></dd>
            </div>
            <div>
              <dt>Address</dt>
              <dd>
                Avenida José Gomes Ferreira n.º 11, Office 53
                <small>Edifício ATLAS II &middot; 1495-139 Algés, Portugal</small>
              </dd>
            </div>
          </dl>
        </div>

        <div>
          <p class="eyebrow">Prefer to write?</p>
          <div class="contact-panel">
            <h2>Email us directly.</h2>
            <p>
              Tell us briefly about your situation or your business. We will be in touch straight
              away to start designing your insurance plan.
            </p>
            <div class="btn-row" style="margin-top:28px">
              <a class="btn btn--primary"
                 href="mailto:geral@sigma-seguros.pt?subject=Enquiry%20%E2%80%94%20SIGMA">
                Send an email
              </a>
              <a class="btn btn--ghost" href="tel:+351211990100">Call us</a>
            </div>
            <p class="form-note" style="margin-top:24px">
              Your message goes from your own mail program straight to SIGMA. Your data does not
              pass through any third-party service.
            </p>
          </div>
        </div>

      </div>
    </div>
  </section>

  <section class="section section--tight section--alt">
    <div class="container">
      <p class="eyebrow">Where we are</p>
      <iframe class="map" title="SIGMA's location in Algés — Avenida José Gomes Ferreira 11, Edifício ATLAS II"
        loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps/embed?origin=mfe&amp;pb=!1m3!2m1!1sSigma+-+Consultoria+de+Seguros,+Alg%C3%A9s!6i17"
        style="margin-top:28px"></iframe>
    </div>
  </section>
"""


# ---------------------------------------------------------------------------
# Imagens (texto alternativo por idioma)
# ---------------------------------------------------------------------------

def images(lang):
    alt = {
        "pt": {
            "hero": "Dois consultores da SIGMA a analisar documentação de risco",
            "consulta": "Consultores da SIGMA em análise de um plano de seguros",
            "cliente": "Cliente a receber o acompanhamento de um consultor SIGMA",
            "natureza": "Floresta em nevoeiro, evocando a proteção contra riscos naturais",
            "badge": "Selo Inn Health — a product by SIGMA Consultores de Seguros",
            "card": "Cartão de saúde virtual Inn Health no telemóvel",
        },
        "en": {
            "hero": "Two SIGMA consultants reviewing risk documentation",
            "consulta": "SIGMA consultants reviewing an insurance plan",
            "cliente": "A client being advised by a SIGMA consultant",
            "natureza": "Forest in fog, evoking protection against natural risks",
            "badge": "Inn Health seal — a product by SIGMA Consultores de Seguros",
            "card": "The Inn Health virtual health card on a phone",
        },
    }[lang]
    return {
        "hero_img": pic("consulta", [700, 1200], 1200, 801, alt["hero"],
                        "(max-width: 900px) 100vw, 45vw", eager=True),
        "consulta_img": pic("consulta", [700, 1200], 1200, 801, alt["consulta"],
                            "(max-width: 760px) 100vw, 48vw"),
        "cliente_img": pic("cliente", [700, 1200], 1200, 800, alt["cliente"],
                           "(max-width: 760px) 100vw, 48vw"),
        "natureza_img": pic("natureza", [900, 1600], 1600, 1066, alt["natureza"],
                            "(max-width: 760px) 100vw, 48vw"),
        "badge_img": pic("inn-badge", [440], 440, 314, alt["badge"],
                         "(max-width: 760px) 60vw, 300px", ext="png"),
        "card_img": pic("inn-card", [500], 500, 859, alt["card"],
                        "(max-width: 760px) 70vw, 320px"),
    }


# ---------------------------------------------------------------------------
# Paginas: cada entrada tem as duas versoes linguisticas
# ---------------------------------------------------------------------------

PAGES = [
    {
        "schema": True,
        "pt": dict(
            path="/", out="index.html", body=HOME_PT,
            title="SIGMA — Consultores de Seguros | Gestão de risco à medida",
            desc="A SIGMA é uma consultora de seguros especializada em gestão de riscos. "
                 "Analisamos a atividade de cada cliente e desenhamos um plano de seguros "
                 "adequado — para particulares e empresas.",
            og="Não existem produtos, coberturas e garantias. Existem soluções efetivas, "
               "exclusivas e com criação de valor para os nossos clientes."),
        "en": dict(
            path="/en/", out="en/index.html", body=HOME_EN,
            title="SIGMA — Insurance Consultants | Risk management, tailored",
            desc="SIGMA is an insurance consultancy specialising in risk management. We analyse "
                 "each client's activity and design an insurance plan that fits — for "
                 "individuals and businesses.",
            og="There are no products, covers or guarantees. There are effective, exclusive "
               "solutions that create value for our clients."),
    },
    {
        "pt": dict(
            path="/o-grupo/", out="o-grupo/index.html", body=GRUPO_PT,
            title="O Grupo — SIGMA Consultores de Seguros",
            desc="Especialistas na gestão de riscos. A missão, a diferenciação e os valores "
                 "que sustentam a relação da SIGMA com clientes e seguradoras."),
        "en": dict(
            path="/en/about/", out="en/about/index.html", body=GRUPO_EN,
            title="The Group — SIGMA Insurance Consultants",
            desc="Specialists in risk management. The mission, the difference and the values "
                 "behind SIGMA's relationship with clients and insurers."),
    },
    {
        "pt": dict(
            path="/inn-health/", out="inn-health/index.html", body=INN_PT,
            title="Inn Health® — Seguro de saúde para hotelaria | SIGMA",
            desc="Inn Health®: videoconsultas 24/7, prescrições no telemóvel e cobertura sem "
                 "exclusões nem limites de idade, para hóspedes de unidades hoteleiras e "
                 "alojamento local."),
        "en": dict(
            path="/en/inn-health/", out="en/inn-health/index.html", body=INN_EN,
            title="Inn Health® — Health cover for hotels | SIGMA",
            desc="Inn Health®: video consultations 24/7, prescriptions on the phone and cover "
                 "with no exclusions or age limits, for guests of hotels and short-term "
                 "rentals."),
    },
    {
        "pt": dict(
            path="/contactos/", out="contactos/index.html", body=CONTACTOS_PT,
            title="Contactos — SIGMA Consultores de Seguros | Algés",
            desc="Telefone 211 990 100, geral@sigma-seguros.pt. Disponíveis 24 horas por dia, "
                 "7 dias por semana. Avenida José Gomes Ferreira 11, Edifício ATLAS II, "
                 "1495-139 Algés."),
        "en": dict(
            path="/en/contact/", out="en/contact/index.html", body=CONTACTOS_EN,
            title="Contact — SIGMA Insurance Consultants | Algés, Lisbon",
            desc="Telephone 211 990 100, geral@sigma-seguros.pt. Available 24 hours a day, "
                 "7 days a week. Avenida José Gomes Ferreira 11, Edifício ATLAS II, "
                 "1495-139 Algés, Portugal."),
    },
]

# ---------------------------------------------------------------------------
# Redireccionamentos das URLs do WordPress antigo
#
# O GitHub Pages nao faz redireccionamentos do lado do servidor, por isso
# geram-se paginas-talao com refresh imediato + canonical a apontar ao destino.
# A Google trata um refresh instantaneo com canonical como redireccionamento
# permanente e transfere o valor da URL antiga.
# ---------------------------------------------------------------------------

REDIRECTS = {
    "about/": "/o-grupo/",                  # pagina de demonstracao nunca preenchida
    "services/": "/inn-health/",            # era a pagina do Inn Health
    "contact/": "/contactos/",
    "hello-world/": "/",                    # artigo por omissao do WordPress
    "category/uncategorized/": "/",
    "author/seomis/": "/",
    "elementor-hf/site-footer/": "/",
}

REDIRECT_TMPL = """<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={dest}">
<link rel="canonical" href="{site}{dest}">
<title>Página movida — SIGMA</title>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
<main class="hero" style="min-height:100vh;display:flex;align-items:center">
  <div class="container">
    <p class="eyebrow">Página movida</p>
    <h1>Esta página mudou de endereço.</h1>
    <p class="hero-lead">
      Se não for reencaminhado automaticamente,
      <a href="{dest}">siga esta ligação</a>.
    </p>
    <div class="btn-row">
      <a class="btn btn--primary" href="{dest}">Continuar</a>
    </div>
  </div>
</main>
</body>
</html>
"""


MANIFEST = """{
  "name": "SIGMA — Consultores de Seguros",
  "short_name": "SIGMA",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#00785E",
  "icons": [
    { "src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
"""


def main():
    urls = []
    for entry in PAGES:
        for lang in ("pt", "en"):
            cfg = entry[lang]
            alt_path = entry["en" if lang == "pt" else "pt"]["path"]
            html = page(
                cfg["path"], lang, alt_path, cfg["title"], cfg["desc"],
                cfg["body"].format(**images(lang)),
                og_desc=cfg.get("og"), schema=entry.get("schema", False),
            )
            target = ROOT / cfg["out"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html, encoding="utf-8")
            urls.append((cfg["path"], alt_path, lang))
            print("escrito", cfg["out"])

    # Sitemap com alternativas hreflang
    blocks = []
    for path, alt, lang in urls:
        pt = path if lang == "pt" else alt
        en = path if lang == "en" else alt
        blocks.append(
            f"  <url>\n    <loc>{SITE}{path}</loc>\n"
            f'    <xhtml:link rel="alternate" hreflang="pt-PT" href="{SITE}{pt}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{pt}"/>\n'
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>{'1.0' if path == '/' else '0.8'}</priority>\n  </url>"
        )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(blocks) + "\n</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8"
    )
    (ROOT / "site.webmanifest").write_text(MANIFEST, encoding="utf-8")
    print("escrito sitemap.xml, robots.txt, site.webmanifest")

    for old, dest in REDIRECTS.items():
        target = ROOT / old / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(REDIRECT_TMPL.format(dest=dest, site=SITE), encoding="utf-8")
    print(f"escritos {len(REDIRECTS)} redireccionamentos")


if __name__ == "__main__":
    main()
