/* CCF Conseil — interactions du site
   Aucun framework, aucune dépendance externe. */
(function () {
  'use strict';

  /* ----------------------------------------------------------------------
     Navigation mobile
     ---------------------------------------------------------------------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav-principal');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
      document.body.classList.toggle('nav-open', !open);
    });

    // Fermeture au clic sur un lien
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        document.body.classList.remove('nav-open');
      }
    });

    // Fermeture à la touche Échap
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        document.body.classList.remove('nav-open');
        toggle.focus();
      }
    });
  }

  /* ----------------------------------------------------------------------
     En-tête condensé au défilement
     ---------------------------------------------------------------------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var lastKnown = 0;
    var ticking = false;
    var onScroll = function () {
      header.classList.toggle('is-scrolled', lastKnown > 12);
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      lastKnown = window.scrollY;
      if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
    }, { passive: true });
    onScroll();
  }

  /* ----------------------------------------------------------------------
     Hauteur réelle de l'en-tête
     Le menu mobile s'ouvre juste sous l'en-tête, quelle que soit sa hauteur :
     pas d'écart ni de recouvrement.
     ---------------------------------------------------------------------- */
  function mesurerHeader() {
    if (!header) { return; }
    var h = Math.round(header.getBoundingClientRect().height);
    document.documentElement.style.setProperty('--header-h', h + 'px');
  }
  mesurerHeader();
  window.addEventListener('resize', mesurerHeader);
  window.addEventListener('orientationchange', mesurerHeader);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(mesurerHeader);
  }

  /* ----------------------------------------------------------------------
     Apparition au défilement
     ---------------------------------------------------------------------- */
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var revealables = document.querySelectorAll('.reveal');

  if (reduced || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealables.forEach(function (el) { observer.observe(el); });
  }

  /* ----------------------------------------------------------------------
     Pré-sélection du motif de rendez-vous depuis l'URL
     Exemple : /rendez-vous.html?motif=controle-fiscal
     ---------------------------------------------------------------------- */
  var params = new URLSearchParams(window.location.search);
  var motif = params.get('motif');
  if (motif) {
    document.querySelectorAll('select[name="motif"]').forEach(function (select) {
      var match = Array.prototype.find.call(select.options, function (opt) {
        return opt.value === motif;
      });
      if (match) { select.value = motif; }
    });
  }

  /* ----------------------------------------------------------------------
     Formulaires : validation légère et anti-robot
     ---------------------------------------------------------------------- */
  document.querySelectorAll('form[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      // Piège à robots : si le champ caché est rempli, on abandonne en silence
      var honeypot = form.querySelector('.hp-field input');
      if (honeypot && honeypot.value !== '') {
        e.preventDefault();
        return;
      }

      // Soumission trop rapide pour un humain
      var started = Number(form.dataset.ts || 0);
      if (started && Date.now() - started < 2500) {
        e.preventDefault();
        return;
      }

      var submit = form.querySelector('[type="submit"]');
      if (submit && form.checkValidity()) {
        submit.disabled = true;
        submit.textContent = 'Envoi en cours…';
      }
    });
    form.dataset.ts = String(Date.now());
  });

  /* ----------------------------------------------------------------------
     Année courante dans le pied de page
     ---------------------------------------------------------------------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();

/* ------------------------------------------------------------------------
   Agenda en ligne
   Le module du prestataire est chargé avec la page. Si le réseau le refuse,
   un message de secours remplace le calendrier : la page ne reste jamais vide.
   ------------------------------------------------------------------------ */
(function () {
  'use strict';

  var conteneur = document.getElementById('booking-widget');
  if (!conteneur) { return; }

  var CALENDLY_JS = 'https://assets.calendly.com/assets/external/widget.js';
  var CALENDLY_CSS = 'https://assets.calendly.com/assets/external/widget.css';

  function urlDeReservation() {
    // L'URL stockée peut déjà porter des paramètres (hide_event_type_details…).
    // On les conserve et on n'ajoute que ce qui manque : aucun doublon.
    var url;
    try { url = new URL(conteneur.dataset.calendly); }
    catch (e) { return conteneur.dataset.calendly; }

    if (!url.searchParams.has('hide_gdpr_banner')) {
      url.searchParams.set('hide_gdpr_banner', '1');
    }
    if (!url.searchParams.has('primary_color')) {
      url.searchParams.set('primary_color', 'b08a33');
    }

    // Motif transmis par la page d'expertise : ?motif=controle-fiscal
    var motif = new URLSearchParams(window.location.search).get('motif');
    if (motif) {
      var libelles = {};
      try { libelles = JSON.parse(conteneur.dataset.motifs || '{}'); } catch (e) { libelles = {}; }
      if (libelles[motif]) { url.searchParams.set('a1', libelles[motif]); }
    }
    return url.toString();
  }

  function afficherSecours(message) {
    conteneur.style.minHeight = '0';
    conteneur.innerHTML =
      '<div class="booking__error" role="alert">' +
      '<b>Le calendrier n\'a pas pu se charger</b>' +
      '<p>' + message + '</p></div>';
  }

  var css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = CALENDLY_CSS;
  document.head.appendChild(css);

  var script = document.createElement('script');
  script.src = CALENDLY_JS;
  script.async = true;

  script.onload = function () {
    if (window.Calendly && typeof window.Calendly.initInlineWidget === 'function') {
      conteneur.innerHTML = '';
      // Sans cette classe, la feuille de style du prestataire ne s'applique pas
      // et son iframe reste a la hauteur par defaut de 150 px.
      conteneur.classList.add('calendly-inline-widget');
      window.Calendly.initInlineWidget({
        url: urlDeReservation(),
        parentElement: conteneur
      });
    } else {
      afficherSecours('Écrivez-nous ou appelez-nous : nous fixons le créneau ensemble.');
    }
  };

  script.onerror = function () {
    afficherSecours(
      'Vérifiez votre connexion, ou appelez-nous directement : nous fixons le créneau ensemble.'
    );
  };

  document.head.appendChild(script);
})();


/* ------------------------------------------------------------------------
   Liens courriel
   Un clic sur une adresse ouvre la messagerie du visiteur, par « mailto: ».
   Sur téléphone et tablette, le système ouvre toujours quelque chose : on ne
   touche à rien. Sur ordinateur, quand aucune messagerie n'est installée, le
   navigateur ne fait rien du tout et le visiteur croit le lien cassé. On le
   détecte — la page garde le focus — et on propose alors Gmail, Outlook,
   Yahoo, ou la copie de l'adresse.
   ------------------------------------------------------------------------ */
(function () {
  'use strict';

  if (window.matchMedia && window.matchMedia('(pointer: coarse)').matches) { return; }

  var DELAI = 1200;        // temps laissé au système pour ouvrir la messagerie
  var panneau = null;
  var declencheur = null;

  function composeurs(adresse) {
    var a = encodeURIComponent(adresse);
    return [
      { nom: 'Gmail',      url: 'https://mail.google.com/mail/?view=cm&fs=1&to=' + a },
      { nom: 'Outlook',    url: 'https://outlook.live.com/mail/0/deeplink/compose?to=' + a },
      { nom: 'Yahoo Mail', url: 'https://compose.mail.yahoo.com/?to=' + a }
    ];
  }

  function surTouche(e) {
    if (e.key === 'Escape' || e.key === 'Esc') { fermer(); }
  }

  function fermer() {
    if (!panneau) { return; }
    panneau.parentNode.removeChild(panneau);
    panneau = null;
    document.removeEventListener('keydown', surTouche);
    if (declencheur) { declencheur.focus(); }
  }

  function bouton(classe, texte) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = classe;
    b.textContent = texte;
    return b;
  }

  function ouvrir(adresse) {
    fermer();

    panneau = document.createElement('div');
    panneau.className = 'courriel';
    panneau.setAttribute('role', 'dialog');
    panneau.setAttribute('aria-modal', 'true');
    panneau.setAttribute('aria-label', 'Écrire à ' + adresse);

    var boite = document.createElement('div');
    boite.className = 'courriel__boite';

    var titre = document.createElement('p');
    titre.className = 'courriel__titre';
    titre.textContent = 'Écrire à ' + adresse;
    boite.appendChild(titre);

    var texte = document.createElement('p');
    texte.className = 'courriel__texte';
    texte.textContent = "Aucune messagerie ne s'est ouverte sur cet ordinateur. "
      + 'Choisissez la vôtre, ou copiez l\'adresse.';
    boite.appendChild(texte);

    var liste = document.createElement('div');
    liste.className = 'courriel__liste';
    composeurs(adresse).forEach(function (c) {
      var lien = document.createElement('a');
      lien.className = 'btn btn--outline';
      lien.href = c.url;
      lien.target = '_blank';
      lien.rel = 'noopener noreferrer';
      lien.textContent = c.nom;
      lien.addEventListener('click', fermer);
      liste.appendChild(lien);
    });
    boite.appendChild(liste);

    var copier = bouton('courriel__copier', "Copier l'adresse");
    copier.addEventListener('click', function () {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(adresse).then(
          function () { copier.textContent = 'Adresse copiée'; },
          function () { copier.textContent = adresse; }
        );
      } else {
        copier.textContent = adresse;
      }
    });
    boite.appendChild(copier);

    var fermeture = bouton('courriel__fermer', '\u00D7');
    fermeture.setAttribute('aria-label', 'Fermer');
    fermeture.addEventListener('click', fermer);
    boite.appendChild(fermeture);

    panneau.appendChild(boite);
    panneau.addEventListener('click', function (e) {
      if (e.target === panneau) { fermer(); }
    });

    document.body.appendChild(panneau);
    document.addEventListener('keydown', surTouche);
    fermeture.focus();
  }

  document.addEventListener('click', function (e) {
    var cible = e.target;
    if (!cible || typeof cible.closest !== 'function') { return; }

    var lien = cible.closest('a[href^="mailto:"]');
    if (!lien) { return; }

    var adresse = lien.getAttribute('href').slice(7).split('?')[0];
    try { adresse = decodeURIComponent(adresse); } catch (err) { /* adresse brute */ }
    if (!adresse) { return; }

    declencheur = lien;

    // On laisse le navigateur tenter l'ouverture normale, puis on vérifie :
    // si la page n'a jamais perdu le focus, c'est que rien ne s'est ouvert.
    window.setTimeout(function () {
      if (document.hasFocus() && !document.hidden) { ouvrir(adresse); }
    }, DELAI);
  });
})();
