// script.js

document.addEventListener("DOMContentLoaded", () => {
  // Mobile Nav Hamburger
  const hamburger = document.querySelector('.hamburger');
  if(hamburger) {
    hamburger.addEventListener('click', () => {
      const navLinks = document.querySelector('.nav-links');
      navLinks.classList.toggle('nav-active');
    });
  }

  // 1. CTA Form
  const ctaForm = document.getElementById('newsletter-form');
  if(ctaForm) {
    ctaForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = ctaForm.querySelector('button');
      btn.textContent = 'Subscribed ✓';
      btn.style.background = '#3b8e2b'; 
    });
  }

  // 2. Press Polaroids Injection (Only if element exists)
  const polaroidGrid = document.getElementById('polaroid-grid');
  if(polaroidGrid) {
    let polaroidHTML = '';
    // Skip img025-029 (moved to Charity page)
    for (let i = 30; i <= 44; i++) {
      if (i === 33 || i === 35) continue; // Skip Variety article and Angel Has Fallen poster
      const num = String(i).padStart(3, '0');
      const rot = (Math.random() * 4.4 - 2).toFixed(2);
      polaroidHTML += `
        <div class="polaroid" style="--rot: ${rot}deg; transform: rotate(${rot}deg);">
          <img src="img/img${num}.jpg" alt="Press ${i}" loading="lazy" onerror="this.parentElement.style.display='none'">
        </div>
      `;
    }
    polaroidGrid.innerHTML = polaroidHTML;
  }

  // 3. Full Archive Mosaic (Only if element exists)
  const mosaic = document.getElementById("archive-mosaic");
  if(mosaic) {
    const fragment = document.createDocumentFragment();
    for (let i = 1; i <= 121; i++) {
      const skipList = [8, 15, 27, 33, 35, 59, 60, 84, 90, 93, 116, 117, 118];
      if (skipList.includes(i)) continue; // Skip posters, articles, quotes, memes
      const num = String(i).padStart(3, '0');
      const img = document.createElement("img");
      img.src = `img/img${num}.jpg`;
      img.loading = "lazy";
      img.alt = `Archive Photo ${i}`;
      img.onerror = () => { img.style.display = "none"; };
      fragment.appendChild(img);
    }
    mosaic.appendChild(fragment);
  }

  // 4. Reels Video Population (Only if element exists)
  const reelsGrid = document.getElementById('reels-grid');
  if(reelsGrid) {
    const sortedVideos = ['vid055.mp4','vid001.mp4','vid018.mp4','vid039.mp4','vid052.mp4','vid013.mp4','vid046.mp4','vid066.mp4','vid058.mp4','vid007.mp4','vid041.mp4','vid033.mp4','vid012.mp4','vid017.mp4','vid062.mp4','vid034.mp4','vid057.mp4','vid069.mp4','vid059.mp4','vid064.mp4','vid025.mp4','vid065.mp4','vid036.mp4','vid005.mp4','vid063.mp4','vid004.mp4','vid061.mp4','vid006.mp4','vid043.mp4','vid042.mp4','vid011.mp4','vid030.mp4','vid067.mp4','vid010.mp4','vid053.mp4','vid038.mp4','vid040.mp4','vid002.mp4','vid068.mp4','vid019.mp4','vid024.mp4','vid022.mp4','vid028.mp4','vid029.mp4','vid037.mp4','vid051.mp4','vid027.mp4','vid015.mp4','vid054.mp4','vid031.mp4','vid016.mp4','vid056.mp4','vid003.mp4','vid023.mp4','vid048.mp4','vid014.mp4','vid021.mp4','vid032.mp4','vid009.mp4','vid008.mp4','vid020.mp4','vid026.mp4','vid060.mp4','vid044.mp4','vid049.mp4','vid045.mp4','vid047.mp4','vid035.mp4','vid050.mp4'];
    let reelsHTML = '';
    sortedVideos.forEach(vid => {
      const num = vid.replace('vid', '').replace('.mp4', '');
      reelsHTML += `
        <div class="reel-item">
          <video src="vid/${vid}" poster="img/img${num}.jpg" loop muted playsinline preload="none" 
                 onmouseover="this.play()" onmouseout="this.pause()" 
                 onerror="this.parentElement.style.display='none'"></video>
        </div>
      `;
    });
    reelsGrid.innerHTML = reelsHTML;
  }

  // 5. Automated Daily News script
  const newsGrid = document.getElementById('news-feed');
  if(newsGrid) {
    const today = new Date();
    const mockNewsDatabase = [
      "Gerard Butler spotted on the set of a highly anticipated new action thriller. The production is currently filming on location.",
      "Rumors circulate about a potential return to the 'Has Fallen' franchise. Fans eagerly await official confirmation from G-BASE.",
      "Gerard Butler's recent charity auction raises record funds. The actor personally attended to meet with VIP donors.",
      "A retrospective on the legacy of '300' marks the anniversary of the film's release. Butler reflects on the intense physical preparation.",
      "New behind-the-scenes footage reveals Butler performing his own stunts in the upcoming blockbuster.",
      "G-BASE announces a new slate of production projects aiming to highlight up-and-coming directors.",
      "Gerard Butler named as the lead in a dramatic adaptation of a bestselling novel, marking a shift towards more character-driven roles.",
      "Fans celebrate Gerard Butler day on social media, making the hashtag trend globally.",
      "Gerard Butler partners with an international conservation group to protect endangered marine habitats.",
      "A surprise appearance at a local pub in Scotland sends fans into a frenzy. Butler shared a pint and took photos with the crowd.",
      "G-BASE secures the rights to a critically acclaimed sci-fi short story, with Butler attached to star and produce.",
      "Gerard Butler graces the cover of GQ's 'Men of the Year' issue, featuring an exclusive in-depth interview.",
      "The actor opens up about his fitness routine and diet regimen that keeps him in leading-man shape."
    ];

    // Create a predictable index based on the date so it changes exactly once per day.
    const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24));
    
    // Generate 8 items per day
    let newsHTML = '';
    for(let i=0; i<8; i++) {
      const index = (dayOfYear + i) % mockNewsDatabase.length;
      const displayDate = new Date(today);
      displayDate.setDate(today.getDate() - i);
      const dateStr = displayDate.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });

      // Wrap items after the 3rd one in a hidden div
      if(i === 3) {
        newsHTML += `<div id="more-automated-news" style="display: none;">`;
      }

      newsHTML += `
        <div class="news-card">
          <div class="news-date">${dateStr}</div>
          <h3 class="news-title">Daily Update ${i === 0 ? "(NEW)" : ""}</h3>
          <p class="news-content">${mockNewsDatabase[index]}</p>
        </div>
      `;
    }
    
    // Close the hidden div and add the See More button
    newsHTML += `
      </div> <!-- End more-automated-news -->
      <div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
        <button class="btn-primary" onclick="document.getElementById('more-automated-news').style.display='block'; this.style.display='none';">SEE MORE NEWS ↓</button>
      </div>
    `;
    

    newsGrid.innerHTML = newsHTML;
  }

  // 7. Film Trailer Modal & Hover Logic (10 seconds)
  const filmCards = document.querySelectorAll('.film-card');
  const modal = document.getElementById('trailer-modal');
  const modalIframe = document.getElementById('trailer-iframe');
  const modalTitle = document.getElementById('trailer-title');

  window.closeTrailer = function() {
    if(modal) {
      modal.classList.remove('active');
      modalIframe.src = '';
    }
  };

  filmCards.forEach(card => {
    let hoverTimer;
    
    card.addEventListener('mouseenter', () => {
      clearTimeout(hoverTimer);
      
      const trailerId = card.getAttribute('data-trailer');
      const title = card.getAttribute('data-title') || card.querySelector('h4')?.innerText;
      
      if(trailerId) {
        hoverTimer = setTimeout(() => {
          if (modal && modalIframe) {
            modalTitle.innerText = title + ' - OFFICIAL TRAILER';
            modalIframe.src = `https://www.youtube.com/embed/${trailerId}?autoplay=1`;
            modal.classList.add('active');
          }
        }, 3000); // 3 seconds
      }
    });
    
    card.addEventListener('mouseleave', () => {
      clearTimeout(hoverTimer);
    });
  });

  // 8. Page Preview CTA Grid
  const pagePreviewsContainer = document.getElementById('page-previews');
  if (pagePreviewsContainer) {
    const pageCtas = [
      {
        slug: 'films',
        label: 'Filmography',
        title: 'Films',
        desc: 'Explore Gerard Butler\'s complete filmography, featuring over 40 films from 300 to Olympus Has Fallen.',
        bullets: ['34+ Films', '$1.8B Box Office', 'Trailers'],
        image: 'img/hall_action.png'
      },
      {
        slug: 'reels',
        label: 'Video Archive',
        title: 'Reels',
        desc: 'Watch exclusive behind-the-scenes clips, interviews, and stunt choreography breakdowns.',
        bullets: ['Interviews', 'Stunts', 'Behind the Scenes'],
        image: 'img/img018.jpg'
      },
      {
        slug: 'gallery',
        label: 'Photo Collection',
        title: 'Gallery',
        desc: 'Browse high-resolution photo galleries from movie sets, red carpets, and fan encounters.',
        bullets: ['Red Carpet', 'Set Photos', 'Fan Encounters'],
        image: 'img/img046.jpg'
      },
      {
        slug: 'news',
        label: 'Latest Updates',
        title: 'News',
        desc: 'Stay up-to-date with the latest casting announcements, release dates, and press tours.',
        bullets: ['Announcements', 'Itinerary', 'Press Tours'],
        image: 'img/img048.jpg'
      },
      {
        slug: 'charity',
        label: 'Philanthropy',
        title: 'Charity',
        desc: 'Learn about Gerard Butler\'s philanthropic efforts and partnerships with global organizations.',
        bullets: ['Mary\'s Meals', 'Disaster Relief', 'Fundraisers'],
        image: 'img/img076.jpg'
      },
      {
        slug: 'fanclub',
        label: 'Community',
        title: 'Fanclub',
        desc: 'Join the official Gerard Butler Fanclub to connect with fans worldwide and access exclusive content.',
        bullets: ['Forums', 'Fan Art', 'VIP Access'],
        image: 'img/gerard_butler_fans_1.png'
      }
    ];

    let html = '';
    pageCtas.forEach(cta => {
      html += `
        <a href="${cta.slug}" class="preview-card" aria-label="${cta.title} — ${cta.desc}">
          <div class="preview-visual-wrapper">
            <div class="preview-skeleton"></div>
            <img 
              data-src="${cta.image}" 
              alt="${cta.title} Preview" 
              class="preview-image" 
              aria-hidden="true" 
            />
          </div>
          <div class="preview-eyebrow">// ${cta.label}</div>
          <h3 class="preview-title">${cta.title}</h3>
          <p class="preview-desc">${cta.desc}</p>
          <ul class="preview-bullets">
            ${cta.bullets.map(b => `<li>${b}</li>`).join('')}
          </ul>
          <span class="preview-btn">Open ${cta.title}</span>
        </a>
      `;
    });
    
    pagePreviewsContainer.innerHTML = html;

    // Lazy load images
    const previewImages = pagePreviewsContainer.querySelectorAll('.preview-image');
    
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            const src = img.getAttribute('data-src');
            
            img.onload = () => {
              img.classList.add('loaded');
            };
            
            img.src = src;
            obs.unobserve(img);
          }
        });
      }, { rootMargin: '200px 0px' });
      
      previewImages.forEach(img => observer.observe(img));
    } else {
      previewImages.forEach(img => {
        img.onload = () => img.classList.add('loaded');
        img.src = img.getAttribute('data-src');
      });
    }
  }

});
