import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I will write a script to replace the translations object, and inject a custom translation function.
# The `setLanguage` function will iterate over an array of DOM selectors and swap out innerHTML.

js_code = """
    const siteTranslations = {
      "Currently @ University of Edinburgh · MSc AI": "Derzeit @ University of Edinburgh · MSc AI",
      "AI Engineer building enterprise-grade agentic systems, multi-modal pipelines and intelligent automation. Turning cutting-edge research into production-ready solutions.": "AI-Ingenieur, der agentische Systeme auf Unternehmensebene, multimodale Pipelines und intelligente Automatisierung entwickelt. Verwandelt modernste Forschung in produktionsreife Lösungen.",
      "View Projects": "Projekte ansehen",
      "About Me": "Über mich",
      "Building the Future<br>with Intelligence": "Die Zukunft mit Intelligenz gestalten",
      "I'm an <strong>AI Engineer</strong> currently pursuing my Master's in Artificial Intelligence at <strong>The University of Edinburgh</strong>. My work lives at the intersection of cutting-edge research and real-world enterprise AI.": "Ich bin ein <strong>AI Engineer</strong> und absolviere derzeit meinen Master in Künstlicher Intelligenz an <strong>The University of Edinburgh</strong>. Meine Arbeit bewegt sich an der Schnittstelle von modernster Forschung und realer angewandter Unternehmens-KI.",
      "At <strong>Prodapt's NextGen Labs (R&D)</strong>, I was part of a team of 50+ developers focused on researching and integrating cutting-edge GenAI tools into enterprise workflows. I personally built 30+ modular AI agents covering everything from voice navigation to medical data digitisation.": "Bei <strong>Prodapt's NextGen Labs (R&D)</strong> war ich Teil eines Teams von 50+ Entwicklern, das sich auf die Erforschung und Integration neuartiger GenAI-Tools in Unternehmensabläufe konzentrierte. Ich baute persönlich 30+ modulare KI-Agenten, von der Sprachnavigation bis zur Digitalisierung medizinischer Daten.",
      "Research Focus": "Forschungsschwerpunkte",
      "Agentic AI, LLM orchestration, RAG, Vision-Language Models, NL2SQL — applied to real-world problems.": "Agentische KI, LLM-Orchestrierung, RAG, Vision-Language Models, NL2SQL — angewendet auf reale Probleme.",
      "Languages": "Sprachen",
      "English (Professional · IELTS C1) · Hindi (Native) · Japanese (Basic)": "Englisch (Fließend · IELTS C1) · Hindi (Muttersprache) · Japanisch (Grundkenntnisse)",
      "Professional Journey": "Beruflicher Werdegang",
      "Experience": "Erfahrung",
      "Where I've built and learned.": "Wo ich gebaut und gelernt habe.",
      "Generative AI Developer — Intern": "Generative KI Entwickler — Praktikant",
      "January 2025 – July 2025": "Januar 2025 – Juli 2025",
      "Contributed to NextGen Labs (R&D), a team of 50+ developers focused on researching cutting-edge GenAI tools and integrating them into enterprise workflows": "Mitarbeit bei NextGen Labs (R&D), einem Team von 50+ Entwicklern zur Erforschung und Integration von GenAI-Tools in Unternehmensabläufe.",
      "Developed 30+ modular AI plugin agents as API endpoints — including Excel-to-Chart (PandasAI), Automated Browser Testing (CrewAI + MCP Playwright), Text-to-Human Audio, and Handwritten Medical Form Digitiser": "Entwicklung von 30+ modularen KI-Plugin-Agenten als API-Endpunkte — einschließlich Excel-zu-Chart (PandasAI), automatisierter Browsertests und handschriftlicher Krankenakten-Digitalisierung.",
      "Built an Interactive Screen Navigation Assistant — real-time voice agent using Gemini Live API that verbally guides employees through portals, pre-loaded with company context": "Aufbau eines interaktiven Bildschirm-Navigationsassistenten — ein Echtzeit-Sprachagent mit Gemini Live API, der Mitarbeiter mündlich durch Portale führt.",
      "Co-developed a Conversational AI Video Editor using LangGraph + MoviePy — trim, blur, subtitle, translate via natural language chat": "Mitentwicklung eines Conversational AI Video Editors (LangGraph + MoviePy) — trimmen, unschärfen, untertiteln, übersetzen via einfachem Chat.",
      "Completed intensive 3-month training covering LangChain, LangGraph, LlamaIndex, AutoGen, CrewAI, RAG, MCP, Big Data and Telecom fundamentals": "Abschluss eines 3-monatigen Intensivtrainings mit Fokus auf LangChain, LangGraph, LLMs, RAG, MCP und Telekommunikations-Grundlagen.",
      "View full experience on LinkedIn": "Volle Erfahrung auf LinkedIn ansehen",
      "Full Stack Developer — Intern": "Full Stack Entwickler — Praktikant",
      "September 2023 – December 2023": "September 2023 – Dezember 2023",
      "Contributed to SWEEP — B2B wholesale app for Switzerland's 2nd-largest telecom carrier": "Beitrag zu SWEEP — B2B Großhandelsanwendung für den zweitgrößten Telekommunikationsanbieter der Schweiz.",
      "Built self-service product configuration framework (Angular frontend + Apollo GraphQL + Java backend + Oracle DB via JPA), eliminating developer dependency for new B2B product launches": "Aufbau eines Self-Service-Produktkonfigurations-Frameworks (Angular, Apollo GraphQL, Java, Oracle DB), wodurch bei Produktneueinführungen keine Entwicklerabhängigkeit mehr bestand.",
      "Designed interactive UI prototypes in Figma; translated business requirements into Confluence technical specs": "Entwurf interaktiver UI-Prototypen in Figma; Übersetzung von Geschäftsanforderungen in technische Confluence-Spezifikationen.",
      "Automated Selenium test scripts, improving test coverage and reducing manual QA effort across the product": "Automatisierung von Selenium-Testskripten, was die Testabdeckung erhöhte und den manuellen QA-Aufwand reduzierte.",
      "Selected Work": "Ausgewählte Arbeiten",
      "Projects": "Projekte",
      "From dissertation research to hackathon finalists — building AI that matters.": "Von der Forschung bis zu den Hackathon-Finalisten — Aufbau von KI, die zählt.",
      "LLM Agentic Chatbot for IUPHAR": "Agentischer LLM-Chatbot für IUPHAR",
      "Agentic chatbot that translates natural language queries into SQL to retrieve live data from the IUPHAR Guide to Pharmacology PostgreSQL database — serving academic researchers and drug discovery teams. Evaluating LangGraph vs CrewAI pipelines with a PostgreSQL MCP server for schema-aware access.": "Agenten-Chatbot, der natürliche Sprachanfragen in SQL übersetzt, um Livedaten aus der Datenbank IUPHAR Guide to Pharmacology abzurufen — für Forscher und Arzneimittelentwicklungsteams.",
      "Jan – Jul 2026": "Jan – Jul 2026",
      "View on GitHub": "Auf GitHub ansehen",
      "AccessAI – Universal Accessibility Browser Extension": "AccessAI – Universelle Browsererweiterung für Barrierefreiheit",
      "AI-powered Chrome extension with three real-time tools: voice-controlled agentic navigator, social cue coaching assistant, and autonomous documentation engine. Multimodal pipeline combining Whisper + GPT-4o Vision for live lecture capture. Low-latency architecture using WebSockets and GPT-4o function calling.": "KI-gestützte Chrome-Erweiterung mit Echtzeit-Tools: sprachgesteuerter Agent, Coaching-Assistent für soziale Signale und Autodokumentation.",
      "Feb 2026": "Feb 2026",
      "Brain Tumor MRI Segmentation using UNet & SegResNet": "Hirntumor-MRT-Segmentierung (UNet & SegResNet)",
      "Developed state-of-the-art segmentation models (UNet, SegResNet) using MONAI to trace boundaries of cancerous brain tissues in MRI scans, assisting neurologists with quantitative volumetric analysis.": "Entwicklung moderner Segmentierungsmodelle unter Verwendung von MONAI zur Verfolgung von Grenzen kanzerösen Hirngewebes in MRT-Scans, um Neurologen bei der Volumenanalyse zu unterstützen.",
      "Spring 2026": "Frühling 2026",
      "Technical Arsenal": "Technisches Arsenal",
      "Skills & Technologies": "Fähigkeiten & Technologien",
      "The tools I use to build intelligent systems.": "Die Werkzeuge, die ich zum Aufbau intelligenter Systeme nutze.",
      "AI / ML / Agents": "KI / ML / Agenten",
      "Languages & Frameworks": "Sprachen & Frameworks",
      "Databases & Cloud": "Datenbanken & Cloud",
      "Tools & Architecture": "Tools & Architektur",
      "Milestones": "Meilensteine",
      "Achievements": "Auszeichnungen",
      "Top 8 / 35+ Teams — AccessAI Hackathon": "Top 8 / 35+ Teams — AccessAI Hackathon",
      "University of Edinburgh (Feb 2026) — Built a multimodal browser extension for accessibility.": "University of Edinburgh (Feb 2026) — Bau einer multimodalen Browsererweiterung für Barrierefreiheit.",
      "Finalist out of 3000+ Teams — AIXplore Hackathon": "Finalist von 3000+ Teams — AIXplore Hackathon",
      "Ranked in the top echelon globally, demonstrating rapid prototyping of agentic systems under pressure.": "Weltweit an der Spitze platziert, schnelle Prototypenentwicklung von agenten-KI unter Zeitdruck bewiesen.",
      "30+ AI Plugins & Agents Deployed": "Über 30 KI-Plugins & Agenten eingesetzt",
      "Built and deployed dozens of scalable enterprise API agents at Prodapt NextGen Labs.": "Erstellung und Bereitstellung Dutzender skalierbarer Unternehmens-API-Agenten in den Prodapt NextGen Labs.",
      "Academic Background": "Akademischer Hintergrund",
      "Education": "Ausbildung",
      "The diverse foundation behind my AI engineering.": "Das breite Fundament hinter meiner KI-Entwicklung.",
      "Master of Science in Artificial Intelligence": "Master of Science in Künstlicher Intelligenz",
      "The University of Edinburgh, UK": "The University of Edinburgh, UK",
      "September 2025 – August 2026": "September 2025 – August 2026",
      "Taught courses spanning from foundation ML theories to practical engineering.": "Kurse von grundlegenden ML-Theorien bis hin zu praktischem Engineering.",
      "Focusing heavily on agentic pipelines and natural language processing.": "Starker Fokus auf agentischen Pipelines und natürlicher Sprachverarbeitung.",
      "Bachelor of Technology in Computer Science": "Bachelor of Technology in Informatik",
      "Vellore Institute of Technology (VIT), India": "Vellore Institute of Technology (VIT), Indien",
      "July 2020 – May 2024": "Juli 2020 – Mai 2024",
      "Graduated with 8.78 CGPA (First Class with Distinction)": "Abschluss mit 8.78 CGPA (Mit Auszeichnung bestanden)",
      "Core Modules: SWE, Cloud Architecture, DBMS, Web Development, Artificial Intelligence": "Kernmodule: SWE, Cloud Architecture, DBMS, Web Development, Künstliche Intelligenz",
      "Verified Skills": "Geprüfte Fähigkeiten",
      "Certifications": "Zertifizierungen",
      "Cloud & Architecture": "Cloud & Architektur",
      "Google Cloud Digital Leader": "Google Cloud Digital Leader",
      "AWS Cloud Foundations": "AWS Cloud Foundations",
      "Language Proficiency": "Sprachkenntnisse",
      "IELTS — Band 7.5 (C1)": "IELTS — Band 7.5 (C1)",
      "Coding Platforms": "Coding-Plattformen",
      "HackerRank — Python 5★": "HackerRank — Python 5★",
      "HackerRank — Java 5★": "HackerRank — Java 5★",
      "Let's Connect": "Lassen Sie uns Kontakt aufnehmen",
      "Open to Opportunities<br>& Collaborations": "Offen für berufliche Gelegenheiten<br>& Zusammenarbeit",
      "I'm open to AI research collaborations, internships, and interesting projects. Connect on LinkedIn or send me a message — no spam, just good conversations.": "Ich bin offen für KI-Forschungs-Kollaborationen, Praktika und interessante Projekte. Einfach auf LinkedIn verbinden oder eine Nachricht schicken — kein Spam, nur gute Gespräche.",
      "Best way to reach me. Connect and chat about AI, research, or opportunities.": "Der beste Weg mich zu erreichen. Verbinden und Chatten über KI und Gelegenheiten.",
      "Check out my open-source projects, research code, and hackathon submissions.": "Sehen Sie sich meine Open-Source-Projekte, Forschungscodes und Hackathon-Beiträge an.",
      "Send an Email": "Eine E-Mail senden",
      "Drop me a message directly to my inbox.": "Schreiben Sie mir direkt in meinen Posteingang.",
      "Name": "Name",
      "Email": "E-Mail",
      "Subject": "Betreff",
      "Message": "Nachricht",
      "Send Message": "Nachricht senden",
      "Designed & built by": "Entworfen & entwickelt von",
      "AI AGENTS BUILT": "KI AGENTEN",
      "COMPANIES": "FIRMEN",
      "PERSONAL PROJECTS": "PROJEKTE",
      "CERTIFICATIONS": "ZERTIFIKATE"
    };

    let originalDb = {};

    function storeOriginals() {
      // Find all elements to possibly translate and store original english versions
      // We will look for elements containing exact strings matching our keys
      const allElems = document.body.querySelectorAll('h1, h2, span, p, label, a, div, strong, li');
      allElems.forEach(el => {
         // Skip if mostly code/script
         if(el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return;
         // Store elements that contain exact english.
         // We do this by iterating keys.
         for (let key in siteTranslations) {
           if (el.innerHTML.trim() === key) {
             el.setAttribute('data-tx-key', key);
           }
         }
      });
      
      // Select input placeholders
      document.querySelectorAll('input, textarea').forEach(el => {
         if (el.placeholder === "John Doe") el.setAttribute('data-tx-ph', 'John Doe');
         if (el.placeholder === "john@example.com") el.setAttribute('data-tx-ph', 'john@example.com');
         if (el.placeholder === "Project Inquiry, AI Research, etc.") el.setAttribute('data-tx-ph', 'Project Inquiry, AI Research, etc.');
         if (el.placeholder === "Hi Rishabh...") el.setAttribute('data-tx-ph', 'Hi Rishabh...');
      });
    }

    const phTrans = {
      "John Doe": "Max Mustermann",
      "john@example.com": "max@beispiel.de",
      "Project Inquiry, AI Research, etc.": "Projektanfrage, KI-Forschung, usw.",
      "Hi Rishabh...": "Hallo Rishabh..."
    };

    function setLanguage(lang) {
      currentLang = lang;
      localStorage.setItem('lang', lang);
      if (langToggle) langToggle.textContent = lang === 'en' ? 'DE' : 'EN';
      
      // Swap simple translations from data-i18n
      document.querySelectorAll('[data-i18n]').forEach(el => {
        const keys = el.getAttribute('data-i18n').split('.');
        let val = translations;
        for (const key of keys) {
          if (val[key]) val = val[key];
          else { val = null; break; }
        }
        if (val && val[lang]) {
          if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') el.placeholder = val[lang];
          else el.innerHTML = val[lang];
        }
      });

      // Apply siteTranslations logic
      document.querySelectorAll('[data-tx-key]').forEach(el => {
        const k = el.getAttribute('data-tx-key');
        if (lang === 'de') {
           if(siteTranslations[k]) el.innerHTML = siteTranslations[k];
        } else {
           el.innerHTML = k;
        }
      });
      
      document.querySelectorAll('[data-tx-ph]').forEach(el => {
        const k = el.getAttribute('data-tx-ph');
        if (lang === 'de') {
           if(phTrans[k]) el.placeholder = phTrans[k];
        } else {
           el.placeholder = k;
        }
      });
      
      // Update SYSTEM PROMPT for Chatbot
      if (lang === 'de') {
         window.ACTIVE_SYSTEM_PROMPT = SYSTEM_PROMPT + "\\n\\nIMPORTANT NOTIFICATION: The user has switched the website language to Deutsch (German). You MUST respond in fluent German for the remainder of this conversation.";
      } else {
         window.ACTIVE_SYSTEM_PROMPT = SYSTEM_PROMPT;
      }
    }
"""

# Replace the existing JS translation logic with our new advanced logic
start_idx = html.find("const translations = {")
end_idx = html.find("let currentTheme = localStorage.getItem('theme')", start_idx)

if start_idx != -1 and end_idx != -1:
    old_js = html[start_idx:end_idx]
    
    # We maintain the base 'translations' for nav bar since that was already working.
    nav_translations = """const translations = {
      nav: {
        about: { en: "About", de: "Über mich" },
        exp: { en: "Experience", de: "Erfahrung" },
        proj: { en: "Projects", de: "Projekte" },
        skills: { en: "Skills", de: "Fähigkeiten" },
        edu: { en: "Education", de: "Ausbildung" },
        contact: { en: "Contact", de: "Kontakt" }
      }
    };"""

    new_html = html[:start_idx] + nav_translations + "\n" + js_code + "\n    " + html[end_idx:]
    
    # Inject call to storeOriginals() right before setLanguage(currentLang) call
    init_call_idx = new_html.find("setLanguage(currentLang);")
    if init_call_idx != -1:
        new_html = new_html[:init_call_idx] + "storeOriginals();\n    " + new_html[init_call_idx:]
        
    # Replace the fetch call to use window.ACTIVE_SYSTEM_PROMPT
    new_html = new_html.replace("system_instruction: { parts: [{ text: SYSTEM_PROMPT }] },", "system_instruction: { parts: [{ text: window.ACTIVE_SYSTEM_PROMPT || SYSTEM_PROMPT }] },")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("HTML updated successfully!")
else:
    print("Could not find start or end index for translations.")

