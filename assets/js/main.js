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
   Agenda en ligne — chargement différé
   Le script du service de réservation n'est appelé qu'au clic du visiteur :
   aucun cookie tiers n'est déposé avant son accord explicite.
   ------------------------------------------------------------------------ */
(function () {
  'use strict';

  var bouton = document.getElementById('booking-load');
  var placeholder = document.getElementById('booking-placeholder');
  var conteneur = document.getElementById('booking-widget');
  if (!bouton || !conteneur || !placeholder) { return; }

  var CALENDLY_JS = 'https://assets.calendly.com/assets/external/widget.js';
  var CALENDLY_CSS = 'https://assets.calendly.com/assets/external/widget.css';

  function urlDeReservation() {
    var base = bouton.dataset.calendly;
    var params = new URLSearchParams();
    params.set('hide_gdpr_banner', '1');
    params.set('primary_color', 'b08a33');

    // Motif transmis par la page d'expertise : ?motif=controle-fiscal
    var motif = new URLSearchParams(window.location.search).get('motif');
    if (motif) {
      var libelles = {};
      try { libelles = JSON.parse(bouton.dataset.motifs || '{}'); } catch (e) { libelles = {}; }
      if (libelles[motif]) { params.set('a1', libelles[motif]); }
    }
    return base + (base.indexOf('?') === -1 ? '?' : '&') + params.toString();
  }

  function afficherSecours(message) {
    conteneur.innerHTML =
      '<div class="booking__error" role="alert">' +
      '<b>Le calendrier n\'a pas pu se charger</b>' +
      '<p>' + message + '</p></div>';
    conteneur.hidden = false;
  }

  bouton.addEventListener('click', function () {
    bouton.disabled = true;
    bouton.textContent = 'Chargement…';

    var css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = CALENDLY_CSS;
    document.head.appendChild(css);

    var script = document.createElement('script');
    script.src = CALENDLY_JS;
    script.async = true;

    script.onload = function () {
      placeholder.hidden = true;
      conteneur.hidden = false;
      if (window.Calendly && typeof window.Calendly.initInlineWidget === 'function') {
        window.Calendly.initInlineWidget({
          url: urlDeReservation(),
          parentElement: conteneur
        });
      } else {
        afficherSecours('Appelez-nous directement, nous fixons le créneau ensemble.');
      }
    };

    script.onerror = function () {
      bouton.disabled = false;
      bouton.textContent = 'Réessayer';
      afficherSecours(
        'Vérifiez votre connexion, ou appelez-nous directement : nous fixons le créneau ensemble.'
      );
    };

    document.head.appendChild(script);
  });
})();
